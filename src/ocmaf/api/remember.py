"""Remember API - write events to memory."""
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from ..event.envelope import EventEnvelope
from ..event.types import EventType
from ..event.scope import Scope
from ..storage.event_store import EventStore
from ..storage.memory_store import MemoryStore
from ..object.model import MemoryObject
from ..object.types import Tier, State, Resolution


class RememberAPI:
    """API for writing to memory."""

    def __init__(self, event_store: EventStore = None, memory_store: MemoryStore = None):
        """Initialize remember API."""
        self.event_store = event_store or EventStore()
        self.memory_store = memory_store or MemoryStore()

    def remember(self, event: EventEnvelope) -> str:
        """Remember an event.

        Writes to event store (source of truth) and triggers
        optional consolidation to update memory objects.

        Returns event_id.
        """
        # Write to event store (append-only)
        event_id = self.event_store.append(event)

        # Optional: auto-consolidate to create/update memory object
        self._consolidate_event(event)

        return event_id

    def _consolidate_event(self, event: EventEnvelope):
        """Consolidate event into memory object."""
        # Create or update memory object from event
        payload = event.payload

        # Extract content from payload
        title = payload.get("title", "")
        content = payload.get("content", "")
        summary = payload.get("summary", "") or content[:200]

        # Extract keywords
        keywords = payload.get("keywords", [])

        # Create memory object
        memory = MemoryObject(
            memory_id=event.event_id,  # Use event_id as memory_id for simplicity
            tier=Tier.WORKING,
            state=State.ACTIVE,
            resolution=Resolution.GIST,
            title=title,
            summary=summary,
            content=content,
            keywords=keywords,
            source_event_ids=[event.event_id],
            user=event.scope.user,
            workspace=event.scope.workspace,
            project=event.scope.project,
            session=event.scope.session,
            tool=event.scope.tool,
        )

        self.memory_store.put(memory)

    def capture_chat_turn(
        self,
        user_msg: str,
        assistant_msg: str,
        meta: Dict[str, Any],
    ) -> str:
        """Capture a chat turn.

        Convenience method for capturing conversation.
        """
        event = EventEnvelope(
            source_tool=meta.get("source_tool", "claude-code"),
            scope=Scope(
                user=meta.get("user", "default"),
                workspace=meta.get("workspace"),
                project=meta.get("project"),
                session=meta.get("session"),
                tool=meta.get("tool"),
            ),
            event_type=EventType.CHAT_TURN,
            payload={
                "user_message": user_msg,
                "assistant_message": assistant_msg,
                "content": f"User: {user_msg}\nAssistant: {assistant_msg}",
                "summary": f"Chat about: {user_msg[:100]}",
                "keywords": self._extract_keywords(user_msg + " " + assistant_msg),
            },
            evidence=meta.get("evidence", []),
            links=meta.get("links", []),
        )
        return self.remember(event)

    def capture_task_result(
        self,
        task: str,
        result: str,
        success: bool,
        evidence: List[str] = None,
        meta: Dict[str, Any] = None,
    ) -> str:
        """Capture task result.

        Records success or failure experience.
        """
        event = EventEnvelope(
            source_tool=meta.get("source_tool", "claude-code") if meta else "claude-code",
            scope=Scope(
                user=meta.get("user", "default") if meta else "default",
                workspace=meta.get("workspace") if meta else None,
                project=meta.get("project") if meta else None,
                session=meta.get("session") if meta else None,
            ),
            event_type=EventType.TASK_RESULT,
            payload={
                "task": task,
                "result": result,
                "success": success,
                "content": f"Task: {task}\nResult: {result}",
                "summary": f"{'Success' if success else 'Failure'}: {task[:100]}",
                "keywords": ["task", "result", "success" if success else "failure"],
            },
            evidence=evidence or [],
        )
        return self.remember(event)

    def capture_decision(
        self,
        decision: str,
        reason: str,
        meta: Dict[str, Any] = None,
    ) -> str:
        """Capture a decision."""
        event = EventEnvelope(
            source_tool=meta.get("source_tool", "claude-code") if meta else "claude-code",
            scope=Scope(
                user=meta.get("user", "default") if meta else "default",
                workspace=meta.get("workspace") if meta else None,
                project=meta.get("project") if meta else None,
                session=meta.get("session") if meta else None,
            ),
            event_type=EventType.DECISION,
            payload={
                "decision": decision,
                "reason": reason,
                "content": f"Decision: {decision}\nReason: {reason}",
                "summary": f"Decision: {decision[:100]}",
                "keywords": ["decision"],
            },
        )
        return self.remember(event)

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract simple keywords from text."""
        # Simple keyword extraction (in production, use proper NLP)
        words = text.lower().split()
        # Filter common words
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                     "being", "have", "has", "had", "do", "does", "did", "will",
                     "would", "could", "should", "may", "might", "must", "can",
                     "to", "of", "in", "for", "on", "with", "at", "by", "from",
                     "as", "into", "through", "during", "before", "after",
                     "and", "or", "but", "if", "because", "so", "that", "this"}
        return [w for w in words if len(w) > 3 and w not in stopwords][:10]
