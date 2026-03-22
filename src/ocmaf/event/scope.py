"""Scope model for multi-level isolation."""
from typing import Optional
from pydantic import BaseModel, Field


class Scope(BaseModel):
    """Memory scope for user/workspace/project/session/tool isolation.

    Hierarchy: user > workspace > project > session > tool
    """
    user: str
    workspace: Optional[str] = None
    project: Optional[str] = None
    session: Optional[str] = None
    tool: Optional[str] = None

    def to_filter_dict(self) -> dict:
        """Convert to filter dictionary for queries."""
        result = {"user": self.user}
        if self.workspace:
            result["workspace"] = self.workspace
        if self.project:
            result["project"] = self.project
        if self.session:
            result["session"] = self.session
        if self.tool:
            result["tool"] = self.tool
        return result

    def matches(self, other: "Scope") -> bool:
        """Check if this scope matches or is a parent of another scope."""
        if self.user != other.user:
            return False
        if self.workspace and other.workspace and self.workspace != other.workspace:
            return False
        if self.project and other.project and self.project != other.project:
            return False
        if self.session and other.session and self.session != other.session:
            return False
        if self.tool and other.tool and self.tool != other.tool:
            return False
        return True
