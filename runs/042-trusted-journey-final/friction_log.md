# Friction Log - Phase 042

**Run ID**: 042-trusted-journey-final
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Trusted User Journey ACHIEVED. The following friction points remain but are NOT blockers.

---

## Remaining Friction Points

### HIGH Severity (Not Blockers)

| ID | Friction | Description | Workaround |
|----|----------|-------------|------------|
| F-001 | PYTHONPATH required | Must prefix commands with `PYTHONPATH=src` | `pip install -e` or wrapper script |
| F-002 | Claude restart required | MCP server needs restart to load new config | Restart Claude after install |

### MEDIUM Severity (Not Blockers)

| ID | Friction | Description | Workaround |
|----|----------|-------------|------------|
| F-003 | Manual source config | Must manually `source ~/.ocmf/config.sh` | Document clearly |
| F-004 | Config overwrites on switch | `install --host X` overwrites config | Document as expected behavior |
| F-005 | Method C no auto-memory | Codex cannot auto-recall/remember | Manual recall/remember only |

---

## Issues NO LONGER Blockers

| Issue | Was | Now |
|-------|-----|-----|
| Claude identity drift | BLOCKER | FIXED - 5x deterministic in current env |
| Switching identity drift | BLOCKER | FIXED - 3x repeatability passed |
| Clean-home first-use | BLOCKER | FIXED - Stable |

---

## User Steps Required

```
1. PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude|codex
2. source ~/.ocmf/config.sh
3. [Restart Claude if using Claude MCP mode]
4. PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "..."
5. PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "..."
```

---

## Overall Assessment

**USER_JOURNEY_TRUSTED: YES**

All friction points are documented, expected, and have workarounds. The core user journey is stable.
