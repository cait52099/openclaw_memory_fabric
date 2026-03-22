# OCMF Claude Real Host Session Validation Evidence

**Run ID**: 014-claude-session-validation
**Date**: 2026-03-12

---

## Executive Summary

This run attempts to validate Claude Real Host Session Bridge through actual Claude interactive session.

**Current Status**: ⏳ AWAITING_HUMAN_INTERACTION

---

## What Has Been Verified

### Binary Environment

| Tool | Path | Version | Status |
|------|------|---------|--------|
| Claude | /Users/caihongwei/.local/bin/claude | 2.1.72 | ✅ |
| Codex | /Applications/Codex.app/.../codex | 0.115.0-alpha.4 | ✅ |
| OpenClaw | not found | N/A | ❌ BLOCKED |

### MCP Configuration

- MCP config file created: ✅ `/tmp/ocmf_mcp.json`
- Claude --mcp-config starts: ✅ Verified

---

## What Needs Human Interaction

### User Action Required

**Step-by-step instructions for user**:

1. Open a NEW terminal (NOT inside Claude Code)
2. Run:
   ```bash
   claude --mcp-config /tmp/ocmf_mcp.json
   ```
3. Wait for Claude to start
4. Type: `/remember This is a test from Claude real host session`
5. Type: `/recall test`
6. Copy all output

---

## Verification After Human Action

### Step 1: Check remember output

Expected output should include:
- success: true
- event_id: <real UUID>
- tool: claude-code

### Step 2: SQLite check

```bash
sqlite3 /tmp/ocmf_bridge_test.db "SELECT event_id, source_tool, payload_json FROM events ORDER BY timestamp DESC LIMIT 1;"
```

Expected:
- event_id: real UUID (not placeholder)
- source_tool: 'claude-code'

### Step 3: Check recall output

Expected:
- count >= 1
- memories array contains remembered content

---

## Three-Way Validation Type Distinction

| Type | Definition | Status |
|------|------------|--------|
| Real Host Bridge | Claude interactive session + MCP config | ⏳ Needs human |
| Direct MCP Invocation | `echo '...' \| python3 -m ocmaf.bridge.mcp_server` | ✅ Verified |
| Synthetic Test | `pytest tests/` | ✅ 45/45 |

---

## FINAL OUTPUT (Pending Human Action)

| Metric | Status |
|--------|--------|
| **FINAL_STATUS** | ⏳ AWAITING_HUMAN |
| **CLAUDE_REAL_HOST** | ⏳ AWAITING_HUMAN |
| **CODEX_REAL_HOST** | ⏳ NOT_TESTED_THIS_RUN |
| **OPENCLAW_ENV_STATUS** | ❌ BLOCKED |
| **是否仍需人工交互** | **YES** |

---

## After Human Completes

Once user provides the output from steps 4-5, this evidence will be updated with:
- Real remember output
- Real event_id
- Real SQLite query result
- Real recall output

---

**Generated**: 2026-03-12
**Status**: ⏳ Awaiting Human Interaction
