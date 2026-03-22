# Friction Log - Phase 044

**Run ID**: 044-trusted-journey-final
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Trusted User Journey ACHIEVED (in current environment). Remaining friction points are NOT blockers.

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

## Issues NO LONGER Blockers (in current environment)

| Issue | Was | Now |
|-------|-----|-----|
| Claude identity drift | BLOCKER | FIXED in current env |
| Switching identity drift | BLOCKER | FIXED in current env |
| Clean-home first-use | BLOCKER | FIXED in current env |

**Note**: The root cause of the intermittent identity drift has NOT been fully identified (`ROOT_CAUSE_IDENTIFIED = NO`). The issue appears to be fixed in the current environment, but this may be due to defensive verification catching edge cases rather than a definitive root cause fix.

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

**USER_JOURNEY_TRUSTED: YES** (in current environment)

All friction points are documented, expected, and have workarounds. The core user journey is stable in the current environment.
