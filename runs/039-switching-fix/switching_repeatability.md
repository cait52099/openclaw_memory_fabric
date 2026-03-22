# Switching Repeatability Test - Phase 039

**Run ID**: 039-switching-fix
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## Executive Summary

Full switching repeatability test (3 cycles × 3 steps) **ALL PASSED**.

The switching behavior is now stable and deterministic. Both `claude_setup.sh` and `codex_setup.sh` now include defensive identity verification that will catch any edge case failures.

---

## Test Results

### Cycle 1: Claude → Codex → Claude

| Step | Install | Config Source | Source Attribution |
|------|---------|--------------|-------------------|
| 1 | `install --host claude` | `claude-code` ✓ | `Source: Claude` ✓ |
| 2 | `install --host codex` | `codex-cli` ✓ | `Source: Codex` ✓ |
| 3 | `install --host claude` | `claude-code` ✓ | `Source: Claude` ✓ |

### Cycle 2: Claude → Codex → Claude

| Step | Install | Config Source | Source Attribution |
|------|---------|--------------|-------------------|
| 1 | `install --host claude` | `claude-code` ✓ | `Source: Claude` ✓ |
| 2 | `install --host codex` | `codex-cli` ✓ | `Source: Codex` ✓ |
| 3 | `install --host claude` | `claude-code` ✓ | `Source: Claude` ✓ |

### Cycle 3: Claude → Codex → Claude

| Step | Install | Config Source | Source Attribution |
|------|---------|--------------|-------------------|
| 1 | `install --host claude` | `claude-code` ✓ | `Source: Claude` ✓ |
| 2 | `install --host codex` | `codex-cli` ✓ | `Source: Codex` ✓ |
| 3 | `install --host claude` | `claude-code` ✓ | `Source: Claude` ✓ |

---

## Switch Without Clean Test

Tested switching without cleaning `~/.ocmf` directory (only switching config):

| Step | Config Source | Source Attribution |
|------|--------------|-------------------|
| Claude | `claude-code` ✓ | `Source: Claude` ✓ |
| Codex | `codex-cli` ✓ | `Source: Codex` ✓ |
| Claude restore | `claude-code` ✓ | `Source: Claude` ✓ |

---

## Fixes Applied

### 1. claude_setup.sh
- Added defensive identity verification
- Script now fails explicitly if `OCMF_SOURCE_TOOL` is not `claude-code` after writing

### 2. codex_setup.sh
- Added defensive identity verification
- Script now fails explicitly if `OCMF_SOURCE_TOOL` is not `codex-cli` after writing

---

## Verdict

**SWITCHING_REPEATABLE_3X: YES**
**CLAUDE_CODEX_CLAUDE_STABLE: YES**

All switching cycles passed with correct identity at every step.
