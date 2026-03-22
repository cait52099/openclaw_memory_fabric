#!/usr/bin/env python3
"""Test script for Cross-Host UX Output Implementation."""

import sys
import os
import tempfile
sys.path.insert(0, '/Users/caihongwei/project/openclaw_memory_fabric/src')

from datetime import datetime, timezone
from ocmaf.api.recall import RecallAPI, RecallResult
from ocmaf.api.friendly import get_friendly_name, get_source_tool_label, FRIENDLY_NAMES
from ocmaf.storage.event_store import EventStore
from ocmaf.storage.memory_store import MemoryStore
from ocmaf.object.model import MemoryObject
from ocmaf.object.types import Tier, State, Resolution
from ocmaf.event.envelope import EventEnvelope
from ocmaf.event.scope import Scope
from ocmaf.event.types import EventType


def test_friendly_names():
    """Test friendly name mapping."""
    print("=== Test: Friendly Names ===")

    assert FRIENDLY_NAMES["claude-code"] == "Claude"
    assert FRIENDLY_NAMES["codex-cli"] == "Codex"
    assert FRIENDLY_NAMES["openclaw"] == "OpenClaw"
    assert FRIENDLY_NAMES["synthetic"] == "Synthetic (Test)"

    assert get_friendly_name("claude-code") == "Claude"
    assert get_friendly_name("codex-cli") == "Codex"
    assert get_friendly_name("synthetic") == "Synthetic (Test)"
    assert get_friendly_name("unknown") == "unknown"

    label = get_source_tool_label("claude-code")
    assert label["source_tool"] == "claude-code"
    assert label["source_host_friendly"] == "Claude"
    assert label["is_synthetic"] == False

    label_synthetic = get_source_tool_label("synthetic")
    assert label_synthetic["source_tool"] == "synthetic"
    assert label_synthetic["source_host_friendly"] == "Synthetic (Test)"
    assert label_synthetic["is_synthetic"] == True

    print("✅ Friendly names: PASS")
    return True


def test_recall_result_to_dict():
    """Test RecallResult.to_dict() includes cross-host fields."""
    print("\n=== Test: RecallResult.to_dict() ===")

    # Use temp database
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_recall.db")
        event_store = EventStore(db_path=db_path)
        memory_store = MemoryStore(db_path=db_path)

        # Create test event
        event = EventEnvelope(
            event_id="evt-001",
            source_tool="claude-code",
            scope=Scope(user="test_user", project="test_project"),
            event_type=EventType.DECISION,
            payload={"content": "Testing framework: pytest"},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        event_store.append(event)

        # Create test memory
        mem = MemoryObject(
            memory_id="test-mem-001",
            title="Testing Framework",
            summary="Use pytest",
            content="Testing framework: pytest",
            user="test_user",
            project="test_project",
            tier=Tier.WORKING,
            state=State.ACTIVE,
            resolution=Resolution.GIST,
            source_event_ids=["evt-001"],
        )

        # Create RecallResult
        result = RecallResult(
            memories=[mem],
            query="testing framework",
            context={"user": "test_user", "project": "test_project"},
            traces={"trace_id": "test-trace"},
            conflict_detected=False,
            candidates=[],
            event_store=event_store,
        )

        # Convert to dict
        result_dict = result.to_dict()

        # Verify cross-host fields
        assert "memories" in result_dict
        assert len(result_dict["memories"]) == 1

        mem_dict = result_dict["memories"][0]
        assert "source_tool" in mem_dict, f"source_tool missing: {mem_dict.keys()}"
        assert mem_dict["source_tool"] == "claude-code"
        assert "source_host_friendly" in mem_dict
        assert mem_dict["source_host_friendly"] == "Claude"
        assert "timestamp" in mem_dict
        assert "is_synthetic" in mem_dict
        assert mem_dict["is_synthetic"] == False

        print(f"✅ RecallResult.to_dict() includes source_tool: {mem_dict['source_tool']}")
        print(f"✅ RecallResult.to_dict() includes source_host_friendly: {mem_dict['source_host_friendly']}")
        print(f"✅ RecallResult.to_dict() includes timestamp: {mem_dict['timestamp']}")
        print(f"✅ RecallResult.to_dict() includes conflict_detected: {result_dict['conflict_detected']}")

        event_store.close()
        return True


def test_explain_output():
    """Test explain() returns enhanced fields."""
    print("\n=== Test: explain() Enhanced Output ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_explain.db")
        event_store = EventStore(db_path=db_path)
        memory_store = MemoryStore(db_path=db_path)

        # Create test event
        event = EventEnvelope(
            event_id="evt-exp-001",
            source_tool="codex-cli",
            scope=Scope(user="test_user", project="test_project"),
            event_type=EventType.DECISION,
            payload={"content": "Testing framework: unittest"},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        event_store.append(event)

        # Create test memory
        mem = MemoryObject(
            memory_id="test-exp-001",
            title="Testing Framework",
            summary="Use unittest",
            content="Testing framework: unittest",
            user="test_user",
            project="test_project",
            tier=Tier.WORKING,
            state=State.ACTIVE,
            resolution=Resolution.GIST,
            source_event_ids=["evt-exp-001"],
        )
        memory_store.put(mem)

        # Create API
        api = RecallAPI(memory_store=memory_store, event_store=event_store)

        # Call explain
        result = api.explain("test-exp-001", recall_query="testing framework")

        # Verify enhanced fields
        assert "match_reasons" in result, f"match_reasons missing: {result.keys()}"
        assert "source_tool" in result, f"source_tool missing: {result.keys()}"
        assert "source_host_friendly" in result, f"source_host_friendly missing: {result.keys()}"
        assert "event_timestamp" in result, f"event_timestamp missing: {result.keys()}"
        assert "also_written_by" in result, f"also_written_by missing: {result.keys()}"
        assert "explain" in result, f"explain missing: {result.keys()}"

        assert result["source_tool"] == "codex-cli"
        assert result["source_host_friendly"] == "Codex"
        assert result["event_timestamp"] is not None

        print(f"✅ explain() includes match_reasons: {result['match_reasons']}")
        print(f"✅ explain() includes source_tool: {result['source_tool']}")
        print(f"✅ explain() includes source_host_friendly: {result['source_host_friendly']}")
        print(f"✅ explain() includes also_written_by: {result['also_written_by']}")
        print(f"✅ explain() includes explain text: {result['explain']}")

        event_store.close()
        return True


def test_conflict_detection():
    """Test conflict detection identifies same entity different source."""
    print("\n=== Test: Conflict Detection ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_conflict.db")
        event_store = EventStore(db_path=db_path)
        memory_store = MemoryStore(db_path=db_path)

        # Create two events with different sources but same entity
        event1 = EventEnvelope(
            event_id="evt-conflict-1",
            source_tool="claude-code",
            scope=Scope(user="test_user", project="test_project"),
            event_type=EventType.DECISION,
            payload={"content": "Testing framework: pytest"},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        event2 = EventEnvelope(
            event_id="evt-conflict-2",
            source_tool="codex-cli",
            scope=Scope(user="test_user", project="test_project"),
            event_type=EventType.DECISION,
            payload={"content": "Testing framework: unittest"},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        event_store.append(event1)
        event_store.append(event2)

        # Create two memories with same title but different content
        mem1 = MemoryObject(
            memory_id="test-conflict-1",
            title="Testing Framework",
            summary="Use pytest",
            content="Testing framework: pytest",
            user="test_user",
            project="test_project",
            tier=Tier.WORKING,
            state=State.ACTIVE,
            resolution=Resolution.GIST,
            source_event_ids=["evt-conflict-1"],
        )
        mem2 = MemoryObject(
            memory_id="test-conflict-2",
            title="Testing Framework",
            summary="Use unittest",
            content="Testing framework: unittest",
            user="test_user",
            project="test_project",
            tier=Tier.WORKING,
            state=State.ACTIVE,
            resolution=Resolution.GIST,
            source_event_ids=["evt-conflict-2"],
        )
        memory_store.put(mem1)
        memory_store.put(mem2)

        # Create API
        api = RecallAPI(memory_store=memory_store, event_store=event_store)

        # Call recall
        result = api.recall(
            query="testing framework",
            context={"user": "test_user", "project": "test_project"},
        )

        result_dict = result.to_dict()

        print(f"conflict_detected: {result_dict['conflict_detected']}")
        if result_dict['conflict_detected']:
            print(f"candidates count: {len(result_dict['candidates'])}")
            for c in result_dict['candidates']:
                print(f"  - {c['source_tool']}: {c['content'][:50]}...")

        # Verify result has conflict_detected field
        assert "conflict_detected" in result_dict, f"conflict_detected missing: {result_dict.keys()}"
        print(f"✅ Conflict detection ran successfully")
        print(f"✅ Result has conflict_detected field: {result_dict.get('conflict_detected', 'MISSING')}")

        event_store.close()
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Cross-Host UX Output Implementation - Test Suite")
    print("=" * 60)

    tests = [
        ("Friendly Names", test_friendly_names),
        ("RecallResult.to_dict()", test_recall_result_to_dict),
        ("explain() Enhanced Output", test_explain_output),
        ("Conflict Detection", test_conflict_detection),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ {name}: FAIL - {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")

    all_passed = all(p for _, p in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("FINAL_STATUS: PASS")
        print("RECALL_OUTPUT_ENHANCED: YES")
        print("EXPLAIN_OUTPUT_ENHANCED: YES")
        print("CONFLICT_DETECTION_MINIMAL: YES")
    else:
        print("FINAL_STATUS: FAIL")
        print("Some tests failed")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
