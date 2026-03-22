# OCMF Phase 7C Evidence Report

**Run ID**: 030-unified-install-e2e
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **PHASE** | 7C (Unified Install E2E) |
| **UNIFIED_INSTALL_E2E** | **PASS** |
| **CLAUDE_WIRING_CORRECT** | **YES** |
| **CODEX_WIRING_CORRECT** | **YES** |
| **UNIFIED_STATUS_RELIABLE** | **YES** |
| **QUICKSTART_TRUTHFUL** | **YES** |

---

## DELIVERABLES

### Phase 7C: Unified Install E2E

| Deliverable | File | Status |
|-------------|------|--------|
| Host Detection Fix | `src/ocmaf/cli/host_detection.py` | ✓ Fixed |
| Claude Setup | `src/ocmaf/hosts/claude_setup.sh` | ✓ Updated |
| Codex Setup | `src/ocmaf/hosts/codex_setup.sh` | ✓ Updated |
| Quickstart | `docs/quickstart.md` | ✓ Updated |
| E2E Evidence | `runs/030-unified-install-e2e/e2e_evidence.md` | ✓ Created |

---

## CATEGORIZATION

### Product Mainline (Phase 7A/7B/7C)

Features actively being developed and maintained:

1. **Unified CLI** (`ocmaf unified`)
   - `install` - Auto-setup for host
   - `status` - Show memory status
   - `config` - Show configuration
   - `recall` - Find memories with provenance
   - `remember` - Save memories
   - `doctor` - Diagnose issues

2. **Auto-Memory** (OCMF_AUTO_MEMORY=1,2,3)
   - Session start auto-recall (Claude only)
   - Session end auto-remember
   - Configurable levels

3. **Host Detection** (FIXED in Phase 7C)
   - Uses env vars, NOT binary existence
   - Correctly distinguishes runtime vs installed

### Regression Guardrail (Phase 6G)

Protected features:

1. **Golden Examples** (Phase 6F)
   - `recall_conflict_golden.txt`
   - `explain_crosshost_golden.txt`
   - `recall_provenance_golden.txt`
   - `injection_text_golden.txt`

2. **Regression Gate** (Phase 6G)
   - `runs/028-regression-gate/run_regression_gate.py`
   - `ops/integrated_gate.sh`

### Host-Specific Paths

| Host | Method | Status | Auto-Memory | Verified |
|------|--------|--------|-------------|----------|
| Claude | A1+B | ✓ Supported | ✓ Via MCP | ✓ E2E |
| Codex | C | ✓ Supported | ✗ Manual only | ✓ Config |
| OpenClaw | BLOCKED | ⚠️ BLOCKED | ⚠️ Blocked | ✗ |

### Specified-Only (Not Implemented)

| Feature | Spec | Reason |
|---------|------|--------|
| OpenClaw unblock | FR-048 | GitHub release unavailable |
| Semantic conflict detection | FR-050 | Would need embeddings |
| User conflict resolution UI | FR-052 | UI layer |

---

## PHASE 7C FIXES

### Host Detection Fix (T-7C-06)

**Before (Phase 7A/7B)**:
- Codex detection used `shutil.which("codex")` as indicator
- Binary existence alone could trigger "codex detected"
- Unreliable - binary exists ≠ Codex is running

**After (Phase 7C)**:
- Only CODEX_API_KEY env var triggers "codex detected"
- Binary existence labeled as "installed (not active)"
- Clear distinction: "installed_capability" vs "current_runtime_host"

### Claude Wiring Fix (T-7C-02)

**Before**:
- Script claimed to configure A1+B
- Did not clearly explain what A1+B actually means
- Could mislead users about auto-recall capability

**After**:
- Clear documentation: "Method A1+B foundation"
- Explains MCP mode vs CLI mode
- Truthful about what auto-memory means for Claude

### Codex Wiring Fix (T-7C-04)

**Before**:
- MCP config entry point unclear
- Could mislead users about auto-memory capability

**After**:
- MCP config with proper cwd and PYTHONPATH
- Clear: Method C = manual recall/remember only

### Quickstart Fix (T-7C-07)

**Before**:
- Claimed "Auto-memory: Supported" for both hosts
- Did not clarify Claude vs Codex difference
- Could mislead users

**After**:
- Clear tables showing Claude vs Codex difference
- Honest about what works and what doesn't
- CLI usage with PYTHONPATH documented

---

## E2E EVIDENCE

### Verified E2E Path

```
1. Install: pip install -e /path/to/ocmf
2. Setup: source ~/.ocmf/hosts/claude_setup.sh
3. Config: source ~/.ocmf/config.sh
4. Status: PYTHONPATH=src ocmaf unified status
5. Remember: PYTHONPATH=src ocmaf remember --content "..."
6. Recall: PYTHONPATH=src ocmaf recall --query "..."
```

**Result**: ✓ Works end-to-end

---

## FILES CREATED/MODIFIED

| File | Change |
|------|--------|
| `src/ocmaf/cli/host_detection.py` | Fixed to use env vars |
| `src/ocmaf/hosts/claude_setup.sh` | Honest A1+B documentation |
| `src/ocmaf/hosts/codex_setup.sh` | Fixed MCP entry point |
| `docs/quickstart.md` | Truthful quickstart |
| `runs/030-unified-install-e2e/e2e_evidence.md` | E2E test results |
| `runs/030-unified-install-e2e/evidence.md` | This file |
| `runs/030-unified-install-e2e/known_limits.md` | Known limits |

---

**FINAL_STATUS: PASS**
**UNIFIED_INSTALL_E2E: PASS**
**CLAUDE_WIRING_CORRECT: YES**
**CODEX_WIRING_CORRECT: YES**
**UNIFIED_STATUS_RELIABLE: YES**
**QUICKSTART_TRUTHFUL: YES**
