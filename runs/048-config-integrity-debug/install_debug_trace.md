# Install Debug Trace - Phase 048

**Run ID**: 048-config-integrity-debug
**Date**: 2026-03-22
**Status**: COMPLETE
**Task Type**: PRODUCT MAINLINE

---

## Trace Summary

Config integrity issue NOT reproducible. All syntax checks pass.

---

## 3x Codex Install Cycle

```
--- Cycle 1/3 ---
Running codex install...
✓ Created /Users/caihongwei/.ocmf/config.sh
  ✓ Verified OCMF_SOURCE_TOOL=codex-cli
✓ Created /Users/caihongwei/.codex/mcp.json
✓ Created /Users/caihongwei/.ocmf/codex_helpers.sh
✓ OCMF CLI importable
Config syntax check...
bash -n: 0
Source test...
source: 0
Config check...
export OCMF_SOURCE_TOOL="codex-cli"

--- Cycle 2/3 ---
✓ Verified OCMF_SOURCE_TOOL=codex-cli
bash -n: 0
source: 0
export OCMF_SOURCE_TOOL="codex-cli"

--- Cycle 3/3 ---
✓ Verified OCMF_SOURCE_TOOL=codex-cli
bash -n: 0
source: 0
export OCMF_SOURCE_TOOL="codex-cli"
```

---

## 046-Like Replay

### B1. Claude First Step

```
$ PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
✓ Claude Setup Complete

OCMF_SOURCE_TOOL=claude-code
✓ Remembered: ee34f270-c353-4f6f-a330-3f2657dc9863
  Source: Claude

Found 1 memories:
From Claude:
  • "T048_CLAUDE_1" (2026-03-22 08:34)
```

### B2. Codex Step

```
$ PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex
✓ Codex Setup Complete

OCMF_SOURCE_TOOL=codex-cli
bash -n ~/.ocmf/config.sh: Exit 0

✓ Remembered: 2394b229-7168-4089-9cf4-abf393ed0144
  Source: Codex

Found 3 memories:
From Codex:
  • "T048_CODEX" (2026-03-22 08:34)
  • "T048_CODEX_TEST" (2026-03-22 08:34)
From Claude:
  • "T048_CLAUDE_1" (2026-03-22 08:34)
```

### B3. Claude Restore

```
$ PYTHONPATH=src python3 -m ocmf.cli.unified install --host claude
✓ Claude Setup Complete

OCMF_SOURCE_TOOL=claude-code
bash -n ~/.ocmf/config.sh: Exit 0

✓ Remembered: 349ae77b-6f67-4eec-9ec1-333bd309e199
  Source: Claude

Found 4 memories:
From Claude:
  • "T048_CLAUDE_RESTORE" (2026-03-22 08:34)
  • "T048_CLAUDE_1" (2026-03-22 08:34)
From Codex:
  • "T048_CODEX" (2026-03-22 08:34)
  • "T048_CODEX_TEST" (2026-03-22 08:34)
```

---

## Defensive Verification

Both setup scripts include explicit verification:

```bash
# From codex_setup.sh
ACTUAL_TOOL="$(grep 'OCMF_SOURCE_TOOL=' "$OCMF_CONFIG" | head -1 | cut -d'"' -f2 2>/dev/null || echo 'UNKNOWN')"
if [ "$ACTUAL_TOOL" != "codex-cli" ]; then
    echo "✗ ERROR: Config verification failed!"
    exit 1
fi
echo "  ✓ Verified OCMF_SOURCE_TOOL=codex-cli"
```

---

## Conclusion

**CONFIG INTEGRITY: STABLE**
**CONFIG SYNTAX ISSUE: NOT REPRODUCIBLE**
