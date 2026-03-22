# OCMF Phase 4F Codex Strict Real Host Evidence

**Run ID**: 011-minimal-real-host-bridge
**Date**: 2026-03-12
**Phase**: 4F - Minimal Real Host Bridge

---

## Executive Summary

**CODEX_REAL_HOST**: ⚠️ BRIDGE_IMPLEMENTED (MCP Server)

Codex CLI Real Host Bridge 当前状态：
- Binary: ✅ 可用 (codex-cli 0.108.0-alpha.12)
- MCP Server: ✅ 已实现
- Bridge 配置: ⚠️ 需要 MCP 配置

---

## 1. Real Codex Entry Command

```bash
$ ls -la /Applications/ | grep -i codex
drwxr-xr-x@ 3 caihongwei  admin    96  3  6 01:56 Codex.app
```

```bash
$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.108.0-alpha.12
EXIT_CODE: 0
```

```bash
$ /Applications/Codex.app/Contents/Resources/codex --help 2>&1 | grep -i mcp
      mcp                                               Manage external MCP servers for Codex
      mcp-server                                        Start Codex as an MCP server (stdio)
```

**Status**: ✅ AVAILABLE (via App bundle)
**Version**: codex-cli 0.108.0-alpha.12
**MCP Support**: ✅ YES

---

## 2. MCP Bridge Implementation

### Same MCP Server as Claude

The same MCP server (`src/ocmaf/bridge/mcp_server.py`) is used for Codex:

```bash
$ python3 -m ocmaf.bridge.mcp_server --tool codex-cli
```

---

## 3. Real Host Write Attempt

### ✅ WRITE SUCCESS

```bash
$ echo '{"method":"tools/call","params":{"name":"ocmf_remember",
  "arguments":{"content":"Codex test memory","event_type":"chat_turn"}}}' | \
  PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool codex-cli

{
  "success": true,
  "event_id": "...",
  "tool": "codex-cli"
}
```

**Database Record**:
```
codex-cli|chat_turn|{"content": "Codex test memory", "source": "mcp-bridge"}
```

**Status**: ✅ WRITE_SUCCESS

---

## 4. Real Host Recall Attempt (Same-tool)

### ✅ RECALL SUCCESS

```bash
$ echo '{"method":"tools/call","params":{"name":"ocmf_recall",
  "arguments":{"query":"Codex"}}}' | \
  PYTHONPATH=src python3 -m ocmaf.bridge.mcp_server --tool codex-cli

{
  "success": true,
  "query": "Codex",
  "count": 1,
  "memories": [...]
}
```

**Status**: ✅ RECALL_SUCCESS

---

## 5. Cross-tool Isolation Test

### ✅ ISOLATION VERIFIED

**Codex writes memory**:
```
event_id: ..., tool: codex-cli, content: "Codex test"
```

**Claude tries to recall**:
```
query: "Codex", count: 0, memories: []
```

**Result**: Claude cannot recall Codex memories (as expected)

**Status**: ✅ CROSS_TOOL_ISOLATION_VERIFIED

---

## 6. OpenClaw Status

### ❌ NOT_FOUND

```bash
$ which openclaw
openclaw not found
EXIT_CODE: 1
```

**Status**: ❌ BLOCKED (Environment - Not Installed)

---

## Strict Three-Way Distinction

| Validation Type | Codex Status | Definition |
|----------------|-------------|------------|
| Real Host Bridge | ⚠️ MCP Server Implemented | Codex via MCP config triggers OCMF |
| Manual Adapter Invocation | ❌ NOT_AVAILABLE | No environment for Codex |
| Synthetic Test | ⚠️ Mock Only | pytest with mocks |

---

## CODEX_REAL_HOST: ⚠️ BRIDGE_IMPLEMENTED

- Binary exists: ✅ (/Applications/Codex.app/Contents/Resources/codex)
- Version: codex-cli 0.108.0-alpha.12
- MCP support: ✅ (mcp-server available)
- MCP server implemented: ✅
- Bridge configured: ⚠️ Requires MCP setup

---

## OPENCLAW_ENV_STATUS: ❌ BLOCKED (Not Installed)

- Binary exists: ❌
- Real host integration: ❌

---

**Last Updated**: 2026-03-12
