#!/usr/bin/env python3
"""Adapter smoke tests."""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_basic_import():
    """Test basic imports."""
    from ocmaf.sdk import MemorySession
    from ocmaf.adapters import ClaudeCodeAdapter
    print("  Import SDK: OK")
    print("  Import Adapter: OK")


def test_memory_session():
    """Test memory session basic operations."""
    from ocmaf.sdk import MemorySession

    # Create temp DB
    db_path = Path(tempfile.mktemp(suffix=".db"))

    try:
        with MemorySession(user="test_user", db_path=db_path) as session:
            # Remember
            event_id = session.capture_chat_turn(
                "What is Python?",
                "Python is a programming language.",
                source_tool="test"
            )
            assert event_id, "Failed to create event"
            print(f"  Remember event: {event_id}")

            # Recall
            result = session.recall("Python")
            print(f"  Found {len(result.memories)} memories")
            assert len(result.memories) > 0, "Failed to recall"

        print("  Memory session: OK")
    finally:
        if db_path.exists():
            db_path.unlink()


def test_adapter_hooks():
    """Test adapter hooks."""
    from ocmaf.adapters.claude_code import ClaudeCodeAdapter

    db_path = Path(tempfile.mktemp(suffix=".db"))

    try:
        adapter = ClaudeCodeAdapter(db_path=db_path)

        # Before response (recall)
        injection = adapter.before_response("test query", {"user": "test_user"})
        print(f"  before_response: {len(injection)} chars")

        # After response (remember)
        event_id = adapter.after_response(
            "Test query",
            "Test response",
            {"user": "test_user"}
        )
        print(f"  after_response: {event_id}")

        print("  Adapter hooks: OK")
    finally:
        if db_path.exists():
            db_path.unlink()


def test_closed_loop():
    """Test complete recall -> remember -> recall closed loop."""
    from ocmaf.adapters.claude_code import ClaudeCodeAdapter

    db_path = Path(tempfile.mktemp(suffix=".db"))

    try:
        adapter = ClaudeCodeAdapter(db_path=db_path)
        context = {"user": "test_user", "session": "test_session"}

        # Round 1
        query1 = "How do I create a Python class?"
        response1 = "Use the class keyword: class MyClass:"

        injection1 = adapter.before_response(query1, context)
        print(f"  Round 1 injection: {len(injection1)} chars")

        event_id = adapter.after_response(query1, response1, context)
        print(f"  Round 1 remembered: {event_id}")

        # Round 2 - should recall from round 1
        query2 = "Show me a Python class example"
        injection2 = adapter.before_response(query2, context)
        print(f"  Round 2 injection: {len(injection2)} chars")

        print("  Closed loop: OK")
    finally:
        if db_path.exists():
            db_path.unlink()


def test_scope_mapping():
    """Test scope mapping."""
    from ocmaf.adapters.scope_mapping import get_scope_mapper

    mapper = get_scope_mapper("claude-code")
    scope = mapper.map_from_context({
        "user": "my_user",
        "workspace": "my_workspace",
        "project": "my_project",
        "session": "my_session"
    })

    assert scope["user"] == "my_user"
    assert scope["workspace"] == "my_workspace"
    assert scope["project"] == "my_project"
    assert scope["session"] == "my_session"

    print("  Scope mapping: OK")


def test_injection_policy():
    """Test injection policy."""
    from ocmaf.adapters.base import InjectionPolicy

    # Test truncation
    policy = InjectionPolicy(max_length=100)
    text = "A" * 200
    truncated = policy.truncate(text)
    assert len(truncated) < 210
    assert "..." in truncated
    print("  Truncation: OK")

    # Test layer-based
    system_policy = InjectionPolicy.for_layer("system")
    user_policy = InjectionPolicy.for_layer("user")

    assert system_policy.max_length < user_policy.max_length
    print(f"  System limit: {system_policy.max_length}")
    print(f"  User limit: {user_policy.max_length}")
    print("  Layer-based policy: OK")


def main():
    """Run all tests."""
    print("=" * 50)
    print("OCMF Adapter Smoke Test")
    print("=" * 50)

    tests = [
        ("Basic Import", test_basic_import),
        ("Memory Session", test_memory_session),
        ("Adapter Hooks", test_adapter_hooks),
        ("Closed Loop", test_closed_loop),
        ("Scope Mapping", test_scope_mapping),
        ("Injection Policy", test_injection_policy),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            print(f"\n--- {name} ---")
            test_func()
            passed += 1
            print(f"{name}: PASS")
        except Exception as e:
            print(f"{name}: FAIL - {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
