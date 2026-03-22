# OCMF Phase 057 Known Limits - Build & TestPyPI Rehearsal

**Run ID**: 057-build-testpypi
**Date**: 2026-03-22
**Status**: PASS (with findings)
**Task Type**: PRODUCT POLISH

---

## FINAL STATUS: PASS

## BUILD_ARTIFACTS_CREATED: YES
## TESTPYPI_REHEARSAL_BLOCKED: YES (no credentials)
## INSTALL_REHEARSAL: PARTIAL (CLI works, host scripts missing)
## TRUSTED_USER_JOURNEY: PRESERVED (from phases 035-050)

---

## HONEST BOUNDARY STATEMENT

**CURRENT_ENV_STABLE: YES**
**ROOT_CAUSE_IDENTIFIED: NO** (unchanged from phases 035-050)

The build rehearsal documents current state but does NOT claim formal release readiness.

---

## BUILD ARTIFACTS STATUS

| Artifact | Status | Location |
|----------|--------|----------|
| Source distribution (.tar.gz) | ✓ Created | dist/ |
| Wheel (.whl) | ✓ Created | dist/ |
| twine check | ✓ Passed | Both artifacts |
| Host scripts in wheel | ✗ Missing | Needs fix |

---

## TESTPYPI REHEARSAL STATUS

| Item | Status | Blocker |
|------|--------|---------|
| Credentials configured | ✗ NO | No ~/.pypirc |
| TestPyPI upload | ✗ NOT ATTEMPTED | Blocked by credentials |
| Artifacts ready for upload | ✓ YES | dist/ |

---

## INSTALLATION VERIFICATION

| Install Method | CLI Works | Host Setup Works | Notes |
|----------------|-----------|-------------------|-------|
| Development (`pip install -e .`) | ✓ | ✓ | Full functionality |
| Wheel (dist/*.whl) | ✓ | ✗ | Host scripts missing |
| sdist | N/A | N/A | Source only |

---

## ISSUES FOUND

### Issue 1: Host Scripts Not in Wheel (HIGH)

**Location**: `src/ocmaf/hosts/*.sh`

**Problem**: Setuptools doesn't include shell scripts by default

**Evidence**:
```bash
$ python3 -m zipfile -l dist/ocmaf-0.1.0-py3-none-any.whl | grep hosts
(empty result)
```

**Fix Required**:
```toml
[tool.setuptools.package-data]
ocmaf = ["hosts/*.sh"]
```

### Issue 2: TestPyPI Credentials Missing (MEDIUM)

**Problem**: No ~/.pypirc configured

**Fix Required**:
1. Create TestPyPI account
2. Generate API token
3. Configure ~/.pypirc

---

## REMAINING FRICTIONS (NOT BLOCKERS)

### MEDIUM Severity

| ID | Friction | Workaround |
|----|----------|------------|
| F-001 | Claude restart required | Restart after install |
| F-002 | Config overwrites on switch | Re-run install |
| F-003 | Codex no auto-memory | Manual recall/remember |
| F-004 | Host scripts missing from wheel | Use dev install for host setup |

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Reason |
|---------|--------|
| OpenClaw unblock | GitHub release unavailable |
| Semantic conflict detection | Would need embeddings |
| Root cause of identity drift | Not identified |
| Host scripts in wheel | Needs packaging fix |
| TestPyPI upload | No credentials |
| PyPI formal release | Not yet published |

---

## FORMAL RELEASE REQUIREMENTS

| Requirement | Status | Notes |
|-------------|--------|-------|
| Build succeeds | ✓ | |
| Artifacts created | ✓ | |
| twine check passes | ✓ | |
| Host scripts in wheel | ✗ | Needs fix |
| TestPyPI verified | ✗ | Blocked by credentials |
| PyPI upload | ✗ | Not done |

---

## NEXT STEPS FOR FORMAL RELEASE

1. **Fix packaging**: Add `package-data` to include hosts/*.sh
2. **TestPyPI upload**: Configure credentials and upload
3. **Verify install**: Test wheel install in clean environment
4. **PyPI upload**: When ready for formal release

---

**Phase 057 COMPLETE**
**Build Artifacts: CREATED**
**TestPyPI Rehearsal: BLOCKED**
**Host Scripts Fix: NEEDED**
**Trusted User Journey: PRESERVED**
**Root Cause: NOT IDENTIFIED (unchanged)**
