# OCMF Phase 031 Known Limits

**Run ID**: 031-install-closure
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## THIS IS A PRODUCT MAINLINE TASK

**Important**: Phase 031 completes the install closure, making OCMF truly installable and usable.

### What Phase 031 Delivers

- ✓ Claude MCP wiring uses correct entry point
- ✓ Codex MCP wiring uses correct entry point
- ✓ Unified install actually runs setup scripts
- ✓ Quickstart shows correct CLI invocations
- ✓ EventType bug fixed

---

## CURRENTLY WORKING

### Install Closure

| Feature | Status | Evidence |
|---------|--------|----------|
| Claude wiring | ✓ Fixed | MCP uses `ocmaf.bridge.mcp_server --tool claude-code` |
| Codex wiring | ✓ Fixed | MCP uses `ocmaf.bridge.mcp_server --tool codex-cli` |
| Unified install | ✓ Fixed | Actually runs setup scripts |
| Quickstart | ✓ Fixed | Shows correct `python3 -m ocmaf.cli.unified` |
| E2E path | ✓ Works | install → config → status → remember → recall |

### Host Paths

| Host | Method | Working | E2E Verified |
|------|--------|---------|---------------|
| Claude | A1+B | ✓ | ✓ |
| Codex | C | ✓ | ✓ |
| OpenClaw | BLOCKED | ✗ | ✗ |

---

## CURRENT LIMITATIONS

### 1. OpenClaw BLOCKED

**Reason**: GitHub release returns 404

**Impact**: OpenClaw users cannot use OCMF

**Resolution**: Requires OpenClaw GitHub release to become available

### 2. Codex Auto-Memory NOT Supported

**Reason**: Method C (manual MCP) doesn't support automatic triggers

**Impact**: Codex users must manually call recall/remember

**Resolution**: Would need Codex to support native hooks (Method A/B)

### 3. PYTHONPATH Required

**Reason**: OCMF not properly installed via pip

**Impact**: Need `PYTHONPATH=src` prefix for CLI commands

**Resolution**: Run `pip install -e /path/to/ocmf` to install properly

### 4. Claude MCP Optional

**Reason**: MCP configuration requires manual restart of Claude

**Impact**: For full auto-recall, need to restart Claude to load MCP server

**Resolution**: Manual step - see quickstart.md

### 5. Host Detection Returns "unknown" Outside Host Environments

**Reason**: Host detection uses env vars (CODEX_API_KEY, CLAUDE_API_KEY)

**Impact**: Running outside Claude/Codex shows "unknown" host

**Resolution**: This is correct behavior - detection is for runtime host, not installed capability

---

## REGRESSION GATE STATUS

### Gate Protected

| Check | Status |
|-------|--------|
| recall_conflict | ✓ Protected |
| explain_crosshost | ✓ Protected |
| recall_provenance | ✓ Protected |
| injection_text | ✓ Protected |

### What Gate Does NOT Protect

- ❌ Unified CLI (new in Phase 7A/7B)
- ❌ Auto-memory (new in Phase 7A/7B)
- ❌ Host detection (new in Phase 7A/7B)
- ❌ Install closure (Phase 031)

---

## PRODUCT LINE STATUS

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 6D-6G | ✓ Complete | Cross-host UX + regression gate |
| Phase 7A | ✓ Complete | Unified entry skeleton |
| Phase 7B | ✓ Complete | Auto-memory behavior |
| Phase 7C | ✓ Complete | Install E2E + wiring fixes |
| Phase 031 | ✓ Complete | Install closure (MCP entry fix) |

**Next**: Product is ready for user testing with fixed install path.

---

## SPECIFIED-ONLY (NOT IMPLEMENTED)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |
| Group by source display | FR-049 | Phase 2 UX enhancement |

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/031-install-closure/install_closure.md` | Detailed fix evidence |
| `runs/031-install-closure/evidence.md` | Full evidence report |
| `runs/031-install-closure/known_limits.md` | This file |

---

**Phase 031 COMPLETE**
**Install Closure PASS**
**Ready for User Testing**
