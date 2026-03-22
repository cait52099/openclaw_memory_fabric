# OCMF Claude Real Host Session Evidence

**Run ID**: 014-claude-session-validation
**Date**: 2026-03-12

---

## What Has Been Verified

### 1. Claude Binary

```
$ which claude
/Users/caihongwei/.local/bin/claude
EXIT: 0

$ claude --version
2.1.72 (Claude Code)
EXIT: 0
```

### 2. MCP Config File

```
$ cat /tmp/ocmf_mcp.json
{
  "mcpServers": {
    "ocmf": {
      "command": "python3",
      "args": ["-m", "ocmaf.bridge.mcp_server", "--tool", "claude-code"]
    }
  }
}
```

### 3. Claude --mcp-config Starts

```
$ claude --mcp-config /tmp/ocmf_mcp.json --version
2.1.72 (Claude Code)
EXIT: 0
```

**Status**: ✅ Claude binary works with MCP config

---

## What Needs Human Interaction

The following checks require human interaction in an actual Claude interactive session:

### Required Steps for User

1. Open a NEW terminal (NOT inside Claude Code)
2. Run:
   ```bash
   claude --mcp-config /tmp/ocmf_mcp.json
   ```
3. Wait for Claude to start
4. Type exactly:
   ```
   /remember This is a test from Claude real host session
   ```
5. Press Enter
6. Type exactly:
   ```
   /recall test
   ```
7. Press Enter
8. Copy ALL output from both commands

### After User Completes These Steps

The following evidence should be collected:

- [ ] Command executed: `claude --mcp-config /tmp/ocmf_mcp.json`
- [ ] Output from `/remember` command
- [ ] Output from `/recall` command
- [ ] SQLite query to verify event_id

---

## SQLite Verification (After remember)

Once user executes remember, run:

```bash
sqlite3 /tmp/ocmf_bridge_test.db "SELECT event_id, source_tool, payload_json FROM events ORDER BY timestamp DESC LIMIT 1;"
```

Expected result:
- event_id: <real UUID>
- source_tool: 'claude-code'
- payload_json: contains the memory content

---

## Expected Recall Output (After recall)

Once user executes recall, the output should show:
- count >= 1
- memories array contains the remembered content

---

## Status

| Check | Status |
|-------|--------|
| Claude binary | ✅ Available |
| MCP config file | ✅ Created |
| --mcp-config starts | ✅ Verified |
| Session remember | ⏳ Needs human |
| SQLite event_id | ⏳ Needs human |
| Session recall | ⏳ Needs human |

---

**CLAUDE_REAL_HOST_STATUS**: ⏳ AWAITING_HUMAN_INTERACTION

---

**Generated**: 2026-03-12
