# User Journey Friction Log

**Run ID**: 036-user-journey-trusted
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

User journey is now stable and trustworthy. All friction points documented below are expected and documented.

---

## Friction Points

### HIGH Severity

| ID | Friction | Description | Workaround |
|----|----------|-------------|------------|
| F-001 | PYTHONPATH required | Must prefix commands with `PYTHONPATH=src` | Use wrapper script or `pip install -e` |
| F-002 | Claude restart required | MCP server needs Claude restart to load new config | Restart Claude after `install --host claude` |

### MEDIUM Severity

| ID | Friction | Description | Workaround |
|----|----------|-------------|------------|
| F-003 | Manual source config | Must manually `source ~/.ocmf/config.sh` | Future: auto-detection in CLI |
| F-004 | Config overwrites on switch | `install --host X` overwrites config | Document as expected behavior |
| F-005 | Method C no auto-memory | Codex cannot auto-recall/remember | Manual recall/remember only |

### INFO

| ID | Observation | Notes |
|----|-------------|-------|
| F-006 | Memory persists across switches | Shared memory.db is correct behavior |
| F-007 | Source attribution correct | After switch, memories show correct host |

---

## User Steps Required

```
1. PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude|codex
2. source ~/.ocmf/config.sh
3. [Restart Claude if using Claude MCP mode]
4. PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "..."
5. PYTHONPATH=src python3 -m ocmf.cli.unified recall --query "..."
```

**Total manual steps after install**: 2-3 (depending on host)

---

## Overall Assessment

**USER_JOURNEY_TRUSTED: YES**

All friction points are documented, expected, and have workarounds. The core user journey is stable.
