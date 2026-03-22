# OCMF Claude Real Host Session Evidence

**Run ID**: 015-claude-session-complete
**Date**: 2026-03-12

---

## Human Interaction Required

### Step 1: Start Claude with MCP Config

**Execute in a NEW terminal (NOT inside Claude Code):**

```bash
claude --mcp-config /tmp/ocmf_mcp.json
```

Wait for Claude to start. You should see the Claude Code prompt.

---

### Step 2: Execute /remember

**In the Claude session, type exactly:**

```
/remember This is a test from Claude real host session
```

**Press Enter and record the output.**

---

### Step 3: Execute /recall

**In the same Claude session, type exactly:**

```
/recall test
```

**Press Enter and record the output.**

---

### Step 4: Exit Claude

**Type:**

```
exit
```

---

## After Human Completes

### Step 5: Verify with SQLite

After exiting Claude, run:

```bash
sqlite3 /tmp/ocmf_bridge_test.db "SELECT event_id, source_tool, payload_json FROM events WHERE source_tool='claude-code' ORDER BY timestamp DESC LIMIT 1;"
```

---

## Evidence Template

Replace the placeholders below with actual outputs:

### Remember Output:
```
[PASTE CLAUDE'S OUTPUT FROM /remember HERE]
```

### Recall Output:
```
[PASTE CLAUDE'S OUTPUT FROM /recall HERE]
```

### SQLite Result:
```
[PASTE SQLITE OUTPUT HERE]
```

---

## Status

**CLAUDE_REAL_HOST_STATUS**: ⏳ AWAITING_HUMAN_INTERACTION

---

**Generated**: 2026-03-12
