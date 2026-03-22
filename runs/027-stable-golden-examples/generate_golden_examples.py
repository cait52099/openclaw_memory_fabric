#!/usr/bin/env python3
"""
Phase 6F: Stable Host-Visible Golden Examples Generator

This script generates stable, reproducible golden examples for:
1. Recall conflict scenario
2. Explain cross-host scenario
3. Recall provenance display
4. Injection text output

Run: python3 runs/027-stable-golden-examples/generate_golden_examples.py
"""

import sys
import os
import tempfile
import shutil
import json
from datetime import datetime, timezone

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../..", "src"))

from ocmaf.storage.event_store import EventStore
from ocmaf.storage.memory_store import MemoryStore
from ocmaf.api.remember import RememberAPI
from ocmaf.api.recall import RecallAPI
from ocmaf.event.envelope import EventEnvelope
from ocmaf.event.scope import Scope
from ocmaf.event.types import EventType


def write_file(path, content):
    """Write content to file."""
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ Written: {path}")


def run_tests():
    """Generate all golden examples."""
    print("=" * 70)
    print("Phase 6F - Stable Host-Visible Golden Examples Generator")
    print("=" * 70)

    # Create temp directory for test DBs
    temp_dir = tempfile.mkdtemp(prefix="ocmf_6f_golden_")
    db_path = os.path.join(temp_dir, "test.db")
    run_dir = os.path.dirname(__file__)

    results = {
        "conflict_test_passed": False,
        "explain_test_passed": False,
        "recall_conflict_golden": None,
        "explain_crosshost_golden": None,
        "recall_provenance_golden": None,
        "injection_text_golden": None,
    }

    try:
        # Initialize stores
        event_store = EventStore(db_path=db_path)
        memory_store = MemoryStore(db_path=db_path)
        remember_api = RememberAPI(event_store, memory_store)
        recall_api = RecallAPI(memory_store, event_store)

        test_project = "golden_test_project"

        # =========================================================
        # PART A: Stable Conflict Scenario
        # =========================================================
        print("\n" + "=" * 70)
        print("PART A: Stable Conflict Scenario")
        print("=" * 70)

        # Write two memories with SAME title but DIFFERENT content from different sources
        print("\nWriting conflict-inducing memories...")
        for i, (content, summary, tool) in enumerate([
            ('Testing framework: pytest is the best for unit testing in Python', 'Pytest recommended', 'claude-code'),
            ('Testing framework: unittest is built-in and works well for Python', 'Unittest recommended', 'codex-cli'),
        ]):
            event = EventEnvelope(
                source_tool=tool,
                scope=Scope(user="test_user", project=test_project),
                event_type=EventType.DECISION,
                payload={
                    "content": content,
                    "summary": summary,
                    "keywords": ["testing", "framework", "pytest", "unittest"],
                    "title": "Testing framework",  # Same title = conflict
                },
            )
            remember_api.remember(event)
            print(f"✓ Memory {i+1} from {tool}: {summary}")

        # Recall to trigger conflict detection
        print("\nExecuting recall for conflict detection...")
        recall_result = recall_api.recall("testing framework", {"user": "test_user", "project": test_project})
        recall_dict = recall_result.to_dict()

        conflict_detected = recall_dict.get("conflict_detected", False)
        candidates = recall_dict.get("candidates", [])

        print(f"\nConflict detected: {conflict_detected}")
        print(f"Candidates: {len(candidates)}")

        # Generate recall conflict golden output
        conflict_lines = []
        conflict_lines.append("=" * 70)
        conflict_lines.append("RECALL CONFLICT GOLDEN EXAMPLE")
        conflict_lines.append("=" * 70)
        conflict_lines.append("")
        conflict_lines.append(f"Query: 'testing framework'")
        conflict_lines.append(f"Conflict detected: {conflict_detected}")
        conflict_lines.append(f"Number of candidates: {len(candidates)}")
        conflict_lines.append("")
        conflict_lines.append("MEMORIES RETURNED:")
        conflict_lines.append("-" * 40)

        for mem in recall_dict.get("memories", []):
            ts = mem.get("timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    ts = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            conflict_lines.append(f"  Source: {mem.get('source_host_friendly', 'Unknown')}")
            conflict_lines.append(f"  Timestamp: {ts}")
            conflict_lines.append(f"  Content: {mem.get('content', '')}")
            conflict_lines.append(f"  Summary: {mem.get('summary', '')}")
            conflict_lines.append("")

        if candidates:
            conflict_lines.append("CONFLICT CANDIDATES:")
            conflict_lines.append("-" * 40)
            for c in candidates:
                conflict_lines.append(f"  [{c.get('source_host_friendly', 'Unknown')}] {c.get('content', '')[:60]}")
            conflict_lines.append("")

        conflict_lines.append("CLI OUTPUT FORMAT:")
        conflict_lines.append("-" * 40)
        conflict_lines.append(f"Found {len(recall_dict.get('memories', []))} memories:")
        for mem in recall_dict.get("memories", []):
            ts = mem.get("timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    ts = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            conflict_lines.append(f"  From {mem.get('source_host_friendly', 'Unknown')}: \"{mem.get('content', '')[:50]}\" ({ts})")

        if conflict_detected:
            conflict_lines.append("")
            conflict_lines.append("⚠️ CONFLICT DETECTED")
            conflict_lines.append(f"  {len(candidates)} conflicting versions found:")
            for c in candidates:
                conflict_lines.append(f"  - [{c.get('source_host_friendly', 'Unknown')}] \"{c.get('content', '')[:50]}\"")

        recall_conflict_golden = "\n".join(conflict_lines)
        conflict_golden_path = os.path.join(run_dir, "recall_conflict_golden.txt")
        write_file(conflict_golden_path, recall_conflict_golden)
        results["recall_conflict_golden"] = conflict_golden_path
        results["conflict_test_passed"] = conflict_detected and len(candidates) >= 2

        # =========================================================
        # PART B: Stable Cross-Host Explain Scenario
        # =========================================================
        print("\n" + "=" * 70)
        print("PART B: Stable Cross-Host Explain Scenario")
        print("=" * 70)

        # Use memories from above - explain on first memory
        if recall_dict.get("memories", []):
            first_mem_id = recall_dict["memories"][0].get("memory_id")

            print(f"\nExecuting explain for: {first_mem_id}")
            explain_result = recall_api.explain(first_mem_id, recall_query="testing framework")

            print(f"Success: {explain_result.get('success')}")
            print(f"Source: {explain_result.get('source_host_friendly')}")
            print(f"Match reasons: {len(explain_result.get('match_reasons', []))}")
            print(f"Also written by: {explain_result.get('also_written_by', [])}")

            # Generate explain cross-host golden output
            explain_lines = []
            explain_lines.append("=" * 70)
            explain_lines.append("EXPLAIN CROSS-HOST GOLDEN EXAMPLE")
            explain_lines.append("=" * 70)
            explain_lines.append("")
            explain_lines.append(f"Memory ID: {first_mem_id}")
            explain_lines.append(f"Recall Query: 'testing framework'")
            explain_lines.append("")
            explain_lines.append("STRUCTURED OUTPUT:")
            explain_lines.append("-" * 40)
            explain_lines.append(f"  success: {explain_result.get('success')}")
            explain_lines.append(f"  source_host_friendly: {explain_result.get('source_host_friendly')}")
            explain_lines.append(f"  event_timestamp: {explain_result.get('event_timestamp')}")
            explain_lines.append(f"  match_reasons: {json.dumps(explain_result.get('match_reasons', []), indent=4)}")
            explain_lines.append(f"  also_written_by: {explain_result.get('also_written_by', [])}")
            explain_lines.append(f"  explain: {explain_result.get('explain')}")
            explain_lines.append("")

            explain_lines.append("CLI FRIENDLY OUTPUT FORMAT:")
            explain_lines.append("-" * 40)
            explain_lines.append("## Memory Explanation")
            explain_lines.append("")
            explain_lines.append(f"Source: {explain_result.get('source_host_friendly')}")

            ts = explain_result.get("event_timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    ts = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
                explain_lines.append(f"Timestamp: {ts}")

            explain_lines.append("")
            explain_lines.append("Match Reasons:")
            for mr in explain_result.get("match_reasons", []):
                if mr["type"] == "keyword":
                    explain_lines.append(f"  • Keyword match: {', '.join(mr.get('matched', []))}")
                elif mr["type"] == "scope":
                    for k, v in mr.get("matched", {}).items():
                        explain_lines.append(f"  • Scope match: {k}={v}")

            also_written = explain_result.get("also_written_by", [])
            if also_written:
                explain_lines.append(f"\nAlso written by: {', '.join(also_written)}")

            explain_lines.append("")
            explain_lines.append(explain_result.get("explain", ""))

            mem_content = explain_result.get("memory", {}).get("content", "")
            if mem_content:
                explain_lines.append(f"\nContent: \"{mem_content}\"")

            explain_crosshost_golden = "\n".join(explain_lines)
            explain_golden_path = os.path.join(run_dir, "explain_crosshost_golden.txt")
            write_file(explain_golden_path, explain_crosshost_golden)
            results["explain_crosshost_golden"] = explain_golden_path
            results["explain_test_passed"] = (
                explain_result.get("success") and
                explain_result.get("source_host_friendly") and
                len(explain_result.get("match_reasons", [])) > 0
            )

        # =========================================================
        # PART C: Recall Provenance Golden Output
        # =========================================================
        print("\n" + "=" * 70)
        print("PART C: Recall Provenance Golden Output")
        print("=" * 70)

        # Write memories with different timestamps
        print("\nWriting memories with different timestamps...")
        for i, (content, summary, tool) in enumerate([
            ('Python version: use 3.11+ for best performance', 'Python 3.11+ recommended', 'claude-code'),
            ('Python version: 3.9 is stable and widely compatible', 'Python 3.9 stable', 'codex-cli'),
            ('Python version: 3.12 has fastest execution', 'Python 3.12 fastest', 'claude-code'),
        ]):
            event = EventEnvelope(
                source_tool=tool,
                scope=Scope(user="test_user", project=test_project),
                event_type=EventType.DECISION,
                payload={
                    "content": content,
                    "summary": summary,
                    "keywords": ["python", "version"],
                    "title": "Python version",
                },
            )
            remember_api.remember(event)
            print(f"✓ Memory {i+1} from {tool}: {summary}")

        recall_result2 = recall_api.recall("python version", {"user": "test_user", "project": test_project})
        recall_dict2 = recall_result2.to_dict()

        # Generate recall provenance golden output
        provenance_lines = []
        provenance_lines.append("=" * 70)
        provenance_lines.append("RECALL PROVENANCE GOLDEN EXAMPLE")
        provenance_lines.append("=" * 70)
        provenance_lines.append("")
        provenance_lines.append(f"Query: 'python version'")
        provenance_lines.append(f"Memories found: {len(recall_dict2.get('memories', []))}")
        provenance_lines.append("")
        provenance_lines.append("MEMORIES WITH PROVENANCE:")
        provenance_lines.append("-" * 40)

        for mem in recall_dict2.get("memories", []):
            ts = mem.get("timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    ts = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            provenance_lines.append(f"  From {mem.get('source_host_friendly', 'Unknown')} ({ts}):")
            provenance_lines.append(f"    Content: {mem.get('content', '')}")
            provenance_lines.append(f"    Summary: {mem.get('summary', '')}")
            provenance_lines.append("")

        provenance_lines.append("CLI OUTPUT FORMAT:")
        provenance_lines.append("-" * 40)
        provenance_lines.append(f"Found {len(recall_dict2.get('memories', []))} memories:")
        for mem in recall_dict2.get("memories", []):
            ts = mem.get("timestamp", "")
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    ts = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            provenance_lines.append(f"  From {mem.get('source_host_friendly', 'Unknown')}: \"{mem.get('content', '')[:50]}\" ({ts})")

        recall_provenance_golden = "\n".join(provenance_lines)
        provenance_golden_path = os.path.join(run_dir, "recall_provenance_golden.txt")
        write_file(provenance_golden_path, recall_provenance_golden)
        results["recall_provenance_golden"] = provenance_golden_path

        # =========================================================
        # PART D: Injection Text Golden Output
        # =========================================================
        print("\n" + "=" * 70)
        print("PART D: Injection Text Golden Output")
        print("=" * 70)

        # Use the conflict recall result
        injection_text = recall_result.to_injection_text()
        gist_text = recall_result.to_gist_text()

        print(f"\nInjection text length: {len(injection_text)} chars")
        print(f"Gist text length: {len(gist_text)} chars")

        # Generate injection text golden output
        injection_lines = []
        injection_lines.append("=" * 70)
        injection_lines.append("INJECTION TEXT GOLDEN EXAMPLE")
        injection_lines.append("=" * 70)
        injection_lines.append("")
        injection_lines.append("to_injection_text() OUTPUT:")
        injection_lines.append("-" * 40)
        injection_lines.append(injection_text)
        injection_lines.append("")
        injection_lines.append("=" * 70)
        injection_lines.append("to_gist_text() OUTPUT:")
        injection_lines.append("-" * 40)
        injection_lines.append(gist_text)

        injection_text_golden = "\n".join(injection_lines)
        injection_golden_path = os.path.join(run_dir, "injection_text_golden.txt")
        write_file(injection_golden_path, injection_text_golden)
        results["injection_text_golden"] = injection_golden_path

        # =========================================================
        # Summary
        # =========================================================
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        print(f"\n✓ Conflict test passed: {results['conflict_test_passed']}")
        print(f"✓ Explain test passed: {results['explain_test_passed']}")
        print(f"✓ Recall conflict golden: {results['recall_conflict_golden']}")
        print(f"✓ Explain cross-host golden: {results['explain_crosshost_golden']}")
        print(f"✓ Recall provenance golden: {results['recall_provenance_golden']}")
        print(f"✓ Injection text golden: {results['injection_text_golden']}")

        all_passed = results["conflict_test_passed"] and results["explain_test_passed"]

        if all_passed:
            print("\n✓ PHASE 6F STABLE GOLDEN EXAMPLES: PASS")
        else:
            print("\n✗ PHASE 6F STABLE GOLDEN EXAMPLES: FAIL")

        return results, all_passed

    finally:
        # Cleanup
        try:
            event_store.close()
            memory_store.close()
            shutil.rmtree(temp_dir)
            print(f"\n✓ Cleanup: removed {temp_dir}")
        except Exception as e:
            print(f"\n⚠ Cleanup error: {e}")


if __name__ == "__main__":
    results, passed = run_tests()
    sys.exit(0 if passed else 1)
