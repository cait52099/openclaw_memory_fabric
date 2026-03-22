# Trusted User Journey Report

**Run ID**: 036-user-journey-trusted
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## Executive Summary

All user journey tests PASSED. The clean-home first-use path is now stable and trustworthy.

---

## Test Results

### 1. Claude Clean-Home First-Use Path

| Step | Command | Result |
|------|---------|--------|
| Clean home | `rm -rf ~/.ocmf && rm -f ~/.claude/mcp_servers.json` | ✓ |
| Install | `PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude` | ✓ |
| Config verify | `grep OCMF_SOURCE_TOOL ~/.ocmf/config.sh` | `claude-code` ✓ |
| Source config | `source ~/.ocmf/config.sh` | ✓ |
| Remember | `remember --content "Claude path works correctly"` | `Source: Claude` ✓ |
| Recall | `recall --query "User journey test"` | `From Claude:` ✓ |

**Evidence**: remember showed "Source: Claude", recall showed "From Claude:"

### 2. Codex Clean-Home First-Use Path

| Step | Command | Result |
|------|---------|--------|
| Clean home | `rm -rf ~/.ocmf && rm -f ~/.codex/mcp.json` | ✓ |
| Install | `PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex` | ✓ |
| Config verify | `grep OCMF_SOURCE_TOOL ~/.ocmf/config.sh` | `codex-cli` ✓ |
| Source config | `source ~/.ocmf/config.sh` | ✓ |
| Remember | `remember --content "Codex path works correctly"` | `Source: Codex` ✓ |
| Recall | `recall --query "User journey test"` | `From Codex:` ✓ |

**Evidence**: remember showed "Source: Codex", recall showed "From Codex:"

### 3. Claude → Codex Switching

| Step | Result |
|------|--------|
| `install --host codex` | ✓ Config changes to `codex-cli` |
| Remember | `Source: Codex` ✓ |
| Recall | Shows cross-host memories correctly |

### 4. Codex → Claude Switching

| Step | Result |
|------|--------|
| `install --host claude` | ✓ Config changes to `claude-code` |
| Remember | `Source: Claude` ✓ |
| Recall | Shows cross-host memories correctly |

---

## User Journey Flow

```
┌─────────────────────────────────────────────────────────────┐
│ CLAUDE FIRST USE                                            │
├─────────────────────────────────────────────────────────────┤
│ 1. rm -rf ~/.ocmf ~/.claude/mcp_servers.json               │
│ 2. PYTHONPATH=src python3 -m ocmaf.cli.unified \           │
│    install --host claude                                    │
│ 3. source ~/.ocmf/config.sh                                 │
│ 4. PYTHONPATH=src python3 -m ocmaf.cli.unified \           │
│    remember --content "..." --type decision                 │
│ 5. PYTHONPATH=src python3 -m ocmaf.cli.unified \           │
│    recall --query "..."                                     │
│                                                              │
│ EXPECTED: Source: Claude / From Claude:                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CODEX FIRST USE                                             │
├─────────────────────────────────────────────────────────────┤
│ 1. rm -rf ~/.ocmf ~/.codex/mcp.json                        │
│ 2. PYTHONPATH=src python3 -m ocmaf.cli.unified \           │
│    install --host codex                                     │
│ 3. source ~/.ocmf/config.sh                                 │
│ 4. PYTHONPATH=src python3 -m ocmaf.cli.unified \           │
│    remember --content "..." --type decision                 │
│ 5. PYTHONPATH=src python3 -m ocmaf.cli.unified \           │
│    recall --query "..."                                     │
│                                                              │
│ EXPECTED: Source: Codex / From Codex:                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Verdict

**PASS** - Trusted User Journey Achieved

1. Claude path works end-to-end ✓
2. Codex path works end-to-end ✓
3. Cross-host switching works correctly ✓
4. Source attribution is correct ✓
5. Cross-host memory sharing works ✓
