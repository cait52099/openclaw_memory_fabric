# OCMF Phase 4G Binary Check Evidence

**Run ID**: 012-real-host-bridge-validation
**Date**: 2026-03-12

---

## Claude Code

```
$ which claude
/Users/caihongwei/.local/bin/claude
EXIT_CODE: 0

$ claude --version
2.1.72 (Claude Code)
EXIT_CODE: 0
```

**MCP Support**:
```
$ claude --help | grep mcp-config
  --mcp-config <configs...>  Load MCP servers from JSON files or strings
```

**Status**: ✅ BINARY_AVAILABLE + MCP_SUPPORTED

---

## Codex CLI

```
$ which codex
codex not found (not in PATH)
EXIT_CODE: 1

$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.115.0-alpha.4
EXIT_CODE: 0
```

**MCP Support**:
```
$ /Applications/Codex.app/Contents/Resources/codex mcp --help
Commands: list, get, add, remove

$ /Applications/Codex.app/Contents/Resources/codex mcp list
No MCP servers configured yet.
```

**After adding OCMF MCP**:
```
$ /Applications/Codex.app/Contents/Resources/codex mcp list
Name  Command  Args                                         Env  Cwd  Status   Auth
ocmf  python3  -m ocmaf.bridge.mcp_server --tool codex-cli  -    -    enabled  Unsupported
```

**Status**: ✅ AVAILABLE (via App bundle at /Applications/Codex.app/Contents/Resources/codex) + MCP_SUPPORTED

---

## OpenClaw

```
$ which openclaw
openclaw not found
EXIT_CODE: 1
```

**Status**: ❌ NOT_FOUND (BLOCKED)

---

## Summary

| Tool | Binary Path | MCP Support | Status |
|------|-------------|-------------|--------|
| Claude Code | /Users/caihongwei/.local/bin/claude | ✅ --mcp-config | AVAILABLE |
| Codex CLI | /Applications/Codex.app/.../codex | ✅ mcp add/list | AVAILABLE |
| OpenClaw | not found | N/A | BLOCKED |

---

**Generated**: 2026-03-12
