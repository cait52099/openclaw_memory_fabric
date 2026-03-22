# OCMF Phase 058 Evidence - Wheel Packaging Fix

**Run ID**: 058-wheel-packaging-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **WHEEL_PACKAGING_FIXED** | **YES** |
| **WHEEL_INSTALL_REHEARSAL_PASS** | **YES** |
| **TESTPYPI_REHEARSAL_DONE** | **NO** (blocked by credentials) |
| **FORMAL_RELEASE_PUBLISHED** | **NO** |
| **ROOT_CAUSE_IDENTIFIED** | **NO** (unchanged) |

---

## CATEGORIZATION

### Trusted User Journey - PRESERVED ✓

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude clean-home | ✓ TRUSTED | phases 035-050 |
| Codex clean-home | ✓ TRUSTED | phases 035-050 |
| Switching | ✓ TRUSTED | phases 039-050 |

### Product Polish - WHEEL PACKAGING FIX (THIS RUN) - ACHIEVED ✓

| Feature | Status | Evidence |
|---------|--------|----------|
| Global install | ✓ PASS | phases 052 |
| Shell/PATH polish | ✓ PASS | phase 053 |
| Quickstart polish | ✓ PASS | phase 054 |
| Release readiness | ✓ PASS | phase 055 |
| Build artifacts | ✓ PASS | phase 057 |
| Wheel packaging fix | ✓ PASS | This run |
| Package-data added | ✓ | pyproject.toml |
| hosts/*.sh in wheel | ✓ FIXED | Verified in wheel |
| Fresh venv rehearsal | ✓ PASS | All tests passed |
| TestPyPI rehearsal | ✗ BLOCKED | No credentials |

### Phase History

| Phase | Focus | Status |
|-------|-------|--------|
| 035-050 | Trusted User Journey | ✓ PASS |
| 051 | Bootstrap wrapper | ✓ PASS |
| 052 | Global install | ✓ PASS |
| 053 | Shell/PATH polish | ✓ PASS |
| 054 | Quickstart polish | ✓ PASS |
| 055 | Release readiness | ✓ PASS |
| 056 | Release artifacts | ✓ PASS |
| 057 | Build & TestPyPI rehearsal | ✓ PASS (findings) |
| 058 | Wheel packaging fix | ✓ PASS (THIS RUN) |

---

## PACKAGING FIX APPLIED

### Change to pyproject.toml

```toml
[tool.setuptools.package-data]
ocmaf = ["hosts/*.sh"]
```

### Result

```
ocmaf/hosts/claude_setup.sh                    2026-03-22 07:15:16         5878
ocmaf/hosts/codex_setup.sh                     2026-03-22 07:31:00         5708
```

Both shell scripts now included in wheel.

---

## WHEEL INSTALL REHEARSAL (FRESH VENV)

### Environment

- Fresh Python venv: `/tmp/ocmaf_test_venv`
- Python 3.12
- Installed from: `dist/ocmaf-0.1.0-py3-none-any.whl`

### Tests Passed

| Test | Result | Output |
|------|--------|--------|
| Wheel install | ✓ | Successfully installed |
| `ocmaf --version` | ✓ | version 0.1.0 |
| Claude install | ✓ | Setup complete |
| Claude remember | ✓ | Source: Claude |
| Claude recall | ✓ | From Claude |
| Codex install | ✓ | Setup complete |
| Codex remember | ✓ | Source: Codex |
| Codex recall | ✓ | From Codex |
| Cross-host recall | ✓ | Both visible |

---

## TESTPYPI STATUS

| Item | Status | Details |
|------|--------|---------|
| Credentials | ✗ MISSING | No ~/.pypirc |
| Upload | ✗ NOT ATTEMPTED | Blocked |
| Artifacts ready | ✓ YES | dist/ valid |

---

## VALIDATION DETAILS

### Build

```
$ python3 -m build
adding 'ocmaf/hosts/claude_setup.sh'
adding 'ocmaf/hosts/codex_setup.sh'
Successfully built ocmaf-0.1.0.tar.gz and ocmaf-0.1.0-py3-none-any.whl
```

### Fresh venv Installation

```
$ python3 -m venv /tmp/ocmaf_test_venv
$ /tmp/ocmaf_test_venv/bin/pip install dist/ocmaf-0.1.0-py3-none-any.whl
Successfully installed ocmaf-0.1.0
```

### Claude Path

```
$ /tmp/ocmaf_test_venv/bin/ocmaf install --host claude
✓ Installation complete!

$ /tmp/ocmaf_test_venv/bin/ocmaf remember --content "T058_CLAUDE_TEST"
✓ Remembered: 02f0cee8-0def-4063-b837-b24ec699708a
  Source: Claude

$ /tmp/ocmaf_test_venv/bin/ocmaf recall --query "T058_CLAUDE"
From Claude:
  • "T058_CLAUDE_TEST" (2026-03-22 11:02)
```

### Codex Path

```
$ /tmp/ocmaf_test_venv/bin/ocmaf install --host codex
✓ Installation complete!

$ /tmp/ocmaf_test_venv/bin/ocmaf remember --content "T058_CODEX_TEST"
✓ Remembered: 5529bff9-632e-40ba-bbd8-3a217b8893da
  Source: Codex

$ /tmp/ocmaf_test_venv/bin/ocmaf recall --query "T058_CODEX"
From Codex:
  • "T058_CODEX_TEST" (2026-03-22 11:02)
```

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| Root cause of identity drift | N/A | Not identified |
| TestPyPI upload | N/A | No credentials |
| PyPI formal release | N/A | Not yet published |

---

## ROOT CAUSE STATUS

**ROOT_CAUSE_IDENTIFIED: NO**

The identity drift issue has never been reproduced. This remains unchanged.

---

## RELEASE STATUS (HONEST)

| Channel | Status |
|---------|--------|
| Development install (`pip install -e .`) | ✓ Available |
| Wheel install (dist/*.whl) | ✓ CLI + host setup works |
| Source distribution | ✓ Created |
| TestPyPI | ✗ NOT UPLOADED (no credentials) |
| PyPI (formal release) | ✗ NOT PUBLISHED |

---

**Phase 058 COMPLETE**
**Wheel Packaging Fix: COMPLETE**
**Wheel Install Rehearsal: PASSED**
**TestPyPI Rehearsal: BLOCKED (credentials)**
**Trusted User Journey: PRESERVED**
