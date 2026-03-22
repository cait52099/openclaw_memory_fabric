# OCMF Unified Host Capability Matrix

**Run ID**: 023-unified-host-matrix
**Date**: 2026-03-22
**Status**: FINAL

---

## PURPOSE

This document consolidates all host verification results into a single authoritative capability matrix for Claude, Codex, and OpenClaw.

---

## EXECUTIVE SUMMARY

| Host | Real Host Proof | Production Path | Method A | Method B | Method C |
|------|----------------|----------------|----------|----------|----------|
| **Claude** | ✅ | **A1 + B** | ✅ (A1 only) | ✅ | ✅ |
| **Codex** | ✅ | **C** | ❌ | ⚠️ | ✅ |
| **OpenClaw** | ⚠️ | **TBD** | ⚠️ | ⚠️ | ⚠️ |

---

## HOST CAPABILITY MATRIX

| Dimension | Claude | Codex | OpenClaw |
|----------|--------|-------|----------|
| **Real host proof** | ✅ VERIFIED | ✅ VERIFIED | ⚠️ BLOCKED |
| **MCP 可用** | ✅ VERIFIED | ✅ VERIFIED | ⚠️ UNKNOWN |
| **Native hooks** | ✅ VERIFIED | ❌ NOT FOUND | ⚠️ UNKNOWN |
| **Auto-trigger (A1)** | ✅ VERIFIED | ❌ NOT AVAILABLE | ⚠️ UNKNOWN |
| **Context injection (A2)** | ❌ NOT SUPPORTED | ❌ NOT AVAILABLE | ⚠️ UNKNOWN |
| **System-prompt (B)** | ✅ VERIFIED | ⚠️ UNTESTED | ⚠️ UNKNOWN |
| **Manual MCP (C)** | ✅ VERIFIED | ✅ VERIFIED | ⚠️ UNKNOWN |
| **Production path** | **A1 + B** | **C** | **TBD** |

---

## CLAUDE LINE (Run 020 - CLOSED)

### Final Classification

| Method | Status | Evidence |
|--------|--------|----------|
| **Method A1** (native auto-trigger) | ✅ PASS | settings hooks call ocmf_* automatically |
| **Method A2** (context injection) | ❌ FAIL | Hooks run as side processes; Claude doesn't read outputs |
| **Method B** (system-prompt) | ✅ PASS | Claude follows injected instructions |
| **Method C** (manual MCP) | ✅ PASS | MCP tool calls work |
| **Production path** | **A1 + B** | A1 for collection, B for recall |

### Key Evidence
- `settings.json` hooks configured for SessionStart/SessionEnd
- `/tmp/auto_memory.sh` calls ocmf_recall and ocmf_remember
- SQLite events confirm `source_tool='claude-code'`
- **A2 fails**: Hook outputs are side-process outputs, not injected into context

### Binary Facts
- Binary: `/usr/local/bin/claude` (or `claude` in PATH)
- Version: Claude 2.1.78 (from run 020)

---

## CODEX LINE (Run 022 - CLOSED)

### Final Classification

| Method | Status | Evidence |
|--------|--------|----------|
| **Method A** (native auto-trigger) | ❌ NOT AVAILABLE | No hooks subsystem in Codex |
| **Method B** (system-prompt) | ⚠️ UNTESTED | Not explored |
| **Method C** (manual MCP) | ✅ PASS | Codex calls ocmf_* via MCP |
| **Production path** | **C** | Fully manual MCP calls |

### Key Evidence
- Real Codex session: `codex exec` with `--full-auto`
- MCP handshake: `mcp: ocmf ready`
- Real remember: event_id = `cec26366-0a10-42c5-b44f-5bdae2e332c3`
- Real recall: count=1, same event_id matched
- SQLite: `source_tool='codex-cli'` confirmed

### Binary Facts
- Binary: `/Applications/Codex.app/Contents/Resources/codex`
- Version: `codex-cli 0.116.0-alpha.10`
- Not in PATH; requires full path or wrapper

### Why Not A
Codex has NO hooks subsystem. Searched entire `codex --help` output:
- No `hooks` subcommand
- No `plugin` subcommand
- No SessionStart/SessionEnd hooks
- No event-based triggers

---

## OPENCLAW LINE (STATUS: BLOCKED)

### Current Status

| Check | Status | Notes |
|-------|--------|-------|
| Real host proof | ⚠️ BLOCKED | Environment issue |
| MCP | ⚠️ UNKNOWN | Not verified |
| Native hooks | ⚠️ UNKNOWN | Not explored |
| Production path | **TBD** | Cannot determine |

### Blockers
- Environment/configuration issues prevented real host validation
- No verification completed at the same level as Claude/Codex

### Position
OpenClaw verification was not completed. Production path cannot be determined. OpenClaw remains a **future candidate** for Method A (if native hooks exist) but current status is TBD.

---

## METHOD SUPPORT MATRIX

| Method | Definition | Claude | Codex | OpenClaw |
|--------|------------|--------|-------|----------|
| **A1** | Native hooks call tools automatically | ✅ | ❌ | ⚠️ |
| **A2** | Hook outputs affect LLM context | ❌ | ❌ | ⚠️ |
| **B** | System-prompt instructions | ✅ | ⚠️ | ⚠️ |
| **C** | Manual MCP tool calls | ✅ | ✅ | ⚠️ |

---

## CROSS-HOST STORAGE

All hosts share the same SQLite event store (`/tmp/ocmf_bridge_test.db`):

| Table | Fields | Notes |
|-------|--------|-------|
| events | event_id, source_tool, event_type, payload_json | source_tool = 'claude-code', 'codex-cli', or 'openclaw' |
| memory_objects | (object layer) | Built from events |
| retrieval_traces | trace_id, query, context | Per-recall traces |

---

## HYGIENE NOTE: Binary Path Corrections

| Host | Old/Wrong | Correct |
|------|-----------|---------|
| Claude | Assumed various | `/usr/local/bin/claude` (verify with `which claude`) |
| Codex | `codex` in PATH | `/Applications/Codex.app/Contents/Resources/codex` (not in PATH) |
| Codex version | 0.108.0-alpha.12 (old) | `0.116.0-alpha.10` (run 022) |

---

## FINAL OUTPUT

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **HOST_MATRIX_CLOSED** | **YES** |
| **CLAUDE_LINE_CLOSED** | **YES** |
| **CODEX_LINE_CLOSED** | **YES** |
| **OPENCLAW_STATUS** | **TBD (BLOCKED)** |
| **RECOMMENDED_PRODUCT_STRATEGY** | **Per-host paths: Claude=A1+B, Codex=C, OpenClaw=TBD** |
