# Install from TestPyPI - Phase 061

**Run ID**: 061-runtime-path-fix
**Date**: 2026-03-22
**Status**: PASS (local wheel verified)
**Task Type**: PRODUCT POLISH

---

## Status

TestPyPI credentials are still missing, but the **runtime path fix has been verified using a local wheel** in a fresh venv.

---

## Test Environment

| Item | Value |
|------|-------|
| Venv | `/tmp/ocmaf_test_venv` |
| Python | 3.12 |
| Package | `ocmaf-0.1.1-py3-none-any.whl` |
| Source | Local build (same as TestPyPI would be) |

---

## Verification Results

### Version Check

```bash
$ /tmp/ocmaf_test_venv/bin/ocmaf --version
ocmaf, version 0.1.1
```

### Claude Path

| Test | Command | Result |
|------|---------|--------|
| Install | `ocmaf install --host claude` | ✓ Setup complete |
| Script path | (shown in output) | `/private/tmp/.../ocmaf/hosts/claude_setup.sh` ✓ |
| Remember | `ocmaf remember --content "T061_CLAUDE_TEST"` | ✓ Source: Claude |
| Recall | `ocmaf recall --query "T061_CLAUDE"` | ✓ From Claude |

### Codex Path

| Test | Command | Result |
|------|---------|--------|
| Install | `ocmaf install --host codex` | ✓ Setup complete |
| Script path | (shown in output) | `/private/tmp/.../ocmaf/hosts/codex_setup.sh` ✓ |
| Remember | `ocmaf remember --content "T061_CODEX_TEST"` | ✓ Source: Codex |
| Recall | `ocmaf recall --query "T061_CODEX"` | ✓ From Codex |

### Cross-Host Recall

```bash
$ /tmp/ocmaf_test_venv/bin/ocmaf recall --query "T061"
Found 2 memories:

From Codex:
  • "T061_CODEX_TEST" (2026-03-22 12:25)

From Claude:
  • "T061_CLAUDE_TEST" (2026-03-22 12:25)
```

---

## Key Fix Verification

**Before Fix**: Script path showed system Python `/Library/Frameworks/...`
**After Fix**: Script path shows correct venv path `/private/tmp/.../ocmaf_test_venv/...`

---

## Note

The runtime path fix works correctly. When TestPyPI credentials become available, the same wheel (0.1.1) can be uploaded and will work the same way.

---

## Summary

| Item | Status |
|------|--------|
| Runtime path fix | ✓ Verified |
| Local wheel test | ✓ PASS |
| TestPyPI upload | ✗ Blocked (credentials) |
| Ready for TestPyPI | ✓ (when credentials added) |
