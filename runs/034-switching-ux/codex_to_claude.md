# Codex to Claude Switching Test

**Run ID**: 034-switching-ux
**Task**: T-7E-02
**Date**: 2026-03-22
**Status**: PASS

---

## Test Steps

### Step 1: Codex configured first
```bash
rm -rf ~/.ocmf
PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex
source ~/.ocmf/config.sh
```
**Result**: ✓ OCMF_SOURCE_TOOL=codex-cli

### Step 2: Switch to Claude
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
```
**Result**: ✓ Claude install ran

### Step 3: Check config after switch
```bash
source ~/.ocmf/config.sh
echo $OCMF_SOURCE_TOOL
```
**Result**: ✓ OCMF_SOURCE_TOOL=claude-code

### Step 4: Remember in "Claude" context
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Claude decision: Use PostgreSQL" --type decision
```
**Result**: ✓ Source: Claude

### Step 5: Recall
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "PostgreSQL"
```
**Result**: ✓ Shows both memories (including previous Claude memory)

---

## Friction Points

| Friction | Severity | Notes |
|----------|----------|-------|
| Config overwrites | MEDIUM | Running install --host X overwrites ~/.ocmf/config.sh |
| No warning on switch | MEDIUM | User may not realize config changed |
| Memory persists | INFO | Previous memories remain visible |

---

## Verdict

**PASS** - Switching from Codex to Claude works correctly.
