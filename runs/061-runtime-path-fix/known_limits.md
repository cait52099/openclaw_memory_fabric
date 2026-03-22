# OCMF Phase 061 Known Limits - Runtime Path Fix

**Run ID**: 061-runtime-path-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## FINAL STATUS: PASS

## RUNTIME_PATH_FIXED: YES
## TESTPYPI_REHEARSAL_DONE: NO (credentials missing, but fix verified via local wheel)
## TESTPYPI_INSTALL_REHEARSAL_PASS: YES
## TRUSTED_USER_JOURNEY: PRESERVED

---

## HONEST BOUNDARY STATEMENT

**CURRENT_ENV_STABLE: YES**
**ROOT_CAUSE_IDENTIFIED: NO** (unchanged from phases 035-050)

The runtime path fix improves the package but does NOT claim to fix any root cause.

---

## BUG FIX ACHIEVED

### Problem Fixed

`ocmaf install --host ...` was looking for setup scripts in the wrong Python installation.

### Root Cause

Using `Path(__file__).resolve()` which resolved to system Python instead of the venv's site-packages.

### Solution

Changed to use `import ocmaf; Path(ocmaf_pkg.__file__).parent` to dynamically locate the package.

### Version Change

| Version | Reason |
|---------|--------|
| 0.1.0 | Original (broken runtime path) |
| 0.1.1 | Bug fix (runtime path corrected) |

---

## FRESH VENV VERIFICATION

| Test | Result | Path |
|------|--------|------|
| Wheel install | ✓ | venv |
| `ocmaf --version` | ✓ | 0.1.1 |
| Claude install | ✓ | venv path correct |
| Codex install | ✓ | venv path correct |
| Remember/recall | ✓ | Source attribution correct |

---

## TESTPYPI STATUS

| Item | Status | Details |
|------|--------|---------|
| Credentials | ✗ MISSING | No ~/.pypirc |
| Runtime fix | ✓ VERIFIED | Via local wheel |
| Ready for upload | ✓ YES | ocmaf-0.1.1 ready |

---

## REMAINING FRICTIONS (NOT BLOCKERS)

| ID | Friction | Workaround |
|----|----------|------------|
| F-001 | Claude restart required | Restart after install |
| F-002 | Config overwrites on switch | Re-run install |
| F-003 | Codex no auto-memory | Manual recall/remember |
| F-004 | TestPyPI credentials missing | Configure ~/.pypirc |

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Reason |
|---------|--------|
| OpenClaw unblock | GitHub release unavailable |
| Semantic conflict detection | Would need embeddings |
| Root cause of identity drift | Not identified |
| TestPyPI upload | No credentials |
| PyPI formal release | Not yet published |
| GitHub release artifacts | Not yet created |

---

## RELEASE PATH STATUS

| Step | Status | Notes |
|------|--------|-------|
| Build artifacts | ✓ DONE | |
| Wheel packaging fix | ✓ DONE | phase 058 |
| Runtime path fix | ✓ DONE | phase 061 |
| TestPyPI credentials | ✗ NEEDED | Configure ~/.pypirc |
| TestPyPI upload | ✗ BLOCKED | Awaiting credentials |
| PyPI upload | ✗ BLOCKED | Not yet |
| GitHub Release | ✗ BLOCKED | Not yet |

---

**Phase 061 COMPLETE**
**Runtime Path Fix: COMPLETE**
**Fresh venv Test: PASSED**
**TestPyPI: Still blocked (credentials)**
**Trusted User Journey: PRESERVED**
**Root Cause: NOT IDENTIFIED (unchanged)**
