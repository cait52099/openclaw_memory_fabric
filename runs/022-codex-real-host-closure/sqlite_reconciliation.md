# SQLite Reconciliation - Codex Real Host Events

**Run ID**: 022-codex-real-host-closure
**Date**: 2026-03-20

---

## Database

| Property | Value |
|----------|-------|
| DB Path | `/tmp/ocmf_bridge_test.db` |
| Events table | events |

---

## Query

```sql
SELECT event_id, source_tool, event_type, payload_json, timestamp
FROM events
WHERE event_id = 'cec26366-0a10-42c5-b44f-5bdae2e332c3'
```

---

## Result

| Field | Value |
|-------|-------|
| event_id | `cec26366-0a10-42c5-b44f-5bdae2e332c3` |
| source_tool | `codex-cli` |
| event_type | `chat_turn` |
| content | `OCMF_REAL_HOST_TEST_1773980433` |
| timestamp | `2026-03-20T04:20:38.147943+00:00` |

---

## Reconciliation Checks

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Event exists | Yes | Yes | ✅ |
| event_id matches | `cec26366-...` | `cec26366-...` | ✅ |
| source_tool | `codex-cli` | `codex-cli` | ✅ |
| event_type | `chat_turn` | `chat_turn` | ✅ |
| content preserved | `OCMF_REAL_HOST_TEST_1773980433` | exact match | ✅ |
| timestamp | valid ISO | valid | ✅ |

---

**AC-CDX-001**: ✅ PASS
