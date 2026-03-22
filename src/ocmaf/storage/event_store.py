"""Event Store - append-only raw event storage."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..event.envelope import EventEnvelope
from ..event.scope import Scope
from .schema import init_schema, get_default_db_path


class EventStore:
    """Append-only event store.

    Single source of truth. All events are immutable once written.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize event store."""
        self.db_path = db_path or get_default_db_path()
        self.conn = init_schema(self.db_path)

    def append(self, event: EventEnvelope) -> str:
        """Append an event to the store.

        Returns the event_id.
        """
        import uuid

        # Ensure event has ID
        if not event.event_id:
            event.event_id = str(uuid.uuid4())

        self.conn.execute(
            """
            INSERT INTO events (
                event_id, version, timestamp, source_tool,
                scope_json, event_type, payload_json,
                evidence_json, links_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.version,
                event.timestamp,
                event.source_tool,
                event.scope.model_dump_json(),
                event.event_type.value,
                json.dumps(event.payload),
                json.dumps(event.evidence),
                json.dumps(event.links),
            )
        )
        self.conn.commit()
        return event.event_id

    def get(self, event_id: str) -> Optional[EventEnvelope]:
        """Get an event by ID."""
        row = self.conn.execute(
            "SELECT * FROM events WHERE event_id = ?", (event_id,)
        ).fetchone()

        if not row:
            return None

        return self._row_to_event(row)

    def query(
        self,
        scope: Optional[Scope] = None,
        source_tool: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 100,
    ) -> List[EventEnvelope]:
        """Query events with filters.

        Uses json_extract for reliable scope filtering instead of LIKE.
        This avoids false positives from JSON LIKE matching.
        """
        query = "SELECT * FROM events WHERE 1=1"
        params = []

        if scope:
            scope_dict = scope.to_filter_dict()
            for key, value in scope_dict.items():
                if value is not None:
                    # Use json_extract for reliable JSON field extraction
                    # This ensures exact matching without false positives
                    query += " AND json_extract(scope_json, '$.{}') = ?".format(key)
                    params.append(value)

        if source_tool:
            query += " AND source_tool = ?"
            params.append(source_tool)

        if event_types:
            placeholders = ",".join("?" * len(event_types))
            query += f" AND event_type IN ({placeholders})"
            params.extend(event_types)

        if since:
            query += " AND timestamp >= ?"
            params.append(since)

        if until:
            query += " AND timestamp <= ?"
            params.append(until)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        rows = self.conn.execute(query, params).fetchall()
        return [self._row_to_event(row) for row in rows]

    def _row_to_event(self, row: sqlite3.Row) -> EventEnvelope:
        """Convert database row to EventEnvelope."""
        return EventEnvelope(
            event_id=row["event_id"],
            version=row["version"],
            timestamp=row["timestamp"],
            source_tool=row["source_tool"],
            scope=Scope(**json.loads(row["scope_json"])),
            event_type=row["event_type"],
            payload=json.loads(row["payload_json"]),
            evidence=json.loads(row["evidence_json"]),
            links=json.loads(row["links_json"]),
        )

    def count(self) -> int:
        """Count total events."""
        return self.conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    def close(self):
        """Close connection."""
        self.conn.close()
