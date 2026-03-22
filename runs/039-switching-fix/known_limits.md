# OCMF Phase 039 Known Limits

**Run ID**: 039-switching-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## CURRENTLY WORKING

### User Journey

| Feature | Status | Notes |
|---------|--------|-------|
| Claude clean-home install | ✓ Works | 3×3 repeatability test passed |
| Claude remember | ✓ Works | Source shows "Claude" |
| Claude recall | ✓ Works | Shows "From Claude:" |
| Codex clean-home install | ✓ Works | Verified |
| Codex remember | ✓ Works | Source shows "Codex" |
| Codex recall | ✓ Works | Shows "From Codex:" |

### Multi-Host Switching

| Feature | Status | Notes |
|---------|--------|-------|
| Claude → Codex switch | ✓ Works | Config changes correctly |
| Codex → Claude switch | ✓ Works | Config changes correctly |
| Switching 3x repeatability | ✓ Works | All 3 cycles passed |
| Cross-host memory sharing | ✓ Works | Shared memory.db visible |

---

## CURRENT LIMITATIONS

### 1. PYTHONPATH Required

**Severity**: HIGH

**Reason**: OCMF not properly installed via pip

**Impact**: Must prefix every command with `PYTHONPATH=src`

**Resolution**: Run `pip install -e /path/to/ocmf` to install properly, or use wrapper script

### 2. Claude MCP Requires Restart

**Severity**: HIGH

**Reason**: MCP server needs Claude to be restarted to load new config

**Impact**: After `install --host claude`, new MCP config only takes effect after Claude restart

**Resolution**: Restart Claude after install

### 3. Manual Config Source Required

**Severity**: MEDIUM

**Reason**: `~/.ocmf/config.sh` doesn't auto-load

**Impact**: User must manually `source ~/.ocmf/config.sh` after install

**Resolution**: Consider auto-detection in CLI (future polish)

### 4. Config Overwrites on Host Switch

**Severity**: MEDIUM

**Reason**: Running `install --host X` overwrites `~/.ocmf/config.sh`

**Impact**: Switching hosts changes OCMF_SOURCE_TOOL (expected but may surprise users)

**Resolution**: Document as expected behavior

### 5. Codex Auto-Memory NOT Supported

**Severity**: HIGH (by design)

**Reason**: Method C (manual MCP) doesn't support automatic triggers

**Impact**: Codex users must manually call recall/remember

**Resolution**: Would need Codex to support native hooks (Method A/B)

### 6. OpenClaw BLOCKED

**Severity**: N/A

**Reason**: GitHub release returns 404

**Impact**: OpenClaw users cannot use OCMF

**Resolution**: Requires OpenClaw GitHub release to become available

---

## ISSUE INVESTIGATION

### Reported: Claude Identity Drift During Switching

**Issue Reported**: "Claude → Codex → Claude switching 过程中宿主身份仍会漂移"

**Investigation Performed**:
- Extensively tested switching cycles: 3×3 repeatability all passed
- Added defensive identity verification to both setup scripts
- Verified setup scripts write correct identity

**Result**: Issue could NOT be reproduced in this test environment

**Fix Applied**:
- Added defensive verification to `claude_setup.sh`
- Added defensive verification to `codex_setup.sh`
- Scripts now fail explicitly if identity verification fails

---

## PRODUCT POLISH PRIORITIES

| Priority | Item | Impact | Effort |
|----------|------|--------|--------|
| P1 | Wrapper script for PYTHONPATH | High | Low |
| P2 | Config switch warning | Medium | Low |
| P3 | Host-specific config files | Medium | Medium |

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/039-switching-fix/switching_repeatability.md` | Full switching test results |
| `runs/039-switching-fix/determinism_debug.md` | Investigation and fix |
| `runs/039-switching-fix/evidence.md` | Phase evidence summary |
| `runs/039-switching-fix/friction_log.md` | Friction points |

---

**Phase 039 COMPLETE**
**Switching Repeatability VERIFIED**
