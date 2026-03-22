# OCMF Phase 6F - Stable Host-Visible Golden Examples Known Limits

**Run ID**: 027-stable-golden-examples
**Date**: 2026-03-22
**Status**: PASS

---

## FINAL STATUS: PASS

---

## PHASE 6F - KNOWN LIMITS

### Stably Covered Scenarios (Phase 6F)

| Scenario | Status | Evidence |
|----------|--------|----------|
| Conflict detection | ✅ Stable | `conflict_detected=True`, 2 candidates |
| Conflict CLI display | ✅ Stable | `⚠️ CONFLICT DETECTED` format |
| Cross-host explain | ✅ Stable | `also_written_by=['claude-code']` |
| Explain provenance | ✅ Stable | `Source: Codex` format |
| Explain match_reasons | ✅ Stable | `Keyword match: testing, framework` |
| Provenance display | ✅ Stable | `From Claude (2026-03-22 01:35)` format |
| Injection text | ✅ Stable | `(From Claude at HH:MM)` format |

### Not Yet Stable / Not Covered

| Scenario | Status | Reason |
|----------|--------|--------|
| Semantic conflict detection | ❌ Not stable | Would need embeddings |
| Group by source display | ❌ Not covered | Phase 2 UX enhancement |
| User conflict resolution UI | ❌ Not covered | UI layer, not API |
| OpenClaw friendly name | ❌ BLOCKED | OpenClaw is BLOCKED |
| Real Claude system-prompt | ❌ Not covered | Requires actual Claude Code env |
| Real Codex CLI output | ❌ Not covered | Requires actual Codex env |

---

## CONFLICT DETECTION ALGORITHM LIMITS

### Current Approach: Title-Based Entity Matching

| Aspect | Status | Notes |
|--------|--------|-------|
| Same title, different content | ✅ Stable | Works reliably |
| Same content, different title | ❌ Not detected | Different entities |
| Semantic similarity | ❌ Not implemented | Would need embeddings |

### Mitigation

The title-based approach is sufficient for MVP. Semantic similarity can be added as Phase 2 enhancement.

---

## STABLE SCENARIO COVERAGE

### Golden Examples Status

| Golden File | Scenario | Stable |
|-------------|----------|--------|
| `recall_conflict_golden.txt` | Conflict detection + display | ✅ Yes |
| `explain_crosshost_golden.txt` | Cross-host explain | ✅ Yes |
| `recall_provenance_golden.txt` | Provenance display | ✅ Yes |
| `injection_text_golden.txt` | Injection text | ✅ Yes |

### Regression Readiness

Golden examples can serve as baseline for regression testing. Any output format changes would be detected by comparing against golden files.

---

## EVIDENCE BOUNDARY SUMMARY

| Category | Coverage | Notes |
|----------|----------|-------|
| API-level implemented | 8/8 fields | All Phase 6D fields |
| Host-visible integrated | 5/5 features | All Phase 6E features |
| Stable scenario coverage | 4/4 scenarios | All Phase 6F scenarios |
| Specified-only | 4 items | Deferred to Phase 2 |

---

## RECOMMENDED NEXT STEPS

### P0 (Must have)

1. **OpenClaw unblock**: When GitHub release is fixed
2. **Real host integration**: Actual Claude/Codex environment test

### P1 (Should have for Phase 2)

1. **Semantic conflict detection**: Add embeddings for better detection
2. **Group by source display**: FR-049 implementation
3. **User resolution UX**: FR-052 implementation

### P2 (Nice to have)

1. **Visual distinction per source**: Icons/colors
2. **Auto-merge suggestions**: For conflicts
3. **Source priority configuration**: User-configurable

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `generate_golden_examples.py` | Golden examples generator |
| `recall_conflict_golden.txt` | Conflict scenario golden |
| `explain_crosshost_golden.txt` | Cross-host explain golden |
| `recall_provenance_golden.txt` | Provenance display golden |
| `injection_text_golden.txt` | Injection text golden |
| `evidence.md` | This file (coverage summary) |
| `known_limits.md` | This file (limits documentation) |

---

**Known limits are FINAL and binding for Phase 6F.**
**Phase 6F implementation is complete and passing.**
**All golden examples are stable and reproducible.**
