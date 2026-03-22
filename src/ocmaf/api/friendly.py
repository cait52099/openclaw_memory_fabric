"""Friendly name mapping for source_tool values."""

FRIENDLY_NAMES = {
    "claude-code": "Claude",
    "codex-cli": "Codex",
    "openclaw": "OpenClaw",
    "synthetic": "Synthetic (Test)",
}


def get_friendly_name(source_tool: str) -> str:
    """Map source_tool to friendly display name.

    Args:
        source_tool: Raw source_tool value (e.g., 'claude-code', 'codex-cli')

    Returns:
        Friendly display name (e.g., 'Claude', 'Codex', 'OpenClaw', 'Synthetic (Test)')
    """
    return FRIENDLY_NAMES.get(source_tool, source_tool)


def get_source_tool_label(source_tool: str) -> dict:
    """Get complete source tool label info.

    Args:
        source_tool: Raw source_tool value

    Returns:
        Dict with source_tool, friendly_name, and is_synthetic flag
    """
    friendly = get_friendly_name(source_tool)
    is_synthetic = source_tool == "synthetic"
    return {
        "source_tool": source_tool,
        "source_host_friendly": friendly,
        "is_synthetic": is_synthetic,
    }
