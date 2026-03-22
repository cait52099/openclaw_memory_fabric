"""Test OpenClaw adapter."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ocmaf.adapters.openclaw import OpenClawAdapter
from src.ocmaf.adapters.claude_code import ClaudeCodeAdapter
from src.ocmaf.adapters.codex_cli import CodexCLIAdapter


class TestOpenClawAdapter:
    """Hermetic test class for OpenClawAdapter."""

    def setup_method(self):
        """Create isolated test database."""
        self.db_path = tempfile.mktemp(suffix='.db')
        self.adapter = OpenClawAdapter(db_path=self.db_path)

    def teardown_method(self):
        """Cleanup test database."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_adapter_import(self):
        """Verify OpenClawAdapter can be imported."""
        from src.ocmaf.adapters import OpenClawAdapter
        assert OpenClawAdapter is not None

    def test_get_name(self):
        """Verify adapter returns correct name."""
        assert self.adapter.get_name() == "openclaw"

    def test_scope_includes_tool(self):
        """Verify scope includes tool='openclaw'."""
        scope = self.adapter.get_scope_from_context({})
        assert scope.get("tool") == "openclaw"

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


def test_standalone_functions():
    """Verify standalone functions work with isolated database."""
    db_path = tempfile.mktemp(suffix='.db')
    try:
        from src.ocmaf.adapters.openclaw import (
            get_recall_context,
            remember_interaction,
        )

        # These should not raise - using isolated db
        result = get_recall_context("test query", user="test", db_path=db_path)
        assert isinstance(result, str)

        result = remember_interaction("query", "response", user="test", db_path=db_path)
        assert isinstance(result, str)
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def run_tests():
    """Run all tests."""
    print("=" * 50)
    print("OpenClaw Adapter Tests")
    print("=" * 50)

    # Run class-based tests
    test_class = TestOpenClawAdapter()
    class_tests = [
        test_class.test_adapter_import,
        test_class.test_get_name,
        test_class.test_scope_includes_tool,
        test_class.test_before_response_returns_string,
        test_class.test_after_response_returns_event_id,
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
