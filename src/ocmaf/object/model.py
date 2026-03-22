"""Memory Object - aggregated from events."""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .types import Tier, State, Resolution


class Score(BaseModel):
    """Memory scoring."""
    relevance: float = 0.0    # 0.0-1.0, how relevant to query
    confidence: float = 0.0   # 0.0-1.0, confidence in accuracy
    freshness: float = 1.0    # 0.0-1.0, how recent


class MemoryObject(BaseModel):
    """Aggregated memory object.

    Built from events via consolidation. Reconstructable from events.
    """
    memory_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tier: Tier = Tier.WORKING
    state: State = State.ACTIVE
    resolution: Resolution = Resolution.GIST

    # Content
    title: str = ""
    summary: str = ""
    content: str = ""
    keywords: List[str] = Field(default_factory=list)

    # Scoring
    score: Score = Field(default_factory=Score)

    # Relationships
    superseded_by: Optional[str] = None  # Replaced by memory_id
    conflict_with: List[str] = Field(default_factory=list)  # Conflicting memory_ids

    # Source tracking
    source_event_ids: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Scope (from source events)
    user: str
    workspace: Optional[str] = None
    project: Optional[str] = None
    session: Optional[str] = None
    tool: Optional[str] = None  # tool scope for isolation

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryObject":
        """Create from dictionary."""
        # Handle nested Score object
        if "score" in data and isinstance(data["score"], dict):
            data["score"] = Score(**data["score"])
        return cls(**data)
