# OCMF Codex Line - Final Position

**Run ID**: 022-codex-real-host-closure
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
| Version | `codex-cli 0.116.0-alpha.10` |
| Executable | ✅ YES |
| `codex exec` works | ✅ YES |

### MCP Integration

| Check | Result |
|-------|--------|
| `codex mcp` subcommand | ✅ Available |
| OCMF MCP configured | ✅ ENABLED |
| Wrapper script | ✅ `/Users/caihongwei/bin/ocmaf-codex` |
| MCP handshake | ✅ `mcp: ocmf ready` |

### Real Host Tool Discovery

```
mcp: ocmf starting
mcp: ocmf ready
tool ocmf.ocmf_remember(...)
tool ocmf.ocmf_recall(...)
```

Codex discovered, started, and called OCMF tools.

### Real Host Remember

| Property | Value |
|----------|-------|
| event_id | `cec26366-0a10-42c5-b44f-5bdae2e332c3` |
| source_tool | `codex-cli` |
| content | `OCMF_REAL_HOST_TEST_1773980433` |
| SQLite stored | ✅ verified |

### Real Host Recall

| Property | Value |
|----------|-------|
| success | true |
| count | 1 |
| memory_id | `cec26366-0a10-42c5-b44f-5bdae2e332c3` |
| content match | ✅ exact |

---

## CODEX METHOD DEFINITIONS

### Method A: Native Auto-Trigger

| Property | Definition |
|----------|------------|
| **Name** | Native auto-trigger |
| **Mechanism** | Codex internal hooks / event-based triggers |
| **Trigger** | Automatic (Session events) |
| **User Input Required** | ❌ NO |
| **Codex Status** | ❌ NOT AVAILABLE |

**Codex Method A = ❌ NOT POSSIBLE**

Codex has NO native hooks, SessionStart/SessionEnd, or auto-trigger mechanism.

### Method B: System-Prompt Assisted

| Property | Definition |
|----------|------------|
| **Name** | System-prompt assisted |
| **Mechanism** | Instructions injected via system prompt |
| **Trigger** | Codex follows injected instructions |
| **User Input Required** | ❌ NO (once configured) |
| **Codex Status** | ⚠️ UNTESTED |

**Codex Method B = ⚠️ UNTESTED**

### Method C: Manual MCP

| Property | Definition |
|----------|------------|
| **Name** | Manual MCP |
| **Mechanism** | Codex explicitly calls ocmf_* tools via MCP |
| **Trigger** | Explicit tool invocation |
| **User Input Required** | ✅ YES |
| **Codex Status** | ✅ VERIFIED |

**Codex Method C = ✅ VERIFIED**

---

## FINAL VERDICT

| Term | Definition | Codex Status |
|------|------------|--------------|
| Native auto-trigger (Method A) | Hooks auto-call tools | ❌ NOT AVAILABLE |
| Pure Method A | Context injection | ❌ NOT AVAILABLE |
| System-prompt assisted (Method B) | Instructions in prompt | ⚠️ UNTESTED |
| Manual MCP (Method C) | Explicit tool calls | ✅ VERIFIED |
| **Codex Production Path** | **Method C** | ✅ CONFIRMED |

---

## CODEX vs CLAUDE COMPARISON

| Capability | Claude | Codex |
|-----------|--------|-------|
| Native auto-trigger (A1) | ✅ VERIFIED | ❌ NOT AVAILABLE |
| Native context injection (A2) | ❌ FAIL | ❌ NOT AVAILABLE |
| System-prompt assisted (B) | ✅ VERIFIED | ⚠️ UNTESTED |
| Manual MCP (C) | ✅ VERIFIED | ✅ VERIFIED |
| **Production path** | **A + B** | **C** |
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

1. **Claude has hooks, Codex doesn't** - Fundamental architectural difference
2. **Claude = semi-automatic, Codex = fully manual** - Claude can auto-capture; Codex requires explicit calls
3. **Same MCP server, different trigger paths** - Both use the same OCMF infrastructure
4. **Unified storage** - Both Claude and Codex events go to the same SQLite database

---

## FINAL OUTPUT

| Metric | Value |
|--------|-------|
| FINAL_STATUS | PASS |
| CODEX_REAL_HOST | PASS |
| CODEX_LINE_CLOSED | YES |
| CODEX_METHOD_A | NOT AVAILABLE |
| CODEX_PURE_METHOD_A | NOT AVAILABLE |
| CODEX_METHOD_B_OR_DEGRADED | UNTESTED |
| RECOMMENDED_CODEX_PRODUCTION_PATH | METHOD_C |

---

**This position is FINAL and binding.**

**Codex line: CLOSED.**
