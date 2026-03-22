# Codex Production Path Determination

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-09

---

## Production Path Analysis

### Method A: Native Auto-Trigger

| Property | Status | Evidence |
|----------|--------|----------|
| Native hooks | ❌ NOT FOUND | No `codex hooks` command |
| Auto-trigger mechanism | ❌ NOT FOUND | No SessionStart/SessionEnd |
| Automatic execution | ❌ NOT AVAILABLE | No pre/post event hooks |
| **Method A verdict** | **❌ NOT POSSIBLE** | |

### Method B: System-Prompt Assisted

| Property | Status | Evidence |
|----------|--------|----------|
| System prompt support | ⚠️ NOT TESTED | Codex may support --system-prompt |
| Claude follows instructions | ✅ YES (Claude) | Run 019 |
| Codex follows instructions | ⚠️ UNKNOWN | Needs testing |
| **Method B verdict** | **⚠️ UNTESTED** | |

### Method C: Manual MCP

| Property | Status | Evidence |
|----------|--------|----------|
| MCP integration | ✅ AVAILABLE | `codex mcp add` |
| OCMF MCP server | ✅ CONFIGURED | enabled in Codex |
| ocmf_remember | ✅ WORKS | event stored |
| ocmf_recall | ✅ WORKS | memory returned |
| ocmf_get_injection | ✅ AVAILABLE | tool exposed |
| **Method C verdict** | **✅ VERIFIED** | |

---

## Codex Production Path

### Final Determination

| Method | Status | Notes |
|--------|--------|-------|
| A - Native auto-trigger | ❌ NOT AVAILABLE | No hooks in Codex |
| B - System-prompt | ⚠️ UNTESTED | Not explored this round |
| C - Manual MCP | ✅ VERIFIED | Real host proof complete |
| **Codex Production Path** | **Method C** | Manual MCP calls |

### Comparison: Claude vs Codex

| Aspect | Claude | Codex |
|--------|--------|-------|
| Method A (native auto-trigger) | ✅ VERIFIED | ❌ NOT AVAILABLE |
| Method A1 | ✅ PASS | ❌ NO |
| Method A2 | ❌ FAIL | ❌ NO |
| Method B (system-prompt) | ✅ VERIFIED | ⚠️ UNTESTED |
| Method C (manual MCP) | ✅ VERIFIED | ✅ VERIFIED |
| **Production path** | **A + B** | **C** |

---

## Implications

### Why Codex = Method C only

1. Codex has NO native hooks/plugin auto-trigger mechanism
2. MCP is the only extension point
3. MCP tools must be explicitly called by the model
4. No automatic background memory collection

### What this means

- Codex users must explicitly call `ocmf_remember` / `ocmf_recall`
- No automatic SessionStart/SessionEnd memory capture
- User must manually trigger memory operations
- Codex is purely a "manual MCP" client

### Recommended for Codex users

1. Configure OCMF MCP server (already done ✅)
2. Call `ocmf_remember` at end of sessions
3. Call `ocmf_recall` at start of sessions
4. Consider system-prompt injection for semi-auto behavior (future work)

---

## AC-CDX-005

- [x] Real host proof complete
- [x] Native automation evaluated
- [x] Production path determined: Method C
- [x] Claude/Codex comparison documented

**Status**: ✅ DETERMINED (Human-in-the-loop: confirm final classification)

**Awaiting human confirmation for production path classification.**
