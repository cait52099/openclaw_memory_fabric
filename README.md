# OCMF — OpenClaw Memory Fabric

OCMF is a cross-host memory layer for AI developer tools.

It gives Claude and Codex a shared, traceable memory for project decisions, constraints, preferences, and execution context — so you do not have to repeatedly restate the same information across tools.

## Why OCMF exists

When you work across multiple AI tools, memory becomes fragmented:

- Claude remembers one set of decisions
- Codex sees a different local context
- important constraints get repeated, drift, or disappear
- tool switching breaks continuity

OCMF solves that by providing a unified memory fabric with:

- shared memory across supported hosts
- provenance-aware recall
- event-backed memory records
- a unified CLI for install / remember / recall
- auditable outputs and evidence-driven validation

## What OCMF does

### Shared memory across hosts
Claude and Codex can read from the same memory layer.

### Provenance-aware recall
Recall results show where a memory came from, such as:

- `From Claude`
- `From Codex`

### Unified CLI
A single `ocmaf` command handles:

- host install
- remember
- recall
- status
- doctor

### Event-backed model
Memories are stored as traceable events instead of opaque blobs.

### Cross-host context
OCMF is designed for workflows where more than one AI host participates in the same project lifecycle.

## Current status

| Area | Status |
|---|---|
| Trusted user journey | Verified in current environment |
| Development install | Available |
| Global CLI (`ocmaf`) | Available |
| Quickstart | Verified |
| Wheel install rehearsal | Verified |
| Formal release readiness | Completed |
| Formal PyPI release | Not published |
| TestPyPI rehearsal | In progress / environment-dependent |
| OpenClaw host | Blocked / TBD |

> Current boundary:
>
> - `CURRENT_ENV_STABLE = YES`
> - `ROOT_CAUSE_IDENTIFIED = NO`
>
> This means the main user journey is working in the current environment, but unresolved lower-level root-cause analysis is still explicitly not claimed as complete.

## Supported hosts

| Host | Status | Production path | Auto-memory |
|---|---|---|---|
| Claude | Supported | A1 + B | Supported |
| Codex | Supported | C | Manual / explicit path |
| OpenClaw | Blocked / TBD | N/A | N/A |

### Host notes

- **Claude** currently has the strongest end-user path.
- **Codex** is supported through the explicit/manual MCP-oriented path.
- **OpenClaw** is not yet available as a supported host.

## Who this is for

OCMF is designed for developers who use more than one AI tool in the same workflow and want:

- less context repetition
- shared project memory across hosts
- traceable provenance
- auditable CLI behavior
- a memory layer that can be validated instead of guessed

## Installation

### Prerequisites

- Python 3.11+
- pip
- macOS / Linux shell environment recommended for the current validated path

### Development install

```bash
git clone git@github.com:cait52099/openclaw_memory_fabric.git
cd openclaw_memory_fabric
python3 -m pip install -e .
