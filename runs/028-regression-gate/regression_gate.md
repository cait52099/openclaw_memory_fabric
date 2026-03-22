# OCMF Phase 6G - Regression Gate Documentation

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

## TASK TYPE: REGRESSION GUARDRAIL

This is a **GUARDRAIL task**, not a feature expansion task.

**Purpose**: Protect the already-implemented user-visible experiences from regression.

**What this task IS**:
- ✅ Regression testing of existing golden examples
- ✅ Comparing current output against stable baselines
- ✅ Classifying any detected differences
- ✅ Protecting existing user-visible features

**What this task is NOT**:
- ❌ New feature development
- ❌ New UX field additions
- ❌ New host capability exploration
- ❌ Expansion of golden example coverage
- ❌ Output style engineering

---

## REGRESSION GATE CHECKS

### Golden Files Covered

| Golden File | Scenario | Status |
|-------------|----------|--------|
| `recall_conflict_golden.txt` | Conflict detection + display | ✅ PASS |
| `explain_crosshost_golden.txt` | Cross-host explain | ✅ PASS |
| `recall_provenance_golden.txt` | Provenance display | ✅ PASS |
| `injection_text_golden.txt` | Injection text | ✅ PASS |

### Regression Types Detected

| Type | Classification | Action |
|------|----------------|--------|
| `no_regression` | All key patterns present | PASS |
| `formatting_drift` | Layout changed but content intact | Review needed |
| `provenance_regression` | Source/friendly/timestamp missing | FAIL |
| `conflict_visibility_regression` | ⚠️ CONFLICT or candidates missing | FAIL |
| `explain_visibility_regression` | Match reasons or also_written_by missing | FAIL |

---

## REGRESSION GATE TEST RESULTS

```
$ python3 runs/028-regression-gate/run_regression_gate.py

✓ recall_conflict: PASS
✓ explain_crosshost: PASS
✓ recall_provenance: PASS
✓ injection_text: PASS

✓ REGRESSION GATE: PASS
  All golden examples verified - no regression detected
```

---

## PROTECTED USER-VISIBLE EXPERIENCES

### 1. Conflict Detection Display

**What users see**:
```
⚠️ CONFLICT DETECTED
  2 conflicting versions found:
  - [Codex] "Testing framework: unittest is built-in and works "
  - [Claude] "Testing framework: pytest is the best for unit tes"
```

**Key patterns checked**:
- `⚠️ CONFLICT DETECTED`
- `conflicting versions`
- `[Claude]`, `[Codex]`

### 2. Cross-Host Explain

**What users see**:
```
## Memory Explanation

Source: Codex
Timestamp: 2026-03-22 01:35

Match Reasons:
  • Keyword match: testing, framework
  • Scope match: project=golden_test_project

Also written by: claude-code

Matched keywords: testing, framework; Source: Codex; Also written by: Claude
```

**Key patterns checked**:
- `Source:`
- `Also written by:`
- `Match Reasons:`

### 3. Provenance Display

**What users see**:
```
Found 2 memories:
  From Codex: "Testing framework: unittest is built-in and works " (2026-03-22 01:35)
  From Claude: "Testing framework: pytest is the best for unit tes" (2026-03-22 01:35)
```

**Key patterns checked**:
- `From Claude`
- `From Codex`

### 4. Injection Text

**What users see**:
```
## Relevant Context

### Testing framework
(From Codex at 01:35)
Summary: Unittest recommended

### Testing framework
(From Claude at 01:35)
Summary: Pytest recommended

⚠️ CONFLICT DETECTED
Multiple versions found (2 conflicting memories):
  - [Codex] "Testing framework: unittest is built-in and works well"
  - [Claude] "Testing framework: pytest is the best for unit testing in Python"
```

**Key patterns checked**:
- `(From Claude` or `(From Codex`
- `⚠️ CONFLICT`

---

## REGRESSION GATE EXECUTION

### Command

```bash
python3 runs/028-regression-gate/run_regression_gate.py
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All golden examples verified - no regression |
| 1 | Regression detected - see output for details |

### Output Files

| File | Purpose |
|------|---------|
| `run_regression_gate.py` | Main regression gate script |
| `recall_conflict_current.txt` | Current recall_conflict output |
| `explain_crosshost_current.txt` | Current explain_crosshost output |
| `recall_provenance_current.txt` | Current recall_provenance output |
| `injection_text_current.txt` | Current injection_text output |

---

## INTEGRATION WITH CI/CD

To integrate this regression gate into CI/CD:

```bash
#!/bin/bash
# regression_gate.sh

echo "Running OCMF Regression Gate..."
python3 runs/028-regression-gate/run_regression_gate.py
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ REGRESSION DETECTED"
    echo "   See runs/028-regression-gate/ for details"
    exit 1
fi

echo "✅ REGRESSION GATE: PASS"
exit 0
```

---

## NEXT STEPS

This regression gate protects existing experiences. The project should continue with:

1. **Main line focus**: Unified entry point / automatic memory experience
2. **Not output style engineering**: The golden examples are for protection, not expansion
3. **Return to main path**: When ready, continue with main product features

---

**This is a GUARDRAIL task**
**Status: REGRESSION_GATE_READY: YES**
**Golden guardrail is ACTIVE and protecting user-visible experiences**
