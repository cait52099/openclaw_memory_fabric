# OCMF Phase 039 Evidence

**Run ID**: 039-switching-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **SWITCHING_REPEATABLE_3X** | **YES** |
| **CLAUDE_CODEX_CLAUDE_STABLE** | **YES** |
| **USER_JOURNEY_READY_TO_RECHECK** | **YES** |

---

## CATEGORIZATION

### Install Closure (Phase 031/032)

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude MCP wiring | ✓ FIXED | runs/031-install-closure/install_closure.md |
| Codex MCP wiring | ✓ FIXED | runs/031-install-closure/install_closure.md |
| OCMF_SOURCE_TOOL fallback | ✓ FIXED | runs/032-install-closure-final/install_closure_final.md |

### User Journey (Phase 036-039)

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude clean-home first-use | ✓ PASS | runs/039-switching-fix/switching_repeatability.md |
| Codex clean-home first-use | ✓ PASS | runs/039-switching-fix/switching_repeatability.md |
| Claude → Codex switch | ✓ PASS | runs/039-switching-fix/switching_repeatability.md |
| Codex → Claude switch | ✓ PASS | runs/039-switching-fix/switching_repeatability.md |
| Switching 3x repeatability | ✓ PASS | runs/039-switching-fix/switching_repeatability.md |

### Code Fix (Phase 039)

| File | Change | Evidence |
|------|--------|----------|
| claude_setup.sh | Added identity verification | runs/039-switching-fix/determinism_debug.md |
| codex_setup.sh | Added identity verification | runs/039-switching-fix/determinism_debug.md |

### Specified-Only (Not Implemented)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| PYTHONPATH wrapper | N/A | Polish item |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |

---

## SWITCHING REPEATABILITY TEST RESULTS

### Full Cycles (3x) - Claude → Codex → Claude

All 9 steps across 3 cycles produced correct identity:

| Cycle | Step 1 Claude | Step 2 Codex | Step 3 Claude Restore |
|-------|---------------|--------------|---------------------|
| 1 | `claude-code` ✓ | `codex-cli` ✓ | `claude-code` ✓ |
| 2 | `claude-code` ✓ | `codex-cli` ✓ | `claude-code` ✓ |
| 3 | `claude-code` ✓ | `codex-cli` ✓ | `claude-code` ✓ |

---

## ISSUE INVESTIGATION

### Reported Issue
"Claude → Codex → Claude switching 过程中宿主身份仍会漂移"

### Investigation Results
- Issue NOT reproducible in this test environment
- Defensive verification added to both setup scripts
- 3×3 switching repeatability tests all passed

---

## FINAL STATUS

| Metric | Value |
|--------|-------|
| FINAL_STATUS | PASS |
| SWITCHING_REPEATABLE_3X | YES |
| CLAUDE_CODEX_CLAUDE_STABLE | YES |
| USER_JOURNEY_READY_TO_RECHECK | YES |

---

**Phase 039 COMPLETE**
**Switching Repeatability VERIFIED**
