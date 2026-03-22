# Friction Log - Phase 037

**Run ID**: 037-claude-identity-fix
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

User journey is stable. The identity drift issue was investigated but could NOT be reproduced in this environment. All friction points documented below are expected and have workarounds.

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

---

## Issue Investigation Notes

### Reported Issue (NOT Reproduced)
- **Issue**: "Claude clean-home path may still be written as Codex identity"
- **Symptoms**: `install --host claude` sometimes writes `OCMF_SOURCE_TOOL=codex-cli`
- **Investigation**: Extensively tested clean-home install, switching cycles, environment variable handling
- **Result**: Issue could NOT be reproduced in this environment

### Possible Explanations
1. Issue may be environment-specific (different shell state, aliases, etc.)
2. Issue may occur only in specific invocation contexts
3. Issue may have been fixed in a previous session

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

**USER_JOURNEY_TRUSTED: YES** (in this environment)

All friction points are documented, expected, and have workarounds. The core user journey is stable.
