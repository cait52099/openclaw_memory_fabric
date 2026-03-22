# OCMF Phase 7C Known Limits

**Run ID**: 030-unified-install-e2e
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## THIS IS A PRODUCT MAINLINE TASK

**Important**: Phase 7C completes the unified install E2E, making OCMF truly usable.

### What Phase 7C Delivers

- ✓ Unified CLI works with PYTHONPATH
- ✓ Host detection uses env vars (not binary)
- ✓ Claude wiring configured correctly
- ✓ Codex wiring configured correctly
- ✓ Quickstart truthful
- ✓ E2E path verified

---

## CURRENTLY WORKING

### Unified Entry

| Feature | Status | Evidence |
|---------|--------|----------|
| Unified CLI | ✓ Works | `PYTHONPATH=src ocmaf unified --help` |
| Host Detection | ✓ Fixed | Uses env vars, not binary |
| Claude Setup | ✓ Works | Configures A1+B environment |
| Codex Setup | ✓ Works | Configures MCP correctly |

### Host Paths

| Host | Method | Working | E2E Verified |
|------|--------|---------|--------------|
| Claude | A1+B | ✓ | ✓ E2E tested |
| Codex | C | ✓ | ✓ Config verified |
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

**Reason**: MCP configuration requires manual editing

**Impact**: For full auto-recall, need to add OCMF to Claude's mcp_servers.json

**Resolution**: Manual step - see quickstart.md

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

---

## PRODUCT LINE STATUS

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 6D-6G | ✓ Complete | Cross-host UX + regression gate |
| Phase 7A | ✓ Complete | Unified entry skeleton |
| Phase 7B | ✓ Complete | Auto-memory behavior |
| Phase 7C | ✓ Complete | Install E2E + wiring fixes |

**Next**: Phase 7C is complete. Product is ready for user testing.

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
| `runs/030-unified-install-e2e/evidence.md` | Full evidence report |
| `runs/030-unified-install-e2e/e2e_evidence.md` | E2E test results |
| `runs/030-unified-install-e2e/known_limits.md` | This file |

---

**Phase 7C COMPLETE**
**Unified Install E2E Ready for User Testing**
