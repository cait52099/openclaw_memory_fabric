# Runtime Path Debug - Phase 061

**Run ID**: 061-runtime-path-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## Bug Identified

### Problem

When installing from wheel (TestPyPI or local), `ocmaf install --host claude` was looking for setup scripts in the **system Python path** instead of the **venv's site-packages**.

### Root Cause

In `src/ocmaf/cli/unified.py`, the hosts directory was being located using:

```python
this_file = Path(__file__).resolve()
ocmf_src = this_file.parent.parent
hosts_dir = ocmf_src / "hosts"
```

This caused `__file__` to resolve to the wrong Python installation when the entry point script (`/Library/Frameworks/Python.framework/.../bin/ocmaf`) used a hardcoded shebang.

### Error Evidence (Before Fix)

```
✗ Setup script not found: /Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/ocmaf/hosts/claude_setup.sh
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                       WRONG - System Python, not venv
```

---

## Fix Applied

### Change to `src/ocmaf/cli/unified.py`

**Before:**
```python
# Find OCMF path (where this source is located)
this_file = Path(__file__).resolve()
# unified.py is at src/ocmaf/cli/unified.py
# go up to src/ocmaf/ which contains hosts/
ocmf_src = this_file.parent.parent
hosts_dir = ocmf_src / "hosts"
```

**After:**
```python
# Find OCMF path dynamically using the ocmaf package location
# This correctly resolves to the installed package location (even in venvs)
import ocmaf as ocmf_pkg
ocmf_src = Path(ocmf_pkg.__file__).parent
hosts_dir = ocmf_src / "hosts"
```

### Version Bump

- **Before**: 0.1.0
- **After**: 0.1.1
- **Reason**: Bug fix release

---

## Verification

### Path Resolution Now Correct

After fix, the setup script is found at the correct venv path:

```
Running: source /private/tmp/ocmaf_test_venv/lib/python3.12/site-packages/ocmaf/hosts/claude_setup.sh
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                       CORRECT - venv site-packages
```

### Fresh venv Test Results

| Test | Result | Path Shown |
|------|--------|------------|
| `ocmaf install --host claude` | ✓ | venv path |
| `ocmaf install --host codex` | ✓ | venv path |
| `ocmaf remember (Claude)` | ✓ | Source: Claude |
| `ocmaf recall (Claude)` | ✓ | From Claude |
| `ocmaf remember (Codex)` | ✓ | Source: Codex |
| `ocmaf recall (Codex)` | ✓ | From Codex |
| Cross-host recall | ✓ | Both visible |

---

## Summary

| Item | Status |
|------|--------|
| Bug identified | ✓ |
| Root cause found | ✓ |
| Fix applied | ✓ |
| Version bumped | ✓ (0.1.1) |
| Artifacts rebuilt | ✓ |
| Fresh venv test | ✓ PASS |
