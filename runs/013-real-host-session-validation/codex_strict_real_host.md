# OCMF Phase 4G-2 Codex Real Host Session Evidence

**Run ID**: 013-real-host-session-validation
**Date**: 2026-03-12

---

## C. Codex Real Host Session Checklist

### RH014: codex mcp list

```
$ /Applications/Codex.app/Contents/Resources/codex mcp list
Name  Command  Args                                         Env  Cwd  Status   Auth
ocmf  python3  -m ocmaf.bridge.mcp_server --tool codex-cli  -    -    enabled  Unsupported
EXIT_CODE: 0
```

**Status**: ✅ PASS - MCP server already added from previous run

---

### RH015-RH020: Codex Session remember/recall

**Status**: ⚠️ NEEDS HUMAN INTERACTION - MCP HANDSHAKE ISSUE

The MCP server was added successfully, but when Codex tries to connect, the handshaking fails:

```
mcp: ocmf failed: MCP client for `ocmf` failed to start: MCP startup failed: handshaking with MCP server failed: connection closed: initialize response
```

This appears to be a protocol compatibility issue between Codex's MCP client and our MCP server implementation.

#### Investigation

Direct MCP server invocation works:
```
$ echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}' | python3 -m ocmaf.bridge.mcp_server --tool codex-cli
{"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion":"2024-11-05",...}}
```

But Codex cannot establish connection.

#### Human Interaction Options

**Option 1**: Try Codex interactive session
```bash
# In interactive Codex session, try to use ocmf_remember tool
```

**Option 2**: Wait for MCP protocol fix
The MCP server implementation may need updates to be compatible with Codex's MCP client.

---

### Direct MCP Invocation (Baseline Reference)

For reference, the MCP server component works correctly with codex-cli tool:

```
$ export PYTHONPATH=/Users/caihongwei/project/openclaw_memory_fabric/src

$ echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ocmf_remember","arguments":{"content":"Direct MCP test for Codex reference"}}}' | \
python3 -m ocmaf.bridge.mcp_server --tool codex-cli

{
  "success": true,
  "event_id": "ref-codex-001",
  "tool": "codex-cli"
}
```

---

## Checklist Status Summary

| Check | Status |
|-------|--------|
| RH014 | ✅ PASS |
| RH015 | ⚠️ NEEDS HUMAN |
| RH016 | ⚠️ NEEDS HUMAN |
| RH017 | ⚠️ NEEDS HUMAN |
| RH018 | ⚠️ NEEDS HUMAN |
| RH019 | ⚠️ NEEDS HUMAN |
| RH020 | ⚠️ NEEDS HUMAN |

---

## Issue Details

**Root Cause**: Codex MCP client fails to handshake with OCMF MCP server
**Error**: `handshaking with MCP server failed: connection closed: initialize response`
**Impact**: Cannot complete RH015-RH020 without fixing MCP protocol compatibility

---

**CODEX_REAL_HOST_STATUS**: ⚠️ MCP_ADD_SUCCESS - HANDSHAKE_FAILED

---

**Generated**: 2026-03-12
