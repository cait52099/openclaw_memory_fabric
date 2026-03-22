# OCMF Phase 048 Known Limits - Config Integrity Debug

**Run ID**: 048-config-integrity-debug
**Date**: 2026-03-22
**Status**: PASS (but issue NOT reproducible)
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS (with caveat)

## CONFIG_INTEGRITY_FIXED: YES (in current environment)

---

## HONEST BOUNDARY STATEMENT

**CURRENT_ENV_STABLE: YES**
**ROOT_CAUSE_IDENTIFIED: NO**

Config integrity is stable in the current environment. However, the root cause of the reported config syntax error has NOT been definitively identified. The stability is attributed to defensive verification in the setup scripts, not a confirmed root cause fix.

**This is NOT a "root cause fixed" statement. This is a "current environment is stable" statement.**

---

## WHAT WORKS (in current environment)

### Claude (Method A1+B)

| Feature | Status | Notes |
|---------|--------|-------|
| Clean-home install | ✓ TRUSTED | `install --host claude` works |
| Config correct | ✓ TRUSTED | `OCMF_SOURCE_TOOL=claude-code` |
| Config syntax valid | ✓ TRUSTED | `bash -n` passes |
| Remember attribution | ✓ TRUSTED | `Source: Claude` |
| Recall attribution | ✓ TRUSTED | `From Claude:` |

### Codex (Method C)

| Feature | Status | Notes |
|---------|--------|-------|
| Clean-home install | ✓ TRUSTED | `install --host codex` works |
| Config correct | ✓ TRUSTED | `OCMF_SOURCE_TOOL=codex-cli` |
| Config syntax valid | ✓ TRUSTED | `bash -n` passes |
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

**Status**: Config syntax issue not reproducible in current environment

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
| Root cause of config syntax | N/A | Not identified |

---

## SUMMARY

### TRUSTED (in current environment)
- ✓ Claude clean-home first-use
- ✓ Codex clean-home first-use
- ✓ Claude ↔ Codex switching
- ✓ Config syntax valid (bash -n / zsh -n)
- ✓ Source verification passes
- ✓ Source attribution correct
- ✓ Cross-host memory sharing

### NOT YET TRUSTED / SPECIFIED-ONLY
- OpenClaw integration (blocked)
- Semantic conflict detection
- User conflict resolution UI
- PYTHONPATH wrapper (polish)
- Host-specific config files (polish)
- Root cause of reported issues (NOT identified - issues not reproducible)

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/048-config-integrity-debug/config_integrity_debug.md` | Config integrity debug trace |
| `runs/048-config-integrity-debug/install_debug_trace.md` | Install verification trace |
| `runs/048-config-integrity-debug/friction_log.md` | Friction points |
| `runs/048-config-integrity-debug/evidence.md` | Phase evidence summary |
| `runs/048-config-integrity-debug/known_limits.md` | This file |

---

**Phase 048 COMPLETE**
**Config Integrity: VERIFIED STABLE (in current environment)**
**Claude: TRUSTED | Codex: TRUSTED | Switching: TRUSTED | Config Syntax: VALID**
