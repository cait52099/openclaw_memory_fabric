# Cross-Host Memory Sharing Test

**Run ID**: 034-switching-ux
**Task**: T-7E-03
**Date**: 2026-03-22
**Status**: PASS

---

## Test Scenario

Verify that Claude writes memory → switch to Codex → Codex can recall Claude's memory

---

## Test Steps

### Step 1: Claude writes memory
```bash
rm -rf ~/.ocmf
PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
source ~/.ocmf/config.sh
PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Cross-host shared memory: Use Kubernetes" --type decision
```
**Result**: ✓ Source: Claude

### Step 2: Switch to Codex
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex
source ~/.ocmf/config.sh
echo $OCMF_SOURCE_TOOL
```
**Result**: ✓ OCMF_SOURCE_TOOL=codex-cli

### Step 3: Recall from Codex context
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "Kubernetes"
```
**Result**: ✓ "From Claude: Cross-host shared memory: Use Kubernetes"

---

## Key Finding

**Cross-host memory sharing WORKS.** When Claude writes a memory, switching to Codex and recalling shows the memory with correct "From Claude:" attribution.

---

## Friction Points

| Friction | Severity | Notes |
|----------|----------|-------|
| Shared memory.db | INFO | Both hosts use same ~/.ocmf/memory.db |
| Source attribution | INFO | Memories correctly attributed to writing host |

---

## Verdict

**PASS** - Cross-host memory sharing works correctly.
