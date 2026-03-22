# OCMF Phase 032 Known Limits

**Run ID**: 032-install-closure-final
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## THIS IS A PRODUCT MAINLINE TASK

**Important**: Phase 032 completes the install closure final fixes.

### What Phase 032 Delivers

- ✓ Claude config merge works
- ✓ OCMF_SOURCE_TOOL fallback works
- ✓ Quickstart uses unified install as main path

---

## CURRENTLY WORKING

### Install Closure Final

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude config merge | ✓ Fixed | Python merge into existing JSON |
| OCMF_SOURCE_TOOL fallback | ✓ Fixed | Shows "Claude"/"Codex" not "Unknown" |
| Quickstart mainline | ✓ Fixed | Uses `ocmaf unified install --host ...` |

---

## CURRENT LIMITATIONS

### 1. OpenClaw BLOCKED

**Reason**: GitHub release returns 404

**Impact**: OpenClaw users cannot use OCMF

**Resolution**: Requires OpenClaw GitHub release to become available

### 2. Codex Auto-Memory NOT Supported

**Reason**: Method C (manual MCP) doesn't support automatic triggers

**Impact**: Codex users must manually call recall/remember

**Resolution**: Would need Codex to support native hooks (Method A/B)

### 3. PYTHONPATH Required

**Reason**: OCMF not properly installed via pip

**Impact**: Need `PYTHONPATH=src` prefix for CLI commands

**Resolution**: Run `pip install -e /path/to/ocmf` to install properly

### 4. Claude MCP Requires Restart

**Reason**: MCP server needs Claude to be restarted to load new config

**Impact**: New MCP config only takes effect after Claude restart

**Resolution**: Manual step - restart Claude after install

---

## REGRESSION GATE STATUS

### Gate Protected

| Check | Status |
|-------|--------|
| recall_conflict | ✓ Protected |
| explain_crosshost | ✓ Protected |
| recall_provenance | ✓ Protected |
| injection_text | ✓ Protected |

---

## PRODUCT LINE STATUS

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 6D-6G | ✓ Complete | Cross-host UX + regression gate |
| Phase 7A | ✓ Complete | Unified entry skeleton |
| Phase 7B | ✓ Complete | Auto-memory behavior |
| Phase 7C | ✓ Complete | Install E2E + wiring fixes |
| Phase 031 | ✓ Complete | Install closure (MCP entry fix) |
| Phase 032 | ✓ Complete | Install closure final (merge + identity) |

**Next**: Product is ready for user testing.

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/032-install-closure-final/install_closure_final.md` | Detailed fix evidence |
| `runs/032-install-closure-final/evidence.md` | Full evidence report |
| `runs/032-install-closure-final/known_limits.md` | This file |

---

**Phase 032 COMPLETE**
**Install Closure Final PASS**
**Ready for User Testing**
