"""Auto-Recall Module for OCMF.

Automatically recalls relevant memories at session start.
Triggered when OCMF_AUTO_MEMORY=1 or OCMF_AUTO_MEMORY=3.
"""
import os
import logging
from typing import Dict, List, Optional, Any

from ..storage.event_store import EventStore
from ..storage.memory_store import MemoryStore
from .recall import RecallAPI

logger = logging.getLogger(__name__)


class AutoRecall:
    """Automatic memory recall at session start.

    This module provides zero-friction memory by automatically
    recalling relevant memories when a new session starts.
    """

    def __init__(self, memory_store: MemoryStore = None, event_store: EventStore = None):
        """Initialize AutoRecall.

        Args:
            memory_store: Optional pre-configured MemoryStore
            event_store: Optional pre-configured EventStore
        """
        self.memory_store = memory_store or MemoryStore()
        self.event_store = event_store or EventStore()
        self.recall_api = RecallAPI(self.memory_store, self.event_store)

    def is_enabled(self) -> bool:
        """Check if auto-recall is enabled.

        Returns:
            True if auto-memory level includes recall
        """
        level = int(os.environ.get("OCMF_AUTO_MEMORY", "0"))
        return level in (1, 3)

    def should_recall(self, session_id: str = None) -> bool:
        """Determine if recall should run for this session.

        Args:
            session_id: Current session ID

        Returns:
            True if recall should be triggered
        """
        if not self.is_enabled():
            return False

        # Check if we have any memories to recall
        try:
            count = self.memory_store.count()
            return count > 0
        except Exception as e:
            logger.warning(f"Could not check memory count: {e}")
            return False

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

    def get_recall_query(self, context: Dict[str, Any]) -> str:
        """Generate recall query from session context.

        Args:
            context: Session context

        Returns:
            Query string for recall
        """
        parts = []

        if context.get("project"):
            parts.append(context["project"])

        if context.get("workspace"):
            parts.append(context["workspace"])

        # Use recent keywords from environment if available
        recent = os.environ.get("OCMF_RECENT_TOPICS", "")
        if recent:
            parts.append(recent)

        return " ".join(parts) if parts else "recent memory"

    def recall(
        self,
        session_id: str = None,
        limit: int = None,
    ) -> Dict[str, Any]:
        """Perform automatic recall for session.

        Args:
            session_id: Current session ID (auto-detected if None)
            limit: Max memories to recall (default from env or 10)

        Returns:
            Dict with:
            - success: bool
            - memories: list of recalled memories
            - conflict_detected: bool
            - candidates: list of conflicting memories (if conflict)
            - injection_text: formatted text for context injection
        """
        if not self.should_recall(session_id):
            return {
                "success": True,
                "skipped": True,
                "reason": "auto-recall not enabled or no memories",
                "memories": [],
            }

        if limit is None:
            limit = int(os.environ.get("OCMF_RECALL_LIMIT", "10"))

        context = self.get_session_context()
        context["session"] = session_id or context.get("session")
        context["limit"] = limit

        query = self.get_recall_query(context)

        try:
            result = self.recall_api.recall(query, context)
            result_dict = result.to_dict()

            # Generate injection text
            injection_text = self._generate_injection_text(result_dict)

            return {
                "success": True,
                "query": query,
                "context": context,
                "memories": result_dict.get("memories", []),
                "conflict_detected": result_dict.get("conflict_detected", False),
                "candidates": result_dict.get("candidates", []),
                "injection_text": injection_text,
                "count": len(result.memories),
            }

        except Exception as e:
            logger.error(f"Auto-recall failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "memories": [],
            }

    def _generate_injection_text(self, result: Dict[str, Any]) -> str:
        """Generate text for context injection.

        Args:
            result: Recall result dict

        Returns:
            Formatted text for system context
        """
        if not result.get("memories"):
            return ""

        lines = ["\n=== Relevant Memories ===\n"]

        # Group by source
        by_source = {}
        for mem in result.get("memories", []):
            source = mem.get("source_host_friendly", "Unknown")
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(mem)

        for source, memories in by_source.items():
            lines.append(f"From {source}:")
            for mem in memories:
                ts = mem.get("timestamp", "")
                if ts:
                    try:
                        from datetime import datetime
                        if isinstance(ts, str):
                            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                            ts = dt.strftime("%H:%M")
                    except:
                        pass

                content = mem.get("content", mem.get("summary", ""))[:100]
                lines.append(f"  • \"{content}\" (From {source} at {ts})")
            lines.append("")

        # Add conflict warning if detected
        if result.get("conflict_detected"):
            lines.append("\n⚠️ CONFLICT DETECTED:")
            lines.append("  Multiple memories have conflicting information.")
            lines.append("  Review before proceeding.\n")

        return "\n".join(lines)

    def close(self):
        """Close resources."""
        if self.memory_store:
            self.memory_store.close()
        if self.event_store:
            self.event_store.close()


def auto_recall(session_id: str = None) -> Dict[str, Any]:
    """Convenience function for auto-recall.

    Args:
        session_id: Optional session ID

    Returns:
        Auto-recall result
    """
    auto = AutoRecall()
    try:
        return auto.recall(session_id)
    finally:
        auto.close()


if __name__ == "__main__":
    # Test auto-recall
    import json

    print("Testing Auto-Recall...")
    print(f"Auto-memory level: {os.environ.get('OCMF_AUTO_MEMORY', '0')}")

    result = auto_recall()
    print(f"\nResult:")
    print(json.dumps(result, indent=2, default=str))
