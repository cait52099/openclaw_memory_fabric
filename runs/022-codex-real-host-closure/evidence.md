# OCMF Codex Line - Final Evidence Summary

**Run ID**: 022-codex-real-host-closure
**Date**: 2026-03-20
**Status**: FINAL - CODEX LINE CLOSED

---

## EXECUTIVE SUMMARY

Codex real host proof completed with strict evidence requirements.

| Metric | Status |
|--------|--------|
| **FINAL_STATUS** | **PASS** |
| **CODEX_REAL_HOST** | **PASS** |
| **CODEX_LINE_CLOSED** | **YES** |
| **CODEX_METHOD_A** | **NOT AVAILABLE** |
| **CODEX_PURE_METHOD_A** | **NOT AVAILABLE** |
| **CODEX_METHOD_B_OR_DEGRADED** | **UNTESTED** |
| **RECOMMENDED_CODEX_PRODUCTION_PATH** | **METHOD_C** |

---

## VERIFIED EVIDENCE

### 1. Codex Binary

| Property | Value |
|----------|-------|
| Path | `/Applications/Codex.app/Contents/Resources/codex` |
| Version | `codex-cli 0.116.0-alpha.10` |
| Executable | ✅ YES |
| `codex exec` | ✅ Works |

### 2. Codex MCP Configuration

| Property | Value |
|----------|-------|
| Config | `~/.codex/config.toml` |
| MCP name | `ocmf` |
| Command | `/Users/caihongwei/bin/ocmaf-codex` |
| Status | **enabled** |

**Note**: Wrapper script required because `python3 -m ocmaf...` needs PYTHONPATH.

### 3. Real Host Remember (Codex)

```
$ codex exec "call ocmf_remember with content OCMF_REAL_HOST_TEST_1773980433"
mcp: ocmf starting
mcp: ocmf ready
tool ocmf.ocmf_remember(...)
event_id = cec26366-0a10-42c5-b44f-5bdae2e332c3
```

| Field | Value |
|-------|-------|
| event_id | `cec26366-0a10-42c5-b44f-5bdae2e332c3` |
| source_tool | `codex-cli` |
| content | `OCMF_REAL_HOST_TEST_1773980433` |
| SQLite stored | ✅ YES |

### 4. Real Host Recall (Codex)

```
tool ocmf.ocmf_recall({"query":"OCMF_REAL_HOST_TEST"})
success = true, count = 1
memory_id = cec26366-0a10-42c5-b44f-5bdae2e332c3
content = OCMF_REAL_HOST_TEST_1773980433
```

| Field | Value |
|-------|-------|
| success | true |
| count | 1 |
| memory_id | matches remember event_id ✅ |
| content | exact match ✅ |

### 5. Closed Loop Verification

| Check | Remember | Recall | Pass |
|-------|----------|--------|------|
| event_id | `cec26366-...` | `cec26366-...` | ✅ |
| content | `OCMF_REAL_HOST_TEST_...` | `OCMF_REAL_HOST_TEST_...` | ✅ |
| source_tool | `codex-cli` | `codex-cli` | ✅ |

### 6. Native Automation Boundary

| Capability | Status |
|------------|--------|
| `codex hooks` | ❌ NOT FOUND |
| `codex plugin` | ❌ NOT FOUND |
| Session hooks | ❌ NOT FOUND |
| Auto-trigger | ❌ NOT AVAILABLE |

---

## METHOD CLASSIFICATION

| Method | Claude | Codex |
|--------|--------|-------|
| A - Native auto-trigger | ✅ VERIFIED | ❌ NOT AVAILABLE |
| A1 - Hooks call tools | ✅ | ❌ |
| A2 - Context injection | ❌ | ❌ |
| B - System-prompt | ✅ VERIFIED | ⚠️ UNTESTED |
| C - Manual MCP | ✅ VERIFIED | ✅ VERIFIED |
| **Production path** | **A + B** | **C** |

---

## KEY DIFFERENCES: CLAUDE vs CODEX

| Aspect | Claude | Codex |
|--------|--------|-------|
| Native hooks | ✅ YES | ❌ NO |
| Settings-based hooks | ✅ YES | ❌ NO |
| Auto-trigger | ✅ YES | ❌ NO |
| MCP extension | ✅ YES | ✅ YES |
| Production path | A + B | C |
| Auto background capture | ✅ | ❌ |
| Manual calls needed | Minimal | All |

---

## EVIDENCE FILES

| File | Purpose |
|------|---------|
| `binary_check.md` | Binary + version verification |
| `mcp_check.md` | MCP configuration + wrapper |
| `codex_real_host.md` | **Real host proof (main evidence)** |
| `sqlite_reconciliation.md` | Database verification |
| `method_boundary.md` | Method A/B/C terminology |
| `evidence.md` | This file |
| `known_limits.md` | Limitations |
| `final_codex_position.md` | Final position |

---

**This evidence is FINAL and binding.**
