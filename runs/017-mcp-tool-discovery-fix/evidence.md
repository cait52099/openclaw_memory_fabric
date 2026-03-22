# OCMF MCP Tool Discovery Fix Evidence

**Run ID**: 017-mcp-tool-discovery-fix
**Date**: 2026-03-19

---

## Executive Summary

Fixed the MCP server to properly expose tools via `tools/list` method.

**Key Findings**:
- MCP server: ✅ Fixed
- tools/list: ✅ Returns 3 tools
- Direct tool call: ✅ Works
- SQLite verification: ✅ Verified

---

## Binary Environment

| Tool | Status |
|------|--------|
| Claude | ✅ /Users/caihongwei/.local/bin/claude |
| Codex | ✅ /Applications/Codex.app/.../codex |
| OpenClaw | ❌ BLOCKED |

---

## MCP Server Fix

### Before
- `capabilities` had wrong format
- No `tools/list` implementation

### After
- `capabilities`: `{"tools": {}}`
- `tools/list` returns ocmf_recall, ocmf_remember, ocmf_get_injection

---

## Verification

### Direct MCP Call Test

```
$ echo '{"method":"tools/call",...}' | python3 -m ocmaf.bridge.mcp_server --tool claude-code

{
  "success": true,
  "event_id": "352df94f-645a-4a08-986b-b8d6202c403f",
  "tool": "claude-code"
}
```

### SQLite

```
$ sqlite3 /tmp/ocmf_bridge_test.db "SELECT * FROM events WHERE event_id='352df94f-645a-4a08-986b-b8d6202c403f';"

352df94f-645a-4a08-986b-b8d6202c403f|claude-code|{"content": "Test from fixed MCP server", "source": "mcp-bridge"}
```

---

## Next Step

User needs to test in actual Claude session:
1. `claude --mcp-config /tmp/ocmf_mcp.json`
2. `/mcp` - verify tools visible
3. Call a tool via natural language
4. Verify SQLite record

---

## FINAL STATUS

| Metric | Status |
|--------|--------|
| **FINAL_STATUS** | ⏳ AWAITING_SESSION_TEST |
| **MCP_TOOL_DISCOVERY** | ✅ FIXED |
| **CLAUDE_MCP_TOOLS_VISIBLE** | ⏳ NEEDS_SESSION_TEST |
| **CLAUDE_REAL_TOOL_CALL** | ⏳ NEEDS_SESSION_TEST |

---

**Generated**: 2026-03-19
