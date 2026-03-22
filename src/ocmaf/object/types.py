"""Object type definitions."""
from enum import Enum


class Tier(str, Enum):
    """Memory tier based on access frequency and importance."""
    WORKING = "working"  # Current working context
    HOT = "hot"          # Frequently accessed
    WARM = "warm"        # Moderately accessed
    COLD = "cold"        # Rarely accessed
    ARCHIVE = "archive"  # Historical/archived


class State(str, Enum):
    """Memory state lifecycle."""
    ACTIVE = "active"       # Currently relevant
    LATENT = "latent"      # Not actively used but available
    REINFORCED = "reinforced"  # Recently reinforced
    DECAYING = "decaying"  # Losing relevance
    SUPERSEDED = "superseded"  # Replaced by newer memory
    CONFLICTED = "conflicted"  # Has conflicts
    QUARANTINED = "quarantined"  # Isolated for review
    ARCHIVED = "archived"  # Fully archived


class Resolution(str, Enum):
    """Memory resolution level for retrieval."""
    CUE = "cue"        # Trigger/keyword match
    GIST = "gist"      # Brief summary
    DETAIL = "detail"  # Full details
    EVIDENCE = "evidence"  # With proof/evidence
