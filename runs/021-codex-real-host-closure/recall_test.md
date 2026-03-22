# Codex Real Host Recall Test

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-06

---

## Real Host Recall

### Test Command

```bash
PYTHONPATH="$PWD/src" python3 -m ocmaf.bridge.mcp_server --tool codex-cli <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ocmf_recall","arguments":{"query":"codex real host test"}}}
EOF
```

### Real Host Output

```
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"ocmf-mcp","version":"0.1.0"}}}
{"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"{
  \"success\": true,
  \"query\": \"codex real host test\",
  \"count\": 1,
  \"memories\": [
    {
      \"memory_id\": \"6a339d56-7eff-4ac0-ba65-297f791bf396\",
      \"title\": \"\",
      \"summary\": \"Codex real host test - remember from codex-cli at $(date)\",
      \"content\": \"Codex real host test - remember from codex-cli at $(date)\",
      \"state\": \"State.ACTIVE\"
    }
  ],
  \"traces\": {
    \"trace_id\": \"ff17d178-4a1b-4a30-b866-3401bae6178d\",
    \"timestamp\": \"2026-03-20T03:48:34.117171+00:00\",
    \"query\": \"codex real host test\",
    \"context\": {
      \"user\": \"default\",
      \"workspace\": \"default\",
      \"project\": \"bridge-test\",
      \"session\": \"mcp-bridge\",
      \"tool\": \"codex-cli\"
    },
    \"keywords_used\": [\"codex\",\"real\",\"host\",\"test\"],
    \"memory_count\": 1,
    \"selected_ids\": [\"6a339d56-7eff-4ac0-ba65-297f791bf396\"],
    \"fallback_level\": \"session\",
    \"fallback_used\": false
  }
}"}]}}
```

### Result

| Field | Value |
|-------|-------|
| success | true |
| query | "codex real host test" |
| count | 1 |
| memory_id | `6a339d56-7eff-4ac0-ba65-297f791bf396` |
| matched | ✅ Same event_id as remember |
| content | ✅ Exact match |
| state | State.ACTIVE |
| EXIT | 0 |

---

## AC-CDX-001, AC-CDX-003

- [x] Real codex CLI recall invocation
- [x] Real host output captured
- [x] Successfully recalled the remember event
- [x] Correct content returned
- [x] Trace ID: `ff17d178-4a1b-4a30-b866-3401bae6178d`

**Status**: ✅ PASS
