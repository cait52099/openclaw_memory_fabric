# OCMF Binary Check Evidence

**Run ID**: 017-mcp-tool-discovery-fix
**Date**: 2026-03-19

---

## Claude Code

```
$ which claude
/Users/caihongwei/.local/bin/claude

$ claude --version
2.1.72 (Claude Code)
```

**Status**: ✅ AVAILABLE

---

## Codex CLI

```
$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.115.0-alpha.4
```

**Status**: ✅ AVAILABLE (via App bundle)

---

## OpenClaw

```
$ which openclaw
openclaw not found
```

**Status**: ❌ BLOCKED

---

## MCP Config

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

---

**Generated**: 2026-03-19
