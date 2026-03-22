# OCMF Phase 6G - Regression Gate Known Limits

**Run ID**: 028-regression-gate
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: REGRESSION GUARDRAIL

---

## FINAL STATUS: PASS

---

## THIS IS A REGRESSION GUARDRAIL TASK

**Important**: This task is NOT a new product initiative. It is a guardrail task to protect existing user-visible experiences.

### Guardrail Purpose

This regression gate exists to:
- Protect the already-implemented user-visible experiences
- Prevent accidental regressions in recall/explain/conflict output
- Ensure golden example outputs remain stable
- Catch formatting drift before it reaches users

### What This Task IS NOT

- ❌ New feature development
- ❌ Product line expansion
- ❌ UX style engineering
- ❌ New host capability exploration
- ❌ Output format optimization

---

## REGRESSION GATE STATUS

### Gate Established

| Aspect | Status | Notes |
|--------|--------|-------|
| Regression gate script | ✅ Ready | `run_regression_gate.py` |
| Golden examples | ✅ 4 files | Covered recall_conflict, explain_crosshost, recall_provenance, injection_text |
| Regression classification | ✅ Ready | formatting_drift, provenance_regression, conflict_visibility_regression, explain_visibility_regression |
| CI/CD integration point | ✅ Ready | Script exit code 0/1 |

### What Regression Gate Checks

The regression gate verifies the PRESENCE of key patterns:

| Check | Key Patterns |
|-------|--------------|
| recall_conflict | `⚠️ CONFLICT DETECTED`, `conflicting versions`, `[Claude]`, `[Codex]` |
| explain_crosshost | `Source:`, `Also written by:`, `Match Reasons:` |
| recall_provenance | `From Claude`, `From Codex` |
| injection_text | `(From Claude`, `(From Codex`, `⚠️ CONFLICT` |

### What Regression Gate Does NOT Check

- Exact string match (allows formatting variations)
- Performance/regression (only output correctness)
- New scenarios (only existing golden examples)

---

## CURRENTLY PROTECTED EXPERIENCES

| Experience | Phase | Protected |
|------------|-------|-----------|
| Conflict detection display | 6E | ✅ |
| Cross-host explain | 6E | ✅ |
| Provenance display | 6E | ✅ |
| Injection text | 6E | ✅ |

---

## SPECIFIED-ONLY (STILL NOT IMPLEMENTED)

These features are specified but not implemented, and are NOT covered by this regression gate:

| Feature | Spec | Reason |
|---------|------|--------|
| Semantic conflict detection | FR-050 | Would need embeddings |
| Group by source display | FR-049 | Phase 2 UX enhancement |
| User conflict resolution | FR-052 | UI layer |
| OpenClaw friendly name | FR-048 | OpenClaw BLOCKED |
| Real Claude system-prompt | N/A | Requires actual Claude Code env |
| Real Codex CLI output | N/A | Requires actual Codex env |

---

## REGRESSION GATE LIMITATIONS

### What This Gate Protects

- ✅ Conflict visibility in output
- ✅ Provenance (source/friendly/timestamp) in output
- ✅ Cross-host explain (also_written_by) in output
- ✅ Key pattern presence

### What This Gate Does NOT Protect

- ❌ Exact formatting (allows minor variations)
- ❌ Performance (not a performance test)
- ❌ New golden examples (only existing 4)
- ❌ New UX features (not scope of this task)

---

## NEXT STEPS

### Return to Main Line

This task was a guardrail to protect what was built. The project should return to the main development line:

1. **Primary focus**: Unified entry point / automatic memory experience
2. **Not output style engineering**: Golden examples are for protection, not expansion
3. **Main line features**: Continue with core product development

### Potential Future Work (Not in Scope)

- Semantic conflict detection (would need embeddings)
- Group by source display (Phase 2 UX)
- User conflict resolution UI
- OpenClaw unblock

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `run_regression_gate.py` | Main regression gate script |
| `regression_gate.md` | Full regression gate documentation |
| `evidence.md` | Evidence report |
| `known_limits.md` | This file |

---

**This regression gate is established but this is not the final product entry point**
**Next phase should return to unified entry point / automatic memory experience main line**

**Known limits are FINAL and binding for Phase 6G.**
**Phase 6G regression gate is complete and PASS.**
