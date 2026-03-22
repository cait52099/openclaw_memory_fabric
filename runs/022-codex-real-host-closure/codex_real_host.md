# Codex Real Host Proof

**Run ID**: 022-codex-real-host-closure
**Date**: 2026-03-20
**Task**: Real Codex Host Tool Discovery + Remember + Recall

---

## Real Host Proof - Full Session Log

### Command Executed

```bash
/Applications/Codex.app/Contents/Resources/codex exec \
  --skip-git-repo-check --sandbox read-only --full-auto \
  "Please call the ocmf_remember tool to remember this exact string: \
   OCMF_REAL_HOST_TEST_1773980433. \
   Then call ocmf_recall with query 'OCMF_REAL_HOST_TEST' \
   and report what you recalled."
```

### Real Codex Output

```
OpenAI Codex v0.116.0-alpha.10 (research preview)
--------
workdir: /private/tmp
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, ...]
session id: 019d0979-3b6a-7302-9e8e-1a8e37eb7018
--------
user
Please call the ocmf_remember tool to remember this exact string: OCMF_REAL_HOST_TEST_1773980433.
Then call ocmf_recall with query 'OCMF_REAL_HOST_TEST' and report what you recalled.
mcp: ocmf starting
mcp: ocmf ready
mcp startup: ready: ocmf
codex
tool ocmf.ocmf_remember({"content":"OCMF_REAL_HOST_TEST_1773980433","event_type":"chat_turn"})
ocmf.ocmf_remember(...) success in 7ms:
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"success\": true,\n  \"event_id\": \"cec26366-0a10-42c5-b44f-5bdae2e332c3\",\n  \"tool\": \"codex-cli\"\n}"
    }
  ]
}
tool ocmf.ocmf_recall({"query":"OCMF_REAL_HOST_TEST"})
ocmf.ocmf_recall({"query":"OCMF_REAL_HOST_TEST"}) success in 1ms:
{
  "content": [
    {
      "type": "text",
      "text": "{\n  \"success\": true,\n  \"query\": \"OCMF_REAL_HOST_TEST\",\n  \"count\": 1,\n  \"memories\": [
    {
      \"memory_id\": \"cec26366-0a10-42c5-b44f-5bdae2e332c3\",
      \"title\": \"\",
      \"summary\": \"OCMF_REAL_HOST_TEST_1773980433\",
      \"content\": \"OCMF_REAL_HOST_TEST_1773980433\",
      \"state\": \"State.ACTIVE\"
    }
  ],
  \"traces\": {
    \"trace_id\": \"ed6544e3-4239-416b-94ab-ad06310ad19e\",
    \"timestamp\": \"2026-03-20T04:20:39.392257+00:00\",
    \"context\": {
      \"user\": \"default\", \"workspace\": \"default\", \"project\": \"bridge-test\",
      \"session\": \"mcp-bridge\", \"tool\": \"codex-cli\"
    },
    \"keywords_used\": [\"ocmf_real_host_test\"],
    \"memory_count\": 1,
    \"selected_ids\": [\"cec26366-0a10-42c5-b44f-5bdae2e332c3\"],
    \"fallback_level\": \"session\", \"fallback_used\": false
  }
}"
    }
  ]
}
codex
Recalled 1 memory: `OCMF_REAL_HOST_TEST_1773980433`
Memory ID: cec26366-0a10-42c5-b44f-5bdae2e332c3
tokens used: 6,292
```

---

## Verification Checklist

| Step | Required | Actual | Pass |
|------|----------|--------|------|
| Real `which codex` | ✅ | ✅ `/Applications/.../codex` | ✅ |
| Real `codex --version` | ✅ | ✅ `0.116.0-alpha.10` | ✅ |
| Codex sees OCMF MCP tools | ✅ | ✅ `mcp: ocmf ready` | ✅ |
| Codex calls ocmf_remember | ✅ | ✅ event_id returned | ✅ |
| Real UUID event_id | ✅ | ✅ `cec26366-0a10-42c5-b44f-5bdae2e332c3` | ✅ |
| Codex calls ocmf_recall | ✅ | ✅ memory returned | ✅ |
| Recall matches remember | ✅ | ✅ same content | ✅ |
| Event ID matches | ✅ | ✅ `cec26366-...` both calls | ✅ |
| SQLite stored | (next section) | | |

---

## SQLite Verification

```sql
SELECT event_id, source_tool, event_type, payload_json, timestamp
FROM events WHERE event_id = 'cec26366-0a10-42c5-b44f-5bdae2e332c3'
```

| Field | Value |
|-------|-------|
| event_id | `cec26366-0a10-42c5-b44f-5bdae2e332c3` |
| source_tool | `codex-cli` |
| event_type | `chat_turn` |
| content | `OCMF_REAL_HOST_TEST_1773980433` |
| timestamp | `2026-03-20T04:20:38.147943+00:00` |

---

## Method Classification

| Method | Definition | Codex Status |
|--------|------------|--------------|
| Method A - Native auto-trigger | Hooks auto-call tools without user input | ❌ NOT AVAILABLE |
| Method B - System-prompt | Claude follows injected instructions | ⚠️ UNTESTED |
| Method C - Manual MCP | User/agent explicitly calls tools | ✅ VERIFIED |

**Codex Production Path = Method C**

---

## AC Verification

- [x] AC-CDX-001: Real binary + remember + recall
- [x] AC-CDX-002: MCP configured + tools discovered
- [x] AC-CDX-003: Same-tool remember + recall closed loop
- [x] AC-CDX-004: Native automation boundary documented
- [x] AC-CDX-005: Production path determined

**FINAL_STATUS: PASS**
