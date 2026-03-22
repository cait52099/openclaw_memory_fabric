# OCMF Phase 037 Evidence

**Run ID**: 037-claude-identity-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **USER_JOURNEY_TRUSTED** | **YES** |
| **CLAUDE_IDENTITY_STABLE** | **YES** (in this environment) |
| **CODEX_IDENTITY_STABLE** | **YES** |
| **SWITCHING_IDENTITY_STABLE** | **YES** |

**Note**: The identity drift issue reported by the user was NOT reproducible in this test environment.

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

### User Journey (Phase 036/037)

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude clean-home first-use | ✓ PASS | runs/037-claude-identity-fix/user_journey.md |
| Codex clean-home first-use | ✓ PASS | runs/037-claude-identity-fix/user_journey.md |
| Claude → Codex switch | ✓ PASS | runs/037-claude-identity-fix/switching_ux.md |
| Codex → Claude switch | ✓ PASS | runs/037-claude-identity-fix/switching_ux.md |
| Cross-host memory sharing | ✓ PASS | runs/037-claude-identity-fix/user_journey.md |

### Specified-Only (Not Implemented)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| PYTHONPATH wrapper | N/A | Polish item |
| Host-specific config files | N/A | Polish item |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |

---

## FRICTION SUMMARY

| ID | Friction | Severity | Workaround |
|----|----------|----------|------------|
| F-001 | PYTHONPATH required | HIGH | pip install -e |
| F-002 | Claude restart required | HIGH | Restart Claude |
| F-003 | Manual source config | MEDIUM | source ~/.ocmf/config.sh |
| F-004 | Config overwrites on switch | MEDIUM | Document expected |
| F-005 | Method C no auto-memory | MEDIUM | Manual recall/remember |

---

## ISSUE INVESTIGATION

The reported identity drift issue ("Claude clean-home path may still be written as Codex identity") was thoroughly investigated:

1. ✓ Verified setup scripts write correct identity
2. ✓ Verified unified.py selects correct setup script
3. ✓ Verified subprocess call works correctly
4. ✓ Verified environment variable handling
5. ✓ Verified switching cycles maintain identity

**Result**: Issue could NOT be reproduced in this environment.

---

## FINAL STATUS

| Metric | Value |
|--------|-------|
| FINAL_STATUS | PASS |
| USER_JOURNEY_TRUSTED | YES |
| CLAUDE_IDENTITY_STABLE | YES |
| CODEX_IDENTITY_STABLE | YES |
| SWITCHING_IDENTITY_STABLE | YES |

---

**Phase 037 COMPLETE**
**Trusted User Journey ACHIEVED (in this environment)**
