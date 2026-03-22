# OCMF Phase 6D - Cross-Host UX Output Implementation Known Limits

**Run ID**: 025-cross-host-ux-output
**Date**: 2026-03-22
**Status**: PASS

---

## FINAL STATUS: PASS

---

## PHASE 6D - KNOWN LIMITS

### Implemented (Phase 6D)

| Feature | Status | Notes |
|---------|--------|-------|
| recall source_tool field | ✅ Implemented | Returns source_tool per memory |
| recall source_host_friendly | ✅ Implemented | Maps to friendly name |
| recall timestamp field | ✅ Implemented | Returns event timestamp |
| recall conflict_detected | ✅ Implemented | Boolean flag |
| recall candidates | ✅ Implemented | Array of conflicting memories |
| explain match_reasons | ✅ Implemented | keyword + scope matches |
| explain source_tool | ✅ Implemented | Provenance |
| explain source_host_friendly | ✅ Implemented | Friendly name |
| explain also_written_by | ✅ Implemented | Cross-host context |
| explain explain text | ✅ Implemented | Human-readable |

### NOT Implemented (Phase 6D)

| Feature | Spec Reference | Reason |
|---------|---------------|--------|
| Group by source display | FR-049 | Phase 2 UX enhancement |
| User conflict resolution UI | FR-052 | UI layer, not API |
| also_written_by detailed context | FR-055 | Simplified for MVP |

---

## CURRENT LIMITATIONS

### 1. Conflict Detection Algorithm

**Current approach**: Title-based entity matching

| Aspect | Status | Notes |
|--------|--------|-------|
| Same title, different content | ✅ Detected | Works |
| Same content, different title | ❌ Not detected | Different entities |
| Semantic similarity | ❌ Not implemented | Would need embeddings |

**Mitigation**: The current title-based approach is sufficient for MVP. Semantic similarity can be added as Phase 2 enhancement.

### 2. also_written_by Query

**Current approach**: Queries same project for memories with same title

| Aspect | Status | Notes |
|--------|--------|-------|
| Same project, same title | ✅ Works | Basic cross-host detection |
| Cross-project detection | ❌ Not supported | By design (project isolation) |
| Performance | ⚠️ O(n) scan | Can be optimized with index |

### 3. match_reasons Coverage

| Match Type | Status | Notes |
|------------|--------|-------|
| keyword match | ✅ Implemented | Extracts from query |
| scope match (project) | ✅ Implemented | Returns project |
| scope match (session) | ✅ Implemented | Returns session |
| time-based match | ❌ Not implemented | Could add recency scoring |

---

## OPENCLAW STATUS (from Phase 6B)

| Check | Result | Evidence |
|-------|--------|----------|
| OpenClaw real host proof | ❌ BLOCKED | GitHub release 404 |
| OpenClaw production path | ❌ TBD | Cannot determine |
| OpenClaw method boundary | ❌ TBD | Cannot determine |

**Action Required**: OpenClaw team must fix GitHub release assets.

---

## CROSS-HOST UX SPEC STATUS

| Component | Status | Implementation |
|-----------|--------|----------------|
| Provenance display | ✅ Spec → ✅ Impl | FR-047 + recall output |
| Friendly name mapping | ✅ Spec → ✅ Impl | FR-048 + friendly.py |
| Conflict detection | ✅ Spec → ✅ Impl | FR-050 + _detect_conflicts |
| Conflict response | ✅ Spec → ✅ Impl | FR-051 + candidates |
| explain match_reasons | ✅ Spec → ✅ Impl | FR-053 + match_reasons |
| explain provenance | ✅ Spec → ✅ Impl | FR-054 + source_tool |
| Cross-host explain | ✅ Spec → ✅ Impl | FR-055 + also_written_by |

### NOT IMPLEMENTED (but specified)

| Component | Spec | Reason |
|-----------|------|--------|
| Group by source | FR-049 | Phase 2 UX |
| User resolution | FR-052 | UI layer |
| Source priority config | Nice to have | Phase 2 |

---

## SUMMARY TABLE

| Category | Implemented | Not Implemented |
|----------|-------------|-----------------|
| recall output fields | 5 (source_tool, friendly, timestamp, conflict_detected, candidates) | 0 |
| explain output fields | 6 (match_reasons, source_tool, friendly, timestamp, also_written_by, explain text) | 0 |
| conflict detection | ✅ Minimal implementation | Can be enhanced |
| friendly name mapping | ✅ All known sources | OpenClaw TBD |

---

## RECOMMENDED NEXT STEPS

### P0 (Must have for Phase 2)

1. **OpenClaw verification**: Unblock when GitHub release is fixed
2. **UI layer for conflict resolution**: Implement FR-052 user decision flow

### P1 (Should have for Phase 2)

1. **Group by source display**: Implement FR-049
2. **Semantic conflict detection**: Enhancement for better conflict detection
3. **Performance optimization**: Index also_written_by queries

### P2 (Nice to have)

1. **Visual distinction per source**: Icons/colors
2. **Auto-merge suggestions**: For conflicts
3. **Source priority configuration**: User-configurable

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `test_recall_explain.py` | Test script with all passing |
| `evidence.md` | Full evidence report |
| `known_limits.md` | This file |

---

**Known limits are FINAL and binding for Phase 6D.**
**Phase 6D implementation is complete and passing.**
