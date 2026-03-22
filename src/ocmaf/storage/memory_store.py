"""Memory Store - aggregated memory objects."""
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..object.model import MemoryObject, Score
from ..object.types import Tier, State, Resolution
from .schema import init_schema, get_default_db_path


class MemoryStore:
    """Store for aggregated memory objects.

    These are derived from events via consolidation.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize memory store."""
        self.db_path = db_path or get_default_db_path()
        self.conn = init_schema(self.db_path)

    def put(self, memory: MemoryObject) -> str:
        """Store or update a memory object."""
        self.conn.execute(
            """
            INSERT OR REPLACE INTO memory_objects (
                memory_id, tier, state, resolution,
                title, summary, content, keywords_json,
                score_json, superseded_by, conflict_with_json,
                source_event_ids_json, created_at, updated_at,
                user, workspace, project, session, tool
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                memory.memory_id,
                memory.tier.value,
                memory.state.value,
                memory.resolution.value,
                memory.title,
                memory.summary,
                memory.content,
                json.dumps(memory.keywords),
                json.dumps(memory.score.model_dump()),
                memory.superseded_by,
                json.dumps(memory.conflict_with),
                json.dumps(memory.source_event_ids),
                memory.created_at,
                memory.updated_at,
                memory.user,
                memory.workspace,
                memory.project,
                memory.session,
                memory.tool,
            )
        )
        self.conn.commit()
        return memory.memory_id

    def get(self, memory_id: str) -> Optional[MemoryObject]:
        """Get a memory object by ID."""
        row = self.conn.execute(
            "SELECT * FROM memory_objects WHERE memory_id = ?", (memory_id,)
        ).fetchone()

        if not row:
            return None

        return self._row_to_memory(row)

    def query(
        self,
        user: str,
        workspace: Optional[str] = None,
        project: Optional[str] = None,
        session: Optional[str] = None,
        tool: Optional[str] = None,
        tier: Optional[Tier] = None,
        state: Optional[State] = None,
        keywords: Optional[List[str]] = None,
        limit: int = 20,
    ) -> List[MemoryObject]:
        """Query memory objects with filters."""
        query = "SELECT * FROM memory_objects WHERE user = ?"
        params = [user]

        if workspace:
            query += " AND workspace = ?"
            params.append(workspace)

        if project:
            query += " AND project = ?"
            params.append(project)

        if session:
            query += " AND session = ?"
            params.append(session)

        if tool:
            query += " AND tool = ?"
            params.append(tool)

        if tier:
            query += " AND tier = ?"
            params.append(tier.value)

        if state:
            query += " AND state = ?"
            params.append(state.value)

        query += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)

        rows = self.conn.execute(query, params).fetchall()

        # Filter by keywords in Python (simple approach)
        results = [self._row_to_memory(row) for row in rows]

        if keywords:
            results = [
                m for m in results
                if any(
                    kw.lower() in m.content.lower() or
                    kw.lower() in m.title.lower() or
                    kw.lower() in m.summary.lower() or
                    kw.lower() in [k.lower() for k in m.keywords]
                    for kw in keywords)
            ]

        return results

    def delete(self, memory_id: str) -> bool:
        """Delete a memory object."""
        cursor = self.conn.execute(
            "DELETE FROM memory_objects WHERE memory_id = ?", (memory_id,)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def _row_to_memory(self, row: sqlite3.Row) -> MemoryObject:
        """Convert database row to MemoryObject."""
        return MemoryObject(
            memory_id=row["memory_id"],
            tier=Tier(row["tier"]),
            state=State(row["state"]),
            resolution=Resolution(row["resolution"]),
            title=row["title"] or "",
            summary=row["summary"] or "",
            content=row["content"] or "",
            keywords=json.loads(row["keywords_json"] or "[]"),
            score=Score(**json.loads(row["score_json"] or "{}")),
            superseded_by=row["superseded_by"],
            conflict_with=json.loads(row["conflict_with_json"] or "[]"),
            source_event_ids=json.loads(row["source_event_ids_json"] or "[]"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            user=row["user"],
            workspace=row["workspace"],
            project=row["project"],
            session=row["session"],
            tool=row["tool"],
        )

    def count(self) -> int:
        """Count total memory objects."""
        return self.conn.execute("SELECT COUNT(*) FROM memory_objects").fetchone()[0]

    def clear_all(self):
        """Clear all memory objects (for testing)."""
        self.conn.execute("DELETE FROM memory_objects")
        self.conn.commit()

    def close(self):
        """Close connection."""
        self.conn.close()
