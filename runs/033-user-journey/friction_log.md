# User Journey Friction Log

**Run ID**: 033-user-journey
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Both Claude and Codex user journeys pass. Main friction points identified.

---

## Friction Points

### HIGH Severity

| ID | Friction | Host | Description | Suggested Fix |
|----|----------|------|-------------|--------------|
| UF-001 | PYTHONPATH required | Both | Every command needs `PYTHONPATH=src` prefix | Create wrapper script or pip install |
| UF-002 | Auto-memory requires MCP restart | Claude | Claude needs restart to load new MCP config | Document clearly in quickstart |

### MEDIUM Severity

| ID | Friction | Host | Description | Suggested Fix |
|----|----------|------|-------------|--------------|
| UF-003 | Manual source config | Both | User must manually `source ~/.ocmf/config.sh` | Consider auto-detection in CLI |
| UF-004 | Method C no auto-memory | Codex | Codex (Method C) doesn't support auto-memory | Document clearly |

### LOW Severity

| ID | Friction | Host | Description | Suggested Fix |
|----|----------|------|-------------|--------------|
| UF-005 | Codex binary not found | Codex | Environment issue, but CLI mode still works | Document workaround |

---

## Per-Host Summary

### Claude

| Aspect | Status | Notes |
|--------|--------|-------|
| Install works | ✓ | install --host claude succeeds |
| Config works | ✓ | source ~/.ocmf/config.sh works |
| Source display | ✓ | Shows "Source: Claude" |
| Recall works | ✓ | Shows "From Claude:" |
| MCP auto-recall | ⚠️ | Requires Claude restart |

### Codex

| Aspect | Status | Notes |
|--------|--------|-------|
| Install works | ✓ | install --host codex succeeds |
| Config works | ✓ | source ~/.ocmf/config.sh works |
| Source display | ✓ | Shows "Source: Codex" |
| Recall works | ✓ | Shows "From Codex:" |
| Auto-memory | ✗ | Method C doesn't support it (expected) |

---

## Overall Assessment

**User Journey**: WORKING

The quickstart path works for both Claude and Codex. Primary friction is the PYTHONPATH requirement which could be addressed with a wrapper script or proper pip install.
