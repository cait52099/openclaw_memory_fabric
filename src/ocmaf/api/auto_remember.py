"""Auto-Remember Module for OCMF.

Automatically remembers key events at session end.
Triggered when OCMF_AUTO_MEMORY=2 or OCMF_AUTO_MEMORY=3.
"""
import os
import logging
from typing import Dict, List, Optional, Any

from ..storage.event_store import EventStore
from ..storage.memory_store import MemoryStore
from ..event.envelope import EventEnvelope
from ..event.scope import Scope
from ..event.types import EventType
from .remember import RememberAPI

logger = logging.getLogger(__name__)


# Keywords that indicate a decision
DECISION_MARKERS = [
    "decided to",
    "choosing",
    "will use",
    "going with",
    "selected",
    "chose",
    "opted for",
    "agreed on",
    "set up",
    "configured",
    "installed",
    "using",
    "created",
]

# Keywords that indicate a fact
FACT_MARKERS = [
    "the project uses",
    "we use",
    "uses",
    "is configured",
    "is set to",
    "currently",
    "exists",
]

# Keywords that indicate a preference
PREFERENCE_MARKERS = [
    "prefer",
    "like better",
    "favor",
    "instead of",
    "rather than",
]


class AutoRemember:
    """Automatic memory remember at session end.

    This module provides zero-friction memory by automatically
    remembering key decisions, facts, and preferences at session end.
    """

    def __init__(self, memory_store: MemoryStore = None, event_store: EventStore = None):
        """Initialize AutoRemember.

        Args:
            memory_store: Optional pre-configured MemoryStore
            event_store: Optional pre-configured EventStore
        """
        self.memory_store = memory_store or MemoryStore()
        self.event_store = event_store or EventStore()
        self.remember_api = RememberAPI(self.event_store, self.memory_store)

    def is_enabled(self) -> bool:
        """Check if auto-remember is enabled.

        Returns:
            True if auto-memory level includes remember
        """
        level = int(os.environ.get("OCMF_AUTO_MEMORY", "0"))
        return level in (2, 3)

    def get_session_context(self) -> Dict[str, Any]:
        """Get context for this session.

        Returns:
            Dict with user, workspace, project, session info
        """
        return {
            "user": os.environ.get("OCMF_SCOPE_USER", "default"),
            "workspace": os.environ.get("OCMF_SCOPE_WORKSPACE"),
            "project": os.environ.get("OCMF_SCOPE_PROJECT"),
            "session": os.environ.get("OCMF_SESSION_ID"),
        }

    def extract_decisions(self, content: str) -> List[str]:
        """Extract decision statements from content.

        Args:
            content: Text to analyze

        Returns:
            List of extracted decisions
        """
        decisions = []
        lines = content.split("\n")

        for line in lines:
            line_lower = line.lower()
            for marker in DECISION_MARKERS:
                if marker in line_lower:
                    # Clean and add
                    decision = line.strip()
                    if decision and len(decision) > 10:
                        decisions.append(decision)
                    break

        return decisions

    def extract_facts(self, content: str) -> List[str]:
        """Extract factual statements from content.

        Args:
            content: Text to analyze

        Returns:
            List of extracted facts
        """
        facts = []
        lines = content.split("\n")

        for line in lines:
            line_lower = line.lower()
            for marker in FACT_MARKERS:
                if marker in line_lower:
                    fact = line.strip()
                    if fact and len(fact) > 10:
                        facts.append(fact)
                    break

        return facts

    def extract_preferences(self, content: str) -> List[str]:
        """Extract preference statements from content.

        Args:
            content: Text to analyze

        Returns:
            List of extracted preferences
        """
        preferences = []
        lines = content.split("\n")

        for line in lines:
            line_lower = line.lower()
            for marker in PREFERENCE_MARKERS:
                if marker in line_lower:
                    pref = line.strip()
                    if pref and len(pref) > 10:
                        preferences.append(pref)
                    break

        return preferences

    def remember(
        self,
        session_id: str = None,
        session_content: str = None,
    ) -> Dict[str, Any]:
        """Perform automatic remember for session.

        This method extracts key decisions, facts, and preferences
        from the session and remembers them.

        Args:
            session_id: Current session ID (auto-detected if None)
            session_content: Optional session content to analyze

        Returns:
            Dict with:
            - success: bool
            - events_remembered: list of event IDs
            - decisions: count of decisions remembered
            - facts: count of facts remembered
            - preferences: count of preferences remembered
        """
        if not self.is_enabled():
            return {
                "success": True,
                "skipped": True,
                "reason": "auto-remember not enabled",
                "events_remembered": [],
            }

        if session_content is None:
            # When no content provided, this is a no-op
            # In real usage, this would be called with conversation history
            return {
                "success": True,
                "skipped": True,
                "reason": "no session content provided",
                "events_remembered": [],
            }

        context = self.get_session_context()
        session = session_id or context.get("session") or "unknown"

        events_remembered = []
        stats = {"decisions": 0, "facts": 0, "preferences": 0}

        # Extract and remember decisions
        decisions = self.extract_decisions(session_content)
        for decision in decisions:
            try:
                event_id = self._remember_content(
                    decision,
                    EventType.DECISION,
                    context,
                    session,
                )
                events_remembered.append(event_id)
                stats["decisions"] += 1
            except Exception as e:
                logger.warning(f"Failed to remember decision: {e}")

        # Extract and remember facts
        facts = self.extract_facts(session_content)
        for fact in facts:
            try:
                event_id = self._remember_content(
                    fact,
                    EventType.FACT,
                    context,
                    session,
                )
                events_remembered.append(event_id)
                stats["facts"] += 1
            except Exception as e:
                logger.warning(f"Failed to remember fact: {e}")

        # Extract and remember preferences
        preferences = self.extract_preferences(session_content)
        for pref in preferences:
            try:
                event_id = self._remember_content(
                    pref,
                    EventType.PREFERENCE,
                    context,
                    session,
                )
                events_remembered.append(event_id)
                stats["preferences"] += 1
            except Exception as e:
                logger.warning(f"Failed to remember preference: {e}")

        return {
            "success": True,
            "session": session,
            "context": context,
            "events_remembered": events_remembered,
            "decisions": stats["decisions"],
            "facts": stats["facts"],
            "preferences": stats["preferences"],
            "total": len(events_remembered),
        }

    def _remember_content(
        self,
        content: str,
        event_type: EventType,
        context: Dict[str, Any],
        session: str,
    ) -> str:
        """Remember a single piece of content.

        Args:
            content: Content to remember
            event_type: Type of event
            context: Session context
            session: Session ID

        Returns:
            Event ID
        """
        scope = Scope(
            user=context.get("user", "default"),
            workspace=context.get("workspace"),
            project=context.get("project"),
            session=session,
        )

        event = EventEnvelope(
            source_tool="cli",  # Auto-remember uses cli source
            scope=scope,
            event_type=event_type,
            payload={
                "content": content,
                "summary": content[:100],
                "keywords": content.split()[:5],
                "auto_generated": True,
            },
        )

        return self.remember_api.remember(event)

    def close(self):
        """Close resources."""
        if self.memory_store:
            self.memory_store.close()
        if self.event_store:
            self.event_store.close()


def auto_remember(session_id: str = None, session_content: str = None) -> Dict[str, Any]:
    """Convenience function for auto-remember.

    Args:
        session_id: Optional session ID
        session_content: Optional session content to analyze

    Returns:
        Auto-remember result
    """
    auto = AutoRemember()
    try:
        return auto.remember(session_id, session_content)
    finally:
        auto.close()


if __name__ == "__main__":
    # Test auto-remember
    import json

    print("Testing Auto-Remember...")

    # Test content extraction
    test_content = """
    We decided to use PostgreSQL for the database.
    The project uses React for the frontend.
    I prefer TypeScript over JavaScript.
    We are going with a microservices architecture.
    The API is configured to use port 3000.
    """

    auto = AutoRemember()
    decisions = auto.extract_decisions(test_content)
    facts = auto.extract_facts(test_content)
    preferences = auto.extract_preferences(test_content)

    print(f"\nExtracted:")
    print(f"  Decisions ({len(decisions)}): {decisions}")
    print(f"  Facts ({len(facts)}): {facts}")
    print(f"  Preferences ({len(preferences)}): {preferences}")

    print(f"\nAuto-memory enabled: {auto.is_enabled()}")
    auto.close()
