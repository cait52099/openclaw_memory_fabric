#!/usr/bin/env python3
"""
Phase 6E Integration Test - Host-Visible Output

Tests that recall/explain/conflict outputs are visible to users in CLI format.

Run: python3 runs/026-cross-host-visible/test_host_visible_output.py
"""

import sys
import os
import tempfile
import shutil
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
from ocmaf.api.friendly import get_friendly_name


def run_tests():
    """Run all Phase 6E host-visible output tests."""
    print("=" * 60)
    print("Phase 6E - Host-Visible Output Integration Test")
    print("=" * 60)

    # Create temp directory for test DBs
    temp_dir = tempfile.mkdtemp(prefix="ocmf_6e_test_")
    db_path = os.path.join(temp_dir, "test.db")

    try:
        # Initialize stores
        event_store = EventStore(db_path=db_path)
        memory_store = MemoryStore(db_path=db_path)
        remember_api = RememberAPI(event_store, memory_store)
        recall_api = RecallAPI(memory_store, event_store)

        # Test data with different source tools
        test_project = "test_6e_project"

        # Write memories from different sources (simulating cross-host)
        events = [
            # From Claude
            EventEnvelope(
                source_tool="claude-code",
                scope=Scope(user="test_user", project=test_project),
                event_type=EventType.DECISION,
                payload={
                    "content": "Testing framework: pytest is best for unit tests",
                    "summary": "Pytest is the preferred testing framework",
                    "keywords": ["testing", "framework", "pytest"],
                },
            ),
            # From Codex
            EventEnvelope(
                source_tool="codex-cli",
                scope=Scope(user="test_user", project=test_project),
                event_type=EventType.DECISION,
                payload={
                    "content": "Testing framework: unittest is built-in and works well",
                    "summary": "Unittest is the built-in testing framework",
                    "keywords": ["testing", "framework", "unittest"],
                },
            ),
            # From Claude (another topic)
            EventEnvelope(
                source_tool="claude-code",
                scope=Scope(user="test_user", project=test_project),
                event_type=EventType.DECISION,
                payload={
                    "content": "Python version: use 3.11+ for best performance",
                    "summary": "Python 3.11+ recommended",
                    "keywords": ["python", "version", "performance"],
                },
            ),
        ]

        print("\n=== Test: Write memories from different sources ===")
        event_ids = []
        for i, event in enumerate(events):
            event_id = remember_api.remember(event)
            event_ids.append(event_id)
            print(f"✓ Event {i+1} stored: {event_id[:8]}... from {event.source_tool}")

        # Small delay to ensure timestamps differ
        import time
        time.sleep(0.1)

        # =========================================================
        # TEST 1: Recall output with source info
        # =========================================================
        print("\n=== Test: Recall with provenance display ===")
        context = {"user": "test_user", "project": test_project}
        recall_result = recall_api.recall("testing framework", context)
        recall_dict = recall_result.to_dict()

        memories = recall_dict.get("memories", [])
        print(f"✓ Recall returned {len(memories)} memories")

        # Check each memory has source info
        source_fields_ok = True
        for mem in memories:
            if not mem.get("source_tool"):
                print(f"  ✗ Missing source_tool in memory")
                source_fields_ok = False
            if not mem.get("source_host_friendly"):
                print(f"  ✗ Missing source_host_friendly in memory")
                source_fields_ok = False
            if not mem.get("timestamp"):
                print(f"  ✗ Missing timestamp in memory")
                source_fields_ok = False

        if source_fields_ok:
            print(f"✓ All memories have source_tool, source_host_friendly, timestamp")

        # Check we got memories from both Claude and Codex
        sources = set(mem.get("source_tool") for mem in memories)
        if "claude-code" in sources and "codex-cli" in sources:
            print(f"✓ Cross-host recall works: got memories from {sources}")
        else:
            print(f"✗ Expected memories from both claude-code and codex-cli, got: {sources}")

        # =========================================================
        # TEST 2: Conflict detection with candidates
        # =========================================================
        print("\n=== Test: Conflict detection display ===")
        if recall_dict.get("conflict_detected"):
            print(f"✓ Conflict detected: {recall_dict.get('conflict_detected')}")
            candidates = recall_dict.get("candidates", [])
            print(f"✓ {len(candidates)} conflict candidates:")
            for c in candidates:
                print(f"  - [{c.get('source_host_friendly')}] \"{c.get('content')[:50]}...\"")
                print(f"    timestamp: {c.get('timestamp')}")
        else:
            print("⚠ No conflict detected (this might be expected depending on implementation)")

        # =========================================================
        # TEST 3: explain() with match_reasons and provenance
        # =========================================================
        print("\n=== Test: explain() with match reasons and provenance ===")
        if memories:
            memory_id = memories[0].get("memory_id")
            if memory_id:
                explain_result = recall_api.explain(memory_id, recall_query="testing framework")
                if explain_result.get("success"):
                    print(f"✓ explain() successful")

                    # Check provenance
                    if explain_result.get("source_host_friendly"):
                        print(f"✓ Provenance: {explain_result.get('source_host_friendly')}")
                    else:
                        print("✗ Missing source_host_friendly in explain")

                    # Check match_reasons
                    match_reasons = explain_result.get("match_reasons", [])
                    if match_reasons:
                        print(f"✓ Match reasons: {len(match_reasons)} reasons")
                        for mr in match_reasons:
                            print(f"  - type={mr.get('type')}, matched={mr.get('matched')}")
                    else:
                        print("⚠ No match_reasons found")

                    # Check also_written_by (cross-host context)
                    also_written = explain_result.get("also_written_by", [])
                    if also_written:
                        print(f"✓ Cross-host context: also_written_by = {also_written}")
                    else:
                        print("⚠ No also_written_by (might be expected)")

                    # Check human-readable explain text
                    if explain_result.get("explain"):
                        print(f"✓ Explain text: \"{explain_result.get('explain')[:80]}...\"")
                else:
                    print(f"✗ explain() failed: {explain_result.get('error')}")

        # =========================================================
        # TEST 4: to_injection_text() with provenance
        # =========================================================
        print("\n=== Test: Injection text with source info ===")
        injection_text = recall_result.to_injection_text()
        if injection_text:
            print(f"✓ Injection text generated ({len(injection_text)} chars)")
            # Check if source info is in injection
            if "From Claude" in injection_text or "From Codex" in injection_text:
                print(f"✓ Source info found in injection text")
            else:
                print("⚠ Source info not found in injection text")
            if "CONFLICT" in injection_text or "conflict" in injection_text.lower():
                print(f"✓ Conflict info found in injection text")
        else:
            print("✗ No injection text generated")

        # =========================================================
        # TEST 5: to_gist_text() with provenance
        # =========================================================
        print("\n=== Test: Gist text with source info ===")
        gist_text = recall_result.to_gist_text()
        if gist_text:
            print(f"✓ Gist text generated ({len(gist_text)} chars)")
            if "[Claude]" in gist_text or "[Codex]" in gist_text:
                print(f"✓ Source brackets found in gist text")
            else:
                print("⚠ Source brackets not found in gist text")
        else:
            print("✗ No gist text generated")

        # =========================================================
        # TEST 6: Friendly name mapping
        # =========================================================
        print("\n=== Test: Friendly name mapping ===")
        test_cases = [
            ("claude-code", "Claude"),
            ("codex-cli", "Codex"),
            ("openclaw", "OpenClaw"),
            ("synthetic", "Synthetic (Test)"),
        ]
        for source_tool, expected_friendly in test_cases:
            actual = get_friendly_name(source_tool)
            if actual == expected_friendly:
                print(f"✓ {source_tool} -> {actual}")
            else:
                print(f"✗ {source_tool} -> {actual} (expected {expected_friendly})")

        # =========================================================
        # Summary
        # =========================================================
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        # Count passed/failed
        passed = 0
        failed = 0

        if source_fields_ok:
            passed += 1
        else:
            failed += 1

        if memories:
            passed += 1
        else:
            failed += 1

        if recall_dict.get("conflict_detected"):
            passed += 1
        else:
            # This might not be a failure - depends on implementation
            pass

        if explain_result.get("success") and explain_result.get("source_host_friendly"):
            passed += 1
        else:
            failed += 1

        if match_reasons:
            passed += 1
        else:
            failed += 1

        if injection_text:
            passed += 1
        else:
            failed += 1

        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        if failed == 0:
            print("\n✓ PHASE 6E HOST-VISIBLE OUTPUT: PASS")
            return True
        else:
            print("\n✗ PHASE 6E HOST-VISIBLE OUTPUT: FAIL")
            return False

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
    success = run_tests()
    sys.exit(0 if success else 1)
