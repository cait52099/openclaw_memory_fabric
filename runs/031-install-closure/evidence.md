# OCMF Phase 031: Install Closure Evidence Report

**Run ID**: 031-install-closure
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## DELIVERABLES

| Deliverable | File | Status |
|-------------|------|--------|
| Claude wiring fix | `src/ocmaf/hosts/claude_setup.sh` | ✓ Fixed |
| Codex wiring fix | `src/ocmaf/hosts/codex_setup.sh` | ✓ Fixed |
| Unified install fix | `src/ocmaf/cli/unified.py` | ✓ Fixed |
| Quickstart truthfulness | `docs/quickstart.md` | ✓ Fixed |
| Install closure evidence | `runs/031-install-closure/install_closure.md` | ✓ Created |
| Evidence report | `runs/031-install-closure/evidence.md` | ✓ This file |
| Known limits | `runs/031-install-closure/known_limits.md` | ✓ Created |

---

## CATEGORIZATION

### Product Mainline (Install Closure)

Features in this phase:

1. **Claude Wiring Fix**
   - MCP config now uses correct entry: `ocmaf.bridge.mcp_server --tool claude-code`

2. **Codex Wiring Fix**
   - MCP config now uses correct entry: `ocmaf.bridge.mcp_server --tool codex-cli`

3. **Unified Install Command**
   - Now actually runs host-specific setup scripts
   -，不再只打印消息

4. **Quickstart Truthfulness**
   - Fixed CLI invocations to use correct module path
   - No more misleading "we set it up for you"

### Host-Specific Paths

| Host | Method | Status | MCP Entry | Verified |
|------|--------|--------|-----------|----------|
| Claude | A1+B | ✓ Works | `ocmaf.bridge.mcp_server --tool claude-code` | ✓ |
| Codex | C | ✓ Works | `ocmaf.bridge.mcp_server --tool codex-cli` | ✓ |
| OpenClaw | BLOCKED | ⚠️ | GitHub release 404 | ✗ |

### Specified-Only (Not Implemented)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |
| Auto-memory for Codex | N/A | Method C doesn't support auto-trigger |

---

## EVIDENCE

### Verified E2E Path

```
1. Install: PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
2. Config: ~/.claude/mcp_servers.json (correct entry point)
3. Status: source ~/.ocmf/config.sh && PYTHONPATH=src python3 -m ocmaf.cli.unified status
4. Remember: PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "..."
5. Recall: PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "..."
```

**Result**: ✓ Works end-to-end

---

## FINAL STATUS

| Metric | Value |
|--------|-------|
| FINAL_STATUS | PASS |
| CLAUDE_WIRING_CORRECT | YES |
| CODEX_WIRING_CORRECT | YES |
| UNIFIED_INSTALL_WORKS | YES |
| UNIFIED_STATUS_RELIABLE | YES |
| QUICKSTART_TRUTHFUL | YES |
| SMOKE_TESTS | PASS |
| REGRESSION_GATE | 4/4 PASS |

---

**FINAL_STATUS: PASS**
**INSTALL_CLOSURE: PASS**
**CLAUDE_WIRING_CORRECT: YES**
**CODEX_WIRING_CORRECT: YES**
