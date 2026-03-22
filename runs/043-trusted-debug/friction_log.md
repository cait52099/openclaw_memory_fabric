# Friction Log - Phase 043

**Run ID**: 043-trusted-debug
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Debug run completed. The reported issue ("trusted journey scenario Claude drifts to `codex-cli`") was NOT reproducible in this environment. All tests passed.

---

## Issue Status

### Reported Issue
"Trusted journey scenario Claude drifts to `codex-cli`"

### Investigation Result
- **NOT REPRODUCIBLE** in this environment
- 042 scenario replay: PASSED
- 3 consecutive scenario runs: ALL PASSED
- Multiple isolated tests: ALL PASSED

---

## Friction Points

### HIGH Severity (Not Blockers)

| ID | Friction | Description | Status |
|----|----------|-------------|--------|
| F-001 | PYTHONPATH required | Must prefix commands with `PYTHONPATH=src` | NOT A BLOCKER |
| F-002 | Claude restart required | MCP server needs restart to load new config | NOT A BLOCKER |

### MEDIUM Severity (Not Blockers)

| ID | Friction | Description | Status |
|----|----------|-------------|--------|
| F-003 | Manual source config | Must manually `source ~/.ocmf/config.sh` | NOT A BLOCKER |
| F-004 | Config overwrites on switch | `install --host X` overwrites config | NOT A BLOCKER |
| F-005 | Method C no auto-memory | Codex cannot auto-recall/remember | NOT A BLOCKER |

---

## Investigation Notes

The reported "trusted journey scenario Claude drifts to `codex-cli`" issue could NOT be reproduced despite extensive testing. Possible explanations:

1. Environment-specific issue
2. Claude Code context (internal invocation)
3. Race condition
4. Previous fixes effective

---

## Overall Assessment

**USER_JOURNEY_READY_TO_RECHECK: YES**

All friction points are documented. The core user journey is stable in this environment.
