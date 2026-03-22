"""Scope mapping rules for different tools.

This module provides scope mapping from various AI tool contexts
to OCMF's user/workspace/project/session/tool hierarchy.
"""
import os
from typing import Any, Dict, Optional


class ScopeMapper:
    """Maps tool-specific context to OCMF scope."""

    # Default mapping rules
    DEFAULT_MAPPING = {
        "user": "default",
        "workspace": None,
        "project": None,
        "session": None,
        "tool": None,
    }

    def __init__(self, tool_name: str):
        """Initialize scope mapper for a specific tool."""
        self.tool_name = tool_name

    def map_from_env(self, extra_env: Optional[Dict[str, str]] = None) -> Dict[str, Optional[str]]:
        """Map scope from environment variables.

        Different tools set different env vars.
        """
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)

        if self.tool_name == "claude-code":
            return self._map_claude_code(env)
        elif self.tool_name == "openclaw":
            return self._map_openclaw(env)
        elif self.tool_name == "codex-cli":
            return self._map_codex_cli(env)
        else:
            return self.DEFAULT_MAPPING.copy()

    def _map_claude_code(self, env: Dict[str, str]) -> Dict[str, Optional[str]]:
        """Map Claude Code environment."""
        return {
            "user": env.get("CLAUDE_USER_ID", "default"),
            "workspace": env.get("CLAUDE_WORKSPACE"),
            "project": env.get("CLAUDE_PROJECT"),
            "session": env.get("CLAUDE_SESSION_ID"),
            "tool": "claude-code",
        }

    def _map_openclaw(self, env: Dict[str, str]) -> Dict[str, Optional[str]]:
        """Map OpenClaw environment."""
        return {
            "user": env.get("OPENCLAW_USER_ID", "default"),
            "workspace": env.get("OPENCLAW_WORKSPACE"),
            "project": env.get("OPENCLAW_PROJECT"),
            "session": env.get("OPENCLAW_SESSION_ID"),
            "tool": "openclaw",
        }

    def _map_codex_cli(self, env: Dict[str, str]) -> Dict[str, Optional[str]]:
        """Map Codex CLI environment."""
        return {
            "user": env.get("CODEX_USER", "default"),
            "workspace": env.get("CODEX_WORKSPACE"),
            "project": env.get("CODEX_PROJECT"),
            "session": env.get("CODEX_SESSION"),
            "tool": "codex-cli",
        }

    def map_from_context(self, context: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Map scope from runtime context dict.

        This handles tool-specific context objects.
        """
        return {
            "user": context.get("user", self.DEFAULT_MAPPING["user"]),
            "workspace": context.get("workspace"),
            "project": context.get("project"),
            "session": context.get("session"),
            "tool": context.get("tool", self.tool_name),
        }

    def resolve_effective_scope(
        self,
        requested_scope: Dict[str, Optional[str]],
        parent_scope: Optional[Dict[str, Optional[str]]] = None,
    ) -> Dict[str, Optional[str]]:
        """Resolve effective scope with inheritance.

        If a scope level is not specified, it may inherit from parent.
        """
        effective = self.DEFAULT_MAPPING.copy()

        # Start with requested scope
        for key in ["user", "workspace", "project", "session", "tool"]:
            if requested_scope.get(key):
                effective[key] = requested_scope[key]
            elif parent_scope and parent_scope.get(key):
                effective[key] = parent_scope[key]

        return effective


def get_scope_mapper(tool_name: str) -> ScopeMapper:
    """Get scope mapper for a specific tool."""
    return ScopeMapper(tool_name)
