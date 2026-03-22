# OCMF Phase 050 Known Limits - Trusted User Journey Final Acceptance

**Run ID**: 050-trusted-final-acceptance
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

## USER_JOURNEY_TRUSTED: YES (in current environment)

---

## HONEST BOUNDARY STATEMENT

**CURRENT_ENV_STABLE: YES**
**ROOT_CAUSE_IDENTIFIED: NO**

The user journey is stable in the current environment. However, the root cause of the intermittent identity drift reported by the user has NOT been definitively identified. The stability in the current environment is attributed to defensive verification in the setup scripts, not a confirmed root cause fix.

**This is NOT a "root cause fixed" statement. This is a "current environment is stable" statement.**

---

## TRUSTED USER JOURNEY - WHAT WORKS (in current environment)

### Claude (Method A1+B)

| Feature | Status | Notes |
|---------|--------|-------|
| Clean-home install | ✓ TRUSTED | `install --host claude` works |
| Config correct | ✓ TRUSTED | `OCMF_SOURCE_TOOL=claude-code` |
| Remember attribution | ✓ TRUSTED | `Source: Claude` |
| Recall attribution | ✓ TRUSTED | `From Claude:` |

### Codex (Method C)

| Feature | Status | Notes |
|---------|--------|-------|
| Clean-home install | ✓ TRUSTED | `install --host codex` works |
| Config correct | ✓ TRUSTED | `OCMF_SOURCE_TOOL=codex-cli` |
| Remember attribution | ✓ TRUSTED | `Source: Codex` |
| Recall attribution | ✓ TRUSTED | `From Codex:` |

### Multi-Host Switching

| Feature | Status | Notes |
|---------|--------|-------|
| Claude → Codex | ✓ TRUSTED | Config changes correctly |
| Codex → Claude | ✓ TRUSTED | Config changes correctly |
| Cross-host memory | ✓ TRUSTED | Shared memory.db works |

---

## CURRENT LIMITATIONS (NOT BLOCKERS)

### 1. PYTHONPATH Required

**Severity**: HIGH (but not a blocker)

**Workaround**: `pip install -e /path/to/ocmf` or wrapper script

### 2. Claude MCP Requires Restart

**Severity**: HIGH (but not a blocker)

**Workaround**: Restart Claude after install

### 3. Manual Config Source Required

**Severity**: MEDIUM (but not a blocker)

**Workaround**: Document clearly

### 4. Config Overwrites on Host Switch

**Severity**: MEDIUM (but not a blocker)

**Workaround**: Document as expected behavior

### 5. Codex Auto-Memory NOT Supported

**Severity**: MEDIUM (but not a blocker - by design)

**Workaround**: Manual recall/remember only

### 6. OpenClaw BLOCKED

**Severity**: N/A

**Workaround**: Requires OpenClaw GitHub release

### 7. Root Cause NOT Identified

**Severity**: MEDIUM (investigation ongoing)

**Status**: Issue not reproducible in current environment

---

## PRODUCT POLISH PRIORITIES (NOT BLOCKERS)

| Priority | Item | Impact | Effort |
|----------|------|--------|--------|
| P1 | Wrapper script for PYTHONPATH | High | Low |
| P2 | Config switch warning | Medium | Low |
| P3 | Host-specific config files | Medium | Medium |

---

## SPECIFIED-ONLY (NOT IMPLEMENTED - NOT BLOCKERS)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |
| Root cause of identity drift | N/A | Not identified |

---

## SUMMARY

### TRUSTED (in current environment)
- ✓ Claude clean-home first-use
- ✓ Codex clean-home first-use
- ✓ Claude ↔ Codex switching
- ✓ Source attribution correct
- ✓ Cross-host memory sharing
- ✓ Claude install determinism (verified across phases 041-050)
- ✓ Trusted journey scenario (verified across phases 043-050)
- ✓ Config integrity stable (verified across phases 047-050)
- ✓ 25+ consecutive install commands verified

### NOT YET TRUSTED / SPECIFIED-ONLY
- OpenClaw integration (blocked)
- Semantic conflict detection
- User conflict resolution UI
- PYTHONPATH wrapper (polish)
- Host-specific config files (polish)
- Root cause of intermittent identity drift (NOT identified - issue not reproducible)

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/050-trusted-final-acceptance/user_journey.md` | User journey test results |
| `runs/050-trusted-final-acceptance/switching_ux.md` | Switching UX summary |
| `runs/050-trusted-final-acceptance/friction_log.md` | Friction points |
| `runs/050-trusted-final-acceptance/evidence.md` | Phase evidence summary |
| `runs/050-trusted-final-acceptance/known_limits.md` | This file |
| `runs/041-install-debug/*` | Determinism debug evidence |
| `runs/043-trusted-debug/*` | Trusted journey debug evidence |
| `runs/045-trusted-debug/*` | Trusted journey debug evidence |
| `runs/046-trusted-final-acceptance/*` | Trusted journey acceptance |
| `runs/048-config-integrity-debug/*` | Config integrity evidence |
| `runs/049-trusted-first-step-debug/*` | First step debug evidence |

---

**Phase 050 COMPLETE**
**TRUSTED USER JOURNEY ACHIEVED (in current environment)**
**Claude: TRUSTED | Codex: TRUSTED | Switching: TRUSTED**
**Current Env Stable: YES | Root Cause Identified: NO**
