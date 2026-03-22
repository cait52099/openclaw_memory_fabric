# Install Debug Trace - Phase 041

**Run ID**: 041-install-debug
**Date**: 2026-03-22
**Status**: PASS (but issue NOT REPRODUCIBLE)
**Task Type**: PRODUCT MAINLINE

---

## Executive Summary

**ISSUE NOT REPRODUCIBLE in this environment.**

The reported issue ("Claude install writes `codex-cli`") could NOT be reproduced despite extensive testing including:
- 5 consecutive clean-home Claude installs
- Multiple installs without cleaning
- Install/alternating cycles
- Tests from different directories

All tests showed correct `OCMF_SOURCE_TOOL="claude-code"`.

---

## Debug Trace: Full State Sampling

### Before Install
```
Environment: No OCMF env vars set
~/.ocmf: Did not exist
~/.claude/mcp_servers.json: Did not exist
```

### During Install
```
Host Detection:
  Detected: claude
  (Forced host: claude)
  Setup script: claude_setup.sh
```

### After Install
```
Config file OCMF_SOURCE_TOOL: "claude-code" ✓
MCP config --tool: "claude-code" ✓
After sourcing: OCMF_SOURCE_TOOL=claude-code ✓
Remember: Source: Claude ✓
Recall: From Claude: ✓
```

---

## Root Cause Investigation

### Possible Sources Analyzed

1. **Old shell environment variable pollution**: NOT FOUND - No OCMF env vars before install
2. **~/.ocmf/config.sh overwritten by other path**: NOT FOUND - Install correctly overwrites
3. **Host parameter passed incorrectly to setup script**: NOT FOUND - Correctly passes `claude`
4. **Shared logic pollution between setup scripts**: NOT FOUND - Each script is independent
5. **Install overwritten by subsequent steps**: NOT FOUND - Config is correct after install
6. **Runtime fallback priority error**: NOT FOUND - remember uses sourced config correctly

### Code Review Findings

Both setup scripts now include defensive verification:
```bash
# DEFENSIVE: Verify the config was written correctly
ACTUAL_TOOL="$(grep 'OCMF_SOURCE_TOOL=' "$OCMF_CONFIG" | head -1 | cut -d'"' -f2 2>/dev/null || echo 'UNKNOWN')"
if [ "$ACTUAL_TOOL" != "claude-code" ]; then
    echo "✗ ERROR: Config verification failed!"
    exit 1
fi
```

---

## 5x Clean-Home Test Results

| Test | Config Source | Status |
|------|--------------|--------|
| 1 | `claude-code` | ✓ PASS |
| 2 | `claude-code` | ✓ PASS |
| 3 | `claude-code` | ✓ PASS |
| 4 | `claude-code` | ✓ PASS |
| 5 | `claude-code` | ✓ PASS |

---

## Additional Tests Performed

### Multiple Installs Without Cleaning
- 5 consecutive `install --host claude`: ALL PASSED

### Alternating Claude/Codex Installs
- Claude → Codex → Claude → Codex...: ALL PASSED

---

## Conclusion

**ROOT_CAUSE_IDENTIFIED: NO - Issue NOT REPRODUCIBLE**

The issue reported by the user could NOT be reproduced in this environment. Possible explanations:

1. **Environment-specific issue**: The issue may occur only in specific shell environments
2. **Claude Code context**: The issue may occur only when Claude Code invokes the install internally
3. **Race condition**: There may be a timing issue not present in sequential testing
4. **Previous session state**: The issue may have been fixed in a previous session

---

## Recommendation

The defensive verification in the setup scripts will catch any future instances of incorrect identity. If the issue persists in the user's environment, additional debugging would be needed with access to the specific environment where the issue occurs.

---

## Files Modified

- `src/ocmaf/hosts/claude_setup.sh` - Defensive verification (Phase 038)
- `src/ocmaf/hosts/codex_setup.sh` - Defensive verification (Phase 039)
