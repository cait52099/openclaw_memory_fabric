# Bootstrap Design - Phase 051

**Run ID**: 051-product-polish
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## Goal

Remove two highest-friction user experience points:
1. No need to manually write `PYTHONPATH=src`
2. No need to manually `source ~/.ocmf/config.sh` after install

---

## Solution: OCMF Bootstrap Wrapper

Created `ocmaf` wrapper script at project root that:
1. Sets PYTHONPATH internally
2. Auto-sources `~/.ocmf/config.sh` if it exists
3. Delegates to the unified CLI

---

## Wrapper Script

```bash
#!/bin/bash
# OCMF Bootstrap Wrapper
# This script provides a convenient entry point to OCMF CLI
# without requiring users to set PYTHONPATH manually.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Set PYTHONPATH to include the src directory
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"

# Auto-source OCMF config if it exists (provides OCMF_SOURCE_TOOL and other env vars)
if [ -f "${HOME}/.ocmf/config.sh" ]; then
    source "${HOME}/.ocmf/config.sh"
fi

# Run the OCMF CLI with any passed arguments
exec python3 -m ocmaf.cli.unified "$@"
```

---

## Usage Comparison

### Before (Old Way)
```bash
# Set PYTHONPATH manually
export PYTHONPATH=src

# Install
python3 -m ocmaf.cli.unified install --host claude

# Had to manually source config
source ~/.ocmf/config.sh

# Remember/recall
python3 -m ocmaf.cli.unified remember --content "..."
python3 -m ocmaf.cli.unified recall --query "..."
```

### After (New Way)
```bash
# Install
./ocmaf install --host claude

# Remember/recall - no manual source needed
./ocmaf remember --content "..."
./ocmaf recall --query "..."
```

---

## New Quickstart

```bash
# 1. Clone/fetch OCMF
cd /path/to/openclaw_memory_fabric

# 2. Install for Claude (no PYTHONPATH needed)
./ocmaf install --host claude

# 3. That's it! Remember and recall work directly
./ocmaf remember --content "My first memory"
./ocmaf recall --query "first memory"

# For Codex:
./ocmaf install --host codex
./ocmaf remember --content "Codex memory"
./ocmf recall --query "codex memory"
```

---

## Limitations

1. **Wrapper must be in project directory**: Users need to be in the OCMF directory to run `./ocmaf`
2. **Full path required for global use**: Or add OCMF to PATH

---

## Future Polish Options (Not in Scope)

1. **Global install**: `pip install -e .` to make `ocmaf` available globally (blocked by pyproject.toml issue)
2. **PATH addition**: Add OCMF bin to PATH during install
3. **Shell integration**: Auto-add wrapper to PATH via install script
