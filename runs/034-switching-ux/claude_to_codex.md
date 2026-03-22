# Claude to Codex Switching Test

**Run ID**: 034-switching-ux
**Task**: T-7E-01
**Date**: 2026-03-22
**Status**: PASS

---

## Test Steps

### Step 1: Claude configured first
```bash
rm -rf ~/.ocmf
PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
source ~/.ocmf/config.sh
```
**Result**: ✓ OCMF_SOURCE_TOOL=claude-code

### Step 2: Switch to Codex
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex
```
**Result**: ✓ Codex install ran

### Step 3: Check config after switch
```bash
source ~/.ocmf/config.sh
echo $OCMF_SOURCE_TOOL
```
**Result**: ✓ OCMF_SOURCE_TOOL=codex-cli

### Step 4: Remember in "Codex" context
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Codex decision: Use Redis" --type decision
```
**Result**: ✓ Source: Codex

### Step 5: Recall
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "Redis"
```
**Result**: ✓ "From Codex: Codex decision: Use Redis"

---

## Friction Points

| Friction | Severity | Notes |
|----------|----------|-------|
| Config overwrites | MEDIUM | Running install --host X overwrites ~/.ocmf/config.sh |
| No warning on switch | MEDIUM | User may not realize config changed |

---

## Verdict

**PASS** - Switching from Claude to Codex works correctly.
