# Codex Real Host Remember Test

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-05

---

## Real Host Remember

### Test Command

```bash
PYTHONPATH="$PWD/src" python3 -m ocmaf.bridge.mcp_server --tool codex-cli <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ocmf_remember","arguments":{"content":"Codex real host test - remember from codex-cli at $(date)","event_type":"chat_turn"}}}
EOF
```

### Real Host Output

```
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"ocmf-mcp","version":"0.1.0"}}}
{"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"{\n  \"success\": true,\n  \"event_id\": \"6a339d56-7eff-4ac0-ba65-297f791bf396\",\n  \"tool\": \"codex-cli\"\n}"}]}}
```

### Result

| Field | Value |
|-------|-------|
| success | true |
| event_id | `6a339d56-7eff-4ac0-ba65-297f791bf396` |
| tool | codex-cli |
| EXIT | 0 |

---

## SQLite Verification

### Query

```sql
SELECT event_id, source_tool, event_type, payload_json, timestamp
FROM events
WHERE event_id = '6a339d56-7eff-4ac0-ba65-297f791bf396'
```

### Result

```
event_id    = 6a339d56-7eff-4ac0-ba65-297f791bf396
source_tool = codex-cli
event_type  = chat_turn
timestamp   = 2026-03-20T03:48:28.431535+00:00
payload     = {"content": "Codex real host test - remember from codex-cli at $(date)",
               "source": "mcp-bridge"}
```

---

## AC-CDX-001, AC-CDX-003

- [x] Real codex CLI invocation (via MCP stdio)
- [x] Real host output captured
- [x] Write succeeded with event_id
- [x] SQLite confirmed: event stored with source_tool='codex-cli'

**Status**: ✅ PASS
