"""Host Auto-Detection for OCMF.

Automatically detects the current AI host environment (Claude, Codex, OpenClaw)
and determines the recommended integration method.
"""
import os
import platform
from typing import Dict, Optional, Tuple

# Host detection mapping
HOST_METHODS = {
    "claude": {
        "name": "Claude",
        "method": "A1+B",
        "description": "Native hooks + system-prompt",
        "auto_memory": True,
    },
    "codex": {
        "name": "Codex",
        "method": "C",
        "description": "Manual MCP",
        "auto_memory": False,
    },
    "openclaw": {
        "name": "OpenClaw",
        "method": "BLOCKED",
        "description": "GitHub release unavailable",
        "auto_memory": False,
    },
}


def detect_claude() -> Tuple[bool, Dict[str, str]]:
    """Detect if running in Claude environment.

    IMPORTANT: Detection is based on env vars which indicate Claude is
    actively running, NOT just that Claude is installed.

    Primary indicator: CLAUDE_API_KEY (only set when Claude is running)
    Secondary: other CLAUDE_* vars
    """
    env_vars = {}

    # Check Claude-specific environment variables
    claude_vars = [
        "CLAUDE_API_KEY",
        "CLAUDE_MODEL",
        "CLAUDE_WORKSPACE",
        "CLAUDE_PROJECT",
    ]

    for var in claude_vars:
        val = os.environ.get(var)
        if val:
            env_vars[var] = val[:20] + "..." if len(val) > 20 else val

    # Primary detection: API key means Claude is active
    is_claude = bool(os.environ.get("CLAUDE_API_KEY"))

    return is_claude, env_vars


def detect_codex() -> Tuple[bool, Dict[str, str]]:
    """Detect if running in Codex environment.

    IMPORTANT: Binary presence alone is NOT sufficient to determine
    that Codex is the current runtime host. A binary might be installed
    but not actively running.

    Detection priority:
    1. CODEX_API_KEY env var (most reliable - only set when Codex is running)
    2. CODEX_* env vars (secondary indicators)
    3. Binary existence (weak indicator - just means installed)
    """
    env_vars = {}

    # Check Codex-specific environment variables (set when Codex is active)
    codex_vars = [
        "CODEX_API_KEY",
        "CODEX_MODEL",
        "CODEX_WORKSPACE",
    ]

    for var in codex_vars:
        val = os.environ.get(var)
        if val:
            env_vars[var] = val[:20] + "..." if len(val) > 20 else val

    # Check if codex binary is available (weak indicator)
    import shutil
    has_codex_binary = shutil.which("codex") is not None
    if has_codex_binary:
        env_vars["CODEX_BINARY"] = "found (installed)"

    # Primary detection: API key means Codex is active
    has_api_key = bool(os.environ.get("CODEX_API_KEY"))

    # Detection result
    # IMPORTANT: We do NOT use binary alone to determine "is_codex"
    # Binary existence means "can be used" but NOT "is currently running"
    is_codex = has_api_key

    # Additional info for debugging
    if has_codex_binary and not has_api_key:
        env_vars["_note"] = "binary installed but not active"

    return is_codex, env_vars


def detect_openclaw() -> Tuple[bool, Dict[str, str]]:
    """Detect if running in OpenClaw environment.

    OpenClaw is currently BLOCKED due to GitHub release being unavailable.
    """
    env_vars = {}

    # Check OpenClaw environment variables
    openclaw_vars = [
        "OPENCLAW_API_KEY",
        "OPENCLAW_VERSION",
    ]

    for var in openclaw_vars:
        val = os.environ.get(var)
        if val:
            env_vars[var] = val[:20] + "..." if len(val) > 20 else val

    # OpenClaw detection is informational only - it's BLOCKED
    is_openclaw = bool(os.environ.get("OPENCLAW_API_KEY"))

    return is_openclaw, env_vars


def detect_host() -> str:
    """Auto-detect the current host environment.

    Returns:
        Host identifier: "claude", "codex", "openclaw", or "unknown"
    """
    # Check in order of reliability
    # Claude has most distinctive env vars
    is_claude, _ = detect_claude()
    if is_claude:
        return "claude"

    # Codex has API key or binary
    is_codex, _ = detect_codex()
    if is_codex:
        return "codex"

    # OpenClaw (even though it's blocked)
    is_openclaw, _ = detect_openclaw()
    if is_openclaw:
        return "openclaw"

    return "unknown"


def get_host_info() -> Dict:
    """Get comprehensive host information.

    DISTINCTION:
    - "installed_capability": What hosts have software installed
    - "current_runtime_host": Which host is actively running RIGHT NOW

    Detection is based on env vars (only set when host is active),
    NOT on binary existence.

    Returns:
        Dict with:
        - detected_host: str (current runtime host)
        - host_friendly: str
        - recommended_method: str
        - source_tool: str
        - status: str
        - env_vars: dict
        - auto_memory_supported: bool
        - detection_basis: str ("env_var" or "unknown")
    """
    detected = detect_host()
    method_info = HOST_METHODS.get(detected, {})

    # Get env vars for each detection
    _, claude_vars = detect_claude()
    _, codex_vars = detect_codex()
    _, openclaw_vars = detect_openclaw()

    all_vars = {}
    all_vars.update(claude_vars)
    all_vars.update(codex_vars)
    all_vars.update(openclaw_vars)

    # Map to source_tool
    source_tool_map = {
        "claude": "claude-code",
        "codex": "codex-cli",
        "openclaw": "openclaw",
    }

    # Determine status and detection basis
    if detected == "unknown":
        status = "not detected"
        detection_basis = "unknown"
    elif detected == "openclaw":
        status = "blocked"
        detection_basis = "env_var"
    else:
        status = "supported"
        detection_basis = "env_var"

    return {
        "detected_host": detected,
        "host_friendly": method_info.get("name", detected.title()),
        "recommended_method": method_info.get("method", "N/A"),
        "source_tool": source_tool_map.get(detected, "cli"),
        "status": status,
        "method_description": method_info.get("description", ""),
        "auto_memory_supported": method_info.get("auto_memory", False),
        "env_vars": all_vars,
        "detection_basis": detection_basis,
    }


def get_method_for_host(host: str) -> Optional[str]:
    """Get recommended integration method for a host.

    Args:
        host: Host identifier

    Returns:
        Method string (e.g., "A1+B", "C") or None
    """
    info = HOST_METHODS.get(host, {})
    return info.get("method")


def is_auto_memory_supported(host: str) -> bool:
    """Check if a host supports auto-memory.

    Args:
        host: Host identifier

    Returns:
        True if auto-memory is supported
    """
    info = HOST_METHODS.get(host, {})
    return info.get("auto_memory", False)


if __name__ == "__main__":
    # Test host detection
    info = get_host_info()
    print(f"Detected Host: {info['detected_host']}")
    print(f"Friendly Name: {info['host_friendly']}")
    print(f"Method: {info['recommended_method']}")
    print(f"Source Tool: {info['source_tool']}")
    print(f"Status: {info['status']}")
    print(f"Auto-Memory: {info['auto_memory_supported']}")
    print(f"\nEnvironment Variables:")
    for var, val in info["env_vars"].items():
        print(f"  {var}: {val}")
