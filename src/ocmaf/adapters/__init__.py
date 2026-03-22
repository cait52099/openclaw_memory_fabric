"""Adapters for different AI tools."""
from .base import Adapter, InjectionPolicy
from .claude_code import ClaudeCodeAdapter, get_recall_context, remember_interaction
from .codex_cli import CodexCLIAdapter, get_recall_context as codex_get_recall_context
from .codex_cli import remember_interaction as codex_remember_interaction
from .codex_cli import remember_task_result as codex_remember_task_result
from .openclaw import OpenClawAdapter, get_recall_context as openclaw_get_recall_context
from .openclaw import remember_interaction as openclaw_remember_interaction

__all__ = [
    "Adapter",
    "InjectionPolicy",
    "ClaudeCodeAdapter",
    "CodexCLIAdapter",
    "OpenClawAdapter",
    "get_recall_context",
    "remember_interaction",
    "codex_get_recall_context",
    "codex_remember_interaction",
    "codex_remember_task_result",
    "openclaw_get_recall_context",
    "openclaw_remember_interaction",
]
