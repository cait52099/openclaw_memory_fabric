# Release Rehearsal - Phase 057

**Run ID**: 057-build-testpypi
**Date**: 2026-03-22
**Status**: PARTIAL PASS (findings documented)
**Type**: Non-Production Release Rehearsal

---

## Rehearsal Summary

| Test | Status | Notes |
|------|--------|-------|
| `python3 -m build` | ✓ PASS | Artifacts created |
| twine check | ✓ PASS | Both artifacts pass |
| TestPyPI upload | ✗ BLOCKED | No credentials |
| Wheel install (CLI) | ✓ PASS | `ocmaf --version` works |
| Wheel install (host setup) | ✗ PARTIAL | Host scripts missing |
| Claude remember/recall | ✓ PASS | Memory works |
| Codex remember/recall | ✓ PASS | Memory works |

---

## Detailed Test Results

### 1. Build Artifacts

```
$ python3 -m build
Successfully built ocmaf-0.1.0.tar.gz and ocmaf-0.1.0-py3-none-any.whl

$ ls -lh dist/
ocmaf-0.1.0-py3-none-any.whl    50K
ocmaf-0.1.0.tar.gz              45K
```

### 2. Wheel Installation Test

```bash
$ python3 -m pip install dist/ocmaf-0.1.0-py3-none-any.whl
Successfully installed ocmaf-0.1.0
```

### 3. CLI Verification

```bash
$ which ocmaf
/Library/Frameworks/Python.framework/Versions/3.12/bin/ocmaf

$ ocmaf --version
ocmaf, version 0.1.0
```

### 4. Host Setup (Wheel)

```bash
$ ocmaf install --host claude
✗ Setup script not found: .../ocmaf/hosts/claude_setup.sh

$ ocmaf install --host codex
✗ Setup script not found: .../ocmaf/hosts/codex_setup.sh
```

### 5. Memory Operations (Still Work)

```bash
$ ocmaf remember --content "T057_WHEEL_TEST"
✓ Remembered: 73e3c034-984d-417f-97e2-239966f5c602
  Source: Codex

$ ocmaf recall --query "T057_WHEEL"
Found 1 memories:

From Codex:
  • "T057_WHEEL_TEST" (2026-03-22 10:53)
```

### 6. Cross-Host Memory

```bash
$ ocmaf recall --query "T057"
Found 2 memories:

From Codex:
  • "T057_CODEX_WHEEL" (2026-03-22 10:53)

From Claude:
  • "T057_CLAUDE_WHEEL" (2026-03-22 10:53)
```

---

## Findings Summary

| Finding | Severity | Status |
|---------|----------|--------|
| Host setup scripts not in wheel | HIGH | Needs fix |
| TestPyPI credentials missing | MEDIUM | Blocked |
| Core CLI works in wheel | N/A | ✓ Verified |
| Memory operations work | N/A | ✓ Verified |

---

## Fix Required for Host Setup Scripts

Add to `pyproject.toml`:

```toml
[tool.setuptools.package-data]
ocmaf = ["hosts/*.sh"]
```

---

## Formal Release Requirements Status

| Requirement | Status |
|-------------|--------|
| Build artifacts | ✓ READY |
| twine check | ✓ PASS |
| TestPyPI credentials | ✗ MISSING |
| Host scripts in wheel | ✗ MISSING |
| Installation verification | PARTIAL |

---

## Conclusion

**Result**: PARTIAL PASS

- Build artifacts created successfully
- Wheel passes twine check
- Core CLI works from wheel
- Host setup scripts missing (needs packaging fix)
- TestPyPI upload blocked (needs credentials)
