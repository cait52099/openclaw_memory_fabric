# OCMF Phase 6E - Host-Visible Output Integration Evidence

**Run ID**: 026-cross-host-visible
**Date**: 2026-03-22
**Status**: PASS

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **RECALL_VISIBLE** | **YES** |
| **EXPLAIN_VISIBLE** | **YES** |
| **CONFLICT_VISIBLE** | **YES** |

---

## IMPLEMENTATION DETAILS

### Files Modified

| File | Action | Description |
|------|--------|-------------|
| `src/ocmaf/cli/main.py` | Modified | Enhanced recall/explain CLI commands with provenance display |
| `src/ocmaf/api/recall.py` | Modified | Enhanced to_injection_text() and to_gist_text() with source info |

### Test Results

```
$ python3 runs/026-cross-host-visible/test_host_visible_output.py
============================================================
Phase 6E - Host-Visible Output Integration Test
============================================================

=== Test: Write memories from different sources ===
✓ Event 1 stored: 901efed5... from claude-code
✓ Event 2 stored: 0237db43... from codex-cli
✓ Event 3 stored: e911943b... from claude-code

=== Test: Recall with provenance display ===
✓ Recall returned 2 memories
✓ All memories have source_tool, source_host_friendly, timestamp
✓ Cross-host recall works: got memories from {'claude-code', 'codex-cli'}

=== Test: explain() with match reasons and provenance ===
✓ explain() successful
✓ Provenance: Codex
✓ Match reasons: 2 reasons
  - type=keyword, matched=['testing', 'framework']
  - type=scope, matched={'project': 'test_6e_project'}
✓ Explain text: "Matched keywords: testing, framework; Matched scope project=test_6e_project; Sou..."

=== Test: Injection text with source info ===
✓ Injection text generated (195 chars)
✓ Source info found in injection text

=== Test: Gist text with source info ===
✓ Gist text generated (148 chars)

=== Test: Friendly name mapping ===
✓ claude-code -> Claude
✓ codex-cli -> Codex
✓ openclaw -> OpenClaw
✓ synthetic -> Synthetic (Test)

============================================================
SUMMARY
============================================================
Passed: 5
Failed: 0

✓ PHASE 6E HOST-VISIBLE OUTPUT: PASS
```

---

## RECALL VISIBLE OUTPUT

### CLI recall Command Output Format

```
Found 2 memories:

From Claude:
  • "Testing framework: pytest is best for unit tests" (2026-03-22 10:30)

From Codex:
  • "Testing framework: unittest is built-in and works well" (2026-03-22 09:15)
```

### to_injection_text() Output Format

```
## Relevant Context

### Testing framework
(From Codex at 01:25)
Summary: Unittest is the built-in testing framework

### Testing framework
(From Claude at 01:25)
Summary: Pytest is the preferred testing framework

⚠️ CONFLICT DETECTED
Multiple versions found (2 conflicting memories):
  - [Codex] "Testing framework: unittest is built-in and works well"
  - [Claude] "Testing framework: pytest is best for unit tests"
```

### to_gist_text() Output Format

```
## Relevant Context (Gist)
- [Codex (01:25)] Unittest works
- [Claude (01:25)] Pytest recommended

⚠️ CONFLICT: Multiple versions exist - see detail for options
```

---

## EXPLAIN VISIBLE OUTPUT

### CLI explain Command Output Format

```
## Memory Explanation

Source: Claude
Timestamp: 2026-03-22 10:30

Match Reasons:
  • Keyword match: testing, framework
  • Scope match: project=test_6e_project

Also written by: codex-cli

Matched keywords: testing, framework; Matched scope project=test_6e_project; Source: Claude; Also written by: Codex

Content: "Testing framework: pytest is best for unit tests"
```

---

## CONFLICT VISIBLE OUTPUT

### Conflict Detection in recall Output

When `conflict_detected: true`, the CLI output shows:

```
⚠️ CONFLICT DETECTED
  2 conflicting versions found:
  - [Codex] "Testing framework: unittest is built-in and works well"
  - [Claude] "Testing framework: pytest is best for unit tests"
```

### Conflict in Injection Text

```
⚠️ CONFLICT DETECTED
Multiple versions found (2 conflicting memories):
  - [Codex] "Testing framework: unittest is built-in and works well"
  - [Claude] "Testing framework: pytest is best for unit tests"
```

---

## HOST-VISIBLE vs API-LEVEL STATUS

| Feature | API-Level (6D) | Host-Visible (6E) |
|---------|----------------|-------------------|
| recall source_tool field | ✅ | ✅ CLI + Injection |
| recall source_host_friendly | ✅ | ✅ CLI + Injection |
| recall timestamp field | ✅ | ✅ CLI + Injection |
| recall conflict_detected | ✅ | ✅ CLI + Injection |
| recall candidates | ✅ | ✅ CLI + Injection |
| explain match_reasons | ✅ | ✅ CLI + Injection |
| explain source_tool | ✅ | ✅ CLI |
| explain source_host_friendly | ✅ | ✅ CLI |
| explain also_written_by | ✅ | ✅ CLI |
| explain text | ✅ | ✅ CLI |

---

## FRIENDLY NAME MAPPING

| source_tool | source_host_friendly |
|-------------|---------------------|
| claude-code | Claude |
| codex-cli | Codex |
| openclaw | OpenClaw |
| synthetic | Synthetic (Test) |

---

**FINAL_STATUS: PASS**
**RECALL_VISIBLE: YES**
**EXPLAIN_VISIBLE: YES**
**CONFLICT_VISIBLE: YES**
