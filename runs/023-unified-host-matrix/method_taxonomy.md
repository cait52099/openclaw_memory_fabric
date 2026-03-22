# OCMF Unified Method Taxonomy

**Run ID**: 023-unified-host-matrix
**Date**: 2026-03-22
**Status**: FINAL - BINDING

---

## PURPOSE

This document establishes a unified, unambiguous terminology for OCMF automation methods. All project documents MUST use these exact definitions.

---

## METHOD TAXONOMY

### Method A: Native Auto-Trigger

| Property | Value |
|----------|-------|
| **Name** | Native auto-trigger |
| **Also called** | Hooks auto-call, background collection |
| **Mechanism** | Host's native event hooks call ocmf_* tools automatically |
| **Trigger** | Automatic (SessionStart, SessionEnd, PreToolUse, etc.) |
| **User Input Required** | ❌ NO |
| **Host Uses Results** | ❌ NO (side process) |
| **Memory Storage** | ✅ YES (events stored) |
| **Use Case** | Background memory collection without user intervention |
| **Host Support** | Claude (✅), Codex (❌), OpenClaw (⚠️) |

**Key property**: The host calls the tools automatically, but does NOT read the outputs. This is a **side process**.

### Pure Method A: Native Context Injection

| Property | Value |
|----------|-------|
| **Name** | Pure Method A / Native context injection |
| **Also called** | Seamless auto-recall, A2 |
| **Mechanism** | Hook outputs are injected into LLM's conversation context |
| **Trigger** | Automatic |
| **User Input Required** | ❌ NO |
| **Host Uses Results** | ✅ YES (outputs affect response) |
| **Memory Storage** | ✅ YES |
| **Use Case** | Zero-friction auto-memory |
| **Host Support** | **NONE** (not supported anywhere) |

**Key property**: The host reads and uses the tool outputs in the current conversation. This is what users typically want from "auto-memory."

**CRITICAL**: Pure Method A is NOT SUPPORTED in any known host. Both Claude and Codex FAIL this category.

### Method B: System-Prompt Assisted

| Property | Value |
|----------|-------|
| **Name** | System-prompt assisted |
| **Also called** | Prompt injection, instruction following |
| **Mechanism** | Memory instructions injected via system prompt |
| **Trigger** | Host follows injected instructions |
| **User Input Required** | ❌ NO (once configured) |
| **Host Uses Results** | ✅ YES (Claude follows instructions) |
| **Memory Storage** | ⚠️ Depends on host compliance |
| **Use Case** | Claude uses memories in conversation |
| **Host Support** | Claude (✅), Codex (⚠️ UNTESTED) |

**Key property**: Claude (or Codex) follows natural language instructions in the system prompt to call ocmf_* tools. Claude actively uses recalled information in its responses.

### Method C: Manual MCP

| Property | Value |
|----------|-------|
| **Name** | Manual MCP |
| **Also called** | Explicit tool calls, user-driven |
| **Mechanism** | User or agent explicitly invokes ocmf_* tools via MCP |
| **Trigger** | Explicit user/agent action |
| **User Input Required** | ✅ YES |
| **Host Uses Results** | ✅ YES |
| **Memory Storage** | ✅ YES |
| **Use Case** | User controls when memories are stored/recalled |
| **Host Support** | Claude (✅), Codex (✅), OpenClaw (⚠️) |

**Key property**: The user explicitly calls the tools. No automation.

---

## DISTINCTION: Method A vs Pure Method A vs Method B

```
Method A (auto-trigger)
├── Triggers: YES (automatic hooks)
├── User input: NO
└── Host reads outputs: NO (side process)

Pure Method A (context injection)
├── Triggers: YES (automatic hooks)
├── User input: NO
└── Host reads outputs: YES ← This is the critical difference

Method B (system-prompt)
├── Triggers: Claude follows instructions
├── User input: NO (once configured)
└── Host reads outputs: YES (Claude acts on memories)

Method C (manual)
├── Triggers: User/agent explicit call
├── User input: YES
└── Host reads outputs: YES
```

---

## WHY Pure Method A FAILS

Both Claude and Codex run hooks as **side processes**:

1. Hook fires → calls ocmf_recall/ocmf_remember via stdio
2. MCP server processes the call → returns JSON response
3. Hook receives response → writes to log file
4. **Claude/Codex NEVER sees the response** in its conversation context

This is a fundamental architectural limitation. Hook outputs are fire-and-forget.

---

## PRODUCTION PATH RECOMMENDATIONS

### Claude: A1 + B (Verified)

| Phase | Method | Why |
|-------|--------|-----|
| Memory collection | A1 | Automatic; no user input needed |
| Memory recall | B | Claude actively uses recalled memories |

**Rationale**: A1 provides automatic background collection. B provides seamless recall where Claude reads and uses the memories in its responses. Neither alone is sufficient.

### Codex: C Only (Verified)

| Phase | Method | Why |
|-------|--------|-----|
| Memory collection | C | Manual ocmf_remember calls |
| Memory recall | C | Manual ocmf_recall calls |

**Rationale**: Codex has no hooks. MCP is the only extension mechanism, requiring explicit tool calls.

### OpenClaw: TBD

Status: BLOCKED. Cannot determine production path until environment issues are resolved.

---

## HOST METHOD SUPPORT SUMMARY

| Host | A1 | A2 | B | C | Production Path |
|------|----|----|---|-----|-----------------|
| Claude | ✅ | ❌ | ✅ | ✅ | **A1 + B** |
| Codex | ❌ | ❌ | ⚠️ | ✅ | **C** |
| OpenClaw | ⚠️ | ⚠️ | ⚠️ | ⚠️ | **TBD** |

---

## TERMINOLOGY RULES (BINDING)

### ❌ PROHIBITED

- ❌ "Method A works" (which A? A1 or A2?)
- ❌ "Native auto-memory" (ambiguous - could mean A1 or A2)
- ❌ "Claude Method A" alone (specify A1 or A2)
- ❌ "Codex Method A" (Codex has NO Method A)

### ✅ REQUIRED

| Meaning | Term |
|---------|------|
| Hooks auto-call tools | "Method A1" or "native auto-trigger" |
| Hook outputs affect context | "Method A2" or "native context injection" (NOT SUPPORTED) |
| System-prompt instructions | "Method B" or "system-prompt assisted" |
| Explicit tool calls | "Method C" or "manual MCP" |
| Claude production | "A1 + B" |
| Codex production | "Method C" |

---

## SYNTHETIC vs REAL HOST

| Term | Definition | Notes |
|------|------------|-------|
| **Synthetic test** | Direct module/function call without real host | e.g., `python3 -c "from ocmaf.sdk import...; session.remember(...)"` |
| **Real host proof** | Real host CLI invokes ocmf_* via MCP | e.g., `codex exec "call ocmf_remember"` |
| **Direct MCP invocation** | Sending JSON-RPC to MCP server directly | Not a real host call |

**Note**: Run 021 used "direct MCP invocation" ( piping JSON-RPC to `python3 -m ocmaf.bridge.mcp_server`). This was correctly identified as insufficient. Run 022 used real `codex exec` which is genuine real host proof.

---

**This taxonomy is FINAL and binding. All project documents must use these terms consistently.**
