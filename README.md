# OCMF - OpenClaw Memory Fabric

**Unified memory layer for AI tools.**

OCMF gives your AI tools (Claude, Codex) a shared memory. It remembers project constraints, decisions, preferences, and cross-tool context — so you don't have to repeat yourself.

---

## Current Status

| Item | Status |
|------|--------|
| **Environment** | Stable (current-env stable) |
| **Development Install** | ✓ Available |
| **Formal Release (PyPI)** | ✗ Not published |
| **Trusted User Journey** | ✓ Verified (phases 035-050) |
| **Global Install** | ✓ Verified (phase 052) |
| **Quickstart** | ✓ Verified (phase 054) |

---

## What is OCMF?

OCMF solves the **memory fragmentation problem** across AI tools:

- When using Claude, your decisions and context are remembered
- When switching to Codex, the same memories are available
- No need to re-explain project constraints, preferences, or history

### Key Features

- **Unified Memory Protocol**: Common event format for all AI hosts
- **Cross-Host Memory**: Share memories between Claude and Codex
- **Provenance Tracking**: Always know where a memory came from
- **Event Sourcing**: All memories traceable to original events
- **Low-Friction Install**: Simple development install, global command

---

## Supported Hosts

| Host | Method | Status | Auto-Memory |
|------|--------|--------|-------------|
| Claude | A1 + B | ✓ Works | ✓ Via MCP |
| Codex | C | ✓ Works | ✗ Manual only |
| OpenClaw | N/A | ⚠️ Blocked | N/A |

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Development Install

```bash
# Clone or navigate to OCMF project directory
cd /path/to/openclaw_memory_fabric

# Install in development mode
python3 -m pip install -e .
```

This makes the `ocmaf` command available globally.

---

## Quick Start

### 1. Install for your AI host

**For Claude:**
```bash
ocmaf install --host claude
```

**For Codex:**
```bash
ocmaf install --host codex
```

### 2. Use it

```bash
# Remember something
ocmaf remember --content "Using PostgreSQL for the main database"

# Recall memories
ocmaf recall --query "database choices"

# Check status
ocmaf status

# Verify setup
ocmaf doctor
```

---

## How It Works

### Memory Attribution

Every memory knows its source:

```
ocmaf recall --query "database"
Found 1 memories:

From Claude:
  • "Using PostgreSQL for the main database" (2026-03-22)
```

### Cross-Host Sharing

Memories from Claude are visible to Codex and vice versa:

```
ocmaf recall --query "project decisions"
Found 2 memories:

From Codex:
  • "SQLite for local development"

From Claude:
  • "PostgreSQL for production"
```

---

## Project Structure

```
openclaw_memory_fabric/
├── src/ocmaf/
│   ├── cli/           # CLI implementation
│   ├── hosts/         # Host-specific adapters
│   └── ...
├── docs/              # Documentation
├── runs/              # Evidence from phases
└── ops/               # Operations scripts
```

---

## Limitations

- **Formal Release**: PyPI release not yet published
- **OpenClaw**: Support blocked (GitHub release unavailable)
- **Auto-Memory**: Codex requires manual recall/remember
- **Root Cause**: Identity drift issue not yet fully identified

---

## Documentation

- [Quickstart Guide](docs/quickstart.md)
- [OCMF Constitution](.specify/memory/constitution.md)
- [Full Documentation](docs/)

---

## Evidence & Phases

All work is logged with evidence in `runs/<phase_id>/`:

| Phase | Focus | Status |
|-------|-------|--------|
| 035-050 | Trusted User Journey | ✓ PASS |
| 051 | Bootstrap wrapper | ✓ PASS |
| 052 | Global install | ✓ PASS |
| 053 | Shell/PATH polish | ✓ PASS |
| 054 | Quickstart polish | ✓ PASS |
| 055 | Release/distribution | ✓ PASS |

---

## Contributing

This project uses a structured development process:
- Specifications in `docs/spec.md`
- Implementation plans in `docs/plan.md`
- Phase evidence in `runs/<run_id>/`

---

## License

MIT
