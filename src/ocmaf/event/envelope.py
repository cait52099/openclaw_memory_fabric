"""Event Envelope - the core memory event structure."""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .types import EventType
from .scope import Scope


class EventEnvelope(BaseModel):
    """Memory Event Envelope - the atomic unit of memory.

    This is the single source of truth. All memory objects must be
    reconstructable from these events.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "1.0"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_tool: str  # e.g., "openclaw", "claude-code", "codex-cli"
    scope: Scope
    event_type: EventType
    payload: Dict[str, Any]  # The actual content
    evidence: List[str] = Field(default_factory=list)  # References to evidence
    links: List[str] = Field(default_factory=list)  # Related memory IDs

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "EventEnvelope":
        """Create from dictionary."""
        return cls(**data)
