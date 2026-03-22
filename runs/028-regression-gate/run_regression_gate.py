#!/usr/bin/env python3
"""
Phase 6G: Regression Gate for Golden Examples

This script implements a regression guardrail to protect the already-implemented
user-visible experiences (recall conflict, explain cross-host, provenance display).

This is a GUARDRAIL task - NOT expanding functionality, just protecting what exists.

Run: python3 runs/028-regression-gate/run_regression_gate.py
"""

import sys
import os
import tempfile
import shutil
import json
from datetime import datetime, timezone
from enum import Enum

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../..", "src"))

from ocmaf.storage.event_store import EventStore
from ocmaf.storage.memory_store import MemoryStore
from ocmaf.api.remember import RememberAPI
from ocmaf.api.recall import RecallAPI
from ocmaf.event.envelope import EventEnvelope
from ocmaf.event.scope import Scope
from ocmaf.event.types import EventType


class RegressionType(Enum):
    """Classification of regression types."""
    NONE = "no_regression"
    FORMATTING_DRIFT = "formatting_drift"
    PROVENANCE_REGRESSION = "provenance_regression"
    CONFLICT_VISIBILITY_REGRESSION = "conflict_visibility_regression"
    EXPLAIN_VISIBILITY_REGRESSION = "explain_visibility_regression"


def check_regression(actual: str, golden: str, check_type: str) -> tuple:
    """Check for regression and classify it.

    This function checks for the PRESENCE of key patterns that indicate
    the user-visible experience is intact, rather than requiring exact match.
    """

    # Define key patterns that MUST be present for each check type
    if check_type == "conflict":
        # For conflict, we need:
        # - ⚠️ CONFLICT DETECTED (conflict visibility)
        # - [Claude] and [Codex] (provenance)
        # - conflicting versions / candidates (conflict candidates)
        key_patterns = {
            "conflict_visibility": ["⚠️ CONFLICT DETECTED", "conflicting versions"],
            "provenance": ["[Claude]", "[Codex]"],
        }
    elif check_type == "explain":
        # For explain, we need:
        # - Source: (provenance)
        # - Also written by: (cross-host context)
        # - Match Reasons: (explain visibility)
        key_patterns = {
            "provenance": ["Source:"],
            "explain_visibility": ["Also written by:", "Match Reasons:"],
        }
    elif check_type == "provenance":
        # For provenance, we need:
        # - From Claude / From Codex (provenance display)
        key_patterns = {
            "provenance": ["From Claude", "From Codex"],
        }
    elif check_type == "injection":
        # For injection, we need:
        # - (From Claude or (From Codex (provenance in injection)
        # - ⚠️ CONFLICT (conflict visibility)
        key_patterns = {
            "provenance": ["(From Claude", "(From Codex"],
            "conflict_visibility": ["⚠️ CONFLICT"],
        }
    else:
        return RegressionType.FORMATTING_DRIFT, "unknown_check_type"

    missing_by_type = {}
    for regression_type, patterns in key_patterns.items():
        for pattern in patterns:
            if pattern not in actual:
                if regression_type not in missing_by_type:
                    missing_by_type[regression_type] = []
                missing_by_type[regression_type].append(pattern)

    if not missing_by_type:
        return RegressionType.NONE, None

    # Classify the regression
    if len(missing_by_type) == 1:
        rt = list(missing_by_type.keys())[0]
        missing = missing_by_type[rt]
        if rt == "provenance":
            return RegressionType.PROVENANCE_REGRESSION, missing
        elif rt == "conflict_visibility":
            return RegressionType.CONFLICT_VISIBILITY_REGRESSION, missing
        elif rt == "explain_visibility":
            return RegressionType.EXPLAIN_VISIBILITY_REGRESSION, missing

    # Multiple types missing = formatting drift
    return RegressionType.FORMATTING_DRIFT, missing_by_type


def generate_recall_conflict_output(event_store, memory_store, remember_api, recall_api):
    """Generate recall conflict output."""
    # Setup test data
    for i, (content, summary, tool) in enumerate([
        ('Testing framework: pytest is the best for unit testing', 'Pytest recommended', 'claude-code'),
        ('Testing framework: unittest is built-in and works well', 'Unittest recommended', 'codex-cli'),
    ]):
        event = EventEnvelope(
            source_tool=tool,
            scope=Scope(user="regression_user", project="regression_test"),
            event_type=EventType.DECISION,
            payload={
                "content": content,
                "summary": summary,
                "keywords": ["testing", "framework"],
                "title": "Testing framework",
            },
        )
        remember_api.remember(event)

    # Recall
    recall_result = recall_api.recall("testing framework", {"user": "regression_user", "project": "regression_test"})
    recall_dict = recall_result.to_dict()

    output_lines = []
    output_lines.append(f"Found {len(recall_dict.get('memories', []))} memories:")

    for mem in recall_dict.get("memories", []):
        ts = mem.get("timestamp", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                ts = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        output_lines.append(f"  From {mem.get('source_host_friendly', 'Unknown')}: \"{mem.get('content', '')[:50]}\" ({ts})")

    if recall_dict.get("conflict_detected"):
        output_lines.append("")
        output_lines.append("⚠️ CONFLICT DETECTED")
        candidates = recall_dict.get("candidates", [])
        output_lines.append(f"  {len(candidates)} conflicting versions found:")
        for c in candidates:
            output_lines.append(f"  - [{c.get('source_host_friendly', 'Unknown')}] \"{c.get('content', '')[:50]}\"")

    return "\n".join(output_lines)


def generate_explain_crosshost_output(event_store, memory_store, remember_api, recall_api):
    """Generate explain cross-host output."""
    # Setup test data
    for i, (content, summary, tool) in enumerate([
        ('Testing framework: pytest is the best', 'Pytest recommended', 'claude-code'),
        ('Testing framework: unittest works well', 'Unittest recommended', 'codex-cli'),
    ]):
        event = EventEnvelope(
            source_tool=tool,
            scope=Scope(user="regression_user", project="regression_test"),
            event_type=EventType.DECISION,
            payload={
                "content": content,
                "summary": summary,
                "keywords": ["testing", "framework"],
                "title": "Testing framework",
            },
        )
        remember_api.remember(event)

    # Recall to get memory_id
    recall_result = recall_api.recall("testing framework", {"user": "regression_user", "project": "regression_test"})
    recall_dict = recall_result.to_dict()

    output_lines = []

    if recall_dict.get("memories"):
        mem_id = recall_dict["memories"][0].get("memory_id")
        explain_result = recall_api.explain(mem_id, recall_query="testing framework")

        output_lines.append("## Memory Explanation")
        output_lines.append("")
        output_lines.append(f"Source: {explain_result.get('source_host_friendly')}")

        ts = explain_result.get("event_timestamp", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                ts = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
            output_lines.append(f"Timestamp: {ts}")

        output_lines.append("")
        output_lines.append("Match Reasons:")
        for mr in explain_result.get("match_reasons", []):
            if mr["type"] == "keyword":
                output_lines.append(f"  • Keyword match: {', '.join(mr.get('matched', []))}")
            elif mr["type"] == "scope":
                for k, v in mr.get("matched", {}).items():
                    output_lines.append(f"  • Scope match: {k}={v}")

        also_written = explain_result.get("also_written_by", [])
        if also_written:
            output_lines.append(f"\nAlso written by: {', '.join(also_written)}")

        output_lines.append("")
        output_lines.append(explain_result.get("explain", ""))

    return "\n".join(output_lines)


def generate_recall_provenance_output(event_store, memory_store, remember_api, recall_api):
    """Generate recall provenance output."""
    # Setup test data with different sources
    for i, (content, summary, tool) in enumerate([
        ('Python version: use 3.11+ for best performance', 'Python 3.11+', 'claude-code'),
        ('Python version: 3.9 is stable', 'Python 3.9 stable', 'codex-cli'),
    ]):
        event = EventEnvelope(
            source_tool=tool,
            scope=Scope(user="regression_user", project="regression_test"),
            event_type=EventType.DECISION,
            payload={
                "content": content,
                "summary": summary,
                "keywords": ["python", "version"],
                "title": "Python version",
            },
        )
        remember_api.remember(event)

    recall_result = recall_api.recall("python version", {"user": "regression_user", "project": "regression_test"})
    recall_dict = recall_result.to_dict()

    output_lines = []
    output_lines.append(f"Found {len(recall_dict.get('memories', []))} memories:")

    for mem in recall_dict.get("memories", []):
        ts = mem.get("timestamp", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                ts = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        output_lines.append(f"  From {mem.get('source_host_friendly', 'Unknown')}: \"{mem.get('content', '')[:50]}\" ({ts})")

    return "\n".join(output_lines)


def generate_injection_text_output(event_store, memory_store, remember_api, recall_api):
    """Generate injection text output."""
    # Setup conflict data
    for i, (content, summary, tool) in enumerate([
        ('Testing: pytest is best', 'Pytest recommended', 'claude-code'),
        ('Testing: unittest works', 'Unittest works', 'codex-cli'),
    ]):
        event = EventEnvelope(
            source_tool=tool,
            scope=Scope(user="regression_user", project="regression_test"),
            event_type=EventType.DECISION,
            payload={
                "content": content,
                "summary": summary,
                "keywords": ["testing"],
                "title": "Testing",
            },
        )
        remember_api.remember(event)

    recall_result = recall_api.recall("testing", {"user": "regression_user", "project": "regression_test"})

    output_parts = []
    output_parts.append(recall_result.to_injection_text())
    output_parts.append("")
    output_parts.append(recall_result.to_gist_text())

    return "\n".join(output_parts)


def run_regression_gate():
    """Run regression gate checks against golden examples."""
    print("=" * 70)
    print("Phase 6G: Regression Gate - Golden Examples Guardrail")
    print("=" * 70)
    print()
    print("⚠️  THIS IS A GUARDRAIL TASK")
    print("   Purpose: Protect existing user-visible experiences")
    print("   Not expanding functionality")
    print()

    # Setup
    temp_dir = tempfile.mkdtemp(prefix="ocmf_6g_regression_")
    db_path = os.path.join(temp_dir, "test.db")
    run_dir = os.path.dirname(__file__)
    golden_dir = os.path.join(run_dir, "..", "027-stable-golden-examples")

    results = {}

    try:
        event_store = EventStore(db_path=db_path)
        memory_store = MemoryStore(db_path=db_path)
        remember_api = RememberAPI(event_store, memory_store)
        recall_api = RecallAPI(memory_store, event_store)

        # Define golden files and their generators
        golden_files = {
            "recall_conflict": {
                "path": os.path.join(golden_dir, "recall_conflict_golden.txt"),
                "generator": lambda: generate_recall_conflict_output(event_store, memory_store, remember_api, recall_api),
                "check_type": "conflict",
            },
            "explain_crosshost": {
                "path": os.path.join(golden_dir, "explain_crosshost_golden.txt"),
                "generator": lambda: generate_explain_crosshost_output(event_store, memory_store, remember_api, recall_api),
                "check_type": "explain",
            },
            "recall_provenance": {
                "path": os.path.join(golden_dir, "recall_provenance_golden.txt"),
                "generator": lambda: generate_recall_provenance_output(event_store, memory_store, remember_api, recall_api),
                "check_type": "provenance",
            },
            "injection_text": {
                "path": os.path.join(golden_dir, "injection_text_golden.txt"),
                "generator": lambda: generate_injection_text_output(event_store, memory_store, remember_api, recall_api),
                "check_type": "injection",
            },
        }

        all_passed = True
        regression_details = []

        for name, config in golden_files.items():
            print(f"\n{'=' * 70}")
            print(f"CHECK: {name}")
            print("=" * 70)

            golden_path = config["path"]
            generator = config["generator"]
            check_type = config["check_type"]

            # Check golden file exists
            if not os.path.exists(golden_path):
                print(f"✗ Golden file not found: {golden_path}")
                all_passed = False
                regression_details.append({
                    "name": name,
                    "status": "FAIL",
                    "reason": "golden_file_missing"
                })
                continue

            # Read golden
            with open(golden_path, 'r') as f:
                golden_content = f.read()

            print(f"✓ Golden file: {golden_path}")

            # Generate current output
            current_output = generator()
            print(f"✓ Generated {len(current_output)} chars")

            # Write current output for comparison
            current_path = os.path.join(run_dir, f"{name}_current.txt")
            with open(current_path, 'w') as f:
                f.write(current_output)
            print(f"✓ Current output: {current_path}")

            # Check for regression
            regression_type, regression_detail = check_regression(current_output, golden_content, check_type)

            print(f"\nRegression check: {regression_type.value}")

            if regression_type == RegressionType.NONE:
                print("✓ PASS: No regression detected")
                results[name] = "PASS"
                regression_details.append({
                    "name": name,
                    "status": "PASS",
                    "regression_type": "none"
                })
            else:
                print(f"✗ FAIL: {regression_type.value}")
                if regression_detail:
                    print(f"  Missing patterns: {regression_detail}")
                results[name] = "FAIL"
                all_passed = False
                regression_details.append({
                    "name": name,
                    "status": "FAIL",
                    "regression_type": regression_type.value,
                    "detail": str(regression_detail)
                })

        # Summary
        print("\n" + "=" * 70)
        print("REGRESSION GATE SUMMARY")
        print("=" * 70)

        for name, status in results.items():
            symbol = "✓" if status == "PASS" else "✗"
            print(f"  {symbol} {name}: {status}")

        print()

        if all_passed:
            print("✓ REGRESSION GATE: PASS")
            print("  All golden examples verified - no regression detected")
            return True, regression_details
        else:
            print("✗ REGRESSION GATE: FAIL")
            print("  Regressions detected in:")
            for rd in regression_details:
                if rd["status"] == "FAIL":
                    print(f"    - {rd['name']}: {rd['regression_type']}")
            return False, regression_details

    finally:
        event_store.close()
        memory_store.close()
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    passed, details = run_regression_gate()
    sys.exit(0 if passed else 1)
