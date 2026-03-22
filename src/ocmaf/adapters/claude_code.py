"""Claude Code adapter for OCMF.

This adapter integrates with Claude Code to provide automatic
recall-before-response and remember-after-response functionality.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional
import uuid

from .base import Adapter, InjectionPolicy
from ..event.envelope import EventEnvelope
from ..event.scope import Scope
from ..event.types import EventType
from ..sdk import MemorySession
from ..object.types import Tier, State, Resolution


class ClaudeCodeAdapter(Adapter):
    """Adapter for Claude Code.

    Provides automatic memory recall before response generation
    and automatic memory storage after response.
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        db_path: Optional[Path] = None,
    ):
        """Initialize Claude Code adapter."""
        super().__init__(config)
        self.db_path = db_path

        # Default injection policy
        self.injection_policy = InjectionPolicy(
            max_length=config.get("max_injection_length", 2000) if config else 2000,
            max_memories=config.get("max_memories", 5) if config else 5,
            prefer_gist=config.get("prefer_gist", True) if config else True,
        )

    def get_name(self) -> str:
        """Get adapter name."""
        return "claude-code"

    def get_scope_from_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract scope from Claude Code context.

        Claude Code provides environment variables and context.
        """
        # Check environment variables for Claude Code context
        user = os.environ.get("CLAUDE_USER_ID", context.get("user", "default"))
        workspace = os.environ.get("CLAUDE_WORKSPACE", context.get("workspace"))
        project = os.environ.get("CLAUDE_PROJECT", context.get("project"))
        session = os.environ.get("CLAUDE_SESSION_ID", context.get("session"))
        tool = context.get("tool", "claude-code")

        return {
            "user": user,
            "workspace": workspace,
            "project": project,
            "session": session,
            "tool": tool,
        }

    def before_response(self, query: str, context: Dict[str, Any]) -> str:
        """Hook called before generating response.

        This is the recall-before-response hook. It retrieves relevant
        memories and returns formatted text for injection.
        """
        # Get scope from context
        scope = self.get_scope_from_context(context)

        # Create memory session
        with MemorySession(
            user=scope.get("user", "default"),
            workspace=scope.get("workspace"),
            project=scope.get("project"),
            session=scope.get("session"),
            tool=scope.get("tool"),  # Phase 3B.1: Explicitly pass tool
            db_path=self.db_path,
        ) as session:
            # Recall relevant memories
            if self.injection_policy.prefer_gist:
                result = session.recall_gist(query, limit=self.injection_policy.max_memories)
            else:
                result = session.recall(query, limit=self.injection_policy.max_memories)

            # Apply injection policy
            injection_text = self.injection_policy.apply(result)

            return injection_text

    def after_response(
        self,
        query: str,
        response: str,
        context: Dict[str, Any],
    ) -> str:
        """Hook called after generating response.

        This is the remember-after-response hook. It stores the
        conversation as a memory event.
        """
        # Get scope from context
        scope = self.get_scope_from_context(context)

        # Create memory session
        with MemorySession(
            user=scope.get("user", "default"),
            workspace=scope.get("workspace"),
            project=scope.get("project"),
            session=scope.get("session"),
            tool=scope.get("tool"),  # Phase 3B.1: Explicitly pass tool
            db_path=self.db_path,
        ) as session:
            # Capture chat turn
            event_id = session.capture_chat_turn(
                user_msg=query,
                assistant_msg=response,
                source_tool="claude-code",
            )

            return event_id

    def before_task(self, task: str, context: Dict[str, Any]) -> str:
        """Hook called before executing a task.

        Similar to before_response but for task execution.
        """
        scope = self.get_scope_from_context(context)

        with MemorySession(
            user=scope.get("user", "default"),
            workspace=scope.get("workspace"),
            project=scope.get("project"),
            session=scope.get("session"),
            tool=scope.get("tool"),  # Phase 3B.1: Explicitly pass tool
            db_path=self.db_path,
        ) as session:
            result = session.recall(task, limit=self.injection_policy.max_memories)
            return self.injection_policy.apply(result)

    def after_task(
        self,
        task: str,
        result: str,
        success: bool,
        context: Dict[str, Any],
    ) -> str:
        """Hook called after task execution."""
        scope = self.get_scope_from_context(context)

        with MemorySession(
            user=scope.get("user", "default"),
            workspace=scope.get("workspace"),
            project=scope.get("project"),
            session=scope.get("session"),
            tool=scope.get("tool"),  # Phase 3B.1: Explicitly pass tool
            db_path=self.db_path,
        ) as session:
            event_id = session.capture_task_result(
                task=task,
                result=result,
                success=success,
                source_tool="claude-code",
            )
            return event_id


# Standalone function for easy integration
def get_recall_context(
    query: str,
    user: str = "default",
    workspace: Optional[str] = None,
    project: Optional[str] = None,
    session: Optional[str] = None,
    db_path: Optional[Path] = None,
    **kwargs,
) -> str:
    """Get recall context for query.

    Simple function for manual integration.
    """
    adapter = ClaudeCodeAdapter(db_path=db_path)
    context = {
        "user": user,
        "workspace": workspace,
        "project": project,
        "session": session,
        **kwargs,
    }
    return adapter.before_response(query, context)


def remember_interaction(
    query: str,
    response: str,
    user: str = "default",
    workspace: Optional[str] = None,
    project: Optional[str] = None,
    session: Optional[str] = None,
    db_path: Optional[Path] = None,
    **kwargs,
) -> str:
    """Remember an interaction.

    Simple function for manual integration.
    """
    adapter = ClaudeCodeAdapter(db_path=db_path)
    context = {
        "user": user,
        "workspace": workspace,
        "project": project,
        "session": session,
        **kwargs,
    }
    return adapter.after_response(query, response, context)
