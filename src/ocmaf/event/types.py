"""Event type definitions."""
from enum import Enum


class EventType(str, Enum):
    """Types of memory events."""
    CHAT_TURN = "chat_turn"
    TASK_RESULT = "task_result"
    DECISION = "decision"
    PREFERENCE = "preference"
    CONSTRAINT = "constraint"
    EVIDENCE = "evidence"
