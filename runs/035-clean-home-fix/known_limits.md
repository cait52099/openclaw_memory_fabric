# OCMF Phase 035 Known Limits

**Run ID**: 035-clean-home-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## CURRENTLY WORKING

### Clean-Home Deterministic Journey (Phase 035)

| Feature | Status | Notes |
|---------|--------|-------|
| Claude install --host claude | ✓ Works | Writes OCMF_SOURCE_TOOL="claude-code" |
| Claude source config | ✓ Works | source ~/.ocmf/config.sh works |
| Claude remember | ✓ Works | Source shows "Claude" |
| Claude recall | ✓ Works | Shows "From Claude:" |
| Codex install --host codex | ✓ Works | Writes OCMF_SOURCE_TOOL="codex-cli" |
| Codex source config | ✓ Works | source ~/.ocmf/config.sh works |
| Codex remember | ✓ Works | Source shows "Codex" |
| Codex recall | ✓ Works | Shows "From Codex:" |

### Multi-Host Switching (Phase 7E - Previously Verified)

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
| `runs/035-clean-home-fix/clean_home_journey.md` | Clean-home test results |
| `runs/035-clean-home-fix/evidence.md` | Phase evidence summary |
| `runs/033-user-journey/claude_journey.md` | Claude journey test |
| `runs/033-user-journey/codex_journey.md` | Codex journey test |
| `runs/034-switching-ux/claude_to_codex.md` | Claude → Codex switch |
| `runs/034-switching-ux/codex_to_claude.md` | Codex → Claude switch |
| `runs/034-switching-ux/cross_host_shared.md` | Cross-host sharing |

---

**Phase 035 COMPLETE**
**Clean-Home Deterministic Journey PASS**
**All Known Issues from Phase 7D/7E Still Apply (see above)**
