# Friction Log - Phase 040

**Run ID**: 040-trusted-journey-final
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Trusted User Journey ACHIEVED. The following friction points remain but are not blockers.

---

## Remaining Friction Points

### HIGH Severity

| ID | Friction | Description | Status | Workaround |
|----|----------|-------------|--------|------------|
| F-001 | PYTHONPATH required | Must prefix commands with `PYTHONPATH=src` | NOT A BLOCKER | Use wrapper script or `pip install -e` |
| F-002 | Claude restart required | MCP server needs restart to load new config | NOT A BLOCKER | Restart Claude after install |

### MEDIUM Severity

| ID | Friction | Description | Status | Workaround |
|----|----------|-------------|--------|------------|
| F-003 | Manual source config | Must manually `source ~/.ocmf/config.sh` | NOT A BLOCKER | Document clearly |
| F-004 | Config overwrites on switch | `install --host X` overwrites config | NOT A BLOCKER | Document as expected behavior |
| F-005 | Method C no auto-memory | Codex cannot auto-recall/remember | NOT A BLOCKER | Manual recall/remember only |

### NOTABLE: These are NO LONGER Blockers

| ID | Was Previously | Now |
|----|---------------|-----|
| Claude identity drift | BLOCKER | FIXED - Verified stable |
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
