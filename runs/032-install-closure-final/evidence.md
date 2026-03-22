# OCMF Phase 032 Evidence Report

**Run ID**: 032-install-closure-final
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## DELIVERABLES

| Deliverable | File | Status |
|-------------|------|--------|
| Claude config merge | `src/ocmaf/hosts/claude_setup.sh` | ✓ Fixed |
| OCMF_SOURCE_TOOL fallback | `src/ocmaf/cli/unified.py` | ✓ Fixed |
| Quickstart unified mainline | `docs/quickstart.md` | ✓ Fixed |
| Evidence | `runs/032-install-closure-final/evidence.md` | ✓ This file |
| Known limits | `runs/032-install-closure-final/known_limits.md` | ✓ Created |

---

## CATEGORIZATION

### Product Mainline (Phase 031/032 Install Closure)

Features completed:

1. **Claude Wiring Fix** (Phase 031)
   - MCP config uses correct entry: `ocmaf.bridge.mcp_server --tool claude-code`

2. **Codex Wiring Fix** (Phase 031)
   - MCP config uses correct entry: `ocmaf.bridge.mcp_server --tool codex-cli`

3. **Unified Install Command** (Phase 031)
   - Actually runs setup scripts

4. **Claude Config Merge** (Phase 032)
   - Safely merges OCMF into existing `~/.claude/mcp_servers.json`

5. **Installed Path Identity** (Phase 032)
   - Uses `OCMF_SOURCE_TOOL` when host detection fails
   - Shows proper source name (Claude/Codex) instead of Unknown/cli

6. **Quickstart Unified Mainline** (Phase 032)
   - Uses `ocmaf unified install --host ...` as primary path

### Host-Specific Paths

| Host | Method | Status | Verified |
|------|--------|--------|----------|
| Claude | A1+B | ✓ Works | ✓ |
| Codex | C | ✓ Works | ✓ |
| OpenClaw | BLOCKED | ⚠️ | ✗ |

---

## FINAL STATUS

| Metric | Value |
|--------|-------|
| FINAL_STATUS | PASS |
| CLAUDE_CONFIG_MERGE_WORKS | YES |
| INSTALLED_PATH_IDENTITY_WORKS | YES |
| QUICKSTART_UNIFIED_MAINLINE | YES |
| SMOKE_TESTS | PASS |
| REGRESSION_GATE | 4/4 PASS |

---

**FINAL_STATUS: PASS**
**INSTALL_CLOSURE_FINAL: PASS**
