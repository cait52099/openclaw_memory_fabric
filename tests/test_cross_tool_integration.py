"""Cross-tool Integration Tests for OCMF.

These tests verify that memories created by one adapter cannot be
recalled by another adapter when using different tool scopes.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ocmaf.adapters.claude_code import ClaudeCodeAdapter
from src.ocmaf.adapters.codex_cli import CodexCLIAdapter
from src.ocmaf.sdk import MemorySession


class TestCrossToolIsolation:
    """Cross-tool isolation tests."""

    def setup_method(self):
        """Create test database."""
        self.db_path = tempfile.mktemp(suffix='.db')
        self.cc_adapter = ClaudeCodeAdapter(db_path=self.db_path)
        self.codex_adapter = CodexCLIAdapter(db_path=self.db_path)

    def teardown_method(self):
        """Cleanup."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_claude_to_codex_isolation(self):
        """Verify Claude Code memories are NOT recalled by Codex CLI.

        This is a HARD ACCEPTANCE test - MUST PASS.
        """
        # Write with Claude Code
        event_id = self.cc_adapter.after_response(
            "Remember: Python preference",
            "Sure, I remember Python is preferred",
            {"user": "test_user", "project": "test_proj"}
        )
        assert event_id, "Claude Code should create event"

        # Recall with Codex CLI - should return 0 memories (isolation)
        injection = self.codex_adapter.before_response(
            "Python preference",
            {"user": "test_user", "project": "test_proj"}
        )

        # HARD ASSERTION: Codex should NOT recall Claude Code's memories
        # The injection should be empty or not contain Claude's memory
        assert injection == "" or "Python preference" not in injection, \
            f"FAIL: Codex recalled Claude's memory! Got: {injection[:100]}"

        print("✓ Claude → Codex isolation: PASS")

    def test_codex_to_claude_isolation(self):
        """Verify Codex CLI memories are NOT recalled by Claude Code.

        This is a HARD ACCEPTANCE test - MUST PASS.
        """
        # Write with Codex CLI
        event_id = self.codex_adapter.after_response(
            "Remember: Use Docker",
            "Sure, I'll use Docker",
            {"user": "test_user", "project": "test_proj"}
        )
        assert event_id, "Codex CLI should create event"

        # Recall with Claude Code - should return 0 memories (isolation)
        injection = self.cc_adapter.before_response(
            "Docker",
            {"user": "test_user", "project": "test_proj"}
        )

        # HARD ASSERTION: Claude should NOT recall Codex's memories
        assert injection == "" or "Docker" not in injection, \
            f"FAIL: Claude recalled Codex's memory! Got: {injection[:100]}"

        print("✓ Codex → Claude isolation: PASS")

    def test_same_tool_recall_claude(self):
        """Verify Claude Code can recall its own memories."""
        # Write with Claude Code
        event_id = self.cc_adapter.after_response(
            "Remember: Test preference",
            "Sure, testing is important",
            {"user": "test_user", "project": "test_proj"}
        )
        assert event_id, "Should create event"

        # Recall with Claude Code - should return memories
        injection = self.cc_adapter.before_response(
            "Test preference",
            {"user": "test_user", "project": "test_proj"}
        )

        # HARD ASSERTION: Claude should recall its own memories
        assert injection != "", "Claude should recall its own memory"
        assert "Test preference" in injection or "testing" in injection.lower(), \
            f"Claude should find its own memory. Got: {injection[:100]}"

        print("✓ Same tool (Claude) recall: PASS")

    def test_same_tool_recall_codex(self):
        """Verify Codex CLI can recall its own memories."""
        # Write with Codex CLI
        event_id = self.codex_adapter.after_response(
            "Remember: API design",
            "Sure, REST API is good",
            {"user": "test_user", "project": "test_proj"}
        )
        assert event_id, "Should create event"

        # Recall with Codex CLI - should return memories
        injection = self.codex_adapter.before_response(
            "API design",
            {"user": "test_user", "project": "test_proj"}
        )

        # HARD ASSERTION: Codex should recall its own memories
        assert injection != "", "Codex should recall its own memory"
        assert "API" in injection or "REST" in injection, \
            f"Codex should find its own memory. Got: {injection[:100]}"

        print("✓ Same tool (Codex) recall: PASS")


def run_tests():
    """Run all cross-tool integration tests."""
    print("=" * 60)
    print("Cross-Tool Integration Tests (Phase 3B.1)")
    print("=" * 60)

    test_class = TestCrossToolIsolation()

    tests = [
        ("test_claude_to_codex_isolation", test_class.test_claude_to_codex_isolation),
        ("test_codex_to_claude_isolation", test_class.test_codex_to_claude_isolation),
        ("test_same_tool_recall_claude", test_class.test_same_tool_recall_claude),
        ("test_same_tool_recall_codex", test_class.test_same_tool_recall_codex),
    ]

    passed = 0
    failed = []

    for test_name, test_fn in tests:
        test_class.setup_method()
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed.append(test_name)
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
            failed.append(test_name)
        finally:
            test_class.teardown_method()

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{len(tests)} passed")
    if failed:
        print(f"Failed: {failed}")
    print("=" * 60)

    return passed == len(tests)


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
