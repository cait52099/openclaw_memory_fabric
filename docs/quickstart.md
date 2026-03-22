# OCMF Quickstart Guide

**OpenClaw Memory Fabric** - Memory that works across AI hosts.

## What is OCMF?

OCMF gives your AI tools (Claude, Codex) a shared memory. It remembers:

- Project constraints and decisions
- What worked and what didn't
- Your preferences and style
- Cross-tool context

You don't need to repeat yourself. OCMF handles it.

---

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

---

## 1. Install

From the OCMF project directory:

```bash
python3 -m pip install -e .
```

This installs OCMF globally and makes the `ocmaf` command available from any directory.

---

## 2. First Use

### For Claude

```bash
ocmaf install --host claude
```

### For Codex

```bash
ocmaf install --host codex
```

That's it! `ocmaf` works from any directory and automatically handles config sourcing.

---

## 3. Daily Usage

### Remember something

```bash
ocmaf remember --content "Using PostgreSQL for the main database"
```

### Recall memories

```bash
ocmaf recall --query "database choices"
```

OCMF automatically shows:
- Where the memory came from (Claude, Codex)
- When it was created
- Any conflicts

### Check status

```bash
ocmaf status
```

### Verify setup

```bash
ocmaf doctor
```

---

## How It Works

### Claude

- **Method**: A1 (native hooks) + B (system-prompt)
- **Usage**: Use `ocmaf` CLI directly
- **Auto-memory**: Supported (if using MCP mode)

### Codex

- **Method**: C (manual MCP)
- **Usage**: Use `ocmaf` CLI directly
- **Auto-memory**: NOT supported (manual recall/remember only)

---

## You Don't Need to Know

These are handled automatically. Don't worry about them:

- ✓ Host method (A1, B, C) - we detect and configure automatically
- ✓ Source tool identification - automatic
- ✓ Provenance tracking - automatic
- ✓ Conflict detection - automatic

**Note**: MCP configuration is set up by the install command, but requires restart of Claude/Codex to take effect.

---

## Conflict Handling

When memories disagree, OCMF shows:

```
⚠️ CONFLICT DETECTED

[Claude] "Use PostgreSQL"
[Codex]  "SQLite is better"

Review before continuing.
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OCMF_AUTO_MEMORY` | 0 | 0=off, 1=recall, 2=remember, 3=both |
| `OCMF_SCOPE_USER` | current user | Your user ID |
| `OCMF_SCOPE_PROJECT` | auto | Project name |
| `OCMF_RECALL_LIMIT` | 10 | Max memories to recall |

### Host Support

| Host | Method | Status | Auto-Memory |
|------|--------|--------|-------------|
| Claude | A1+B | ✓ Works | ✓ Via MCP |
| Codex | C | ✓ Works | ✗ Manual only |
| OpenClaw | BLOCKED | ⚠️ | ⚠️ |

---

## Troubleshooting / Advanced

### "Host not detected"

This is normal if you're running outside Claude/Codex environment.
The setup still works - you can use CLI mode directly:

```bash
ocmaf recall --query "..."
```

### Check Setup

```bash
ocmaf doctor
```

### Using Python Directly (Advanced)

If you need to use Python directly without the `ocmaf` command:

```bash
# Set PYTHONPATH to the src directory
export PYTHONPATH=/path/to/openclaw_memory_fabric/src

# Install for a specific host
python3 -m ocmaf.cli.unified install --host claude

# Remember/recall using Python module
python3 -m ocmaf.cli.unified remember --content "..."
python3 -m ocmaf.cli.unified recall --query "..."

# Source the OCMF config for environment variables
source ~/.ocmf/config.sh
```

**Note**: The `python3 -m pip install -e .` method above is the recommended approach. The Python-direct method above is for advanced users who need fine-grained control.

---

## What Gets Remembered

OCMF extracts from your conversations:

1. **Decisions**: "decided to use X", "choosing Y"
2. **Facts**: "the project uses Z", "configured to..."
3. **Preferences**: "prefer X over Y", "like better..."

---

## Evidence

All operations are logged to `runs/<run_id>/` for audit.

---

## Need Help?

```bash
ocmaf --help
ocmaf install --help
ocmaf recall --help
```
