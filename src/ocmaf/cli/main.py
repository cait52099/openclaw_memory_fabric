"""CLI for OCMF."""
import click
import json
from pathlib import Path

from ..event.envelope import EventEnvelope
from ..event.scope import Scope
from ..event.types import EventType
from ..storage.event_store import EventStore
from ..storage.memory_store import MemoryStore
from ..api.remember import RememberAPI
from ..api.recall import RecallAPI


@click.group()
def cli():
    """OpenClaw Memory Fabric CLI."""
    pass


@cli.command()
@click.option("--user", default="default", help="User ID")
@click.option("--workspace", help="Workspace ID")
@click.option("--project", help="Project ID")
@click.option("--session", help="Session ID")
@click.option("--tool", default="cli", help="Source tool")
@click.argument("content")
def remember(user, workspace, project, session, tool, content):
    """Remember a memory."""
    event_store = EventStore()
    memory_store = MemoryStore()
    remember_api = RememberAPI(event_store, memory_store)

    event = EventEnvelope(
        source_tool=tool,
        scope=Scope(
            user=user,
            workspace=workspace,
            project=project,
            session=session,
        ),
        event_type=EventType.DECISION,
        payload={
            "content": content,
            "summary": content[:100],
            "keywords": content.split()[:5],
        },
    )

    event_id = remember_api.remember(event)
    click.echo(f"Remembered: {event_id}")

    event_store.close()
    memory_store.close()


@cli.command()
@click.option("--user", default="default", help="User ID")
@click.option("--workspace", help="Workspace ID")
@click.option("--project", help="Project ID")
@click.option("--session", help="Session ID")
@click.option("--limit", default=10, help="Max results")
@click.option("--format", default="friendly", help="Output format: friendly, json")
@click.argument("query")
def recall(user, workspace, project, session, limit, format, query):
    """Recall memories with cross-host provenance display."""
    memory_store = MemoryStore()
    event_store = EventStore()
    recall_api = RecallAPI(memory_store, event_store)

    context = {
        "user": user,
        "workspace": workspace,
        "project": project,
        "session": session,
        "limit": limit,
    }

    result = recall_api.recall(query, context)

    # Use enhanced to_dict() which includes source info
    result_dict = result.to_dict()

    if not result.memories:
        click.echo("No memories found.")
    else:
        if format == "json":
            click.echo(json.dumps(result_dict, indent=2, default=str))
        else:
            # Friendly format with provenance
            click.echo(f"Found {len(result.memories)} memories:")

            # Group by source for cleaner display
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
                        # Format timestamp nicely
                        try:
                            from datetime import datetime
                            if isinstance(ts, str):
                                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                                ts = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            pass
                    click.echo(f"  • \"{mem.get('content', mem.get('summary', ''))[:100]}\" ({ts})" if ts else f"  • \"{mem.get('content', mem.get('summary', ''))[:100]}\"")

            # Show conflict warning if detected
            if result_dict.get("conflict_detected"):
                candidates = result_dict.get("candidates", [])
                click.echo("\n⚠️ CONFLICT DETECTED")
                click.echo(f"  {len(candidates)} conflicting versions found:")
                for c in candidates:
                    click.echo(f"  - [{c.get('source_host_friendly', 'Unknown')}] \"{c.get('content', '')[:60]}\"")

    memory_store.close()
    event_store.close()


@cli.command()
@click.argument("memory_id")
def expand(memory_id):
    """Expand memory to full details."""
    memory_store = MemoryStore()
    event_store = EventStore()
    recall_api = RecallAPI(memory_store, event_store)

    memory = recall_api.expand(memory_id)

    if memory:
        click.echo(json.dumps(memory.to_dict(), indent=2))
    else:
        click.echo("Memory not found.")

    memory_store.close()
    event_store.close()


@cli.command()
@click.argument("memory_id")
@click.option("--format", default="friendly", help="Output format: friendly, json")
def explain(memory_id, format):
    """Explain why a memory was recalled with provenance and match reasons."""
    memory_store = MemoryStore()
    event_store = EventStore()
    recall_api = RecallAPI(memory_store, event_store)

    explanation = recall_api.explain(memory_id)

    if not explanation.get("success"):
        click.echo(f"Error: {explanation.get('error', 'Unknown')}")
    else:
        if format == "json":
            click.echo(json.dumps(explanation, indent=2, default=str))
        else:
            # Friendly format with provenance and match reasons
            click.echo("## Memory Explanation")

            # Source and provenance
            click.echo(f"\nSource: {explanation.get('source_host_friendly', 'Unknown')}")
            ts = explanation.get("event_timestamp", "")
            if ts:
                try:
                    from datetime import datetime
                    if isinstance(ts, str):
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        ts = dt.strftime("%Y-%m-%d %H:%M")
                    click.echo(f"Timestamp: {ts}")
                except:
                    click.echo(f"Timestamp: {ts}")

            # Match reasons
            match_reasons = explanation.get("match_reasons", [])
            if match_reasons:
                click.echo("\nMatch Reasons:")
                for mr in match_reasons:
                    if mr["type"] == "keyword":
                        click.echo(f"  • Keyword match: {', '.join(mr.get('matched', []))}")
                    elif mr["type"] == "scope":
                        for k, v in mr.get("matched", {}).items():
                            click.echo(f"  • Scope match: {k}={v}")

            # Also written by (cross-host context)
            also_written_by = explanation.get("also_written_by", [])
            if also_written_by:
                click.echo(f"\nAlso written by: {', '.join(also_written_by)}")

            # Human-readable explain text
            if explanation.get("explain"):
                click.echo(f"\n{explanation.get('explain')}")

            # Content preview
            mem = explanation.get("memory", {})
            content = mem.get("content", mem.get("summary", ""))
            if content:
                click.echo(f"\nContent: \"{content[:200]}\"")

    memory_store.close()
    event_store.close()


@cli.command()
def stats():
    """Show memory statistics."""
    event_store = EventStore()
    memory_store = MemoryStore()

    event_count = event_store.count()
    memory_count = memory_store.count()

    click.echo(f"Events: {event_count}")
    click.echo(f"Memory Objects: {memory_count}")

    event_store.close()
    memory_store.close()


if __name__ == "__main__":
    cli()
