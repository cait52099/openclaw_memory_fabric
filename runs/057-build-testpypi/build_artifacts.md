# Build Artifacts - Phase 057

**Run ID**: 057-build-testpypi
**Date**: 2026-03-22
**Status**: PASS (with findings)
**Task Type**: PRODUCT POLISH

---

## Build Summary

| Item | Status | Details |
|------|--------|---------|
| Build command | ✓ SUCCESS | `python3 -m build` |
| Exit code | ✓ 0 | Clean build |
| sdist created | ✓ YES | `ocmaf-0.1.0.tar.gz` |
| wheel created | ✓ YES | `ocmaf-0.1.0-py3-none-any.whl` |
| twine check | ✓ PASSED | Both artifacts pass |

---

## Build Command & Output

```bash
$ python3 -m build
* Creating isolated environment: venv+pip...
* Getting build dependencies for sdist...
...
Successfully built ocmaf-0.1.0.tar.gz and ocmaf-0.1.0-py3-none-any.whl
```

---

## Artifacts Created

| File | Size | Type |
|------|------|------|
| `ocmaf-0.1.0.tar.gz` | 45K | Source distribution |
| `ocmaf-0.1.0-py3-none-any.whl` | 50K | Wheel (pure Python) |

### Artifact Locations

```
/Users/caihongwei/project/openclaw_memory_fabric/dist/
├── ocmaf-0.1.0.tar.gz
└── ocmaf-0.1.0-py3-none-any.whl
```

---

## Twine Check Results

```bash
$ twine check dist/*
Checking  dist/ocmaf-0.1.0-py3-none-any.whl: PASSED
Checking  dist/ocmaf-0.1.0.tar.gz: PASSED
```

Both artifacts pass twine's metadata and format checks.

---

## Finding: Host Setup Scripts Not Included in Wheel

### Issue

The wheel does not include the `hosts/` directory containing shell scripts:

```
src/ocmaf/hosts/claude_setup.sh
src/ocmaf/hosts/codex_setup.sh
```

### Evidence

```bash
$ python3 -m zipfile -l dist/ocmaf-0.1.0-py3-none-any.whl | grep hosts
(empty - no hosts directory in wheel)
```

### Impact

| Function | Wheel Install | Dev Install |
|----------|---------------|-------------|
| `ocmaf --version` | ✓ Works | ✓ Works |
| `ocmaf install --host claude` | ✗ Setup script not found | ✓ Works |
| `ocmaf remember` | ✓ Works | ✓ Works |
| `ocmaf recall` | ✓ Works | ✓ Works |

### Root Cause

Setuptools does not include non-Python files by default. The `hosts/` directory contains `.sh` files which need explicit `package_data` configuration.

### Fix Required

Add to `pyproject.toml`:

```toml
[tool.setuptools.package-data]
ocmaf = ["hosts/*.sh"]
```

Or convert shell scripts to Python for cross-platform compatibility.

---

## Summary

| Item | Status |
|------|--------|
| Build succeeds | ✓ |
| Artifacts created | ✓ |
| twine check passes | ✓ |
| Host scripts in wheel | ✗ Missing |
| Fix needed before formal release | ✓ Identified |
