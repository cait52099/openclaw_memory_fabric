# OCMF Phase 032: Install Closure Final Evidence

**Run ID**: 032-install-closure-final
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **CLAUDE_CONFIG_MERGE_WORKS** | **YES** |
| **INSTALLED_PATH_IDENTITY_WORKS** | **YES** |
| **QUICKSTART_UNIFIED_MAINLINE** | **YES** |
| **SMOKE_TESTS** | **PASS** |
| **REGRESSION_GATE** | **4/4 PASS** |

---

## FIXES IMPLEMENTED

### Fix 1: Claude Config Merge

**Problem**: When `~/.claude/mcp_servers.json` already exists, `claude_setup.sh` just printed "please add manually" and skipped.

**File Fixed**: `src/ocmaf/hosts/claude_setup.sh`

**Before**:
```
MCP config exists: ~/.claude/mcp_servers.json
(To add OCMF, manually add to mcp_servers.json)
```

**After**:
```
MCP config exists: ~/.claude/mcp_servers.json
Merging OCMF into existing MCP config...
✓ OCMF already in MCP config
✓ Merged MCP config
```

**Implementation**: Uses Python to safely merge OCMF entry into existing JSON config without overwriting other entries.

---

### Fix 2: OCMF_SOURCE_TOOL Fallback

**Problem**: When host detection fails (outside Claude/Codex env), `remember`/`recall` showed "Source: Unknown" or "From cli".

**Files Fixed**: `src/ocmaf/cli/unified.py`

**Before**:
```
✓ Remembered: abc123
  Source: Unknown
```

**After**:
```
✓ Remembered: abc123
  Source: Claude
```

**Implementation**: When `host_info.get("source_tool")` returns "cli" (detection failed), now falls back to `OCMF_SOURCE_TOOL` env var (set by `source ~/.ocmf/config.sh`).

---

### Fix 3: Quickstart Unified Mainline

**Problem**: Quickstart told users to `source src/ocmaf/hosts/*.sh` directly, which is not the intended UX.

**File Fixed**: `docs/quickstart.md`

**Before**:
```bash
source src/ocmaf/hosts/claude_setup.sh
```

**After**:
```bash
PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
source ~/.ocmf/config.sh
```

---

## E2E EVIDENCE

### Claude Install -> Remember -> Recall

```
=== Step 1: Install ===
$ PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
✓ claude setup completed successfully
✓ Installation complete!

=== Step 2: Config ===
$ source ~/.ocmf/config.sh
$ echo $OCMF_SOURCE_TOOL
claude-code

=== Step 3: Remember ===
$ PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Using Claude for project memory" --type decision
✓ Remembered: 565beb2c-0826-4630-9bf1-bf84ed1d3257
  Source: Claude

=== Step 4: Recall ===
$ PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "Claude"
Found 1 memories:

From Claude:
  • "Using Claude for project memory" (2026-03-22 06:15)
```

### Codex Install

```
$ PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex
✓ codex setup completed successfully
✓ Installation complete!
```

---

## SMOKE TESTS

```
✓ Test 1: unified CLI loads
✓ Test 2: host detection works - unknown
✓ Test 3: storage accessible - events=32, memories=31
✓ Test 4: recall works

=== ALL SMOKE TESTS PASSED ===
```

---

## REGRESSION GATE

```
✓ recall_conflict: PASS
✓ explain_crosshost: PASS
✓ recall_provenance: PASS
✓ injection_text: PASS

✓ REGRESSION GATE: PASS
```

---

## FILES MODIFIED

| File | Change |
|------|--------|
| `src/ocmaf/hosts/claude_setup.sh` | Added config merge logic |
| `src/ocmaf/cli/unified.py` | Added OCMF_SOURCE_TOOL fallback |
| `docs/quickstart.md` | Changed to unified install main path |

---

**FINAL_STATUS: PASS**
**CLAUDE_CONFIG_MERGE_WORKS: YES**
**INSTALLED_PATH_IDENTITY_WORKS: YES**
**QUICKSTART_UNIFIED_MAINLINE: YES**
