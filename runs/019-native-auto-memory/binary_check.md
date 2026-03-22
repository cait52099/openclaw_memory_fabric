# OCMF Binary Check Evidence

**Run ID**: 019-native-auto-memory
**Date**: 2026-03-19

---

## Claude Code

```
$ which claude
/Users/caihongwei/.local/bin/claude

$ claude --version
2.1.78 (Claude Code)
```

**Status**: ✅ AVAILABLE

---

## Claude Capabilities for Auto-Memory

| Capability | Flag | Status |
|------------|------|--------|
| System Prompt | `--system-prompt` | ✅ Available |
| Append System Prompt | `--append-system-prompt` | ✅ Available |
| MCP Config | `--mcp-config` | ✅ Available |
| Custom Agents | `--agents` | ✅ Available |

---

## Codex CLI

```
$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.116.0-alpha.1
```

**Status**: ✅ Available (via App bundle)

---

## OpenClaw

```
$ which openclaw
openclaw not found
```

**Status**: ❌ BLOCKED (not installed)

---

## MCP Config

```
$ cat /tmp/ocmf_mcp.json
{
  "mcpServers": {
    "ocmf": {
      "command": "python3",
      "args": ["-m", "ocmaf.bridge.mcp_server", "--tool", "claude-code"],
      "env": {
        "PYTHONPATH": "/Users/caihongwei/project/openclaw_memory_fabric/src"
      }
    }
  }
}
```

---

## Auto-Memory System Prompt

Location: `runs/019-native-auto-memory/auto_memory_system_prompt.md`

**Status**: ✅ Created

---

**Generated**: 2026-03-19
