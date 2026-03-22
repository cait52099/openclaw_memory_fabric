# OCMF Phase 4F Binary Check

**Run ID**: 009-real-host-evidence-repair
**Date**: 2026-03-12
**Phase**: 4F - Strict Real Host Evidence Repair

---

## Binary Detection Results

### Claude Code

```bash
$ which claude
/Users/caihongwei/.local/bin/claude
---EXIT_CODE: 0
```

```bash
$ claude --version
2.1.72 (Claude Code)
---EXIT_CODE: 0
```

**Status**: ✅ BINARY_AVAILABLE
**Version**: 2.1.72

---

### Codex CLI

```bash
$ which codex
codex not found
---EXIT_CODE: 1
```

**Status**: ❌ NOT_FOUND

---

### OpenClaw

```bash
$ which openclaw
openclaw not found
---EXIT_CODE: 1
```

**Status**: ❌ NOT_FOUND

---

## Summary

| Binary | Path | Exit Code | Status |
|--------|------|-----------|--------|
| claude | /Users/caihongwei/.local/bin/claude | 0 | ✅ AVAILABLE |
| codex | - | 1 | ❌ NOT_FOUND |
| openclaw | - | 1 | ❌ NOT_FOUND |

---

**Last Updated**: 2026-03-12
