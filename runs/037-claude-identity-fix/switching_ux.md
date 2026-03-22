# Multi-Host Switching UX Report - Phase 037

**Run ID**: 037-claude-identity-fix
**Date**: 2026-03-22
**Status**: PASS

---

## Executive Summary

Multi-host switching works correctly. Claude ↔ Codex switching changes OCMF_SOURCE_TOOL appropriately, and cross-host memory sharing is functional.

**The identity drift issue (Claude → Codex → Claude causing drift to Codex) was NOT reproducible in testing.**

---

## Test Results

| Test | Status | OCMF_SOURCE_TOOL | Source Attribution |
|------|--------|------------------|-------------------|
| Claude clean-home | ✓ PASS | `claude-code` | `Source: Claude` |
| Switch to Codex | ✓ PASS | `codex-cli` | `Source: Codex` |
| Switch back to Claude | ✓ PASS | `claude-code` | `Source: Claude` |

---

## Key Findings

1. **Config correctly overwrites on switch**: Running `install --host X` correctly overwrites `~/.ocmf/config.sh` with new OCMF_SOURCE_TOOL
2. **Memory persists across switches**: Shared `~/.ocmf/memory.db` means memories survive host switches
3. **Source attribution correct after each switch**: After each switch, new memories show the correct host

---

## Switching Flow Verified

```
install --host claude → OCMF_SOURCE_TOOL="claude-code" → Source: Claude ✓
install --host codex  → OCMF_SOURCE_TOOL="codex-cli"    → Source: Codex  ✓
install --host claude → OCMF_SOURCE_TOOL="claude-code" → Source: Claude ✓
```

---

## Issue Notes

The reported identity drift (where Claude → Codex → Claude would result in Codex identity) was NOT reproducible. Each `install --host X` command correctly sets the target identity.

---

## Verdict

**PASS** - Multi-host switching UX is working correctly in this environment.
