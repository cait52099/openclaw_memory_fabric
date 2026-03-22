# OCMF Codex Line - Known Limits

**Run ID**: 022-codex-real-host-closure
**Date**: 2026-03-20
**Status**: FINAL - CODEX LINE CLOSED

---

## KNOWN LIMITS - CODEX METHOD A

### Native Auto-Trigger

| Capability | Status | Reason |
|------------|--------|--------|
| Native hooks | ❌ NOT FOUND | Codex has no hooks subsystem |
| SessionStart hook | ❌ NOT FOUND | No session lifecycle hooks |
| SessionEnd hook | ❌ NOT FOUND | No session lifecycle hooks |
| Auto-trigger mechanism | ❌ NOT AVAILABLE | No event-based triggers |
| Background collection | ❌ NOT AVAILABLE | Requires explicit calls |

**Codex Method A = NOT POSSIBLE**

This is a fundamental architectural difference from Claude.

---

## KNOWN LIMITS - CODEX METHOD B

### System-Prompt Assisted

| Capability | Status | Reason |
|------------|--------|--------|
| System-prompt support | ⚠️ UNTESTED | Not explored in this run |
| MCP + prompt combo | ⚠️ UNTESTED | Not explored |
| Auto-memory via prompt | ⚠️ UNTESTED | Needs testing |

**Codex Method B = UNTESTED**

---

## KNOWN LIMITS - CODEX METHOD C

### Manual MCP

| Capability | Status | Evidence |
|------------|--------|----------|
| MCP integration | ✅ VERIFIED | `codex exec` output |
| OCMF MCP configured | ✅ VERIFIED | `codex mcp list` |
| Wrapper script needed | ✅ VERIFIED | PYTHONPATH required |
| ocmf_remember | ✅ VERIFIED | Real Codex call |
| ocmf_recall | ✅ VERIFIED | Real Codex call |
| SQLite storage | ✅ VERIFIED | DB query |

---

## PRODUCTION PATH

### Codex = Method C Only

| Component | Method | Limitation |
|-----------|--------|------------|
| Memory collection | C (manual) | User must explicitly call remember |
| Memory recall | C (manual) | User must explicitly call recall |
| Background auto-capture | ❌ | Not available for Codex |
| Native hooks | ❌ | Not available in Codex |

---

## COMPARISON: CLAUDE vs CODEX

| Aspect | Claude | Codex |
|--------|--------|-------|
| Native auto-trigger | ✅ YES | ❌ NO |
| Settings hooks | ✅ YES | ❌ NO |
| MCP extension | ✅ YES | ✅ YES |
| Manual MCP | ✅ YES | ✅ YES |
| Production path | A + B | C |
| Auto background | ✅ | ❌ |
| Manual calls needed | Minimal | All |

---

## KNOWN GAPS

### 1. No Automatic Background Capture

Codex users must remember to call `ocmf_remember` after sessions. Claude can auto-capture via hooks.

### 2. No Native Automation

Codex lacks Claude's hook-based automation. Every memory operation requires explicit tool call.

### 3. Method B Not Tested

System-prompt injection was not explored. This could potentially provide semi-automatic behavior.

### 4. PATH Issue

Codex binary is not in PATH. Must use full path.

### 5. PYTHONPATH Requirement

OCMF MCP server requires PYTHONPATH to find modules. Wrapper script at `~/bin/ocmaf-codex` solves this.

---

## SUMMARY

| Method | Claude | Codex |
|--------|--------|-------|
| A - Native auto-trigger | ✅ VERIFIED | ❌ NOT AVAILABLE |
| A2 - Context injection | ❌ FAIL | ❌ NOT AVAILABLE |
| B - System-prompt | ✅ VERIFIED | ⚠️ UNTESTED |
| C - Manual MCP | ✅ VERIFIED | ✅ VERIFIED |
| **Production** | **A + B** | **C** |

---

**Codex line is CLOSED. These limits are final.**
