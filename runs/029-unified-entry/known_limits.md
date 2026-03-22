# OCMF Phase 7A/7B Known Limits

**Run ID**: 029-unified-entry
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## THIS IS A PRODUCT MAINLINE TASK

**Important**: This task continues the main product development line, NOT a guardrail or exploratory task.

### Mainline Purpose

Phase 7A/7B delivers:
- Unified entry point for Claude and Codex
- Automatic memory experience (zero-command usage)
- Regression gate integration for continuous quality

### What This Task IS

- ✓ Unified CLI interface
- ✓ Auto-memory implementation
- ✓ Host setup scripts
- ✓ Regression gate attachment

### What This Task is NOT

- ❌ New feature exploration
- ❌ OpenClaw unblock
- ❌ Web UI
- ❌ replay/eval

---

## CURRENTLY IMPLEMENTED

### Unified Entry Point

| Feature | Status | Evidence |
|---------|--------|----------|
| Unified CLI (`ocmaf unified`) | ✓ | `src/ocmaf/cli/unified.py` |
| Host auto-detection | ✓ | `src/ocmaf/cli/host_detection.py` |
| Claude setup script | ✓ | `src/ocmaf/hosts/claude_setup.sh` |
| Codex setup script | ✓ | `src/ocmaf/hosts/codex_setup.sh` |

### Automatic Memory

| Feature | Status | Evidence |
|---------|--------|----------|
| Auto-memory behavior spec | ✓ | `docs/auto_memory_behavior.md` |
| Auto-recall (level 1,3) | ✓ | `src/ocmaf/api/auto_recall.py` |
| Auto-remember (level 2,3) | ✓ | `src/ocmaf/api/auto_remember.py` |
| Quickstart documentation | ✓ | `docs/quickstart.md` |

### Host Coverage

| Host | Method | Unified Entry | Auto-Memory |
|------|--------|---------------|-------------|
| Claude | A1+B | ✓ Supported | ✓ Supported |
| Codex | C | ✓ Supported | ✗ Manual only |
| OpenClaw | BLOCKED | ⚠️ Blocked | ⚠️ Blocked |

---

## CURRENT LIMITATIONS

### OpenClaw Blocked

**Reason**: GitHub release returns 404

**Impact**: OpenClaw users cannot use OCMF

**Workaround**: Use Claude or Codex instead

**Resolution**: Requires OpenClaw GitHub release to become available

### Codex Auto-Memory Not Supported

**Reason**: Method C (manual MCP) doesn't support automatic triggers

**Impact**: Codex users must manually run recall/remember

**Workaround**: Run `ocmaf recall` and `ocmaf remember` commands

**Resolution**: Would need Codex to support native hooks (Method A/B)

### Auto-Remember Extraction is Basic

**Reason**: Keyword-based extraction is simple

**Impact**: May miss nuanced decisions or facts

**Workaround**: Manual `ocmaf remember` for important content

**Resolution**: Future could use LLM for better extraction

---

## REGRESSION GATE STATUS

### Gate Established

| Check | Status | Evidence |
|-------|--------|----------|
| Regression gate script | ✓ Ready | `runs/028-regression-gate/run_regression_gate.py` |
| Golden examples | ✓ 4 files | Covered by Phase 6F |
| Gate integration | ✓ Attached | `ops/integrated_gate.sh` |

### What Gate Protects

- ✓ Conflict visibility in output
- ✓ Provenance (source/friendly/timestamp) in output
- ✓ Cross-host explain (also_written_by) in output
- ✓ Key pattern presence

### What Gate Does NOT Protect

- ❌ Auto-memory behavior
- ❌ Unified CLI interface
- ❌ New features (only existing golden examples)

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

These features are specified but not implemented:

| Feature | Spec | Reason |
|---------|------|--------|
| Semantic conflict detection | FR-050 | Would need embeddings |
| Group by source display | FR-049 | Phase 2 UX enhancement |
| User conflict resolution | FR-052 | UI layer |
| OpenClaw friendly name | FR-048 | OpenClaw BLOCKED |

---

## PATH FORWARD

### Immediate Next Steps

1. **User Testing**: Have users try unified entry + auto-memory
2. **Bug Fixes**: Address any issues found
3. **Documentation**: Expand quickstart as needed

### Future Work (Not in Scope)

1. OpenClaw unblock (waiting on GitHub release)
2. Semantic conflict detection (would need embeddings)
3. Group by source display (Phase 2 UX)
4. User conflict resolution UI

---

## PRODUCT LINE STATUS

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 6G | ✓ Complete | Regression guardrail established |
| Phase 7A | ✓ Complete | Unified entry point |
| Phase 7B | ✓ Complete | Automatic memory experience |

**Next Phase**: Return to main line - unified entry + auto-memory as primary product

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/029-unified-entry/evidence.md` | Full evidence report |
| `runs/029-unified-entry/validation.md` | Validation results |
| `runs/029-unified-entry/known_limits.md` | This file |

---

**Phase 7A/7B is COMPLETE**
**Product mainline ready for user testing**
