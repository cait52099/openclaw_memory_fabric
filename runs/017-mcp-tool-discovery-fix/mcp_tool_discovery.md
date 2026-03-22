# OCMF MCP Tool Discovery Fix Evidence

**Run ID**: 017-mcp-tool-discovery-fix
**Date**: 2026-03-19

---

## Issue Identified

The original MCP server was not properly exposing tools to Claude Code:
- `capabilities` field format was incorrect
- `tools/list` method was not implemented

---

## Fix Applied

### Changes to `src/ocmaf/bridge/mcp_server.py`:

1. Fixed `capabilities` format to use `{"tools": {}}`
2. Added `tools/list` method implementation that returns:
   - ocmf_recall
   - ocmf_remember
   - ocmf_get_injection

---

## Test Results

### 1. Initialize Response

```
$ echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | \
PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool claude-code

{"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "ocmf-mcp", "version": "0.1.0"}}}
```

### 2. Tools List Response

```
$ echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | \
PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool claude-code

{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "ocmf_recall",
        "description": "Recall relevant memories from OCMF",
        "inputSchema": {...}
      },
      {
        "name": "ocmf_remember",
        "description": "Store an event into OCMF memory",
        "inputSchema": {...}
      },
      {
        "name": "ocmf_get_injection",
        "description": "Get injection text for LLM context",
        "inputSchema": {...}
      }
    ]
  }
}
```

### 3. Tool Call Test

```
$ echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"ocmf_remember","arguments":{"content":"Test from fixed MCP server"}}}' | \
PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool claude-code

{
  "success": true,
  "event_id": "352df94f-645a-4a08-986b-b8d6202c403f",
  "tool": "claude-code"
}
```

### 4. SQLite Verification

```
$ sqlite3 /tmp/ocmf_bridge_test.db "SELECT event_id, source_tool, payload_json FROM events WHERE event_id='352df94f-645a-4a08-986b-b8d6202c403f';"

352df94f-645a-4a08-986b-b8d6202c403f|claude-code|{"content": "Test from fixed MCP server", "source": "mcp-bridge"}
```

---

## Status

| Check | Status |
|-------|--------|
| MCP server fix | ✅ Complete |
| tools/list implementation | ✅ Working |
| Tool call test | ✅ Success |
| SQLite verification | ✅ Verified |

---

**MCP_TOOL_DISCOVERY_STATUS**: ✅ FIXED

---

**Generated**: 2026-03-19
