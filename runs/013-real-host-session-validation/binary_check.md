# OCMF Phase 4G-2 Binary Check Evidence

**Run ID**: 013-real-host-session-validation
**Date**: 2026-03-12

---

## A. Binary / Environment Checklist

### RH001: which claude

```
$ which claude
/Users/caihongwei/.local/bin/claude
EXIT_CODE: 0
```

### RH002: claude --version

```
$ claude --version
2.1.72 (Claude Code)
EXIT_CODE: 0
```

### RH003: which codex

```
$ which codex
codex not found (not in PATH)

$ ls -la /Applications/Codex.app/Contents/Resources/codex
-rwxr-xr-x@ 1 caihongwei  staff  104331712  3 12 07:02 /Applications/Codex.app/Contents/Resources/codex
EXIT_CODE: 0
```

### RH004: codex --version

```
$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.115.0-alpha.4
EXIT_CODE: 0
```

### RH005: which openclaw

```
$ which openclaw
openclaw not found
EXIT_CODE: 1
```

### RH006: Summary

| Tool | Path | Version | Status |
|------|------|---------|--------|
| Claude | /Users/caihongwei/.local/bin/claude | 2.1.72 | ✅ AVAILABLE |
| Codex | /Applications/Codex.app/.../codex | 0.115.0-alpha.4 | ✅ AVAILABLE |
| OpenClaw | not found | N/A | ❌ BLOCKED |

---

**Checklist Status**:
- RH001: ✅ PASS
- RH002: ✅ PASS
- RH003: ✅ PASS
- RH004: ✅ PASS
- RH005: ✅ PASS (recorded as BLOCKED)
- RH006: ✅ PASS

---

**Generated**: 2026-03-12
