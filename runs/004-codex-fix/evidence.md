# OCMF Phase 3B.1 Cross-tool Foundation Fix Evidence

**Run ID**: 004-codex-fix
**Date**: 2026-03-11
**Phase**: 3B.1 - Cross-tool Foundation Fix

---

## Executive Summary

Phase 3B.1 implementation complete. Two hard blocks have been fixed:
1. ClaudeCodeAdapter now explicitly passes tool='claude-code'
2. Cross-tool integration tests with real assertions added and integrated into verify_smoke.sh

---

## Implementation Details

### Files Modified

| File | Change |
|------|--------|
| `src/ocmaf/adapters/claude_code.py` | Added tool parameter to all 4 MemorySession calls |
| `ops/verify_smoke.sh` | Added Codex adapter + cross-tool integration tests |

### Files Created

| File | Description |
|------|-------------|
| `tests/test_cross_tool_integration.py` | Cross-tool integration tests with real assertions |
| `runs/004-codex-fix/evidence.md` | This evidence document |

---

## Key Changes

### ClaudeCodeAdapter Tool Transmission Fix

**Before** (lines 76-82):
```python
with MemorySession(
    user=scope.get("user", "default"),
    workspace=scope.get("workspace"),
    project=scope.get("project"),
    session=scope.get("session"),
    db_path=self.db_path,
) as session:
```

**After** (Phase 3B.1):
```python
with MemorySession(
    user=scope.get("user", "default"),
    workspace=scope.get("workspace"),
    project=scope.get("project"),
    session=scope.get("session"),
    tool=scope.get("tool"),  # Phase 3B.1: Explicitly pass tool
    db_path=self.db_path,
) as session:
```

Applied to:
- before_response (line 81)
- after_response (line 115)
- before_task (line 139)
- after_task (line 160)

---

## Test Results

### P0 Regression Tests (16/16 passed)
```
✓ test_protocol_import
✓ test_error_strategy
✓ test_scope_fields
✓ test_scope_to_filter_dict
✓ test_scope_matching
✓ test_fallback_levels_defined
✓ test_session_to_project_fallback
✓ test_no_fallback_to_different_project
✓ test_explain_returns_structure
✓ test_explain_invalid_id
✓ test_explain_json_serializable
✓ test_query_uses_json_extract
✓ test_tool_isolation
✓ test_tool_in_memory_object
✓ test_workspace_to_user_fallback
✓ test_project_isolation_preserved
```

### Adapter Smoke Tests (6/6 passed)
```
✓ Basic Import
✓ Memory Session
✓ Adapter Hooks
✓ Closed Loop
✓ Scope Mapping
✓ Injection Policy
```

### Codex Adapter Tests (7/7 passed)
```
✓ test_adapter_import
✓ test_get_name
✓ test_scope_includes_tool
✓ test_before_response_returns_string
✓ test_after_response_returns_event_id
✓ test_cross_tool_isolation
✓ test_standalone_functions
```

### Cross-Tool Integration Tests (4/4 passed) - NEW
```
✓ test_claude_to_codex_isolation
✓ test_codex_to_claude_isolation
✓ test_same_tool_recall_claude
✓ test_same_tool_recall_codex
```

---

## Hard Acceptance Verification

| Acceptance | Status | Evidence |
|-----------|--------|----------|
| ClaudeCodeAdapter before_response 显式传入 tool='claude-code' | ✅ PASS | Code change verified |
| ClaudeCodeAdapter after_response 显式传入 tool='claude-code' | ✅ PASS | Code change verified |
| Claude 写入后，Codex 默认不召回 | ✅ PASS | test_claude_to_codex_isolation |
| Codex 写入后，Claude 默认不召回 | ✅ PASS | test_codex_to_claude_isolation |
| 同 tool 正常 recall 可工作 | ✅ PASS | test_same_tool_recall_* |
| tests 有真实断言 | ✅ PASS | All tests have assertions |
| verify_smoke 纳入新测试 | ✅ PASS | verify_smoke.sh updated |
| P0 regression 不退化 | ✅ PASS | 16/16 tests pass |
| adapter smoke 不退化 | ✅ PASS | 6/6 tests pass |

---

## verify_smoke.sh Updated

Added to verify_smoke.sh:
```bash
echo ""
echo "--- Running Codex Adapter Tests ---"
python3 tests/test_codex_adapter.py

echo ""
echo "--- Running Cross-Tool Integration Tests (Phase 3B.1) ---"
python3 tests/test_cross_tool_integration.py
```

---

## Decision

### Phase 3B.1 Go Criteria

| Criteria | Status |
|----------|--------|
| ClaudeCodeAdapter tool 透传修复 | ✅ PASS |
| Cross-tool 断言测试 | ✅ PASS |
| verify_smoke 纳入 | ✅ PASS |
| 无回归 | ✅ PASS |

---

## FINAL STATUS: ✅ PASS

## DUAL_ADAPTER_FOUNDATION: ✅ PASS

## OPENCLAW_GATE: GO

**Rationale**: All hard blocks fixed, cross-tool foundation verified.

---

**Evidence Generated**: 2026-03-11
**Status**: Phase 3B.1 Complete - READY FOR OpenClaw Adapter
