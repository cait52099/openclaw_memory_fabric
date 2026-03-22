# Build Artifacts - Phase 058

**Run ID**: 058-wheel-packaging-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## Build Summary

| Item | Status | Details |
|------|--------|---------|
| Build command | ✓ SUCCESS | `python3 -m build` |
| Exit code | ✓ 0 | Clean build |
| sdist created | ✓ YES | `ocmaf-0.1.0.tar.gz` |
| wheel created | ✓ YES | `ocmaf-0.1.0-py3-none-any.whl` |
| hosts/*.sh in wheel | ✓ FIXED | Now included |

---

## Packaging Fix Applied

### Before

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

### After

```toml
[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
ocmaf = ["hosts/*.sh"]
```

### Files Now Included in Wheel

```
ocmaf/hosts/claude_setup.sh
ocmaf/hosts/codex_setup.sh
```

---

## Build Command & Output

```bash
$ python3 -m build
...
adding 'ocmaf/hosts/claude_setup.sh'
adding 'ocmaf/hosts/codex_setup.sh'
...
Successfully built ocmaf-0.1.0.tar.gz and ocmaf-0.1.0-py3-none-any.whl
```

---

## Artifacts Created

| File | Size |
|------|------|
| `ocmaf-0.1.0.tar.gz` | 49K |
| `ocmaf-0.1.0-py3-none-any.whl` | 55K |

### Verification

```bash
$ python3 -m zipfile -l dist/ocmaf-0.1.0-py3-none-any.whl | grep hosts
ocmaf/hosts/claude_setup.sh                    2026-03-22 07:15:16         5878
ocmaf/hosts/codex_setup.sh                     2026-03-22 07:31:00         5708
```

---

## Summary

| Item | Status |
|------|--------|
| Packaging fix applied | ✓ |
| Build succeeds | ✓ |
| hosts/*.sh in wheel | ✓ FIXED |
| Artifacts created | ✓ |
