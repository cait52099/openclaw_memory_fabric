# Release Checklist - OCMF v0.1.0

**Version**: 0.1.0
**Status**: Release Readiness (NOT YET PUBLISHED)
**Date**: 2026-03-22

---

## Pre-Release Checklist

### 1. Packaging & Version

| Item | Status | Notes |
|------|--------|-------|
| Version defined in pyproject.toml | ✓ PASS | version = "0.1.0" |
| Entry point configured | ✓ PASS | ocmaf = "ocmaf.cli.unified:unified" |
| Dependencies pinned | ✓ PASS | pydantic>=2.0, click>=8.0 |
| License defined | ✓ PASS | MIT |
| README.md referenced in pyproject.toml | ✓ PASS | readme = "README.md" |
| README.md exists at project root | ✓ PASS | Created phase 056 |
| CHANGELOG.md exists at project root | ✓ PASS | Created phase 056 |

### 2. Development Install Verification

| Item | Status | Command | Expected |
|------|--------|---------|----------|
| `python3 -m pip install -e .` works | ⬜ | | Exit code 0 |
| `ocmaf` command available globally | ⬜ | `which ocmaf` | Path to ocmaf |
| `ocmaf --version` works | ⬜ | | version 0.1.0 |
| `ocmaf --help` works | ⬜ | | Help output |

### 3. Quickstart Verification

| Item | Status | Command | Expected |
|------|--------|---------|----------|
| Claude install works | ⬜ | `ocmaf install --host claude` | ✓ Claude Setup Complete |
| Claude remember works | ⬜ | `ocmaf remember --content "..."` | Source: Claude |
| Claude recall works | ⬜ | `ocmaf recall --query "..."` | From Claude: |
| Codex install works | ⬜ | `ocmaf install --host codex` | ✓ Codex Setup Complete |
| Codex remember works | ⬜ | `ocmaf remember --content "..."` | Source: Codex |
| Codex recall works | ⬜ | `ocmaf recall --query "..."` | From Codex: |
| Cross-host recall works | ⬜ | `ocmaf recall --query "..."` | Shows both Claude + Codex |

### 4. Documentation Completeness

| Item | Status | Location |
|------|--------|----------|
| Quickstart guide | ✓ PASS | docs/quickstart.md |
| Constitution | ✓ PASS | .specify/memory/constitution.md |
| Spec document | ✓ PASS | docs/spec.md |
| Plan document | ✓ PASS | docs/plan.md |
| Analysis document | ✓ PASS | docs/analysis.md |
| Checklist | ✓ PASS | docs/checklist.md |
| README at root | ✓ PASS (NEW) | README.md |
| CHANGELOG at root | ✓ PASS (NEW) | CHANGELOG.md |

### 5. Host Integration Status

| Host | Install | Remember | Recall | Attribution | Status |
|------|---------|----------|--------|-------------|--------|
| Claude | ✓ | ✓ | ✓ | ✓ | Trusted (phases 035-050) |
| Codex | ✓ | ✓ | ✓ | ✓ | Trusted (phases 035-050) |
| OpenClaw | ✗ | ✗ | ✗ | ✗ | Blocked |

### 6. Phase History Verification

| Phase | Focus | Status |
|-------|-------|--------|
| 035-050 | Trusted User Journey | ✓ PASS |
| 051 | Bootstrap wrapper | ✓ PASS |
| 052 | Global install | ✓ PASS |
| 053 | Shell/PATH polish | ✓ PASS |
| 054 | Quickstart polish | ✓ PASS |
| 055 | Release/distribution | ✓ PASS |

### 7. Release Artifact Status

| Artifact | Status | Location |
|----------|--------|----------|
| Source distribution (tar.gz) | ⬜ | Build with `python3 -m build` |
| Wheel distribution | ⬜ | Build with `python3 -m build` |
| PyPI upload | ✗ NOT DONE | Requires credentials + testing |
| GitHub Release | ✗ NOT DONE | Requires git tag + GitHub CLI |

---

## Formal Release Requirements (NOT YET MET)

### Required for PyPI Release

| Item | Status | Notes |
|------|--------|-------|
| Test package upload (TestPyPI) | ⬜ | Not run |
| Verify TestPyPI install works | ⬜ | Not run |
| Fix any install issues | N/A | No issues yet |
| Upload to PyPI (real) | ⬜ | Requires credentials |
| Create git tag | ⬜ | Not done |
| Create GitHub Release | ⬜ | Not done |

### Required for GitHub Release

| Item | Status | Notes |
|------|--------|-------|
| Git tag (v0.1.0) | ⬜ | Not created |
| Release notes | ⬜ | Need to write |
| GitHub Release creation | ⬜ | Not done |

---

## Current Release Status

| Item | Status |
|------|--------|
| **Development Install** | ✓ READY |
| **README.md** | ✓ READY (NEW) |
| **CHANGELOG.md** | ✓ READY (NEW) |
| **Quickstart** | ✓ READY |
| **Trusted User Journey** | ✓ VERIFIED |
| **Formal PyPI Release** | ✗ NOT PUBLISHED |
| **GitHub Release** | ✗ NOT CREATED |

---

## Release Decision

### Can Release: YES (when ready)

All development install verification items pass.

### Should Release: TBD

- [ ] Decide if v0.1.0 alpha is ready for PyPI
- [ ] Set up TestPyPI credentials if needed
- [ ] Run test package upload
- [ ] Verify install from TestPyPI
- [ ] Create git tag
- [ ] Upload to real PyPI
- [ ] Create GitHub Release

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |

---

## Notes

- This checklist represents **release readiness**, not actual release
- Formal PyPI release requires additional setup (credentials, testing)
- GitHub Release creation is separate from PyPI
- Current status: **Development install only, not publicly indexed**
