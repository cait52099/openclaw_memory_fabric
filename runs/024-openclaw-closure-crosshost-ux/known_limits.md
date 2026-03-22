# OCMF Phase 6B/6C - Known Limits

**Run ID**: 024-openclaw-closure-crosshost-ux
**Date**: 2026-03-22
**Status**: OPENCLAW BLOCKED

---

## OPENCLAW KNOWN LIMITS

### Environment Blocker

| Issue | Detail | Resolution |
|-------|--------|------------|
| Download URL broken | GitHub release 404 | OpenClaw team must fix release |
| Cannot install | brew install fails | Wait for fix then retry |
| Real host proof | Blocked | Same as above |
| Method verification | Blocked | Same as above |

---

## CROSS-HOST UX SPEC KNOWN GAPS

### MVP Scope

The cross-host UX spec is complete but NOT IMPLEMENTED yet. Known gaps:

| Gap | Impact | Priority |
|-----|--------|----------|
| Provenance display not in recall output | Users can't see source | P0 |
| Conflict detection not implemented | Conflicts not caught | P0 |
| explain() doesn't return match_reason | Can't explain recall | P1 |
| Friendly name mapping not in code | Hardcoded values | P2 |

---

## SUMMARY

| Component | Status |
|-----------|--------|
| OpenClaw real host proof | ❌ BLOCKED |
| OpenClaw method boundary | ⚠️ UNKNOWN |
| OpenClaw production path | ⚠️ TBD |
| Cross-host UX spec | ✅ COMPLETE (not implemented) |
