"""Recall API - retrieve memories."""
import uuid
import json
import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from ..storage.memory_store import MemoryStore
from ..storage.event_store import EventStore
from ..object.model import MemoryObject
from ..object.types import State
from .friendly import get_source_tool_label


class RecallResult:
    """Result of a recall operation."""

    def __init__(
        self,
        memories: List[MemoryObject],
        query: str,
        context: Dict[str, Any],
        traces: Dict[str, Any],
        conflict_detected: bool = False,
        candidates: List[Dict[str, Any]] = None,
        event_store: EventStore = None,
    ):
        self.memories = memories
        self.query = query
        self.context = context
        self.traces = traces
        self.conflict_detected = conflict_detected
        self.candidates = candidates or []
        self.event_store = event_store

    def to_dict(self) -> dict:
        """Convert to dictionary with enhanced cross-host fields.

        Each memory now includes:
        - source_tool: The tool that created the memory
        - source_host_friendly: Human-readable host name
        - timestamp: When the memory was created
        - is_synthetic: Whether this is synthetic test data
        """
        # Get source info for each memory from events
        memory_list = []
        for m in self.memories:
            mem_dict = m.model_dump()

            # Get source_tool from first source event
            source_tool = "unknown"
            event_timestamp = mem_dict.get("created_at", "")
            if m.source_event_ids:
                event = self.event_store.get(m.source_event_ids[0]) if hasattr(self, 'event_store') else None
                if event:
                    source_tool = getattr(event, 'source_tool', 'unknown')
                    if isinstance(event.timestamp, datetime):
                        event_timestamp = event.timestamp.isoformat()
                    elif hasattr(event, 'timestamp') and isinstance(event.timestamp, str):
                        event_timestamp = event.timestamp

            # Add cross-host fields
            label_info = get_source_tool_label(source_tool)
            mem_dict.update(label_info)
            mem_dict["timestamp"] = event_timestamp
            mem_dict["memory_id"] = m.memory_id

            memory_list.append(mem_dict)

        result = {
            "memories": memory_list,
            "query": self.query,
            "context": self.context,
            "traces": self.traces,
            "conflict_detected": self.conflict_detected,
        }

        if self.candidates:
            result["candidates"] = self.candidates

        return result

    def to_injection_text(self, max_length: int = 2000) -> str:
        """Convert to prompt injection text (detail mode).

        Returns a formatted string for injecting into LLM context.
        Now includes source_tool, friendly name, and timestamp for cross-host provenance.
        """
        if not self.memories:
            return ""

        lines = ["## Relevant Context"]
        for mem in self.memories:
            # Get source info from events
            source_tool = "unknown"
            event_timestamp = ""
            if mem.source_event_ids and self.event_store:
                event = self.event_store.get(mem.source_event_ids[0])
                if event:
                    source_tool = getattr(event, 'source_tool', 'unknown')
                    ts = getattr(event, 'timestamp', None)
                    if ts:
                        if isinstance(ts, datetime):
                            event_timestamp = ts.strftime("%H:%M")
                        elif isinstance(ts, str):
                            try:
                                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                                event_timestamp = dt.strftime("%H:%M")
                            except:
                                pass

            friendly = get_source_tool_label(source_tool)
            friendly_name = friendly.get("source_host_friendly", source_tool)

            lines.append(f"\n### {mem.title or mem.memory_id[:8]}")

            # Add provenance info
            provenance_str = f"From {friendly_name}"
            if event_timestamp:
                provenance_str += f" at {event_timestamp}"
            lines.append(f"({provenance_str})")

            lines.append(f"Summary: {mem.summary}")

            # Conflict warning with cross-host context
            if mem.state == State.CONFLICTED:
                lines.append(f"⚠️ WARNING: This has conflicts with {mem.conflict_with}")
            if mem.superseded_by:
                lines.append(f"⚠️ NOTE: This has been superseded")

        # Add conflict detection summary if present
        if self.conflict_detected and self.candidates:
            lines.append("\n⚠️ CONFLICT DETECTED")
            lines.append(f"Multiple versions found ({len(self.candidates)} conflicting memories):")
            for c in self.candidates[:5]:  # Limit to 5
                lines.append(f"  - [{c.get('source_host_friendly', 'Unknown')}] \"{c.get('content', '')[:60]}\"")

        text = "\n".join(lines)
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length] + "\n... (truncated)"
        return text

    def to_gist_text(self, max_memories: int = 3) -> str:
        """Get gist text for quick injection.

        Now includes source_tool and timestamp for cross-host provenance.
        """
        if not self.memories:
            return ""

        lines = ["## Relevant Context (Gist)"]
        for mem in self.memories[:max_memories]:
            # Get source info from events
            source_tool = "unknown"
            event_timestamp = ""
            if mem.source_event_ids and self.event_store:
                event = self.event_store.get(mem.source_event_ids[0])
                if event:
                    source_tool = getattr(event, 'source_tool', 'unknown')
                    ts = getattr(event, 'timestamp', None)
                    if ts:
                        if isinstance(ts, datetime):
                            event_timestamp = ts.strftime("%H:%M")
                        elif isinstance(ts, str):
                            try:
                                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                                event_timestamp = dt.strftime("%H:%M")
                            except:
                                pass

            friendly = get_source_tool_label(source_tool)
            friendly_name = friendly.get("source_host_friendly", source_tool)

            ts_str = f" ({event_timestamp})" if event_timestamp else ""
            lines.append(f"- [{friendly_name}{ts_str}] {mem.summary}")

        # Add conflict note if present
        if self.conflict_detected:
            lines.append("\n⚠️ CONFLICT: Multiple versions exist - see detail for options")

        return "\n".join(lines)


class RecallAPI:
    """API for recalling memories."""

    # Fallback policy: session -> project -> workspace -> user
    FALLBACK_LEVELS = ["session", "project", "workspace", "user"]
    DEFAULT_LIMIT = 10

    def __init__(self, memory_store: MemoryStore = None, event_store: EventStore = None):
        """Initialize recall API."""
        self.memory_store = memory_store or MemoryStore()
        self.event_store = event_store or EventStore()

    def recall(
        self,
        query: str,
        context: Dict[str, Any],
    ) -> RecallResult:
        """Recall relevant memories with fallback policy.

        Implements: cue -> candidate -> conflict -> gist -> detail -> evidence
        Falls back: session -> project -> workspace -> user
        """
        user = context.get("user", "default")
        workspace = context.get("workspace")
        project = context.get("project")
        session = context.get("session")
        tool = context.get("tool")  # P0.1: Extract tool from context

        # Extract keywords from query
        keywords = self._extract_keywords(query)
        limit = context.get("limit", self.DEFAULT_LIMIT)

        # Try each scope level with fallback
        fallback_level = None
        memories = []

        # Build scope combinations for fallback (most specific first)
        # P0.1 FIX: workspace -> user fallback now works
        # Fallback rules:
        # - session -> project (same project)
        # - project -> project-only (ignore workspace, same project)
        # - workspace -> user (only when no project)
        # Project isolation is NEVER crossed
        scope_levels = []

        # Most specific: session level (with project and workspace)
        if session:
            scope_levels.append({"session": session, "project": project, "workspace": workspace, "user": user})
            # Fallback: session -> project (same project, ignore session)
            scope_levels.append({"project": project, "workspace": workspace, "user": user})
        elif project:
            # Project level: try with specified workspace first
            scope_levels.append({"project": project, "workspace": workspace, "user": user})
            # Fallback: project-only (ignore workspace, same project)
            scope_levels.append({"project": project, "user": user})
        elif workspace:
            # Workspace -> user fallback (only when no project specified)
            scope_levels.append({"workspace": workspace, "user": user})
            # P0.1 FIX: workspace -> user fallback
            scope_levels.append({"user": user})
        else:
            # User only
            scope_levels.append({"user": user})

        for scope_dict in scope_levels:
            # Query memory store with current scope (include tool for isolation)
            memories = self.memory_store.query(
                user=scope_dict.get("user", user),
                workspace=scope_dict.get("workspace"),
                project=scope_dict.get("project"),
                tool=tool,  # P0.1: Pass tool for isolation
                session=scope_dict.get("session"),
                keywords=keywords,
                limit=limit,
            )

            # Filter out superseded memories
            memories = [m for m in memories if m.state != State.SUPERSEDED]

            # Check if we have results
            if memories:
                # Determine which fallback level we used
                if scope_dict.get("session"):
                    fallback_level = "session"
                elif scope_dict.get("project"):
                    fallback_level = "project"
                elif scope_dict.get("workspace"):
                    fallback_level = "workspace"
                else:
                    fallback_level = "user"
                break

        # Enhanced conflict detection with cross-host support
        conflict_detected, candidates = self._detect_conflicts(memories)

        # Generate traces for debugging (include fallback info)
        trace_id = str(uuid.uuid4())
        traces = {
            "trace_id": trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "query": query,
            "context": context,
            "keywords_used": keywords,
            "memory_count": len(memories),
            "selected_ids": [m.memory_id for m in memories],
            "fallback_level": fallback_level,
            "fallback_used": fallback_level is not None and (
                (session and fallback_level != "session") or
                (project and fallback_level != "session" and fallback_level != "project") or
                (workspace and fallback_level not in ["session", "project", "workspace"])
            ),
        }

        # Save trace
        self._save_trace(traces)

        return RecallResult(
            memories=memories,
            query=query,
            context=context,
            traces=traces,
            conflict_detected=conflict_detected,
            candidates=candidates,
            event_store=self.event_store,
        )

    def recall_gist(
        self,
        query: str,
        context: Dict[str, Any],
    ) -> RecallResult:
        """Recall with gist-level resolution (skip detail)."""
        result = self.recall(query, context)
        # Mark as gist resolution
        result.traces["resolution"] = "gist"
        return result

    def expand(self, memory_id: str) -> Optional[MemoryObject]:
        """Get full details of a memory."""
        return self.memory_store.get(memory_id)

    def explain(self, memory_id: str, recall_query: str = None) -> Dict[str, Any]:
        """Explain why a memory was recalled.

        Returns enhanced information including:
            - memory: The memory object
            - source_tool / source_host_friendly: Provenance
            - match_reasons: Why this memory was recalled
            - also_written_by: Other hosts that wrote this memory
            - source_events: Source events that created it
            - related_memories: Related memories
            - state_info: Current state and transitions
            - explain: Human-readable explanation

        All returned data is JSON-serializable (no datetime objects).
        """
        memory = self.memory_store.get(memory_id)
        if not memory:
            return {"error": "Memory not found", "success": False}

        # Get source_tool and provenance from first source event
        source_tool = "unknown"
        event_timestamp = memory.created_at
        for event_id in memory.source_event_ids:
            event = self.event_store.get(event_id)
            if event:
                source_tool = getattr(event, 'source_tool', 'unknown')
                if isinstance(event.timestamp, datetime):
                    event_timestamp = event.timestamp.isoformat()
                elif hasattr(event, 'timestamp') and isinstance(event.timestamp, str):
                    event_timestamp = event.timestamp
                break

        # Get provenance info
        provenance = get_source_tool_label(source_tool)

        # Build match_reasons from keywords
        match_reasons = []
        if recall_query:
            query_keywords = self._extract_keywords(recall_query)
            matched_keywords = [kw for kw in query_keywords if kw.lower() in memory.content.lower() or kw.lower() in memory.title.lower()]
            if matched_keywords:
                match_reasons.append({
                    "type": "keyword",
                    "matched": matched_keywords,
                })
            # Check scope match
            if memory.project:
                match_reasons.append({
                    "type": "scope",
                    "matched": {"project": memory.project},
                })
            if memory.session:
                match_reasons.append({
                    "type": "scope",
                    "matched": {"session": memory.session},
                })

        # Get also_written_by - other hosts that wrote to this memory's entity
        also_written_by = []
        entity_key = memory.title.lower().strip() if memory.title else memory.summary.lower().strip()[:50]
        if entity_key:
            # Find other memories with same title/content
            all_mems = self.memory_store.query(
                user=memory.user,
                project=memory.project,
                keywords=[],
                limit=100,
            )
            for mem in all_mems:
                if mem.memory_id == memory.memory_id:
                    continue
                mem_key = mem.title.lower().strip() if mem.title else mem.summary.lower().strip()[:50]
                if mem_key == entity_key:
                    for event_id in mem.source_event_ids:
                        event = self.event_store.get(event_id)
                        if event:
                            other_source = getattr(event, 'source_tool', None)
                            if other_source and other_source != source_tool:
                                if other_source not in also_written_by:
                                    also_written_by.append(other_source)

        # Get source events
        source_events = []
        for event_id in memory.source_event_ids:
            event = self.event_store.get(event_id)
            if event:
                event_dict = event.to_dict()
                # Ensure timestamp is ISO string
                if isinstance(event_dict.get("timestamp"), datetime):
                    event_dict["timestamp"] = event_dict["timestamp"].isoformat()
                source_events.append(event_dict)

        # Get related memories (from conflict_with and superseded_by)
        related = []
        # Add conflicted memories
        for linked_id in memory.conflict_with:
            linked = self.memory_store.get(linked_id)
            if linked:
                related.append({
                    "memory_id": linked.memory_id,
                    "title": linked.title,
                    "state": linked.state.value,
                    "relationship": "conflict",
                })
        # Add superseded memory
        if memory.superseded_by:
            linked = self.memory_store.get(memory.superseded_by)
            if linked:
                related.append({
                    "memory_id": linked.memory_id,
                    "title": linked.title,
                    "state": linked.state.value,
                    "relationship": "superseded_by",
                })

        # Ensure memory dict is JSON-serializable
        memory_dict = memory.to_dict()
        # Convert any datetime fields
        if "created_at" in memory_dict and isinstance(memory_dict["created_at"], datetime):
            memory_dict["created_at"] = memory_dict["created_at"].isoformat()
        if "updated_at" in memory_dict and isinstance(memory_dict["updated_at"], datetime):
            memory_dict["updated_at"] = memory_dict["updated_at"].isoformat()

        # Build human-readable explain text
        explain_parts = []
        if match_reasons:
            for mr in match_reasons:
                if mr["type"] == "keyword":
                    explain_parts.append(f"Matched keywords: {', '.join(mr['matched'])}")
                elif mr["type"] == "scope":
                    for k, v in mr["matched"].items():
                        explain_parts.append(f"Matched scope {k}={v}")
        explain_parts.append(f"Source: {provenance['source_host_friendly']}")
        if also_written_by:
            also_friendly = [get_source_tool_label(s)["source_host_friendly"] for s in also_written_by]
            explain_parts.append(f"Also written by: {', '.join(also_friendly)}")
        explain_text = "; ".join(explain_parts)

        return {
            "memory_id": memory_id,
            "recall_query": recall_query,
            "match_reasons": match_reasons,
            "source_tool": source_tool,
            "source_host_friendly": provenance["source_host_friendly"],
            "event_timestamp": event_timestamp,
            "also_written_by": also_written_by,
            "explain": explain_text,
            "memory": memory_dict,
            "source_events": source_events,
            "related_memories": related,
            "state_info": {
                "current_state": memory.state.value,
                "tier": memory.tier.value,
                "score": memory.score.model_dump() if hasattr(memory.score, 'model_dump') else dict(memory.score),
                "superseded_by": memory.superseded_by,
                "conflicts_with": memory.conflict_with,
            },
            "success": True,
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from query."""
        words = text.lower().split()
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                     "being", "have", "has", "had", "do", "does", "did", "will",
                     "would", "could", "should", "may", "might", "must", "can",
                     "to", "of", "in", "for", "on", "with", "at", "by", "from",
                     "as", "into", "through", "during", "before", "after",
                     "and", "or", "but", "if", "because", "so", "that", "this",
                     "what", "which", "who", "whom", "whose", "where", "when",
                     "why", "how"}
        return [w for w in words if len(w) > 2 and w not in stopwords][:5]

    def _detect_conflicts(self, memories: List[MemoryObject]) -> tuple:
        """Detect conflicts among memories.

        Conflict detection identifies when the same topic/entity has different
        content from different source_tool values.

        Returns:
            Tuple of (conflict_detected: bool, candidates: list of conflicting memories)
        """
        if len(memories) < 2:
            return False, []

        # Build a map of entity/topic to memories
        # Use content hash to detect same entity, then check if content differs
        entity_map = {}

        for mem in memories:
            # Use title/content as entity key
            entity_key = mem.title.lower().strip() if mem.title else mem.summary.lower().strip()[:50]

            if entity_key not in entity_map:
                entity_map[entity_key] = []
            entity_map[entity_key].append(mem)

        # Find conflicts: same entity key but different content from different sources
        conflicts = []
        for entity_key, mems in entity_map.items():
            if len(mems) < 2:
                continue

            # Get unique sources for this entity
            sources = set()
            for mem in mems:
                if mem.source_event_ids:
                    event = self.event_store.get(mem.source_event_ids[0])
                    if event:
                        sources.add(getattr(event, 'source_tool', 'unknown'))

            # If same entity from multiple sources, check for content difference
            if len(sources) > 1:
                contents = set(m.content for m in mems)
                if len(contents) > 1:
                    # Conflicting content from different sources
                    for mem in mems:
                        event = self.event_store.get(mem.source_event_ids[0]) if mem.source_event_ids else None
                        source_tool = getattr(event, 'source_tool', 'unknown') if event else 'unknown'
                        ts = getattr(event, 'timestamp', mem.created_at) if event else mem.created_at
                        if isinstance(ts, datetime):
                            ts = ts.isoformat()

                        conflicts.append({
                            "memory_id": mem.memory_id,
                            "content": mem.content,
                            "source_tool": source_tool,
                            "source_host_friendly": get_source_tool_label(source_tool)["source_host_friendly"],
                            "timestamp": ts,
                            "entity_key": entity_key,
                        })

        if conflicts:
            return True, conflicts
        return False, []

    def _save_trace(self, traces: Dict[str, Any]):
        """Save retrieval trace."""
        # For MVP, we could save to a file or table
        # This is for debugging/analysis
        pass
