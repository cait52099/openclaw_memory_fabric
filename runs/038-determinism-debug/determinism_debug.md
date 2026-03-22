# Determinism Debug Report - Phase 038

**Run ID**: 038-determinism-debug
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## Issue Investigation

### Reported Problem
- "Claude clean-home path may still be written as Codex identity"
- "Claude → Codex → Claude switching过程中宿主身份仍会漂移"

### Root Cause Analysis

The reported issue could NOT be reproduced in this test environment. Extensive testing showed:

1. **Setup script selection**: `unified.py` correctly selects `claude_setup.sh` when `--host claude`
2. **Heredoc writing**: The heredoc correctly writes `OCMF_SOURCE_TOOL="claude-code"`
3. **Subprocess invocation**: The subprocess correctly runs `source claude_setup.sh`

### Code Review Findings

After detailed code review, I identified a potential vulnerability in the heredoc handling:

**Original code**:
```bash
cat > "$OCMF_CONFIG" << EOF
...
export OCMF_SOURCE_TOOL="claude-code"
...
EOF
```

**Issue**: The unquoted heredoc could theoretically be affected by shell state. Also lacked validation.

**Fix applied**:
```bash
cat > "$OCMF_CONFIG" << 'HEREDOC_END'
# OCMF Configuration for Claude
# Source tool identification - CLAUDE IDENTITY
export OCMF_SOURCE_TOOL="claude-code"
...
HEREDOC_END

# DEFENSIVE: Verify the config was written correctly
ACTUAL_TOOL="$(grep 'OCMF_SOURCE_TOOL=' "$OCMF_CONFIG" | head -1 | cut -d'"' -f2 2>/dev/null || echo 'UNKNOWN')"
if [ "$ACTUAL_TOOL" != "claude-code" ]; then
    echo "✗ ERROR: Config verification failed!"
    exit 1
fi
echo "  ✓ Verified OCMF_SOURCE_TOOL=claude-code"
```

### Fix Summary

1. Added explicit validation to verify `OCMF_SOURCE_TOOL` is correctly written
2. Added clear comment "CLAUDE IDENTITY" to prevent accidental changes
3. Script now fails explicitly if identity verification fails

---

## Repeatability Test Results

### Clean-Home Claude Path (3x)

| Run | OCMF_SOURCE_TOOL | Remember Source | Status |
|-----|------------------|----------------|--------|
| 1 | `claude-code` | `Source: Claude` | ✓ PASS |
| 2 | `claude-code` | `Source: Claude` | ✓ PASS |
| 3 | `claude-code` | `Source: Claude` | ✓ PASS |

### Switching: Claude → Codex → Claude (3x)

| Cycle | Claude | Codex | Claude Restore | Status |
|-------|--------|-------|----------------|--------|
| 1 | `claude-code` ✓ | `codex-cli` ✓ | `claude-code` ✓ | ✓ PASS |
| 2 | `claude-code` ✓ | `codex-cli` ✓ | `claude-code` ✓ | ✓ PASS |
| 3 | `claude-code` ✓ | `codex-cli` ✓ | `claude-code` ✓ | ✓ PASS |

### Remember/Recall Attribution (Post-Switch)

| Step | Config Source | Remember Output | Recall Attribution |
|------|--------------|-----------------|-------------------|
| After Claude install | `claude-code` | `Source: Claude` | ✓ |
| After Codex switch | `codex-cli` | `Source: Codex` | ✓ |
| After Claude restore | `claude-code` | `Source: Claude` | ✓ |

---

## Conclusion

**Issue Status**: NOT REPRODUCED in test environment

**Fix Applied**: Added defensive validation to catch any edge cases

**Test Results**: 3x3 repeatability tests all PASS

**Note**: The issue reported by the user could not be reproduced. The fix adds explicit validation to catch any future edge cases.

---

## Files Modified

- `src/ocmaf/hosts/claude_setup.sh` - Added identity verification
