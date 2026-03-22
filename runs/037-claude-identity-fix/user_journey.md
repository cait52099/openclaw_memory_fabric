# User Journey Report - Phase 037

**Run ID**: 037-claude-identity-fix
**Date**: 2026-03-22
**Status**: PASS (but see notes)
**Task Type**: PRODUCT MAINLINE

---

## Executive Summary

Clean-home user journey tests PASSED in this environment. However, the identity drift issue reported by the user was NOT reproducible in my testing environment. The Claude and Codex paths work correctly, switching is stable, and source attribution is correct.

**Note**: The issue described (Claude install writing Codex identity) could not be reproduced. This may indicate:
1. The issue was already fixed in a previous session
2. The issue is specific to certain environment conditions
3. The issue occurs only in specific invocation contexts (e.g., through Claude Code vs direct shell)

---

## Test Results

### 1. Claude Clean-Home Path

| Step | Result |
|------|--------|
| `install --host claude` | ✓ Success |
| `~/.ocmf/config.sh` | `OCMF_SOURCE_TOOL="claude-code"` ✓ |
| `remember` | `Source: Claude` ✓ |
| `recall` | `From Claude:` ✓ |

### 2. Codex Clean-Home Path

| Step | Result |
|------|--------|
| `install --host codex` | ✓ Success |
| `~/.ocmf/config.sh` | `OCMF_SOURCE_TOOL="codex-cli"` ✓ |
| `remember` | `Source: Codex` ✓ |
| `recall` | `From Codex:` ✓ |

### 3. Switching: Claude → Codex → Claude

| Step | OCMF_SOURCE_TOOL | Remember Source |
|------|------------------|----------------|
| After Claude install | `claude-code` | `Source: Claude` ✓ |
| After Codex install | `codex-cli` | `Source: Codex` ✓ |
| After Claude reinstall | `claude-code` | `Source: Claude` ✓ |

---

## Identity Stability Verification

The key test was verifying that after each `install --host X`, the config file and remember/recall outputs correctly reflect the target host:

```
Claude clean-home:
  Config: export OCMF_SOURCE_TOOL="claude-code"
  Remember: Source: Claude
  Recall: From Claude:

Codex after Claude:
  Config: export OCMF_SOURCE_TOOL="codex-cli"
  Remember: Source: Codex
  Recall: From Codex:

Claude restored:
  Config: export OCMF_SOURCE_TOOL="claude-code"
  Remember: Source: Claude
```

**All tests passed with correct identity attribution.**

---

## Issue Investigation

The reported issue ("Claude clean-home path may still be written as Codex identity") was investigated thoroughly:

1. **Checked setup scripts**: Both `claude_setup.sh` and `codex_setup.sh` correctly write their respective identities
2. **Checked unified.py**: Correctly selects setup script based on `--host` parameter
3. **Checked subprocess call**: Correctly sources the selected setup script
4. **Tested with environment variables**: Even when `OCMF_SOURCE_TOOL` was pre-set, install correctly overwrote it
5. **Tested switching cycles**: Claude → Codex → Claude maintains correct identity

**Result**: The identity drift issue could NOT be reproduced in this test environment.

---

## Verdict

**FINAL_STATUS: PASS**

The user journey is stable in this environment. The Claude identity drift issue was not reproducible, suggesting it may be:
- Environment-specific
- Already fixed
- Dependent on specific invocation conditions

**USER_JOURNEY_TRUSTED: YES** (in this environment)
