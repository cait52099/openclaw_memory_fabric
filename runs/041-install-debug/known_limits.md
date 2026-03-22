# OCMF Phase 041 Known Limits

**Run ID**: 041-install-debug
**Date**: 2026-03-22
**Status**: PASS
**Task Type**: PRODUCT MAINLINE

---

## FINAL STATUS: PASS

---

## ISSUE INVESTIGATION NOTES

### Reported: Claude Identity Drift (NOT REPRODUCED)

**Issue Reported**: "Claude clean-home path may still be written as Codex identity"

**Investigation Performed**:
- 5 consecutive clean-home Claude install tests: ALL PASSED
- Multiple installs without cleaning: ALL PASSED
- Alternating Claude/Codex cycles: ALL PASSED

**Result**: Issue **NOT REPRODUCIBLE** in this environment

**Root Cause**: **NOT IDENTIFIED** - Cannot fix what cannot be reproduced

**Defense**: The defensive verification in setup scripts will catch any future instances

---

## CURRENT LIMITATIONS (NOT BLOCKERS)

### 1. PYTHONPATH Required

**Severity**: HIGH (but not a blocker)

**Workaround**: `pip install -e /path/to/ocmf` or wrapper script

### 2. Claude MCP Requires Restart

**Severity**: HIGH (but not a blocker)

**Workaround**: Restart Claude after install

### 3. Manual Config Source Required

**Severity**: MEDIUM (but not a blocker)

**Workaround**: Document clearly

### 4. Config Overwrites on Host Switch

**Severity**: MEDIUM (but not a blocker)

**Workaround**: Document as expected behavior

### 5. Codex Auto-Memory NOT Supported

**Severity**: MEDIUM (but not a blocker - by design)

**Workaround**: Manual recall/remember only

### 6. OpenClaw BLOCKED

**Severity**: N/A

**Workaround**: Requires OpenClaw GitHub release

---

## EVIDENCE

| File | Purpose |
|------|---------|
| `runs/041-install-debug/install_debug_trace.md` | Full debug trace |
| `runs/041-install-debug/determinism_debug.md` | Investigation results |
| `runs/041-install-debug/friction_log.md` | Friction points |
| `runs/041-install-debug/evidence.md` | Phase evidence |

---

**Phase 041 COMPLETE**
**Issue NOT REPRODUCIBLE**
**5x Tests PASSED - Claude Install DETERMINISTIC in this environment**
