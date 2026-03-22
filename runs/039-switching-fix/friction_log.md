# Friction Log - Phase 039

**Run ID**: 039-switching-fix
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Switching repeatability verified with 3 full cycles. All tests passed. Defensive verification added to both setup scripts.

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

## Issue Investigation

### Reported Issue
"Claude → Codex → Claude switching 过程中宿主身份仍会漂移"

### Investigation Results

1. **NOT REPRODUCIBLE**: Issue could not be reproduced in this test environment
2. **FIX APPLIED**: Added defensive verification to both setup scripts
3. **VERIFICATION**: 3×3 switching repeatability tests all passed

### Fix Details

Added identity verification to both `claude_setup.sh` and `codex_setup.sh`:
- Scripts now verify `OCMF_SOURCE_TOOL` is correctly written after creating config
- Scripts fail explicitly if verification fails

---

## Overall Assessment

**SWITCHING_REPEATABLE_3X: YES**
**USER_JOURNEY_READY_TO_RECHECK: YES**

All switching cycles passed with correct identity at every step.
