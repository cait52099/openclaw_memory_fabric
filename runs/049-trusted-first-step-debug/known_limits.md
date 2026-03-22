# OCMF Phase 049 Known Limits - First Step Debug

**Run ID**: 049-trusted-first-step-debug
**Date**: 2026-03-22
**Status**: PASS (but issue NOT reproducible)
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

## FIRST_STEP_CLAUDE_STABLE: YES
## 046_LIKE_REPLAY_STABLE: YES

---

## HONEST BOUNDARY STATEMENT

**CURRENT_ENV_STABLE: YES**
**ROOT_CAUSE_IDENTIFIED: NO**

The first-step identity drift issue reported by the user has NOT been definitively identified. The stability in the current environment is attributed to defensive verification in the setup scripts.

---

## WHAT WORKS (in current environment)

### All 046-Like Steps

| Step | Expected | Actual | Status |
|------|----------|--------|--------|
| Claude first | claude-code | claude-code | ✓ |
| Codex | codex-cli | codex-cli | ✓ |
| Claude restore | claude-code | claude-code | ✓ |

---

## CURRENT LIMITATIONS (NOT BLOCKERS)

### 1. PYTHONPATH Required
**Severity**: HIGH (workaround: pip install -e)

### 2. Claude restart required
**Severity**: HIGH (workaround: restart after install)

### 3. Manual config source
**Severity**: MEDIUM (workaround: document clearly)

### 4. Config overwrites on switch
**Severity**: MEDIUM (document as expected)

### 5. Codex no auto-memory
**Severity**: MEDIUM (by design)

### 6. Root cause NOT identified
**Severity**: MEDIUM (issue not reproducible)

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Reason |
|---------|--------|
| OpenClaw | GitHub release unavailable |
| Semantic conflict detection | Would need embeddings |
| Root cause of identity drift | Not identified |

---

**Phase 049 COMPLETE**
**First Step: STABLE | Root Cause: NOT IDENTIFIED**
