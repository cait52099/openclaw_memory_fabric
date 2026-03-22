"""Python SDK for OCMF."""
import os
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional
from pathlib import Path

from .event.envelope import EventEnvelope
from .event.scope import Scope
from .event.types import EventType
from .storage.event_store import EventStore
from .storage.memory_store import MemoryStore
from .api.remember import RememberAPI
from .api.recall import RecallAPI, RecallResult


class MemorySession:
    """Context manager for memory operations."""

    def __init__(
        self,
        user: str = "default",
        workspace: Optional[str] = None,
        project: Optional[str] = None,
        session: Optional[str] = None,
        tool: Optional[str] = None,  # P0.1: Add tool parameter for isolation
        db_path: Optional[Path] = None,
    ):
        """Initialize memory session."""
        self.user = user
        self.workspace = workspace
        self.project = project
        self.session = session
        self.tool = tool  # P0.1: Store tool

        self.event_store = EventStore(db_path)
        self.memory_store = MemoryStore(db_path)
        self.remember_api = RememberAPI(self.event_store, self.memory_store)
        self.recall_api = RecallAPI(self.memory_store, self.event_store)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the session."""
        self.event_store.close()
        self.memory_store.close()

    def remember(self, event: EventEnvelope) -> str:
        """Remember an event."""
        return self.remember_api.remember(event)

    def recall(self, query: str, **kwargs) -> RecallResult:
        """Recall relevant memories."""
        context = {
            "user": self.user,
            "workspace": self.workspace,
            "project": self.project,
            "session": self.session,
            "tool": self.tool,  # P0.1: Pass tool for isolation
            **kwargs,
        }
        return self.recall_api.recall(query, context)

    def recall_gist(self, query: str, **kwargs) -> RecallResult:
        """Recall with gist resolution."""
        context = {
            "user": self.user,
            "workspace": self.workspace,
            "project": self.project,
            "session": self.session,
            "tool": self.tool,  # P0.1: Pass tool for isolation
            **kwargs,
        }
        return self.recall_api.recall_gist(query, context)

    def expand(self, memory_id: str):
        """Expand a memory to full details."""
        return self.recall_api.expand(memory_id)

    def explain(self, memory_id: str):
        """Explain why a memory was recalled."""
        return self.recall_api.explain(memory_id)

    def capture_chat_turn(self, user_msg: str, assistant_msg: str, **meta) -> str:
        """Capture a chat turn."""
        meta.update({
            "user": self.user,
            "workspace": self.workspace,
            "project": self.project,
            "session": self.session,
            "tool": self.tool,  # P0.1: Pass tool for isolation
        })
        return self.remember_api.capture_chat_turn(user_msg, assistant_msg, meta)

    def capture_task_result(self, task: str, result: str, success: bool, **meta) -> str:
        """Capture task result."""
        meta.update({
            "user": self.user,
            "workspace": self.workspace,
            "project": self.project,
            "session": self.session,
            "tool": self.tool,  # P0.1: Pass tool for isolation
        })
        return self.remember_api.capture_task_result(task, result, success, meta=meta)

    def capture_decision(self, decision: str, reason: str, **meta) -> str:
        """Capture a decision."""
        meta.update({
            "user": self.user,
            "workspace": self.workspace,
            "project": self.project,
            "session": self.session,
            "tool": self.tool,  # P0.1: Pass tool for isolation
        })
        return self.remember_api.capture_decision(decision, reason, meta)

    def get_injection_text(self, query: str, **kwargs) -> str:
        """Get text for LLM context injection."""
        result = self.recall(query, **kwargs)
        return result.to_injection_text()

    def get_gist_text(self, query: str, **kwargs) -> str:
        """Get gist text for quick injection."""
        result = self.recall_gist(query, **kwargs)
        return result.to_gist_text()


def init(
    user: str = "default",
    workspace: Optional[str] = None,
    project: Optional[str] = None,
    session: Optional[str] = None,
    tool: Optional[str] = None,  # P0.1: Add tool parameter
    db_path: Optional[Path] = None,
) -> MemorySession:
    """Initialize a memory session."""
    return MemorySession(user, workspace, project, session, tool, db_path)


def remember(event: EventEnvelope, **kwargs) -> str:
    """Quick remember function."""
    with MemorySession(**kwargs) as session:
        return session.remember(event)


def recall(query: str, **kwargs) -> RecallResult:
    """Quick recall function."""
    with MemorySession(**kwargs) as session:
        return session.recall(query)
