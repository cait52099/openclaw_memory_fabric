# OCMF Phase 4F Claude Strict Real Host Evidence

**Run ID**: 011-minimal-real-host-bridge
**Date**: 2026-03-12
**Phase**: 4F - Minimal Real Host Bridge

---

## Executive Summary

**CLAUDE_REAL_HOST**: ⚠️ BRIDGE_IMPLEMENTED (MCP Server)

Claude Code Real Host Bridge 当前状态：
- Binary: ✅ 可用 (v2.1.72)
- MCP Server: ✅ 已实现
- Bridge 配置: ⚠️ 需要 --mcp-config 配置

---

## 1. Real Claude Entry Command

```bash
$ which claude
/Users/caihongwei/.local/bin/claude
EXIT_CODE: 0

$ claude --version
2.1.72 (Claude Code)
EXIT_CODE: 0
```

**Status**: ✅ BINARY_AVAILABLE

---

## 2. MCP Bridge Implementation

### MCP Server Code

Created: `src/ocmaf/bridge/mcp_server.py`

```python
class OCMFMCP:
    def _recall(self, args):
        query = args.get("query", "")
        session = self._get_session()
        result = session.recall(query)
        return {"success": True, "memories": [...]}

    def _remember(self, args):
        content = args.get("content", "")
        envelope = EventEnvelope(...)
        event_id = session.remember(envelope)
        return {"success": True, "event_id": event_id}
```

### MCP Server Test

```bash
$ echo '{"jsonrpc":"2.0","id":1,"method":"initialize"}' | \
  PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool claude-code

{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05",...
```

**Status**: ✅ MCP_SERVER_IMPLEMENTED

---

## 3. Real Host Write Attempt

### ✅ WRITE SUCCESS

```bash
$ echo '{"method":"tools/call","params":{"name":"ocmf_remember",
  "arguments":{"content":"This is a test memory from MCP bridge"}}}' | \
  PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool claude-code

{
  "success": true,
  "event_id": "ba0b7b8c-21a3-4069-8fae-94bde1396af3",
  "tool": "claude-code"
}
```

**Database Record**:
```
$ sqlite3 /tmp/ocmf_bridge_test.db \
  "SELECT event_id, source_tool, payload_json FROM events;"

ba0b7b8c-21a3-4069-8fae-94bde1396af3|claude-code|{"content": "This is a test memory from MCP bridge", "source": "mcp-bridge"}
```

**Status**: ✅ WRITE_SUCCESS

---

## 4. Real Host Recall Attempt (Same-tool)

### ✅ RECALL SUCCESS

```bash
$ echo '{"method":"tools/call","params":{"name":"ocmf_recall",
  "arguments":{"query":"test"}}}' | \
  PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool claude-code

{
  "success": true,
  "query": "test",
  "count": 1,
  "memories": [
    {
      "memory_id": "ba0b7b8c-21a3-4069-8fae-94bde1396af3",
      "summary": "This is a test memory from MCP bridge",
      "state": "State.ACTIVE"
    }
  ]
}
```

**Status**: ✅ RECALL_SUCCESS

---

## 5. Cross-tool Isolation Test

### ✅ ISOLATION VERIFIED

**Claude writes memory**:
```
$ echo '{"method":"tools/call","params":{"name":"ocmf_remember",
  "arguments":{"content":"This memory is from CLAUDE tool"}}}' | \
  PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool claude-code

{"success": true, "event_id": "9f88434d-60f3-4d52-84bc-60fa351a0ffa", ...}
```

**Codex tries to recall**:
```bash
$ echo '{"method":"tools/call","params":{"name":"ocmf_recall",
  "arguments":{"query":"Claude"}}}' | \
  PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool codex-cli

{
  "success": true,
  "query": "Claude",
  "count": 0,
  "memories": [],
  "traces": {
    "context": {
      "tool": "codex-cli"
    }
  }
}
```

**Result**: Codex cannot recall Claude memories (as expected)

**Status**: ✅ CROSS_TOOL_ISOLATION_VERIFIED

---

## 6. Manual Adapter Invocation (NOT Real Host)

### Available but NOT Real Host

```python
# This is MANUAL adapter invocation, NOT Real Host Validation
from adapters.claude_code import ClaudeCodeAdapter
adapter = ClaudeCodeAdapter()
result = adapter.before_response(query, context)
```

**Status**: ✅ AVAILABLE

**Important**: This is MANUAL invocation, NOT Real Host Bridge Validation

---

## 7. Synthetic Test Results

```bash
$ python3 -m pytest tests/ -v
============================== 45 passed in 0.20s ==============================
```

**Status**: ✅ 45/45 PASS

---

## Strict Three-Way Distinction

| Validation Type | Claude Status | Definition |
|----------------|--------------|------------|
| Real Host Bridge | ⚠️ MCP Server Implemented | Claude via MCP config triggers OCMF |
| Manual Adapter Invocation | ✅ AVAILABLE | Direct adapter function call |
| Synthetic Test | ✅ 45/45 PASS | pytest auto execution |

---

## CLAUDE_REAL_HOST: ⚠️ BRIDGE_IMPLEMENTED

- Binary exists: ✅
- MCP support: ✅ (--mcp-config available)
- MCP server implemented: ✅
- Bridge configured: ⚠️ Requires --mcp-config setup
- Real CLI integration: ⚠️ Requires user to configure MCP

---

**Last Updated**: 2026-03-12
