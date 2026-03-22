# OCMF Phase 038 Evidence

**Run ID**: 038-determinism-debug
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **CLAUDE_INSTALL_DETERMINISTIC** | **YES** |
| **CLEAN_HOME_REPEATABLE_3X** | **YES** |
| **SWITCHING_REPEATABLE_3X** | **YES** |
| **USER_JOURNEY_READY_TO_RECHECK** | **YES** |

---

## CATEGORIZATION

### Install Closure (Phase 031/032)

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude MCP wiring | ✓ FIXED | runs/031-install-closure/install_closure.md |
| Codex MCP wiring | ✓ FIXED | runs/031-install-closure/install_closure.md |
| OCMF_SOURCE_TOOL fallback | ✓ FIXED | runs/032-install-closure-final/install_closure_final.md |
| Quickstart truthfulness | ✓ FIXED | runs/032-install-closure-final/install_closure_final.md |

### Clean-Home First-Use Stability (Phase 035)

| Feature | Status | Evidence |
|---------|--------|----------|
| Clean-home Claude install | ✓ PASS | runs/035-clean-home-fix/clean_home_journey.md |
| Clean-home Codex install | ✓ PASS | runs/035-clean-home-fix/clean_home_journey.md |
| Deterministic host identity | ✓ PASS | runs/035-clean-home-fix/clean_home_journey.md |

### User Journey (Phase 036/037/038)

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude clean-home first-use | ✓ PASS | runs/038-determinism-debug/determinism_debug.md |
| Codex clean-home first-use | ✓ PASS | runs/038-determinism-debug/determinism_debug.md |
| Claude → Codex switch | ✓ PASS | runs/038-determinism-debug/determinism_debug.md |
| Codex → Claude switch | ✓ PASS | runs/038-determinism-debug/determinism_debug.md |
| Cross-host memory sharing | ✓ PASS | runs/038-determinism-debug/determinism_debug.md |

### Code Fix (Phase 038)

| File | Change | Evidence |
|------|--------|----------|
| claude_setup.sh | Added identity verification | runs/038-determinism-debug/determinism_debug.md |

### Specified-Only (Not Implemented)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| PYTHONPATH wrapper | N/A | Polish item |
| Host-specific config files | N/A | Polish item |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |

---

## REPEATABILITY TEST RESULTS

### Clean-Home Claude Path (3x)

All 3 runs produced:
- `OCMF_SOURCE_TOOL=claude-code` ✓
- `Source: Claude` ✓

### Switching: Claude → Codex → Claude (3x)

All 3 cycles produced correct identity at each step:
- Claude: `claude-code` ✓
- Codex: `codex-cli` ✓
- Claude restore: `claude-code` ✓

---

## ISSUE INVESTIGATION

### Reported Issue
"Claude clean-home path may still be written as Codex identity"

### Investigation Results
- Issue NOT reproducible in this test environment
- Defensive validation added to claude_setup.sh
- 3x3 repeatability tests all passed

---

## FINAL STATUS

| Metric | Value |
|--------|-------|
| FINAL_STATUS | PASS |
| CLAUDE_INSTALL_DETERMINISTIC | YES |
| CLEAN_HOME_REPEATABLE_3X | YES |
| SWITCHING_REPEATABLE_3X | YES |
| USER_JOURNEY_READY_TO_RECHECK | YES |

---

**Phase 038 COMPLETE**
**Determinism Issue: NOT REPRODUCED - Defensive Fix Applied**
