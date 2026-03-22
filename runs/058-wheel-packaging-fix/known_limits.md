# OCMF Phase 058 Known Limits - Wheel Packaging Fix

**Run ID**: 058-wheel-packaging-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## FINAL STATUS: PASS

## WHEEL_PACKAGING_FIXED: YES
## WHEEL_INSTALL_REHEARSAL_PASS: YES
## TESTPYPI_REHEARSAL_DONE: NO (blocked by credentials)
## TRUSTED_USER_JOURNEY: PRESERVED (from phases 035-050)

---

## HONEST BOUNDARY STATEMENT

**CURRENT_ENV_STABLE: YES**
**ROOT_CAUSE_IDENTIFIED: NO** (unchanged from phases 035-050)

The wheel packaging fix and rehearsal improve distribution readiness but does NOT claim to fix any root cause.

---

## PACKAGING FIX ACHIEVED

### Change Made

Added to `pyproject.toml`:

```toml
[tool.setuptools.package-data]
ocmaf = ["hosts/*.sh"]
```

### Result

Both shell scripts now included in wheel:
- `ocmaf/hosts/claude_setup.sh`
- `ocmaf/hosts/codex_setup.sh`

---

## WHEEL INSTALL REHEARSAL RESULTS

| Install Method | CLI Works | Host Setup Works | Notes |
|----------------|-----------|-------------------|-------|
| Fresh venv + wheel | ✓ | ✓ | Full functionality |

### Fresh venv Test Results

| Test | Result |
|------|--------|
| Wheel install | ✓ |
| `ocmaf --version` | ✓ |
| Claude install | ✓ |
| Claude remember/recall | ✓ |
| Codex install | ✓ |
| Codex remember/recall | ✓ |
| Cross-host recall | ✓ |

---

## TESTPYPI REHEARSAL STATUS

| Item | Status | Blocker |
|------|--------|---------|
| Credentials configured | ✗ NO | No ~/.pypirc |
| TestPyPI upload | ✗ NOT ATTEMPTED | Blocked by credentials |
| Artifacts ready for upload | ✓ YES | dist/ |

---

## REMAINING FRICTIONS (NOT BLOCKERS)

### MEDIUM Severity

| ID | Friction | Workaround |
|----|----------|------------|
| F-001 | Claude restart required | Restart after install |
| F-002 | Config overwrites on switch | Re-run install |
| F-003 | Codex no auto-memory | Manual recall/remember |

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

## FORMAL RELEASE REQUIREMENTS

| Requirement | Status | Notes |
|-------------|--------|-------|
| Build succeeds | ✓ | |
| Artifacts created | ✓ | |
| hosts/*.sh in wheel | ✓ | Fixed this phase |
| Wheel install rehearsal | ✓ | Passed in fresh venv |
| TestPyPI verified | ✗ | Blocked by credentials |
| PyPI upload | ✗ | Not done |

---

## NEXT STEPS FOR FORMAL RELEASE

1. ~~Fix wheel packaging~~ ✓ DONE
2. ~~Verify wheel install rehearsal~~ ✓ DONE
3. Configure TestPyPI credentials (if desired)
4. Upload to TestPyPI and verify
5. When ready, upload to PyPI
6. Create GitHub Release

---

**Phase 058 COMPLETE**
**Wheel Packaging Fix: COMPLETE**
**Wheel Install Rehearsal: PASSED**
**TestPyPI Rehearsal: BLOCKED (credentials)**
**Trusted User Journey: PRESERVED**
**Root Cause: NOT IDENTIFIED (unchanged)**
