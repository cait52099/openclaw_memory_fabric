# OCMF Phase 4F Binary Check - STRICT

**Run ID**: 011-minimal-real-host-bridge
**Date**: 2026-03-12
**Phase**: 4F - Minimal Real Host Bridge

---

## Binary Detection - Machine Facts

### Claude Code

```bash
$ which claude
/Users/caihongwei/.local/bin/claude
EXIT_CODE: 0
```

```bash
$ claude --version
2.1.72 (Claude Code)
EXIT_CODE: 0
```

```bash
$ claude --help 2>&1 | grep -i mcp
      --mcp-config <configs...>                         Load MCP servers from JSON files or strings (space-separated)
      --strict-mcp-config                               Only use MCP servers from --mcp-config
      mcp                                               Configure and manage MCP servers
```

**Status**: ✅ BINARY_AVAILABLE
**Version**: 2.1.72
**MCP Support**: ✅ YES (--mcp-config available)

---

### Codex CLI

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
**MCP Support**: ✅ YES (mcp-server available)

---

### OpenClaw

```bash
$ which openclaw
openclaw not found
EXIT_CODE: 1
```

**Status**: ❌ NOT_FOUND

---

## Summary Table

| Binary | Path | Exit Code | Status | MCP Support |
|--------|------|-----------|--------|-------------|
| claude | /Users/caihongwei/.local/bin/claude | 0 | ✅ AVAILABLE | ✅ YES |
| codex | /Applications/Codex.app/Contents/Resources/codex | 0 | ✅ AVAILABLE | ✅ YES |
| openclaw | - | 1 | ❌ NOT_FOUND | N/A |

---

## Bridge Mechanism Analysis

### Claude Bridge Option

- **MCP Config**: `--mcp-config <json>`
- **MCP Available**: ✅ YES
- **Bridge Path**: Implement MCP server → Configure --mcp-config

### Codex Bridge Option

- **MCP Config**: Codex has `mcp-server` command
- **MCP Available**: ✅ YES
- **Bridge Path**: Run as MCP server or implement wrapper

---

**Last Updated**: 2026-03-12
