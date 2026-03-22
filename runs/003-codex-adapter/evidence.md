# OCMF Phase 3B: Codex CLI Adapter Implementation Evidence

**Run ID**: 003-codex-adapter
**Date**: 2026-03-11
**Phase**: 3B - Codex CLI Adapter

---

## Executive Summary

Phase 3B implementation complete. The Codex CLI adapter has been successfully implemented with explicit tool='codex-cli' transmission through the recall/remember paths, ensuring proper cross-tool memory isolation.

---

## Implementation Details

### Files Created

| File | Description |
|------|-------------|
| `src/ocmaf/adapters/codex_cli.py` | Codex CLI adapter implementation |
| `tests/test_codex_adapter.py` | Adapter unit tests |
| `runs/003-codex-adapter/evidence.md` | This evidence document |

### Files Modified

| File | Description |
|------|-------------|
| `src/ocmaf/sdk.py` | Added `tool` parameter to MemorySession |
| `src/ocmaf/adapters/__init__.py` | Exported CodexCLIAdapter |

---

## Acceptance Criteria Verification

| AC | Criteria | Status | Evidence |
|----|----------|--------|----------|
| AC-AD-Codex-001 | Codex CLI adapter implements get_name/before_response/after_response | ✅ PASS | `test_get_name`, `test_before_response_returns_string`, `test_after_response_returns_event_id` |
| AC-AD-Codex-002 | Scope correctly maps Codex CLI context | ✅ PASS | `test_scope_includes_tool` |
| AC-AD-Codex-003 | **Must explicitly pass tool='codex-cli' to remember/recall paths** | ✅ PASS | Implementation in `get_scope_from_context()` returns `tool='codex-cli'`, passed to `MemorySession(tool=...)` |
| AC-AD-Codex-004 | Task result correctly converted to event | ✅ PASS | `after_task` method implemented |
| AC-AD-Codex-005 | Smoke tests pass | ✅ PASS | 7/7 adapter tests pass, 16/16 P0 regression tests pass |

---

## Key Implementation: tool='codex-cli' Transmission

### P0.1 Requirement Met

The critical requirement from P0.1 review was that tool must be explicitly transmitted through the recall/remember paths. The implementation ensures:

1. **Scope Extraction**:
   ```python
   def get_scope_from_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
       # ...
       tool = "codex-cli"  # Always explicitly set
       return {
           "user": user,
           "workspace": workspace,
           "project": project,
           "session": session,
           "tool": tool,
       }
   ```

2. **MemorySession Creation**:
   ```python
   with MemorySession(
       user=scope.get("user", "default"),
       workspace=scope.get("workspace"),
       project=scope.get("project"),
       session=scope.get("session"),
       tool=scope.get("tool"),  # P0.1: Explicitly pass tool='codex-cli'
       db_path=self.db_path,
   ) as session:
   ```

3. **SDK Enhancement**:
   - Added `tool` parameter to `MemorySession.__init__()`
   - Added `tool` to all recall/remember context builders
   - Updated standalone `init()` function

---

## Test Results

### Codex CLI Adapter Tests (7/7 passed)
```
✓ test_adapter_import
✓ test_get_name
✓ test_scope_includes_tool
✓ test_before_response_returns_string
✓ test_after_response_returns_event_id
✓ test_cross_tool_isolation
✓ test_standalone_functions
```

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

---

## Cross-Tool Isolation Verification

The implementation ensures:
- Memories created with `tool='codex-cli'` are isolated from memories created with `tool='claude-code'`
- Recall only returns memories matching the same tool (or fallback levels without tool)
- Project boundaries are strictly maintained

---

## Known Limitations

1. **Codex CLI Not Installed**: Actual Codex CLI integration not tested (Tier B - requires CLI wrapper)
2. **Environment Variables**: Codex CLI environment variables (CODEX_*) may not be available in test environment
3. **Fallback Behavior**: When querying without specifying tool, falls back to all tools (by design for cross-tool recall)

---

## Gate Decision

### Phase 3B Go/No-Go Criteria

| Criteria | Status | Evidence |
|----------|--------|----------|
| Codex CLI adapter implements required interfaces | ✅ PASS | 7/7 tests pass |
| tool='codex-cli' explicitly transmitted | ✅ PASS | Code review |
| Scope mapping works | ✅ PASS | test_scope_includes_tool |
| Cross-tool isolation verified | ✅ PASS | P0 regression tests |
| SDK supports tool parameter | ✅ PASS | Code changes |

### Decision: **GO**

---

## Next Steps

1. **Phase 3C**: Cross-tool E2E testing (Claude Code ↔ Codex CLI)
2. **Optional**: Test with actual Codex CLI installation
3. **Optional**: Add integration test with real Codex CLI runs

---

## Version History

- **v1.0.0** (2026-03-11): Initial Phase 3B implementation

---

**Evidence Generated**: 2026-03-11
**Status**: Phase 3B Complete - GO
