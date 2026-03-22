# Clean-Home Fix Friction Log

**Run ID**: 035-clean-home-fix
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Clean-home deterministic journey test PASSED. The reported issue ("install --host claude may write Codex identity") was NOT reproducible. All tests show correct behavior.

---

## Friction Points

### HIGH Severity

| ID | Friction | Description | Suggested Fix |
|----|----------|-------------|---------------|
| CF-001 | PYTHONPATH required | Must prefix commands with PYTHONPATH=src | Create wrapper script or pip install |

### MEDIUM Severity

| ID | Friction | Description | Suggested Fix |
|----|----------|-------------|---------------|
| CF-002 | Manual source config | Must manually source ~/.ocmf/config.sh | Auto-detection in CLI (future) |
| CF-003 | Config overwrites on switch | Running install --host X overwrites config | Document as expected behavior |
| CF-004 | Method C no auto-memory | Codex cannot auto-recall/remember | Document clearly |

### INFO

| ID | Observation | Notes |
|----|-------------|-------|
| CF-005 | Clean-home works correctly | install --host claude writes correct identity |
| CF-006 | Cross-host switching works | Memory persists, attribution correct |

---

## Overall Assessment

**Clean-Home Deterministic Journey**: WORKING

The issue reported during Phase 7D/7E testing was NOT reproducible in this test environment. The install command correctly handles:
1. `--host claude` → writes `OCMF_SOURCE_TOOL="claude-code"`
2. `--host codex` → writes `OCMF_SOURCE_TOOL="codex-cli"`
3. Pre-existing config is correctly overwritten
4. Environment variable `OCMF_SOURCE_TOOL` does not pollute install

**No additional friction points identified beyond those from Phase 7D/7E.**
