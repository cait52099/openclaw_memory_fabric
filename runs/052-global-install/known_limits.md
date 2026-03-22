# OCMF Phase 052 Known Limits - Global Install

**Run ID**: 052-global-install
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## FINAL STATUS: PASS

## GLOBAL_INSTALL_WORKS: YES
## TRUSTED_USER_JOURNEY: PRESERVED (from phases 035-050)

---

## HONEST BOUNDARY STATEMENT

**CURRENT_ENV_STABLE: YES**
**ROOT_CAUSE_IDENTIFIED: NO** (unchanged from phases 035-050)

The global install polish addresses the need to run from any directory but does NOT claim to fix any root cause.

---

## GLOBAL INSTALL ACHIEVED

### Changes Made

| File | Change |
|------|--------|
| `pyproject.toml` | Fixed dependencies (removed sqlite3 stdlib), fixed entry point to unified |
| `src/ocmaf/cli/unified.py` | Added `_auto_source_config()` for automatic config sourcing |

### New Usage

```bash
# Install globally (editable)
pip install -e /path/to/openclaw_memory_fabric

# Use from ANY directory
ocmaf install --host claude
ocmaf remember --content "..."
ocmaf recall --query "..."

# For Codex
ocmaf install --host codex
```

### What Works

| Feature | Status |
|---------|--------|
| `ocmaf` global command | ✓ Works from any directory |
| No PYTHONPATH needed | ✓ Automatic |
| No manual source needed | ✓ Auto-source implemented |
| Claude attribution | ✓ Source: Claude / From Claude |
| Codex attribution | ✓ Source: Codex / From Codex |
| Cross-host memory | ✓ Works |

---

## REMAINING FRICTIONS (NOT BLOCKERS)

### MEDIUM Severity

| ID | Friction | Workaround |
|----|----------|------------|
| F-001 | Claude restart required | Restart after install |
| F-002 | Config overwrites on switch | Document as expected behavior |
| F-003 | Codex no auto-memory | By design |

### NOT ADDRESSED (Out of Scope)

| Item | Reason |
|------|--------|
| OpenClaw unblock | GitHub release unavailable |
| Semantic conflict detection | Would need embeddings |
| User conflict resolution UI | UI layer |

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |
| Root cause of identity drift | N/A | Not identified |

---

## SUMMARY

### TRUSTED (in current environment)
- ✓ Claude clean-home first-use (phases 035-050)
- ✓ Codex clean-home first-use (phases 035-050)
- ✓ Claude ↔ Codex switching (phases 039-050)
- ✓ Source attribution correct
- ✓ Cross-host memory sharing

### PRODUCT POLISH (phases 051-052)
- ✓ Repo-local wrapper (phase 051)
- ✓ Global install (phase 052) - THIS RUN

### NOT YET ADDRESSED
- OpenClaw integration (blocked)
- Semantic conflict detection
- User conflict resolution UI

---

**Phase 052 COMPLETE**
**Global Install: ACHIEVED**
**Trusted User Journey: PRESERVED**
