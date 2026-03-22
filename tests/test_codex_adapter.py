"""Test Codex CLI adapter - Hermetic Version."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ocmaf.adapters.codex_cli import CodexCLIAdapter
from src.ocmaf.adapters.claude_code import ClaudeCodeAdapter
from src.ocmaf.event.scope import Scope


class TestCodexAdapter:
    """Hermetic test class for CodexCLIAdapter."""

    def setup_method(self):
        """Create isolated test database."""
        self.db_path = tempfile.mktemp(suffix='.db')
        self.adapter = CodexCLIAdapter(db_path=self.db_path)

    def teardown_method(self):
        """Cleanup test database."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_adapter_import(self):
        """Verify CodexCLIAdapter can be imported."""
        from src.ocmaf.adapters import CodexCLIAdapter
        assert CodexCLIAdapter is not None

    def test_get_name(self):
        """Verify adapter returns correct name."""
        assert self.adapter.get_name() == "codex-cli"

    def test_scope_includes_tool(self):
        """Verify scope includes tool='codex-cli'."""
        scope = self.adapter.get_scope_from_context({})
        assert scope.get("tool") == "codex-cli"

    def test_before_response_returns_string(self):
        """Verify before_response returns string."""
        result = self.adapter.before_response("test query", {"user": "test"})
        assert isinstance(result, str)

    def test_after_response_returns_event_id(self):
        """Verify after_response returns event_id."""
        result = self.adapter.after_response(
            "test query",
            "test response",
            {"user": "test"}
        )
        assert isinstance(result, str)  # event_id or empty string

    def test_cross_tool_isolation(self):
        """Verify cross-tool isolation works with Codex CLI.

        This test has REAL assertions - verifies that memories written
        by Codex CLI are NOT recalled by Claude Code.
        """
        # Write with tool='codex-cli'
        event_id = self.adapter.after_response(
            "Remember this: Python preference",
            "Sure, I'll remember Python preference",
            {"user": "test", "project": "test_proj"}
        )
        assert event_id, "Should create event"

        # Create Claude Code adapter with SAME db_path to verify isolation
        cc_adapter = ClaudeCodeAdapter(db_path=self.db_path)

        # Try to recall with tool='claude-code' - should NOT find
        cc_result = cc_adapter.before_response(
            "Python preference",
            {"user": "test", "project": "test_proj"}
        )

        # HARD ASSERTION: Claude should NOT recall Codex's memories
        assert cc_result == "" or "Python preference" not in cc_result, \
            f"FAIL: Claude recalled Codex's memory! Got: {cc_result[:100]}"


def test_standalone_functions():
    """Verify standalone functions work with isolated database."""
    db_path = tempfile.mktemp(suffix='.db')
    try:
        from src.ocmaf.adapters.codex_cli import (
            get_recall_context,
            remember_interaction,
            remember_task_result,
        )

        # These should not raise - using isolated db
        result = get_recall_context("test query", user="test", db_path=db_path)
        assert isinstance(result, str)

        result = remember_interaction("query", "response", user="test", db_path=db_path)
        assert isinstance(result, str)

        result = remember_task_result("task", "result", True, user="test", db_path=db_path)
        assert isinstance(result, str)
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def run_tests():
    """Run all tests."""
    print("=" * 50)
    print("Codex CLI Adapter Tests (Hermetic)")
    print("=" * 50)

    # Run class-based tests
    test_class = TestCodexAdapter()
    class_tests = [
        test_class.test_adapter_import,
        test_class.test_get_name,
        test_class.test_scope_includes_tool,
        test_class.test_before_response_returns_string,
        test_class.test_after_response_returns_event_id,
        test_class.test_cross_tool_isolation,
    ]

    passed = 0
    failed = []

    # Class-based tests need setup/teardown
    for test_fn in class_tests:
        test_class.setup_method()
        try:
            test_fn()
            print(f"  ✓ {test_fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test_fn.__name__}: {e}")
            failed.append(test_fn.__name__)
        except Exception as e:
            print(f"  ✗ {test_fn.__name__}: ERROR - {e}")
            failed.append(test_fn.__name__)
        finally:
            test_class.teardown_method()

    # Standalone functions test
    try:
        test_standalone_functions()
        print(f"  ✓ test_standalone_functions")
        passed += 1
    except AssertionError as e:
        print(f"  ✗ test_standalone_functions: {e}")
        failed.append("test_standalone_functions")
    except Exception as e:
        print(f"  ✗ test_standalone_functions: ERROR - {e}")
        failed.append("test_standalone_functions")

    print(f"\nResults: {passed}/{passed + len(failed)} passed")
    if failed:
        print(f"Failed: {failed}")
    return len(failed) == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
