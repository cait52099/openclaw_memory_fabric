# Packaging Design - Phase 052

**Run ID**: 052-global-install
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT POLISH

---

## Goal

Enable global installation of `ocmaf` command so users can run from any directory without:
1. Needing to be in the project directory
2. Manually setting PYTHONPATH
3. Manually sourcing config

---

## Changes Made

### 1. Fixed pyproject.toml

**Before:**
```toml
dependencies = [
    "pydantic>=2.0",
    "click>=8.0",
    "sqlite3 (stdlib)",  # INVALID - not a PEP 508 dependency
]
```

**After:**
```toml
dependencies = [
    "pydantic>=2.0",
    "click>=8.0",
]
```

**Before (wrong entry point):**
```toml
ocmaf = "ocmaf.cli.main:cli"
```

**After (correct entry point):**
```toml
ocmaf = "ocmaf.cli.unified:unified"
```

### 2. Added Auto-Source Config to unified.py

Added `_auto_source_config()` function that:
1. Checks if `~/.ocmf/config.sh` exists
2. Sources it using subprocess to capture env vars
3. Updates `os.environ` with OCMF_* variables

This allows the global install to pick up `OCMF_SOURCE_TOOL` without manual sourcing.

---

## Installation

```bash
# Install globally (editable mode for development)
pip install -e /path/to/openclaw_memory_fabric

# Or install globally (one-time)
pip install /path/to/openclaw_memory_fabric
```

---

## Usage

### After Installation

```bash
# From ANY directory
ocmaf install --host claude
ocmaf remember --content "..."
ocmaf recall --query "..."

# For Codex
ocmaf install --host codex
ocmaf remember --content "..."
ocmaf recall --query "..."
```

### What Changed

| Aspect | Before | After |
|--------|--------|-------|
| Working directory | Must be in project dir | Any directory |
| PYTHONPATH | Manual export | Automatic |
| Source config | Manual `source ~/.ocmf/config.sh` | Automatic |
| Entry point | `./ocmaf` (wrapper) | `ocmaf` (global) |

---

## Implementation Details

### Entry Point

The `pyproject.toml` now correctly points to the unified CLI:

```toml
[project.scripts]
ocmaf = "ocmaf.cli.unified:unified"
```

### Auto-Config-Source

Added to `unified.py`:

```python
def _auto_source_config():
    """Auto-source OCMF config if it exists."""
    config_path = Path.home() / ".ocmf" / "config.sh"
    if config_path.exists():
        try:
            result = subprocess.run(
                ["bash", "-c", f"source {config_path} && env"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "=" in line:
                        key, _, value = line.partition("=")
                        if key.startswith("OCMF_"):
                            os.environ[key] = value
        except Exception:
            pass

_auto_source_config()
```

---

## Verification

All commands tested from `/tmp` (not project directory):

| Command | From /tmp | Source Attribution |
|---------|-----------|-------------------|
| `ocmaf install --host claude` | ✓ | N/A |
| `ocmaf remember --content "..."` | ✓ | Source: Claude |
| `ocmaf recall --query "..."` | ✓ | From Claude |
| `ocmaf install --host codex` | ✓ | N/A |
| `ocmaf remember --content "..."` | ✓ | Source: Codex |
| `ocmaf recall --query "..."` | ✓ | From Codex |
| Switching claude→codex→claude | ✓ | Correct attribution |
