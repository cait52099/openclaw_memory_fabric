# OCMF Phase 7A/7B Evidence Report

**Run ID**: 029-unified-entry
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **PHASE** | 7A (Unified Entry) + 7B (Auto-Memory) |
| **UNIFIED_ENTRY_READY** | **YES** |
| **AUTO_MEMORY_MAINLINE_READY** | **YES** |
| **REGRESSION_GUARDRAIL_ATTACHED** | **YES** |

---

## DELIVERABLES

### Phase 7A: Unified Entry Point

| Deliverable | File | Status |
|-------------|------|--------|
| Unified CLI Interface | `src/ocmaf/cli/unified.py` | ✓ Created |
| Host Auto-Detection | `src/ocmaf/cli/host_detection.py` | ✓ Created |
| Claude Setup Script | `src/ocmaf/hosts/claude_setup.sh` | ✓ Created |
| Codex Setup Script | `src/ocmaf/hosts/codex_setup.sh` | ✓ Created |

### Phase 7B: Automatic Memory Experience

| Deliverable | File | Status |
|-------------|------|--------|
| Auto-Memory Behavior Spec | `docs/auto_memory_behavior.md` | ✓ Created |
| Auto-Recall Implementation | `src/ocmaf/api/auto_recall.py` | ✓ Created |
| Auto-Remember Implementation | `src/ocmaf/api/auto_remember.py` | ✓ Created |
| Regression Gate Integration | `ops/integrated_gate.sh` | ✓ Created |
| User Quickstart | `docs/quickstart.md` | ✓ Created |
| Validation Report | `runs/029-unified-entry/validation.md` | ✓ Created |

---

## CATEGORIZATION

### Product Mainline (Phase 7A/7B)

Features actively being developed and maintained:

1. **Unified CLI** (`ocmaf unified`)
   - `install` - Auto-setup for host
   - `status` - Show memory status
   - `config` - Show configuration
   - `recall` - Find memories with provenance
   - `remember` - Save memories
   - `doctor` - Diagnose issues

2. **Auto-Memory** (OCMF_AUTO_MEMORY=1,2,3)
   - Session start auto-recall
   - Session end auto-remember
   - Configurable levels

3. **Host Detection** (automatic)
   - Claude → Method A1+B, auto-memory supported
   - Codex → Method C, manual only
   - OpenClaw → BLOCKED

### Regression Guardrail (Phase 6G)

Features protected from regression:

1. **Golden Examples** (Phase 6F)
   - `recall_conflict_golden.txt`
   - `explain_crosshost_golden.txt`
   - `recall_provenance_golden.txt`
   - `injection_text_golden.txt`

2. **Regression Gate** (Phase 6G)
   - `runs/028-regression-gate/run_regression_gate.py`
   - Pattern-based comparison (not exact match)
   - `ops/integrated_gate.sh` - Gate attached to main line

3. **Protected Outputs**
   - `⚠️ CONFLICT DETECTED` display
   - `From Claude:` provenance format
   - `match_reasons` in explain
   - `also_written_by` cross-host context

### Host-Specific Paths

| Host | Method | Status | Auto-Memory |
|------|--------|--------|-------------|
| Claude | A1+B | ✓ Supported | ✓ Yes |
| Codex | C | ✓ Supported | ✗ Manual only |
| OpenClaw | TBD | ⚠️ BLOCKED | ⚠️ Blocked |

### Specified-Only (Not Implemented)

Features designed but not currently implemented:

| Feature | Spec | Reason |
|---------|------|--------|
| Semantic conflict detection | FR-050 | Would need embeddings |
| Group by source display | FR-049 | Phase 2 UX enhancement |
| User conflict resolution UI | FR-052 | UI layer |
| OpenClaw unblock | FR-048 | GitHub release unavailable |

---

## EVIDENCE BOUNDARY

### Implemented (This Phase - 7A/7B)

| Feature | Evidence |
|---------|----------|
| Unified CLI | `python3 -m ocmaf.cli.unified --help` works |
| Host detection | `get_host_info()` returns correct host |
| Claude setup | `claude_setup.sh` creates config |
| Codex setup | `codex_setup.sh` creates MCP config |
| Auto-recall | `auto_recall()` returns memories |
| Auto-remember | `auto_remember()` extracts decisions |
| Gate integration | `ops/integrated_gate.sh` returns exit code |

### Implemented (Prior Phases - Protected by Gate)

| Feature | Phase | Protected |
|---------|-------|-----------|
| recall source_tool | 6D | ✓ Yes |
| recall friendly name | 6D | ✓ Yes |
| recall timestamp | 6D | ✓ Yes |
| recall conflict_detected | 6D | ✓ Yes |
| recall candidates | 6D | ✓ Yes |
| explain match_reasons | 6D | ✓ Yes |
| explain also_written_by | 6D | ✓ Yes |
| CLI recall output | 6E | ✓ Yes |
| CLI explain output | 6E | ✓ Yes |
| CLI conflict output | 6E | ✓ Yes |

---

## INTEGRATION POINTS

### With Phase 6G Regression Gate

```
ops/integrated_gate.sh
    └── runs/028-regression-gate/run_regression_gate.py
            ├── recall_conflict_golden.txt
            ├── explain_crosshost_golden.txt
            ├── recall_provenance_golden.txt
            └── injection_text_golden.txt
```

### With Phase 6D API Layer

```
src/ocmaf/api/
    ├── recall.py          # Enhanced with source_tool, friendly, timestamp
    ├── explain.py          # Enhanced with match_reasons, also_written_by
    ├── auto_recall.py      # NEW - wraps recall for auto-memory
    └── auto_remember.py    # NEW - wraps remember for auto-memory
```

### With Host Setup

```
src/ocmaf/hosts/
    ├── claude_setup.sh     # NEW - Method A1+B setup
    └── codex_setup.sh      # NEW - Method C setup
```

---

## FILES CREATED

| File | Purpose |
|------|---------|
| `src/ocmaf/cli/unified.py` | Unified entry CLI |
| `src/ocmaf/cli/host_detection.py` | Host auto-detection |
| `src/ocmaf/hosts/claude_setup.sh` | Claude setup script |
| `src/ocmaf/hosts/codex_setup.sh` | Codex setup script |
| `src/ocmaf/api/auto_recall.py` | Auto-recall implementation |
| `src/ocmaf/api/auto_remember.py` | Auto-remember implementation |
| `docs/auto_memory_behavior.md` | Auto-memory behavior spec |
| `docs/quickstart.md` | User quickstart guide |
| `ops/integrated_gate.sh` | Regression gate integration |
| `runs/029-unified-entry/validation.md` | Validation report |
| `runs/029-unified-entry/evidence.md` | This file |
| `runs/029-unified-entry/known_limits.md` | Known limits |

---

**FINAL_STATUS: PASS**
**UNIFIED_ENTRY_READY: YES**
**AUTO_MEMORY_MAINLINE_READY: YES**
**REGRESSION_GUARDRAIL_ATTACHED: YES**
