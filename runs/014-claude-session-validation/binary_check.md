# OCMF Binary Check Evidence

**Run ID**: 014-claude-session-validation
**Date**: 2026-03-12

---

## Binary Verification

### Claude

```
$ which claude
/Users/caihongwei/.local/bin/claude
EXIT: 0

$ claude --version
2.1.72 (Claude Code)
EXIT: 0
```

**Status**: ✅ AVAILABLE

### Codex

```
$ which codex
codex not found (not in PATH)

$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.115.0-alpha.4
EXIT: 0
```

**Status**: ✅ AVAILABLE (via App bundle)

### OpenClaw

```
$ which openclaw
openclaw not found
EXIT: 1
```

**Status**: ❌ BLOCKED

---

## MCP Configuration

### MCP Config File

```
$ cat /tmp/ocmf_mcp.json
{
  "mcpServers": {
    "ocmf": {
      "command": "python3",
      "args": ["-m", "ocmaf.bridge.mcp_server", "--tool", "claude-code"]
    }
  }
}
```

### Claude --mcp-config Test

```
$ unset CLAUDECODE
$ claude --mcp-config /tmp/ocmf_mcp.json --version
2.1.72 (Claude Code)
EXIT: 0
```

**Status**: ✅ Claude can start with MCP config

---

**Generated**: 2026-03-12
