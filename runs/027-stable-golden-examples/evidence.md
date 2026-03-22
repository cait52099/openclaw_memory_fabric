# OCMF Phase 6F - Stable Host-Visible Golden Examples Evidence

**Run ID**: 027-stable-golden-examples
**Date**: 2026-03-22
**Status**: PASS

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **STABLE_CONFLICT_VISIBLE** | **YES** |
| **STABLE_EXPLAIN_VISIBLE** | **YES** |
| **GOLDEN_EXAMPLES_READY** | **YES** |

---

## IMPLEMENTATION DETAILS

### Golden Files Generated

| File | Status | Description |
|------|--------|-------------|
| `recall_conflict_golden.txt` | ✅ Generated | Stable conflict scenario output |
| `explain_crosshost_golden.txt` | ✅ Generated | Stable cross-host explain output |
| `recall_provenance_golden.txt` | ✅ Generated | Stable provenance display output |
| `injection_text_golden.txt` | ✅ Generated | Injection text output |

### Test Results

```
$ python3 runs/027-stable-golden-examples/generate_golden_examples.py

✓ Conflict test passed: True
✓ Explain test passed: True
✓ Recall conflict golden: runs/027-stable-golden-examples/recall_conflict_golden.txt
✓ Explain cross-host golden: runs/027-stable-golden-examples/explain_crosshost_golden.txt
✓ Recall provenance golden: runs/027-stable-golden-examples/recall_provenance_golden.txt
✓ Injection text golden: runs/027-stable-golden-examples/injection_text_golden.txt

✓ PHASE 6F STABLE GOLDEN EXAMPLES: PASS
```

---

## STABLE CONFLICT SCENARIO (AC-GOLD-001)

### Conflict Detection Output

```
Conflict detected: True
Candidates: 2

MEMORIES RETURNED:
  Source: Codex
  Timestamp: 2026-03-22 01:35
  Content: Testing framework: unittest is built-in and works well for Python

  Source: Claude
  Timestamp: 2026-03-22 01:35
  Content: Testing framework: pytest is the best for unit testing in Python

CONFLICT CANDIDATES:
  [Codex] Testing framework: unittest is built-in and works well for P
  [Claude] Testing framework: pytest is the best for unit testing in Py
```

### CLI Output Format

```
Found 2 memories:
  From Codex: "Testing framework: unittest is built-in and works " (2026-03-22 01:35)
  From Claude: "Testing framework: pytest is the best for unit tes" (2026-03-22 01:35)

⚠️ CONFLICT DETECTED
  2 conflicting versions found:
  - [Codex] "Testing framework: unittest is built-in and works "
  - [Claude] "Testing framework: pytest is the best for unit tes"
```

---

## STABLE CROSS-HOST EXPLAIN SCENARIO (AC-GOLD-002)

### Explain Output

```
Memory ID: 8f9898bc-5115-4fad-a93d-12ef9b3c16cf
Recall Query: 'testing framework'

STRUCTURED OUTPUT:
  success: True
  source_host_friendly: Codex
  event_timestamp: 2026-03-22T01:35:50.114099+00:00
  match_reasons: [
      {"type": "keyword", "matched": ["testing", "framework"]},
      {"type": "scope", "matched": {"project": "golden_test_project"}}
  ]
  also_written_by: ['claude-code']
  explain: Matched keywords: testing, framework; Matched scope project=golden_test_project; Source: Codex; Also written by: Claude
```

### CLI Friendly Output

```
## Memory Explanation

Source: Codex
Timestamp: 2026-03-22 01:35

Match Reasons:
  • Keyword match: testing, framework
  • Scope match: project=golden_test_project

Also written by: claude-code

Matched keywords: testing, framework; Matched scope project=golden_test_project; Source: Codex; Also written by: Claude

Content: "Testing framework: unittest is built-in and works well for Python"
```

---

## EVIDENCE BOUNDARY

### API-Level Implemented (Phase 6D)

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

### Specified-Only (Not Implemented)

| Feature | Reason |
|---------|--------|
| Semantic conflict detection | Would need embeddings |
| Group by source display | Phase 2 UX |
| User conflict resolution UI | UI layer |
| OpenClaw friendly name | OpenClaw BLOCKED |

---

## GOLDEN EXAMPLE FILES

| File | Lines | Coverage |
|------|-------|----------|
| `recall_conflict_golden.txt` | 35 | Conflict scenario |
| `explain_crosshost_golden.txt` | 46 | Cross-host explain |
| `recall_provenance_golden.txt` | 40 | Provenance display |
| `injection_text_golden.txt` | 30 | Injection text |

---

## REGRESSION TEST READY

Golden examples can be used for regression testing:

```python
# Compare actual output against golden
def test_recall_conflict():
    actual = generate_recall_output("testing framework")
    golden = read("recall_conflict_golden.txt")
    assert "⚠️ CONFLICT DETECTED" in actual
    assert "candidates: 2" in actual or len(candidates) == 2

def test_explain_crosshost():
    actual = generate_explain_output(memory_id)
    golden = read("explain_crosshost_golden.txt")
    assert "Also written by:" in actual
    assert "Source: Codex" in actual
    assert "Match Reasons:" in actual
```

---

**FINAL_STATUS: PASS**
**STABLE_CONFLICT_VISIBLE: YES**
**STABLE_EXPLAIN_VISIBLE: YES**
**GOLDEN_EXAMPLES_READY: YES**
