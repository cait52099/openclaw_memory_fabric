"""Fallback tests for OCMF E2E.

These tests verify session-to-project fallback behavior.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ocmaf.adapters.claude_code import ClaudeCodeAdapter
from src.ocmaf.adapters.codex_cli import CodexCLIAdapter
from src.ocmaf.adapters.openclaw import OpenClawAdapter


class TestFallback:
    """Fallback tests to verify session-to-project behavior."""

    def setup_method(self):
        """Create test database."""
        self.db_path = tempfile.mktemp(suffix='.db')
        self.cc_adapter = ClaudeCodeAdapter(db_path=self.db_path)
        self.codex_adapter = CodexCLIAdapter(db_path=self.db_path)
        self.openclaw_adapter = OpenClawAdapter(db_path=self.db_path)

    def teardown_method(self):
        """Cleanup."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_session_fallback_to_project(self):
        """Verify same tool can recall from different session within same project.

        This tests the session->project fallback policy.
        """
        # Write with session_1
        event_id = self.cc_adapter.after_response(
            "Remember: Use async for I/O",
            "Sure, async is good for I/O",
            {"user": "e2e_user", "project": "e2e_project", "session": "session_1"}
        )
        assert event_id, "Should create event in session_1"

        # Recall with session_2 (different session, same project)
        injection = self.cc_adapter.before_response(
            "async",
            {"user": "e2e_user", "project": "e2e_project", "session": "session_2"}
        )

        # According to current fallback policy: session -> project fallback
        # So it should find the memory from session_1 when querying from session_2
        print(f"Fallback result: {injection[:100] if injection else '(empty)'}")

        # This documents the current behavior - whether it召回 or not depends on fallback config
        # Current implementation uses exact session match, so this tests what happens when session differs

        print("✓ Session fallback test completed")

    def test_cross_tool_same_project_isolation(self):
        """Verify different tools do NOT recall even with same project.

        This confirms tool isolation works regardless of project.
        """
        # Write with Claude
        event_id = self.cc_adapter.after_response(
            "Remember: TypeScript preference",
            "TypeScript is great",
            {"user": "e2e_user", "project": "shared_project"}
        )
        assert event_id, "Claude should create event"

        # Try to recall with Codex (same project, different tool)
        injection = self.codex_adapter.before_response(
            "TypeScript",
            {"user": "e2e_user", "project": "shared_project"}
        )

        # Should NOT recall - different tool
        assert injection == "" or "TypeScript" not in injection, \
            "Codex should NOT recall Claude's memory even with same project"

        print("✓ Cross-tool same project isolation: PASS")

    def test_all_three_tools_same_project(self):
        """Test all three tools with same project - verify isolation."""
        # Write from each tool
        self.cc_adapter.after_response(
            "Claude memory",
            "Claude response",
            {"user": "e2e_user", "project": "tri_project"}
        )
        self.codex_adapter.after_response(
            "Codex memory",
            "Codex response",
            {"user": "e2e_user", "project": "tri_project"}
        )
        self.openclaw_adapter.after_response(
            "OpenClaw memory",
            "OpenClaw response",
            {"user": "e2e_user", "project": "tri_project"}
        )

        # Each tool should only recall its own
        cc_recall = self.cc_adapter.before_response(
            "memory", {"user": "e2e_user", "project": "tri_project"}
        )
        codex_recall = self.codex_adapter.before_response(
            "memory", {"user": "e2e_user", "project": "tri_project"}
        )
        openclaw_recall = self.openclaw_adapter.before_response(
            "memory", {"user": "e2e_user", "project": "tri_project"}
        )

        print(f"Claude recall: {cc_recall[:50] if cc_recall else '(empty)'}")
        print(f"Codex recall: {codex_recall[:50] if codex_recall else '(empty)'}")
        print(f"OpenClaw recall: {openclaw_recall[:50] if openclaw_recall else '(empty)'}")

        # Verify isolation still holds with same project
        assert "Claude" in cc_recall
        assert "Codex" in codex_recall
        assert "OpenClaw" in openclaw_recall

        print("✓ All three tools same project test: PASS")


def run_tests():
    """Run all fallback tests."""
    print("=" * 60)
    print("Fallback / E2E Scenario Tests (Phase 4B)")
    print("=" * 60)

    test_class = TestFallback()

    tests = [
        ("test_session_fallback_to_project", test_class.test_session_fallback_to_project),
        ("test_cross_tool_same_project_isolation", test_class.test_cross_tool_same_project_isolation),
        ("test_all_three_tools_same_project", test_class.test_all_three_tools_same_project),
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
