"""SQLite schema initialization."""
import sqlite3
from pathlib import Path
from typing import Optional


def get_default_db_path() -> Path:
    """Get default database path."""
    home = Path.home()
    ocmf_dir = home / ".ocmaf"
    ocmf_dir.mkdir(exist_ok=True)
    return ocmf_dir / "memory.db"


def init_schema(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Initialize database schema."""
    if db_path is None:
        db_path = get_default_db_path()

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # Create tables
    conn.executescript("""
        -- Events table (append-only source of truth)
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            version TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            source_tool TEXT NOT NULL,
            scope_json TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            evidence_json TEXT NOT NULL,
            links_json TEXT NOT NULL
        );

        -- Create index on scope and timestamp for efficient queries
        CREATE INDEX IF NOT EXISTS idx_events_scope ON events(scope_json);
        CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
        CREATE INDEX IF NOT EXISTS idx_events_source_tool ON events(source_tool);
        CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);

        -- Memory Objects table (derived/aggregated)
        CREATE TABLE IF NOT EXISTS memory_objects (
            memory_id TEXT PRIMARY KEY,
            tier TEXT NOT NULL,
            state TEXT NOT NULL,
            resolution TEXT NOT NULL,
            title TEXT,
            summary TEXT,
            content TEXT,
            keywords_json TEXT,
            score_json TEXT,
            superseded_by TEXT,
            conflict_with_json TEXT,
            source_event_ids_json TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            user TEXT NOT NULL,
            workspace TEXT,
            project TEXT,
            session TEXT,
            tool TEXT
        );

        -- Create indexes for memory objects
        CREATE INDEX IF NOT EXISTS idx_memory_user ON memory_objects(user);
        CREATE INDEX IF NOT EXISTS idx_memory_workspace ON memory_objects(workspace);
        CREATE INDEX IF NOT EXISTS idx_memory_project ON memory_objects(project);
        CREATE INDEX IF NOT EXISTS idx_memory_session ON memory_objects(session);
        CREATE INDEX IF NOT EXISTS idx_memory_tier ON memory_objects(tier);
        CREATE INDEX IF NOT EXISTS idx_memory_state ON memory_objects(state);
        CREATE INDEX IF NOT EXISTS idx_memory_tool ON memory_objects(tool);

        -- Retrieval traces for analysis
        CREATE TABLE IF NOT EXISTS retrieval_traces (
            trace_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            query TEXT NOT NULL,
            context_json TEXT,
            results_json TEXT,
            selected_memory_ids_json TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_traces_timestamp ON retrieval_traces(timestamp);
    """)

    conn.commit()
    return conn
