# Multi-Host Switching UX Report

**Run ID**: 036-user-journey-trusted
**Date**: 2026-03-22
**Status**: PASS

---

## Executive Summary

Multi-host switching works correctly. Claude ↔ Codex switching changes OCMF_SOURCE_TOOL appropriately, and cross-host memory sharing is functional.

---

## Test Results

| Test | Status | Notes |
|------|--------|-------|
| Claude → Codex switch | ✓ PASS | Config changes to codex-cli |
| Codex → Claude switch | ✓ PASS | Config changes to claude-code |
| Cross-host recall | ✓ PASS | Memories visible across hosts |

---

## Key Findings

1. **Config overwrites on switch**: Running `install --host X` overwrites `~/.ocmf/config.sh` with new OCMF_SOURCE_TOOL
2. **Memory persists**: Shared `~/.ocmf/memory.db` means memories survive host switches
3. **Source attribution correct**: After switch, new memories show correct host, old memories retain original attribution

---

## Switching Flow

```
Claude → Codex:    install --host codex → OCMF_SOURCE_TOOL=codex-cli
Codex → Claude:    install --host claude → OCMF_SOURCE_TOOL=claude-code
```

---

## Product Polish Priorities

| Priority | Item | Impact | Effort |
|----------|------|--------|--------|
| P1 | Wrapper script for PYTHONPATH | High | Low |
| P2 | Config switch warning | Medium | Low |
| P3 | Host-specific config files | Medium | Medium |

---

## Verdict

**PASS** - Multi-host switching UX is working as designed.
