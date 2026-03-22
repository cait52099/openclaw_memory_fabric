"""Minimal OCMF MCP Server for Real Host Bridge."""
import json
import sys
from pathlib import Path
from typing import Any, Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ocmaf.sdk import MemorySession
from ocmaf.event.envelope import EventEnvelope
from ocmaf.event.scope import Scope
from ocmaf.event.types import EventType


class OCMFMCP:
    """Minimal OCMF MCP Server."""

    def __init__(self, tool_name: str = "unknown"):
        """Initialize MCP server."""
        self.tool_name = tool_name
        self.session = None
        self.db_path = Path("/tmp/ocmf_bridge_test.db")

    def _get_session(self) -> MemorySession:
        """Get or create memory session."""
        if self.session is None:
            self.session = MemorySession(
                user="default",
                workspace="default",
                project="bridge-test",
                session="mcp-bridge",
                tool=self.tool_name,
                db_path=self.db_path,
            )
        return self.session

    def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tool call."""
        if tool_name == "ocmf_recall":
            return self._recall(arguments)
        elif tool_name == "ocmf_remember":
            return self._remember(arguments)
        elif tool_name == "ocmf_get_injection":
            return self._get_injection(arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _recall(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Recall memories."""
        query = args.get("query", "")
        session = self._get_session()
        result = session.recall(query)

        # Return structured results
        memories = []
        for mem in result.memories:
            memories.append({
                "memory_id": mem.memory_id,
                "title": mem.title,
                "summary": mem.summary,
                "content": mem.content[:500] if mem.content else "",
                "state": str(mem.state),
            })

        return {
            "success": True,
            "query": query,
            "count": len(memories),
            "memories": memories,
            "traces": result.traces,
        }

    def _remember(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Remember an event."""
        content = args.get("content", "")
        event_type = args.get("event_type", "chat_turn")

        session = self._get_session()

        # Map event type
        type_map = {
            "chat_turn": EventType.CHAT_TURN,
            "task_result": EventType.TASK_RESULT,
            "decision": EventType.DECISION,
        }
        evt_type = type_map.get(event_type, EventType.CHAT_TURN)

        # Create scope
        scope = Scope(
            user="default",
            workspace="default",
            project="bridge-test",
            session="mcp-bridge",
            tool=self.tool_name,
        )

        # Create event envelope with all required fields
        envelope = EventEnvelope(
            source_tool=self.tool_name,
            scope=scope,
            event_type=evt_type,
            payload={
                "content": content,
                "source": "mcp-bridge",
            },
        )

        event_id = session.remember(envelope)

        return {
            "success": True,
            "event_id": event_id,
            "tool": self.tool_name,
        }

    def _get_injection(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get injection text."""
        query = args.get("query", "")
        session = self._get_session()
        injection = session.get_injection_text(query)

        return {
            "success": True,
            "query": query,
            "injection": injection,
        }


def main():
    """Main entry point for MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="OCMF MCP Server")
    parser.add_argument("--tool", default="unknown", help="Tool name (claude-code, codex-cli)")
    args = parser.parse_args()

    mcp = OCMFMCP(tool_name=args.tool)

    # Simple JSON-RPC like protocol for stdio
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())

            # Handle initialize request
            if request.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "ocmf-mcp",
                            "version": "0.1.0"
                        }
                    }
                }
                print(json.dumps(response), flush=True)
                continue

            # Handle tools/list request (for tool discovery)
            if request.get("method") == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "ocmf_recall",
                                "description": "Recall relevant memories from OCMF",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "Search query for memories"
                                        }
                                    },
                                    "required": ["query"]
                                }
                            },
                            {
                                "name": "ocmf_remember",
                                "description": "Store an event into OCMF memory",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "content": {
                                            "type": "string",
                                            "description": "Content to remember"
                                        },
                                        "event_type": {
                                            "type": "string",
                                            "description": "Type of event (chat_turn, task_result, decision)",
                                            "enum": ["chat_turn", "task_result", "decision"]
                                        }
                                    },
                                    "required": ["content"]
                                }
                            },
                            {
                                "name": "ocmf_get_injection",
                                "description": "Get injection text for LLM context",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "Query to get relevant context"
                                        }
                                    },
                                    "required": ["query"]
                                }
                            }
                        ]
                    }
                }
                print(json.dumps(response), flush=True)
                continue

            # Handle tool call
            if request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name", "")
                arguments = request.get("params", {}).get("arguments", {})

                result = mcp.handle_tool_call(tool_name, arguments)

                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
                print(json.dumps(response), flush=True)
                continue

            # Handle ping
            if request.get("method") == "ping":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {}
                }
                print(json.dumps(response), flush=True)
                continue

        except json.JSONDecodeError:
            break
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response), flush=True)
            break


if __name__ == "__main__":
    main()
