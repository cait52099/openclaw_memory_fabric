# OCMF source_tool Display Specification

**Run ID**: 024-openclaw-closure-crosshost-ux
**Date**: 2026-03-22
**Status**: FINAL
**Task**: T-6C-02

---

## source_tool Values

| source_tool | Friendly Name | Host Type | Notes |
|-------------|---------------|-----------|-------|
| claude-code | Claude | Desktop App | Claude Code |
| codex-cli | Codex | CLI | Codex CLI |
| openclaw | OpenClaw | Desktop App | OpenClaw (when available) |
| synthetic | Synthetic | Test | Direct module calls, not real host |

---

## Display Rules

1. **Always show friendly name** alongside source_tool
2. **Group by source** when multiple memories from same host
3. **Indicate "Synthetic" clearly** so users know it's test data
4. **Never show raw source_tool** without friendly mapping

---

## Mapping Table

```python
FRIENDLY_NAMES = {
    "claude-code": "Claude",
    "codex-cli": "Codex",
    "openclaw": "OpenClaw",
    "synthetic": "Synthetic (Test)"
}
```

---

**AC-XHOST-002**: ✅ SPECIFIED
