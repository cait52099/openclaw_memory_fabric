# Release Rehearsal - Phase 056

**Run ID**: 056-release-readiness
**Date**: 2026-03-22
**Status**: PASS
**Type**: Non-Publish Release Rehearsal

---

## Rehearsal Summary

| Test | Status | Output |
|------|--------|--------|
| `which ocmaf` | ✓ PASS | /Library/Frameworks/.../bin/ocmaf |
| `ocmaf --version` | ✓ PASS | ocmaf, version 0.1.0 |
| `ocmaf --help` | ✓ PASS | Usage: ocmaf [OPTIONS] COMMAND [ARGS]... |
| `ocmaf install --host claude` | ✓ PASS | ✓ Installation complete! |
| `ocmaf remember (Claude)` | ✓ PASS | Source: Claude |
| `ocmaf recall (Claude)` | ✓ PASS | From Claude: |
| `ocmaf install --host codex` | ✓ PASS | ✓ Installation complete! |
| `ocmaf remember (Codex)` | ✓ PASS | Source: Codex |
| `ocmaf recall (Codex)` | ✓ PASS | From Codex: |

---

## Detailed Test Output

### 1. Global Command Availability

```bash
$ which ocmaf
/Library/Frameworks/Python.framework/Versions/3.12/bin/ocmaf

$ ocmaf --version
ocmaf, version 0.1.0
```

### 2. Claude Path

```bash
$ ocmaf install --host claude
...
✓ claude setup completed successfully
✓ Installation complete!

$ ocmaf remember --content "T056_CLAUDE_REHEARSAL"
✓ Remembered: 64177f08-6ec6-4f04-8ee0-420300dff4d8
  Source: Claude

$ ocmaf recall --query "T056_CLAUDE"
Found 1 memories:

From Claude:
  • "T056_CLAUDE_REHEARSAL" (2026-03-22 10:46)
```

### 3. Codex Path

```bash
$ ocmaf install --host codex
...
✓ codex setup completed successfully
✓ Installation complete!

$ ocmaf remember --content "T056_CODEX_REHEARSAL"
✓ Remembered: 4a34dae1-96cd-46c2-a762-0674af4a92a7
  Source: Codex

$ ocmaf recall --query "T056_CODEX"
Found 1 memories:

From Codex:
  • "T056_CODEX_REHEARSAL" (2026-03-22 10:46)
```

---

## Cross-Host Memory Verification

```bash
$ ocmaf recall --query "T056"
Found 2 memories:

From Codex:
  • "T056_CODEX_REHEARSAL" (2026-03-22 10:46)

From Claude:
  • "T056_CLAUDE_REHEARSAL" (2026-03-22 10:46)
```

✓ Both Claude and Codex memories visible in cross-host recall.

---

## Artifacts Created

| File | Purpose |
|------|---------|
| README.md | Project homepage |
| CHANGELOG.md | Version history |
| release_checklist.md | Pre-release verification |
| release_rehearsal.md | This file |
| release_readiness.md | Overall readiness summary |
| evidence.md | Phase evidence |
| known_limits.md | Known limitations |

---

## Formal Release Requirements Status

| Requirement | Status |
|-------------|--------|
| Development install verified | ✓ PASS |
| README created | ✓ PASS |
| CHANGELOG created | ✓ PASS |
| Release checklist created | ✓ PASS |
| Quickstart verified | ✓ PASS |
| Host paths verified | ✓ PASS |
| PyPI upload | ✗ NOT DONE |
| GitHub Release | ✗ NOT DONE |

---

## Rehearsal Conclusion

**Result**: ✓ PASS

All development install and basic usage tests pass. The project is ready for formal release once:
1. TestPyPI upload is verified
2. Credentials are configured
3. Git tag is created
