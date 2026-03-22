# OCMF Phase 040 Known Limits - Trusted User Journey Final

**Run ID**: 040-trusted-journey-final
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

## USER_JOURNEY_TRUSTED: YES

---

## TRUSTED USER JOURNEY - WHAT WORKS

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

**Reason**: OCMF not properly installed via pip

**Impact**: Must prefix every command with `PYTHONPATH=src`

**Workaround**: `pip install -e /path/to/ocmf` or wrapper script

### 2. Claude MCP Requires Restart

**Severity**: HIGH (but not a blocker)

**Reason**: MCP server needs Claude to be restarted to load new config

**Impact**: After `install --host claude`, new MCP config only takes effect after Claude restart

**Workaround**: Restart Claude after install

### 3. Manual Config Source Required

**Severity**: MEDIUM (but not a blocker)

**Reason**: `~/.ocmf/config.sh` doesn't auto-load

**Impact**: User must manually `source ~/.ocmf/config.sh` after install

**Workaround**: Document clearly

### 4. Config Overwrites on Host Switch

**Severity**: MEDIUM (but not a blocker)

**Reason**: Running `install --host X` overwrites `~/.ocmf/config.sh`

**Impact**: Switching hosts changes OCMF_SOURCE_TOOL

**Workaround**: Document as expected behavior

### 5. Codex Auto-Memory NOT Supported

**Severity**: MEDIUM (but not a blocker - by design)

**Reason**: Method C (manual MCP) doesn't support automatic triggers

**Impact**: Codex users must manually call recall/remember

**Workaround**: Manual recall/remember only

### 6. OpenClaw BLOCKED

**Severity**: N/A (OpenClaw not supported)

**Reason**: GitHub release returns 404

**Impact**: OpenClaw users cannot use OCMF

**Workaround**: Requires OpenClaw GitHub release

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

---

## SUMMARY: TRUSTED VS NOT TRUSTED

### TRUSTED (This Run)
- ✓ Claude clean-home first-use
- ✓ Codex clean-home first-use
- ✓ Claude ↔ Codex switching
- ✓ Source attribution correct
- ✓ Cross-host memory sharing

### NOT YET TRUSTED / SPECIFIED-ONLY
- OpenClaw integration (blocked)
- Semantic conflict detection
- User conflict resolution UI
- PYTHONPATH wrapper (polish)
- Host-specific config files (polish)

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/040-trusted-journey-final/user_journey.md` | User journey test results |
| `runs/040-trusted-journey-final/switching_ux.md` | Switching UX summary |
| `runs/040-trusted-journey-final/evidence.md` | Phase evidence summary |
| `runs/040-trusted-journey-final/friction_log.md` | Friction points |
| `runs/035-clean-home-fix/*` | Clean-home fix evidence |
| `runs/039-switching-fix/*` | Switching fix evidence |

---

**Phase 040 COMPLETE**
**TRUSTED USER JOURNEY ACHIEVED**
**Claude: TRUSTED | Codex: TRUSTED | Switching: TRUSTED**
