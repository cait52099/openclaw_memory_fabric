# Friction Log - Phase 041

**Run ID**: 041-install-debug
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Debug run completed. The reported issue ("Claude install writes `codex-cli`") was NOT reproducible in this environment. All 5x tests passed with correct identity.

---

## Issue Status

### Reported Issue
"Claude clean-home path may still be written as Codex identity"

### Investigation Result
- **NOT REPRODUCIBLE** in this environment
- 5 consecutive clean-home tests: ALL PASSED
- Multiple installs without cleaning: ALL PASSED
- Alternating Claude/Codex cycles: ALL PASSED

---

## Friction Points

### HIGH Severity

| ID | Friction | Description | Status |
|----|----------|-------------|--------|
| F-001 | PYTHONPATH required | Must prefix commands with `PYTHONPATH=src` | NOT A BLOCKER |
| F-002 | Claude restart required | MCP server needs restart to load new config | NOT A BLOCKER |

### MEDIUM Severity

| ID | Friction | Description | Status |
|----|----------|-------------|--------|
| F-003 | Manual source config | Must manually `source ~/.ocmf/config.sh` | NOT A BLOCKER |
| F-004 | Config overwrites on switch | `install --host X` overwrites config | NOT A BLOCKER |
| F-005 | Method C no auto-memory | Codex cannot auto-recall/remember | NOT A BLOCKER |

### Investigation Notes

The reported "Claude install writes `codex-cli`" issue could NOT be reproduced despite extensive testing. Possible explanations:

1. Environment-specific issue
2. Claude Code context (internal invocation)
3. Race condition
4. Previous fixes effective

---

## Overall Assessment

**USER_JOURNEY_READY_TO_RECHECK: YES**

All friction points are documented and expected. The core user journey is stable in this environment.
