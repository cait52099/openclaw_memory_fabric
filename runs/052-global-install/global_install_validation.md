# Global Install Validation - Phase 052

**Run ID**: 052-global-install
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## Validation: Claude Global Path

### Commands Executed (from /tmp)

```bash
# Clean start
rm -rf ~/.ocmf/
rm -rf ~/.codex/

# Install Claude (from /tmp, not project dir)
ocmaf install --host claude

# Remember (no manual source)
ocmaf remember --content "T052_GLOBAL_TEST"

# Recall
ocmaf recall --query "T052_GLOBAL_TEST"
```

### Results

| Step | Command | Exit Code | Output | Source |
|------|---------|-----------|--------|--------|
| Install | `ocmaf install --host claude` | 0 | ✓ Claude Setup Complete | N/A |
| Remember | `ocmaf remember --content "..."` | 0 | ✓ Remembered, Source: Claude | Claude |
| Recall | `ocmaf recall --query "..."` | 0 | ✓ Found 1 memories: From Claude | Claude |

### Verification: PASS ✓

- No PYTHONPATH manually set
- No manual source of config.sh
- Source attribution: `Source: Claude` ✓
- Recall attribution: `From Claude` ✓

---

## Validation: Codex Global Path

### Commands Executed (from /tmp)

```bash
# Switch to Codex
rm -f ~/.ocmf/config.sh
ocmaf install --host codex

# Remember (no manual source)
ocmaf remember --content "T052_CODEX_GLOBAL"

# Recall
ocmaf recall --query "T052_CODEX"
```

### Results

| Step | Command | Exit Code | Output | Source |
|------|---------|-----------|--------|--------|
| Install | `ocmaf install --host codex` | 0 | ✓ Codex Setup Complete | N/A |
| Remember | `ocmaf remember --content "..."` | 0 | ✓ Remembered, Source: Codex | Codex |
| Recall | `ocmaf recall --query "..."` | 0 | ✓ Found 1 memories: From Codex | Codex |

### Verification: PASS ✓

- No PYTHONPATH manually set
- No manual source of config.sh
- Source attribution: `Source: Codex` ✓
- Recall attribution: `From Codex` ✓

---

## Validation: Switching Global Path

### Commands Executed (from /tmp)

```bash
# Switch back to Claude
rm -f ~/.ocmf/config.sh
ocmaf install --host claude

# Remember
ocmaf remember --content "T052_CLAUDE_AFTER_CODEX"

# Recall (should show all 3 memories)
ocmaf recall --query "T052"
```

### Results

| Step | Command | Exit Code | Output |
|------|---------|-----------|--------|
| Claude restore | `ocmaf install --host claude` | 0 | ✓ Claude Setup Complete |
| Remember | `ocmaf remember --content "..."` | 0 | ✓ Source: Claude |
| Recall | `ocmaf recall --query "T052"` | 0 | ✓ Found 3 memories |

**Recall Output:**
```
Found 3 memories:

From Claude:
  • "T052_CLAUDE_AFTER_CODEX" (2026-03-22 09:04)
  • "T052_GLOBAL_TEST" (2026-03-22 09:03)

From Codex:
  • "T052_CODEX_GLOBAL" (2026-03-22 09:03)
```

### Verification: PASS ✓

- Cross-host memory sharing works ✓
- Source attribution correct ✓

---

## Summary

| Test | PYTHONPATH | Manual Source | Attribution | Status |
|------|-------------|---------------|-------------|--------|
| Claude global path | NO | NO | Claude ✓ | ✓ PASS |
| Codex global path | NO | NO | Codex ✓ | ✓ PASS |
| Switching path | NO | NO | Both ✓ | ✓ PASS |

---

## New Quickstart

```bash
# 1. Install globally
pip install -e /path/to/openclaw_memory_fabric

# 2. Setup for Claude (from ANY directory)
ocmaf install --host claude

# 3. Use directly
ocmaf remember --content "..."
ocmaf recall --query "..."

# For Codex:
ocmaf install --host codex
ocmaf remember --content "..."
ocmaf recall --query "..."
```
