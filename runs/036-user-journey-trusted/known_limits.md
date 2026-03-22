# OCMF Phase 036 Known Limits

**Run ID**: 036-user-journey-trusted
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## CURRENTLY WORKING

### User Journey (Phase 036)

| Feature | Status | Notes |
|---------|--------|-------|
| Claude clean-home install | ✓ Works | `install --host claude` succeeds |
| Claude source config | ✓ Works | `source ~/.ocmf/config.sh` works |
| Claude remember | ✓ Works | Source shows "Claude" |
| Claude recall | ✓ Works | Shows "From Claude:" |
| Codex clean-home install | ✓ Works | `install --host codex` succeeds |
| Codex source config | ✓ Works | `source ~/.ocmf/config.sh` works |
| Codex remember | ✓ Works | Source shows "Codex" |
| Codex recall | ✓ Works | Shows "From Codex:" |

### Multi-Host Switching (Phase 7E)

| Feature | Status | Notes |
|---------|--------|-------|
| Claude → Codex switch | ✓ Works | Config changes correctly |
| Codex → Claude switch | ✓ Works | Config changes correctly |
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
| `runs/036-user-journey-trusted/user_journey.md` | User journey test results |
| `runs/036-user-journey-trusted/switching_ux.md` | Switching UX summary |
| `runs/036-user-journey-trusted/evidence.md` | Phase evidence summary |
| `runs/036-user-journey-trusted/friction_log.md` | Friction points |
| `runs/035-clean-home-fix/*` | Clean-home fix evidence |
| `runs/033-user-journey/*` | Phase 7D evidence |
| `runs/034-switching-ux/*` | Phase 7E evidence |

---

**Phase 036 COMPLETE**
**Trusted User Journey ACHIEVED**
**User Journey PASS**
**Multi-Host Switching PASS**
