# Friction Log - Phase 038

**Run ID**: 038-determinism-debug
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Determinism issue investigated. The reported issue ("Claude install writes Codex identity") was NOT reproducible in testing. Fix adds defensive validation to catch any edge cases.

---

## Friction Points

### HIGH Severity

| ID | Friction | Description | Workaround |
|----|----------|-------------|------------|
| F-001 | PYTHONPATH required | Must prefix commands with `PYTHONPATH=src` | Use wrapper script or `pip install -e` |
| F-002 | Claude restart required | MCP server needs Claude restart to load new config | Restart Claude after `install --host claude` |

### MEDIUM Severity

| ID | Friction | Description | Workaround |
|----|----------|-------------|------------|
| F-003 | Manual source config | Must manually `source ~/.ocmf/config.sh` | Future: auto-detection in CLI |
| F-004 | Config overwrites on switch | `install --host X` overwrites config | Document as expected behavior |
| F-005 | Method C no auto-memory | Codex cannot auto-recall/remember | Manual recall/remember only |

---

## Issue Investigation Notes

### Reported Issue
- "Claude clean-home path may still be written as Codex identity"
- "Claude → Codex → Claude switching 过程中宿主身份仍会漂移"

### Investigation Results

1. **NOT REPRODUCIBLE**: Issue could not be reproduced in this test environment
2. **FIX APPLIED**: Added defensive validation to claude_setup.sh
3. **VERIFICATION**: 3x3 repeatability tests all passed

### Fix Details

Added identity verification to `claude_setup.sh`:
```bash
# DEFENSIVE: Verify the config was written correctly
ACTUAL_TOOL="$(grep 'OCMF_SOURCE_TOOL=' "$OCMF_CONFIG" | head -1 | cut -d'"' -f2 2>/dev/null || echo 'UNKNOWN')"
if [ "$ACTUAL_TOOL" != "claude-code" ]; then
    echo "✗ ERROR: Config verification failed!"
    exit 1
fi
echo "  ✓ Verified OCMF_SOURCE_TOOL=claude-code"
```

---

## Overall Assessment

**USER_JOURNEY_READY_TO_RECHECK: YES**

All friction points documented. Core user journey is stable.
