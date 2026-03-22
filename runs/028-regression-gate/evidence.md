# OCMF Phase 6G - Regression Gate Evidence

**Run ID**: 028-regression-gate
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: REGRESSION GUARDRAIL

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **REGRESSION_GATE_READY** | **YES** |
| **GOLDEN_GUARDRAIL_ACTIVE** | **YES** |
| **Task Type** | REGRESSION_GUARDRAIL |

---

## TASK TYPE DEFINITION

### This is a REGRESSION GUARDRAIL task

**Purpose**: Protect already-implemented user-visible experiences from regression.

**What this task IS**:
- Regression testing of existing golden examples
- Comparing current output against stable baselines
- Classifying any detected differences
- Protecting existing user-visible features

**What this task is NOT**:
- New feature development
- New UX field additions
- New host capability exploration
- Expansion of golden example coverage

---

## PROTECTED EXPERIENCES

### User-Visible Experiences Being Protected

| Experience | Phase | What Users See |
|------------|-------|----------------|
| Conflict Detection Display | 6E | `⚠️ CONFLICT DETECTED` with candidates |
| Cross-Host Explain | 6E | `Also written by:`, `Source:`, `Match Reasons:` |
| Provenance Display | 6E | `From Claude (2026-03-22 01:35)` format |
| Injection Text | 6E | `(From Claude at HH:MM)` in context |

---

## REGRESSION GATE TEST RESULTS

```
$ python3 runs/028-regression-gate/run_regression_gate.py

======================================================================
CHECK: recall_conflict
======================================================================
✓ Golden file: .../recall_conflict_golden.txt
✓ Generated 375 chars
✓ Current output: .../recall_conflict_current.txt
Regression check: no_regression
✓ PASS: No regression detected

======================================================================
CHECK: explain_crosshost
======================================================================
✓ Golden file: .../explain_crosshost_golden.txt
✓ Generated 306 chars
✓ Current output: .../explain_crosshost_current.txt
Regression check: no_regression
✓ PASS: No regression detected

======================================================================
CHECK: recall_provenance
======================================================================
✓ Golden file: .../recall_provenance_golden.txt
✓ Generated 165 chars
✓ Current output: .../recall_provenance_current.txt
Regression check: no_regression
✓ PASS: No regression detected

======================================================================
CHECK: injection_text
======================================================================
✓ Golden file: .../injection_text_golden.txt
✓ Generated 965 chars
✓ Current output: .../injection_text_current.txt
Regression check: no_regression
✓ PASS: No regression detected

======================================================================
REGRESSION GATE SUMMARY
======================================================================
  ✓ recall_conflict: PASS
  ✓ explain_crosshost: PASS
  ✓ recall_provenance: PASS
  ✓ injection_text: PASS

✓ REGRESSION GATE: PASS
  All golden examples verified - no regression detected
```

---

## EVIDENCE BOUNDARY

### Implemented (API-Level, Phase 6D)

| Feature | Status | Evidence |
|---------|--------|----------|
| recall source_tool field | ✅ | API returns source_tool |
| recall source_host_friendly | ✅ | API returns friendly name |
| recall timestamp field | ✅ | API returns timestamp |
| recall conflict_detected | ✅ | API returns boolean |
| recall candidates | ✅ | API returns candidate list |
| explain match_reasons | ✅ | API returns match array |
| explain source_tool | ✅ | API returns source |
| explain also_written_by | ✅ | API returns cross-host context |

### Host-Visible Integrated (Phase 6E)

| Feature | Status | Evidence |
|---------|--------|----------|
| CLI recall output | ✅ | Friendly format with source |
| CLI explain output | ✅ | Friendly format with match_reasons |
| CLI conflict output | ✅ | ⚠️ CONFLICT DETECTED display |
| Injection text | ✅ | Source annotations included |
| Gist text | ✅ | Source brackets included |

### Stable Scenario Coverage (Phase 6F)

| Scenario | Status | Evidence |
|----------|--------|----------|
| Conflict detection stable | ✅ | `conflict_detected=True`, 2 candidates |
| Cross-host explain stable | ✅ | `also_written_by=['claude-code']` |
| Provenance display stable | ✅ | Source + timestamp format stable |
| Injection text stable | ✅ | (From Claude at HH:MM) format |

### Regression Gate (Phase 6G - This Task)

| Check | Status | Evidence |
|-------|--------|----------|
| recall_conflict regression | ✅ PASS | Key patterns present |
| explain_crosshost regression | ✅ PASS | Key patterns present |
| recall_provenance regression | ✅ PASS | Key patterns present |
| injection_text regression | ✅ PASS | Key patterns present |

### Specified-Only (Not Implemented)

| Feature | Reason |
|---------|--------|
| Semantic conflict detection | Would need embeddings |
| Group by source display | Phase 2 UX enhancement |
| User conflict resolution UI | UI layer |
| OpenClaw friendly name | OpenClaw BLOCKED |

---

## FILES GENERATED

| File | Purpose |
|------|---------|
| `run_regression_gate.py` | Main regression gate script |
| `regression_gate.md` | Regression gate documentation |
| `evidence.md` | This file |
| `known_limits.md` | Limits documentation |
| `recall_conflict_current.txt` | Current output snapshot |
| `explain_crosshost_current.txt` | Current output snapshot |
| `recall_provenance_current.txt` | Current output snapshot |
| `injection_text_current.txt` | Current output snapshot |

---

## REGRESSION GATE READY

The regression gate is now ACTIVE and can be used to:

1. **Prevent regressions**: Run before commits to ensure no regression
2. **Detect drift**: Identify when output format changes
3. **Classify issues**: Categorize regressions by type
4. **Protect experiences**: Ensure user-visible features remain intact

---

**FINAL_STATUS: PASS**
**REGRESSION_GATE_READY: YES**
**GOLDEN_GUARDRAIL_ACTIVE: YES**
**Task Type: REGRESSION_GUARDRAIL**
