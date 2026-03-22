"""Unified Entry Point CLI for OCMF.

This module provides a unified CLI interface that:
- Auto-detects the current host environment
- Provides simple commands: install, status, config, recall, remember
- Hides MCP complexity from users
"""
import click
import json
import os
import subprocess
import sys
from pathlib import Path

from .host_detection import detect_host, get_host_info, HOST_METHODS
from ..storage.event_store import EventStore
from ..storage.memory_store import MemoryStore
from ..api.remember import RememberAPI
from ..api.recall import RecallAPI
from ..event.envelope import EventEnvelope
from ..event.scope import Scope
from ..event.types import EventType


def _auto_source_config():
    """Auto-source OCMF config if it exists.

    This allows the CLI to pick up OCMF_SOURCE_TOOL and other settings
    without requiring users to manually source their config file.
    """
    config_path = Path.home() / ".ocmf" / "config.sh"
    if config_path.exists():
        try:
            # Source the config using bash in a subprocess and capture env vars
            result = subprocess.run(
                ["bash", "-c", f"source {config_path} && env"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Update current process environment with config vars
                for line in result.stdout.splitlines():
                    if "=" in line:
                        key, _, value = line.partition("=")
                        # Only import OCMF-specific vars
                        if key.startswith("OCMF_"):
                            os.environ[key] = value
        except Exception:
            # If anything goes wrong, just continue without the config
            pass


# Auto-source config on module load
_auto_source_config()


@click.group()
@click.version_option(version="0.1.1")
def unified():
    """OCMF Unified Entry Point - Memory that works across AI hosts.

    Automatically detects your AI host (Claude, Codex, OpenClaw) and
    configures memory to work seamlessly. No need to understand MCP.
    """
    pass


@unified.command()
@click.option("--host", default=None, help="Force specific host: claude, codex, openclaw")
@click.option("--method", default=None, help="Force specific method: a1, b, c")
@click.option("--dry-run", is_flag=True, help="Show what would be done without doing it")
def install(host, method, dry_run):
    """Install OCMF for the current AI host.

    Automatically detects your host and configures the recommended
    memory integration method. Users don't need to understand MCP.
    """
    import subprocess
    from pathlib import Path

    host_info = get_host_info()

    if dry_run:
        click.echo("=== DRY RUN - No changes will be made ===\n")

    click.echo("OCMF Installer")
    click.echo("=" * 40)

    # Detect host
    detected_host = host or host_info.get("detected_host", "unknown")
    host_type = HOST_METHODS.get(detected_host, {})

    click.echo(f"\nHost Detection:")
    click.echo(f"  Detected: {detected_host}")
    click.echo(f"  Method: {method or host_info.get('recommended_method', 'unknown')}")
    click.echo(f"  Status: {host_info.get('status', 'unknown')}")

    if detected_host == "unknown" and not host:
        click.echo("\n⚠️  Could not detect AI host.")
        click.echo("   Please specify --host manually: claude, codex, openclaw")
        sys.exit(1)

    if host:
        detected_host = host
        click.echo(f"  (Forced host: {host})")

    # Show method recommendation
    recommended = method or host_info.get("recommended_method")
    click.echo(f"\nRecommended Integration:")
    click.echo(f"  Method: {recommended}")

    if detected_host == "claude":
        click.echo("  Setup: Native hooks (A1) + system-prompt (B)")
        click.echo("  Auto-memory: Supported")
    elif detected_host == "codex":
        click.echo("  Setup: Manual MCP (Method C)")
        click.echo("  Auto-memory: Requires manual recall/remember")
    elif detected_host == "openclaw":
        click.echo("  ⚠️  OpenClaw integration is BLOCKED (GitHub release unavailable)")
        click.echo("  Status: TBD")
        sys.exit(1)

    if dry_run:
        click.echo("\n=== DRY RUN COMPLETE ===")
        return

    # Find OCMF path dynamically using the ocmaf package location
    # This correctly resolves to the installed package location (even in venvs)
    import ocmaf as ocmaf_pkg
    ocmf_src = Path(ocmaf_pkg.__file__).parent
    hosts_dir = ocmf_src / "hosts"

    # Run the appropriate setup script
    click.echo(f"\n--- Running {detected_host} setup ---")

    if detected_host == "claude":
        setup_script = hosts_dir / "claude_setup.sh"
    elif detected_host == "codex":
        setup_script = hosts_dir / "codex_setup.sh"
    else:
        click.echo(f"\n✗ No setup script for {detected_host}")
        sys.exit(1)

    if not setup_script.exists():
        click.echo(f"\n✗ Setup script not found: {setup_script}")
        sys.exit(1)

    click.echo(f"  Running: source {setup_script}")

    try:
        result = subprocess.run(
            ["bash", "-c", f"source {setup_script}"],
            capture_output=True,
            text=True,
            cwd=str(ocmf_src)
        )

        if result.returncode == 0:
            click.echo(result.stdout)
            click.echo(f"\n✓ {detected_host} setup completed successfully")
        else:
            click.echo(f"\n✗ {detected_host} setup failed:")
            click.echo(f"  stdout: {result.stdout}")
            click.echo(f"  stderr: {result.stderr}")
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n✗ Error running setup: {e}")
        sys.exit(1)

    click.echo("\n✓ Installation complete!")
    click.echo("\nNext steps:")
    click.echo("  1. Run 'source ~/.ocmf/config.sh' to load configuration")
    click.echo("  2. Run 'PYTHONPATH=src ocmaf unified status' to verify setup")


@unified.command()
def status():
    """Show OCMF status and host information.

    Displays the current host, integration method, and memory statistics.
    """
    host_info = get_host_info()

    click.echo("OCMF Status")
    click.echo("=" * 40)

    click.echo(f"\nHost:")
    click.echo(f"  Detected: {host_info.get('detected_host', 'unknown')}")
    click.echo(f"  Method: {host_info.get('recommended_method', 'N/A')}")
    click.echo(f"  Status: {host_info.get('status', 'unknown')}")

    if host_info.get("env_vars"):
        click.echo(f"\nEnvironment Variables:")
        for var, val in host_info["env_vars"].items():
            click.echo(f"  {var}: {val}")

    # Memory stats
    try:
        event_store = EventStore()
        memory_store = MemoryStore()

        event_count = event_store.count()
        memory_count = memory_store.count()

        click.echo(f"\nMemory Statistics:")
        click.echo(f"  Events: {event_count}")
        click.echo(f"  Memory Objects: {memory_count}")

        event_store.close()
        memory_store.close()
    except Exception as e:
        click.echo(f"\nMemory Statistics: (could not read) {e}")

    # Show auto-memory config
    auto_mode = os.environ.get("OCMF_AUTO_MEMORY", "0")
    click.echo(f"\nAuto-Memory Mode: {auto_mode}")
    if auto_mode == "0":
        click.echo("  (Use 'export OCMF_AUTO_MEMORY=1' to enable)")


@unified.command()
@click.option("--show-all", is_flag=True, help="Show all configuration including secrets")
def config(show_all):
    """Show OCMF configuration for current host.

    Displays the configuration needed for memory integration.
    MCP details are hidden by default.
    """
    host_info = get_host_info()

    click.echo("OCMF Configuration")
    click.echo("=" * 40)

    click.echo(f"\nHost: {host_info.get('detected_host', 'unknown')}")
    click.echo(f"Method: {host_info.get('recommended_method', 'N/A')}")

    detected_host = host_info.get("detected_host")

    if detected_host == "claude":
        click.echo("\nClaude Configuration:")
        click.echo("  Integration: Native hooks + system-prompt")
        click.echo("  Auto-memory: Supported (enable with OCMF_AUTO_MEMORY=1)")
        click.echo("  MCP: Not required for basic use")

        mcp_config = os.path.expanduser("~/.claude/mcp_servers.json")
        click.echo(f"\n  MCP Config: {mcp_config}")
        if Path(mcp_config).exists():
            click.echo("  MCP Status: Configured")
        else:
            click.echo("  MCP Status: Not configured (optional)")

    elif detected_host == "codex":
        click.echo("\nCodex Configuration:")
        click.echo("  Integration: Manual MCP (Method C)")
        click.echo("  Auto-memory: Not supported (manual recall/remember)")
        click.echo("  MCP: Required")

        mcp_config = os.path.expanduser("~/.codex/mcp.json")
        click.echo(f"\n  MCP Config: {mcp_config}")
        if Path(mcp_config).exists():
            click.echo("  MCP Status: Configured")
        else:
            click.echo("  MCP Status: Not configured")

    elif detected_host == "openclaw":
        click.echo("\n⚠️  OpenClaw: BLOCKED")
        click.echo("   GitHub release unavailable")

    click.echo("\nEnvironment Variables:")
    click.echo("  OCMF_AUTO_MEMORY: 0=off, 1=on (auto recall/remember)")
    click.echo("  OCMF_SCOPE_USER: Default user ID")
    click.echo("  OCMF_SCOPE_PROJECT: Default project ID")


@unified.command()
@click.option("--query", required=True, help="Search query")
@click.option("--user", default=None, help="User ID")
@click.option("--project", default=None, help="Project ID")
@click.option("--format", default="friendly", help="Output format: friendly, json")
def recall(query, user, project, format):
    """Recall memories with automatic provenance display.

    This is the main command for retrieving relevant memories.
    Provenance (source, timestamp) is shown automatically.
    """
    # Build context from environment/defaults
    context = {
        "user": user or os.environ.get("OCMF_SCOPE_USER", "default"),
        "workspace": os.environ.get("OCMF_SCOPE_WORKSPACE"),
        "project": project or os.environ.get("OCMF_SCOPE_PROJECT"),
        "session": os.environ.get("OCMF_SESSION_ID"),
        "limit": 10,
    }

    memory_store = MemoryStore()
    event_store = EventStore()
    recall_api = RecallAPI(memory_store, event_store)

    result = recall_api.recall(query, context)
    result_dict = result.to_dict()

    if not result.memories:
        click.echo("No memories found.")
    else:
        if format == "json":
            click.echo(json.dumps(result_dict, indent=2, default=str))
        else:
            click.echo(f"Found {len(result.memories)} memories:")

            # Group by source
            by_source = {}
            for mem in result_dict.get("memories", []):
                source = mem.get("source_host_friendly", "Unknown")
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(mem)

            for source, memories in by_source.items():
                click.echo(f"\nFrom {source}:")
                for mem in memories:
                    ts = mem.get("timestamp", "")
                    if ts:
                        try:
                            from datetime import datetime
                            if isinstance(ts, str):
                                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                                ts = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            pass
                    content = mem.get("content", mem.get("summary", ""))[:100]
                    click.echo(f"  • \"{content}\" ({ts})" if ts else f"  • \"{content}\"")

            # Show conflict warning
            if result_dict.get("conflict_detected"):
                candidates = result_dict.get("candidates", [])
                click.echo("\n⚠️ CONFLICT DETECTED")
                click.echo(f"  {len(candidates)} conflicting versions found:")
                for c in candidates:
                    src = c.get("source_host_friendly", "Unknown")
                    content = c.get("content", "")[:60]
                    click.echo(f"  - [{src}] \"{content}\"")

    memory_store.close()
    event_store.close()


@unified.command()
@click.option("--content", required=True, help="Content to remember")
@click.option("--type", default="decision", help="Event type: decision, fact, preference, context")
@click.option("--user", default=None, help="User ID")
@click.option("--project", default=None, help="Project ID")
def remember(content, type, user, project):
    """Remember a memory with automatic provenance.

    Stores the content with source information. Users don't
    need to specify source - it's automatic.
    """
    host_info = get_host_info()

    # Fallback to OCMF_SOURCE_TOOL if host detection fails
    detected_tool = host_info.get("source_tool", "cli")
    source_tool = os.environ.get("OCMF_SOURCE_TOOL", detected_tool)

    # Map event type (only valid EventType values)
    type_map = {
        "decision": EventType.DECISION,
        "preference": EventType.PREFERENCE,
        "constraint": EventType.CONSTRAINT,
        "chat_turn": EventType.CHAT_TURN,
        "task_result": EventType.TASK_RESULT,
        "evidence": EventType.EVIDENCE,
    }
    event_type = type_map.get(type.lower(), EventType.DECISION)

    # Build scope
    scope = Scope(
        user=user or os.environ.get("OCMF_SCOPE_USER", "default"),
        workspace=os.environ.get("OCMF_SCOPE_WORKSPACE"),
        project=project or os.environ.get("OCMF_SCOPE_PROJECT"),
        session=os.environ.get("OCMF_SESSION_ID"),
    )

    event = EventEnvelope(
        source_tool=source_tool,
        scope=scope,
        event_type=event_type,
        payload={
            "content": content,
            "summary": content[:100],
            "keywords": content.split()[:5],
        },
    )

    event_store = EventStore()
    memory_store = MemoryStore()
    remember_api = RememberAPI(event_store, memory_store)

    event_id = remember_api.remember(event)

    click.echo(f"✓ Remembered: {event_id}")

    # Show friendly source name
    source_friendly = os.environ.get("OCMF_SOURCE_TOOL", host_info.get('host_friendly', source_tool))
    # Convert tool name to friendly name
    friendly_map = {
        "claude-code": "Claude",
        "codex-cli": "Codex",
        "openclaw": "OpenClaw",
        "cli": "CLI",
    }
    display_source = friendly_map.get(source_friendly, source_friendly)
    click.echo(f"  Source: {display_source}")

    event_store.close()
    memory_store.close()


@unified.command()
def doctor():
    """Diagnose OCMF setup issues.

    Runs diagnostic checks and reports any problems.
    """
    click.echo("OCMF Doctor")
    click.echo("=" * 40)

    issues = []
    checks = []

    # Check Python version
    py_version = sys.version_info
    checks.append(("Python version", py_version >= (3, 11), f"{py_version.major}.{py_version.minor}"))

    # Check storage
    try:
        event_store = EventStore()
        event_store.count()
        event_store.close()
        checks.append(("EventStore accessible", True, "OK"))
    except Exception as e:
        checks.append(("EventStore accessible", False, str(e)))
        issues.append(f"EventStore: {e}")

    # Check memory store
    try:
        memory_store = MemoryStore()
        memory_store.count()
        memory_store.close()
        checks.append(("MemoryStore accessible", True, "OK"))
    except Exception as e:
        checks.append(("MemoryStore accessible", False, str(e)))
        issues.append(f"MemoryStore: {e}")

    # Check host detection
    host_info = get_host_info()
    detected = host_info.get("detected_host")
    checks.append(("Host detection", detected != "unknown", detected or "not detected"))

    # Check auto-memory setting
    auto_mode = os.environ.get("OCMF_AUTO_MEMORY", "0")
    checks.append(("Auto-memory", True, f"OCMF_AUTO_MEMORY={auto_mode}"))

    click.echo("\nChecks:")
    for name, passed, detail in checks:
        status = "✓" if passed else "✗"
        click.echo(f"  {status} {name}: {detail}")

    if issues:
        click.echo("\nIssues found:")
        for issue in issues:
            click.echo(f"  ⚠️  {issue}")
        sys.exit(1)
    else:
        click.echo("\n✓ All checks passed")


if __name__ == "__main__":
    unified()
