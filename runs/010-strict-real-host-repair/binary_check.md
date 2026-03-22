# OCMF Phase 4F Binary Check - STRICT

**Run ID**: 010-strict-real-host-repair
**Date**: 2026-03-12
**Phase**: 4F - Strict Real Host Evidence Repair

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

**Status**: ✅ BINARY_AVAILABLE
**Version**: 2.1.72

---

### Codex CLI

```bash
$ which codex
codex not found
EXIT_CODE: 1
```

```bash
$ codex --version
(eval):1: command not found: codex
EXIT_CODE: 127
```

**Status**: ❌ NOT_FOUND

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

| Binary | Path | Exit Code | Status |
|--------|------|-----------|--------|
| claude | /Users/caihongwei/.local/bin/claude | 0 | ✅ AVAILABLE |
| codex | - | 1 | ❌ NOT_FOUND |
| openclaw | - | 1 | ❌ NOT_FOUND |

---

## MCP Mechanism Analysis (Claude Code)

```bash
$ claude --help 2>&1 | grep -i mcp
      --mcp-config PATH    Path to MCP configuration file
```

**Finding**: Claude Code supports `--mcp-config` flag
**BUT**: Requires implementing MCP server (new feature development)

---

**Last Updated**: 2026-03-12
