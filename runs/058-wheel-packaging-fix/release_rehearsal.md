# Release Rehearsal - Phase 058

**Run ID**: 058-wheel-packaging-fix
**Date**: 2026-03-22
**Status**: PASS
**Type**: Non-Production Release Rehearsal

---

## Rehearsal Summary

| Test | Status | Output |
|------|--------|--------|
| Fresh venv created | ✓ | /tmp/ocmaf_test_venv |
| Wheel install | ✓ | Successfully installed |
| `ocmaf --version` | ✓ | version 0.1.0 |
| `ocmaf install --host claude` | ✓ | Setup complete |
| Claude remember | ✓ | Source: Claude |
| Claude recall | ✓ | From Claude |
| `ocmaf install --host codex` | ✓ | Setup complete |
| Codex remember | ✓ | Source: Codex |
| Codex recall | ✓ | From Codex |
| Cross-host recall | ✓ | Both Claude + Codex |

---

## Detailed Test Results

### 1. Fresh venv Creation

```bash
$ python3 -m venv /tmp/ocmaf_test_venv
$ /tmp/ocmaf_test_venv/bin/pip --version
pip 24.0 from /private/tmp/ocmaf_test_venv/lib/python3.12/site-packages/pip
```

### 2. Wheel Installation

```bash
$ /tmp/ocmaf_test_venv/bin/pip install dist/ocmaf-0.1.0-py3-none-any.whl
Installing collected packages: typing-extensions, click, annotated-types, typing-inspection, pydantic-core, pydantic, ocmaf
Successfully installed annotated-types-0.7.0 click-8.3.1 ocmaf-0.1.0 pydantic-2.12.5 pydantic-core-2.41.5 typing-extensions-4.15.0 typing-inspection-0.4.2
```

### 3. CLI Verification

```bash
$ /tmp/ocmaf_test_venv/bin/ocmaf --version
ocmaf, version 0.1.0
```

### 4. Claude Path

```bash
$ /tmp/ocmaf_test_venv/bin/ocmaf install --host claude
✓ Installation complete!

$ /tmp/ocmaf_test_venv/bin/ocmaf remember --content "T058_CLAUDE_TEST"
✓ Remembered: 02f0cee8-0def-4063-b837-b24ec699708a
  Source: Claude

$ /tmp/ocmaf_test_venv/bin/ocmaf recall --query "T058_CLAUDE"
Found 1 memories:

From Claude:
  • "T058_CLAUDE_TEST" (2026-03-22 11:02)
```

### 5. Codex Path

```bash
$ /tmp/ocmaf_test_venv/bin/ocmaf install --host codex
✓ Installation complete!

$ /tmp/ocmaf_test_venv/bin/ocmaf remember --content "T058_CODEX_TEST"
✓ Remembered: 5529bff9-632e-40ba-bbd8-3a217b8893da
  Source: Codex

$ /tmp/ocmaf_test_venv/bin/ocmaf recall --query "T058_CODEX"
Found 1 memories:

From Codex:
  • "T058_CODEX_TEST" (2026-03-22 11:02)
```

### 6. Cross-Host Recall

```bash
$ /tmp/ocmaf_test_venv/bin/ocmaf recall --query "T058"
Found 2 memories:

From Codex:
  • "T058_CODEX_TEST" (2026-03-22 11:02)

From Claude:
  • "T058_CLAUDE_TEST" (2026-03-22 11:02)
```

---

## Rehearsal Result

**Result**: ✓ PASS

All wheel install tests passed in fresh venv:
- ✓ Claude host setup works
- ✓ Claude remember/recall works
- ✓ Codex host setup works
- ✓ Codex remember/recall works
- ✓ Cross-host memory visible
