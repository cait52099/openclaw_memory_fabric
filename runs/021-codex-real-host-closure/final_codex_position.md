# OCMF Codex Line - Final Position

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Status**: FINAL - CODEX LINE CLOSED

---

## PURPOSE

This document establishes the definitive, binding position on Codex native automation capabilities for the OCMF project.

---

## CODEX REAL HOST PROOF

### Binary Verification

| Check | Result |
|-------|--------|
| Binary exists | ✅ `/Applications/Codex.app/Contents/Resources/codex` |
| Version | `codex-cli 0.116.0-alpha.1` |
| Executable | ✅ YES |
| In PATH | ❌ NO (use full path) |

### MCP Integration

| Check | Result |
|-------|--------|
| `codex mcp` subcommand | ✅ Available |
| OCMF MCP server configured | ✅ ENABLED |
| MCP tools exposed | ✅ 3 tools (recall, remember, get_injection) |
| Remember works | ✅ event_id returned |
| Recall works | ✅ memory returned |
| SQLite storage | ✅ verified |

---

## CODEX METHOD DEFINITIONS

### Method A: Native Auto-Trigger

| Property | Definition |
|----------|------------|
| **Name** | Native auto-trigger |
| **Mechanism** | Codex hooks / event-based triggers |
| **Trigger** | Automatic on session events |
| **User Input Required** | ❌ NO |
| **Claude Status** | ❌ NOT AVAILABLE |
| **Codex Status** | ❌ NOT AVAILABLE |

**Codex Method A = ❌ NOT POSSIBLE**

Codex has NO native hooks, SessionStart/SessionEnd, or auto-trigger mechanism.

### Method B: System-Prompt Assisted

| Property | Definition |
|----------|------------|
| **Name** | System-prompt assisted |
| **Mechanism** | Instructions injected via system prompt |
| **Trigger** | Claude/Codex follows injected instructions |
| **User Input Required** | ❌ NO (once configured) |
| **Codex Status** | ⚠️ UNTESTED |

**Codex Method B = ⚠️ UNTESTED** (not explored in this run)

### Method C: Manual MCP

| Property | Definition |
|----------|------------|
| **Name** | Manual MCP |
| **Mechanism** | User/agent explicitly calls ocmf_* tools |
| **Trigger** | Explicit tool invocation |
| **User Input Required** | ✅ YES (manual calls) |
| **Claude Uses Results** | ✅ YES |
| **Codex Status** | ✅ VERIFIED |

**Codex Method C = ✅ VERIFIED**

---

## FINAL VERDICT

| Term | Definition | Codex Status |
|------|------------|--------------|
| Native auto-trigger (Method A) | Hooks auto-call tools | ❌ NOT AVAILABLE |
| System-prompt assisted (Method B) | Claude follows instructions | ⚠️ UNTESTED |
| Manual MCP (Method C) | User calls tools | ✅ VERIFIED |
| **Codex Production Path** | **Method C** | ✅ CONFIRMED |

---

## CODEX vs CLAUDE COMPARISON

| Capability | Claude | Codex |
|-----------|--------|-------|
| Native auto-trigger (A1) | ✅ VERIFIED | ❌ NOT AVAILABLE |
| Native context injection (A2) | ❌ FAIL | ❌ NOT AVAILABLE |
| System-prompt assisted (B) | ✅ VERIFIED | ⚠️ UNTESTED |
| Manual MCP (C) | ✅ VERIFIED | ✅ VERIFIED |
| Production path | A + B | C |
| MCP configuration | settings.json | `codex mcp add` |
| Real host remember | ✅ PASS | ✅ PASS |
| Real host recall | ✅ PASS | ✅ PASS |

---

## PRODUCTION RECOMMENDATION

### For Claude Users

| Phase | Method | Purpose |
|-------|--------|---------|
| Memory collection | A1 | Automatic background capture |
| Memory recall | B | Claude uses memories in context |

**Claude: Use A + B combination**

### For Codex Users

| Phase | Method | Purpose |
|-------|--------|---------|
| Memory collection | C | Manual ocmf_remember calls |
| Memory recall | C | Manual ocmf_recall calls |

**Codex: Use Method C only (manual MCP)**

---

## KEY DIFFERENCES

1. **Claude has hooks, Codex doesn't** - This is the fundamental architectural difference
2. **Claude = semi-automatic, Codex = fully manual** - Claude can auto-capture; Codex requires explicit calls
3. **Same MCP server, different trigger paths** - Both use the same OCMF infrastructure
4. **Unified storage** - Both Claude and Codex events go to the same SQLite database

---

## EVIDENCE SUMMARY

| Evidence File | Status |
|--------------|--------|
| binary_check.md | ✅ Written |
| mcp_check.md | ✅ Written |
| codex_hooks.md | ✅ Written |
| mcp_config.md | ✅ Written |
| remember_test.md | ✅ Written |
| recall_test.md | ✅ Written |
| closed_loop.md | ✅ Written |
| native_auto.md | ✅ Written |
| sqlite_reconciliation.md | ✅ Written |
| production_path.md | ✅ Written |
| this file | ✅ Final position |

---

**This position is FINAL and binding.**

**Codex line: CLOSED.**
