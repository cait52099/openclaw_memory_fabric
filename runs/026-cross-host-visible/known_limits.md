# OCMF Phase 6E - Host-Visible Output Integration Known Limits

**Run ID**: 026-cross-host-visible
**Date**: 2026-03-22
**Status**: PASS

---

## FINAL STATUS: PASS

---

## PHASE 6E - KNOWN LIMITS

### Implemented (Phase 6E - Host-Visible)

| Feature | Status | Notes |
|---------|--------|-------|
| CLI recall source_tool display | ✅ Implemented | Shows source in output |
| CLI recall friendly name display | ✅ Implemented | Shows "From Claude" / "From Codex" |
| CLI recall timestamp display | ✅ Implemented | Shows (2026-03-22 10:30) format |
| CLI recall JSON format | ✅ Implemented | --format=json option |
| CLI explain provenance display | ✅ Implemented | Source, timestamp, match_reasons |
| CLI explain match_reasons | ✅ Implemented | Shows keyword + scope matches |
| CLI explain also_written_by | ✅ Implemented | Cross-host context |
| to_injection_text() source info | ✅ Implemented | "(From Claude at HH:MM)" format |
| to_gist_text() source info | ✅ Implemented | "[Claude (HH:MM)]" format |
| Conflict CLI display | ✅ Implemented | ⚠️ CONFLICT DETECTED + candidates |
| Conflict injection text | ✅ Implemented | ⚠️ CONFLICT DETECTED block |

### NOT Implemented (Phase 6E)

| Feature | Spec Reference | Reason |
|---------|---------------|--------|
| Claude system-prompt integration | T-6E-04~06 | Requires actual Claude Code environment |
| Group by source display | FR-049 | Phase 2 UX enhancement |
| User conflict resolution UI | FR-052 | UI layer, not API |

### Deferred from Phase 6D

| Feature | Reason |
|---------|--------|
| Semantic conflict detection | Would need embeddings |
| also_written_by detailed context | Simplified for MVP |
| OpenClaw friendly name | OpenClaw is BLOCKED |

---

## CURRENT LIMITATIONS

### 1. CLI Output Format

**Current approach**: Text-based output with provenance annotations

| Aspect | Status | Notes |
|--------|--------|-------|
| Source info in recall | ✅ Works | "(From Claude at 10:30)" |
| Source info in explain | ✅ Works | "Source: Claude" |
| Source info in injection | ✅ Works | "(From Claude at HH:MM)" |
| JSON format available | ✅ Works | --format=json flag |

### 2. Conflict Detection

**Current approach**: Title-based entity matching (same as Phase 6D)

| Aspect | Status | Notes |
|--------|--------|-------|
| Same title, different content | ✅ Detected | Works |
| Same content, different title | ❌ Not detected | Different entities |
| Semantic similarity | ❌ Not implemented | Would need embeddings |

### 3. Injection Text Length

| Aspect | Status | Notes |
|--------|--------|-------|
| Truncation at 2000 chars | ✅ Works | "... (truncated)" |
| Memory limit in gist | ✅ Works | max_memories=3 default |

---

## HOST-VISIBLE OUTPUT SPEC STATUS

| Component | Status | Implementation |
|-----------|--------|----------------|
| Provenance display (FR-047) | ✅ Spec → ✅ Impl | CLI + Injection text |
| Friendly name mapping (FR-048) | ✅ Spec → ✅ Impl | All known sources |
| Group by source (FR-049) | ❌ Not implemented | Phase 2 UX |
| Conflict detection (FR-050) | ✅ Spec → ✅ Impl | conflict_detected + candidates |
| Conflict response (FR-051) | ✅ Spec → ✅ Impl | candidates array |
| User resolution (FR-052) | N/A | UX decision |
| explain() match_reasons (FR-053) | ✅ Spec → ✅ Impl | keyword/scope matches |
| explain() provenance (FR-054) | ✅ Spec → ✅ Impl | source_tool + friendly |
| Cross-host explain (FR-055) | ✅ Spec → ✅ Impl | also_written_by |

---

## SUMMARY TABLE

| Category | Host-Visible (6E) | API-Level (6D) | Spec-Only |
|----------|------------------|----------------|-----------|
| recall output fields | 5/5 | 5/5 | 0 |
| explain output fields | 6/6 | 6/6 | 0 |
| conflict detection | ✅ | ✅ | - |
| CLI format output | ✅ | N/A | - |
| Injection text output | ✅ | N/A | - |

---

## RECOMMENDED NEXT STEPS

### P0 (Must have for Phase 7)

1. **OpenClaw verification**: Unblock when GitHub release is fixed
2. **Claude system-prompt integration**: Actual Claude Code environment test

### P1 (Should have for Phase 2)

1. **Group by source display**: Implement FR-049
2. **Semantic conflict detection**: Enhancement for better conflict detection
3. **User resolution UX**: Implement FR-052

### P2 (Nice to have)

1. **Visual distinction per source**: Icons/colors
2. **Auto-merge suggestions**: For conflicts
3. **Source priority configuration**: User-configurable

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `test_host_visible_output.py` | Integration test with all passing |
| `evidence.md` | Full evidence report |
| `known_limits.md` | This file |

---

**Known limits are FINAL and binding for Phase 6E.**
**Phase 6E implementation is complete and passing.**
