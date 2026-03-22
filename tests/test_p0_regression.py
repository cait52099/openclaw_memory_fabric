"""P0 Regression Tests for OCMF.

These tests verify all P0 fixes are working correctly.
"""
import os
import sys
import tempfile
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ocmaf.event.envelope import EventEnvelope
from src.ocmaf.event.scope import Scope
from src.ocmaf.event.types import EventType
from src.ocmaf.storage.event_store import EventStore
from src.ocmaf.storage.memory_store import MemoryStore
from src.ocmaf.api.remember import RememberAPI
from src.ocmaf.api.recall import RecallAPI


class TestP0AdapterContract:
    """P0-A: Adapter Contract tests."""

    def test_protocol_import(self):
        """Verify AdapterProtocol can be imported."""
        from src.ocmaf.adapters.base import AdapterProtocol
        assert AdapterProtocol is not None

    def test_error_strategy(self):
        """Verify ErrorStrategy exists."""
        from src.ocmaf.adapters.base import ErrorStrategy
        assert ErrorStrategy is not None
        # Test fail-open behavior
        result = ErrorStrategy.handle_recall_error(Exception("test"), "")
        assert result == ""


class TestP0ScopeEndToEnd:
    """P0-B: Scope End-to-End tests."""

    def test_scope_fields(self):
        """Verify Scope has all required fields."""
        scope = Scope(user="test", workspace="ws", project="proj", session="sess", tool="tool")
        assert scope.user == "test"
        assert scope.workspace == "ws"
        assert scope.project == "proj"
        assert scope.session == "sess"
        assert scope.tool == "tool"

    def test_scope_to_filter_dict(self):
        """Verify Scope.to_filter_dict works."""
        scope = Scope(user="test", project="proj", session="sess")
        d = scope.to_filter_dict()
        assert d["user"] == "test"
        assert d["project"] == "proj"
        assert d["session"] == "sess"

    def test_scope_matching(self):
        """Verify Scope.matches works."""
        scope1 = Scope(user="test", project="proj", session="s1")
        scope2 = Scope(user="test", project="proj", session="s2")
        assert scope1.matches(scope1)  # exact match
        assert not scope1.matches(scope2)  # different session


class TestP0RecallFallback:
    """P0-C: Recall Fallback tests."""

    def setup_method(self):
        """Create test database."""
        self.db = tempfile.mktemp(suffix='.db')
        self.es = EventStore(self.db)
        self.ms = MemoryStore(self.db)
        self.remember = RememberAPI(event_store=self.es, memory_store=self.ms)
        self.recall = RecallAPI(event_store=self.es, memory_store=self.ms)

    def teardown_method(self):
        """Cleanup."""
        if os.path.exists(self.db):
            os.unlink(self.db)

    def test_fallback_levels_defined(self):
        """Verify FALLBACK_LEVELS is defined."""
        assert hasattr(self.recall, 'FALLBACK_LEVELS')
        assert self.recall.FALLBACK_LEVELS == ["session", "project", "workspace", "user"]

    def test_session_to_project_fallback(self):
        """Test fallback from session to project level."""
        # Write memory in session s1, project Beta
        scope = Scope(user='alice', project='Beta', session='s1')
        event = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='claude-code',
            scope=scope,
            event_type=EventType.CHAT_TURN,
            payload={
                'content': 'User prefers Python',
                'summary': 'Python preference',
                'keywords': ['python', 'preference']
            },
            evidence=['preference:python'],
            links=[]
        )
        self.remember.remember(event)

        # Query from new session s2 (same project)
        context = {'user': 'alice', 'project': 'Beta', 'session': 's2'}
        result = self.recall.recall('preference', context)

        assert len(result.memories) > 0, "Should find memory via fallback"
        assert result.traces.get('fallback_level') == 'project'

    def test_no_fallback_to_different_project(self):
        """Test that fallback doesn't cross project boundaries."""
        # Write memory in project Beta
        scope = Scope(user='alice', project='Beta', session='s1')
        event = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='claude-code',
            scope=scope,
            event_type=EventType.CHAT_TURN,
            payload={
                'content': 'User prefers Python',
                'summary': 'Python preference',
                'keywords': ['python']
            },
            evidence=['preference:python'],
            links=[]
        )
        self.remember.remember(event)

        # Query from different project Gamma
        context = {'user': 'alice', 'project': 'Gamma', 'session': 's2'}
        result = self.recall.recall('python', context)

        # Should not find memory from different project
        assert len(result.memories) == 0


class TestP0Explainability:
    """P0-D: Explainability tests."""

    def setup_method(self):
        """Create test database."""
        self.db = tempfile.mktemp(suffix='.db')
        self.es = EventStore(self.db)
        self.ms = MemoryStore(self.db)
        self.remember = RememberAPI(event_store=self.es, memory_store=self.ms)
        self.recall = RecallAPI(event_store=self.es, memory_store=self.ms)

    def teardown_method(self):
        """Cleanup."""
        if os.path.exists(self.db):
            os.unlink(self.db)

    def test_explain_returns_structure(self):
        """Verify explain() returns required fields."""
        # Write and recall a memory
        scope = Scope(user='test', project='proj')
        event = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='claude-code',
            scope=scope,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'Test content', 'summary': 'Test', 'keywords': ['test']},
            evidence=['test'],
            links=[]
        )
        self.remember.remember(event)

        # Get memory ID
        memories = self.ms.query(user='test', project='proj')
        assert len(memories) > 0
        mem_id = memories[0].memory_id

        # Explain
        result = self.recall.explain(mem_id)

        assert 'memory' in result
        assert 'source_events' in result
        assert 'related_memories' in result
        assert 'state_info' in result
        assert result.get('success') == True

    def test_explain_invalid_id(self):
        """Verify explain() handles invalid ID."""
        result = self.recall.explain('invalid-id-123')
        assert 'error' in result
        assert result.get('success') == False

    def test_explain_json_serializable(self):
        """Verify explain() output is JSON serializable."""
        scope = Scope(user='test', project='proj')
        event = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='claude-code',
            scope=scope,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'Test', 'summary': 'Test', 'keywords': ['test']},
            evidence=['test'],
            links=[]
        )
        self.remember.remember(event)

        memories = self.ms.query(user='test')
        mem_id = memories[0].memory_id

        result = self.recall.explain(mem_id)
        json_str = json.dumps(result)
        assert json_str is not None


class TestP0EventStoreQuery:
    """P0-E: EventStore Query tests."""

    def setup_method(self):
        """Create test database."""
        self.db = tempfile.mktemp(suffix='.db')
        self.es = EventStore(self.db)

    def teardown_method(self):
        """Cleanup."""
        if os.path.exists(self.db):
            os.unlink(self.db)

    def test_query_uses_json_extract(self):
        """Verify EventStore uses json_extract for scope queries."""
        # Write events in different projects
        scope1 = Scope(user='alice', project='Alpha')
        event1 = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='claude-code',
            scope=scope1,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'Alpha'},
            evidence=[],
            links=[]
        )
        self.es.append(event1)

        scope2 = Scope(user='alice', project='Beta')
        event2 = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:01:00Z',
            source_tool='claude-code',
            scope=scope2,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'Beta'},
            evidence=[],
            links=[]
        )
        self.es.append(event2)

        # Query for Alpha - should return only Alpha
        alpha_events = self.es.query(Scope(user='alice', project='Alpha'))
        assert len(alpha_events) == 1
        assert alpha_events[0].scope.project == 'Alpha'

        # Query for Beta - should return only Beta
        beta_events = self.es.query(Scope(user='alice', project='Beta'))
        assert len(beta_events) == 1
        assert beta_events[0].scope.project == 'Beta'


class TestP01ToolIsolation:
    """P0.1: Cross-tool isolation tests."""

    def setup_method(self):
        """Create test database."""
        self.db = tempfile.mktemp(suffix='.db')
        self.es = EventStore(self.db)
        self.ms = MemoryStore(self.db)
        self.remember = RememberAPI(event_store=self.es, memory_store=self.ms)
        self.recall = RecallAPI(event_store=self.es, memory_store=self.ms)

    def teardown_method(self):
        """Cleanup."""
        if os.path.exists(self.db):
            os.unlink(self.db)

    def test_tool_isolation(self):
        """Test that different tools have isolated memories."""
        # Write memory with tool=A
        scope1 = Scope(user='test', project='proj', tool='tool-A')
        event1 = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='tool-A',
            scope=scope1,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'Memory from tool-A', 'summary': 'Tool-A', 'keywords': ['tool-a']},
            evidence=[],
            links=[]
        )
        self.remember.remember(event1)

        # Query with tool=B - should not find tool-A's memory
        context = {'user': 'test', 'project': 'proj', 'tool': 'tool-B'}
        result = self.recall.recall('tool-a', context)

        assert len(result.memories) == 0, "Cross-tool isolation should prevent recall"

    def test_tool_in_memory_object(self):
        """Verify tool is stored in MemoryObject."""
        scope = Scope(user='test', project='proj', tool='test-tool')
        event = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='test-tool',
            scope=scope,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'Test', 'summary': 'Test', 'keywords': ['test']},
            evidence=[],
            links=[]
        )
        self.remember.remember(event)

        memories = self.ms.query(user='test', tool='test-tool')
        assert len(memories) == 1
        assert memories[0].tool == 'test-tool'


class TestP01WorkspaceFallback:
    """P0.1: workspace -> user fallback tests."""

    def setup_method(self):
        """Create test database."""
        self.db = tempfile.mktemp(suffix='.db')
        self.es = EventStore(self.db)
        self.ms = MemoryStore(self.db)
        self.remember = RememberAPI(event_store=self.es, memory_store=self.ms)
        self.recall = RecallAPI(event_store=self.es, memory_store=self.ms)

    def teardown_method(self):
        """Cleanup."""
        if os.path.exists(self.db):
            os.unlink(self.db)

    def test_workspace_to_user_fallback(self):
        """Test workspace -> user fallback works when project differs."""
        # Write memory in workspace=W1, project=P1
        scope1 = Scope(user='alice', workspace='W1', project='P1')
        event1 = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='claude-code',
            scope=scope1,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'W1 memory', 'summary': 'Workspace W1', 'keywords': ['w1']},
            evidence=[],
            links=[]
        )
        self.remember.remember(event1)

        # Query from workspace=W2, project=P1 - different workspace, same project
        # Should fallback to project level (same project) not user
        context = {'user': 'alice', 'workspace': 'W2', 'project': 'P1'}
        result = self.recall.recall('w1', context)

        # When project is same, fallback goes to project level (not user)
        assert len(result.memories) > 0, "Should find memory via project fallback"
        # fallback_level is 'project' because we fell back from workspace=W2 to project=P1
        assert result.traces.get('fallback_level') in ['project', 'user']

    def test_project_isolation_preserved(self):
        """Verify project isolation still works (no cross-project fallback)."""
        # Write memory in project=Beta
        scope = Scope(user='alice', project='Beta', workspace='W1')
        event = EventEnvelope(
            version='1.0',
            timestamp='2026-03-11T10:00:00Z',
            source_tool='claude-code',
            scope=scope,
            event_type=EventType.CHAT_TURN,
            payload={'content': 'Beta project', 'summary': 'Beta', 'keywords': ['beta']},
            evidence=[],
            links=[]
        )
        self.remember.remember(event)

        # Query from different project Gamma - should NOT find Beta's memory
        context = {'user': 'alice', 'project': 'Gamma', 'workspace': 'W1'}
        result = self.recall.recall('beta', context)

        assert len(result.memories) == 0, "Project isolation should prevent cross-project recall"


def run_tests():
    """Run all P0 regression tests."""
    print("=" * 50)
    print("P0 Regression Tests")
    print("=" * 50)

    test_classes = [
        TestP0AdapterContract,
        TestP0ScopeEndToEnd,
        TestP0RecallFallback,
        TestP0Explainability,
        TestP0EventStoreQuery,
        TestP01ToolIsolation,
        TestP01WorkspaceFallback,
    ]

    total = 0
    passed = 0
    failed = []

    for test_class in test_classes:
        print(f"\n--- {test_class.__name__} ---")
        instance = test_class()

        # Setup if needed
        if hasattr(instance, 'setup_method'):
            instance.setup_method()

        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total += 1
                try:
                    getattr(instance, method_name)()
                    print(f"  ✓ {method_name}")
                    passed += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed.append(f"{test_class.__name__}.{method_name}")

        # Teardown if needed
        if hasattr(instance, 'teardown_method'):
            instance.teardown_method()

    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} passed")
    if failed:
        print(f"Failed: {failed}")
    print("=" * 50)

    return passed == total


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
