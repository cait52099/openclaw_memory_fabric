# OCMF Unified Host Matrix - Known Limits

**Run ID**: 023-unified-host-matrix
**Date**: 2026-03-22
**Status**: FINAL

---

## FINAL STATUS: HOST MATRIX CLOSED

---

## CLAUDE KNOWN LIMITS

### Method A2 (Context Injection) = Not Supported

| Check | Result | Reason |
|-------|--------|--------|
| Hook outputs in context | ❌ | Hooks run as side processes |
| Seamless auto-recall | ❌ | Results don't affect response |

**Impact**: Claude cannot do "zero-friction auto-memory" where hook outputs are automatically injected. Users must use Method B (system-prompt) for recall to work.

**Workaround**: Method A1 + B combination provides equivalent functionality.

### Native Hooks Dependency

| Check | Result | Notes |
|-------|--------|-------|
| Hooks require config | ✅ | Must configure `~/.claude/settings.json` |
| Hooks require shell | ✅ | Calls `/tmp/auto_memory.sh` |
| PYTHONPATH required | ✅ | MCP server needs OCMF in path |

---

## CODEX KNOWN LIMITS

### No Native Hooks

| Check | Result | Notes |
|-------|--------|-------|
| Hooks subsystem | ❌ NOT FOUND | No `codex hooks` command |
| SessionStart/End | ❌ NOT FOUND | No session lifecycle hooks |
| Auto-trigger | ❌ NOT AVAILABLE | Must use manual MCP calls |

**Impact**: Codex cannot do automatic background memory collection. Users must explicitly call `ocmf_remember` and `ocmf_recall`.

### Method B Untested

| Check | Result | Notes |
|-------|--------|-------|
| System-prompt for memory | ⚠️ UNTESTED | Not explored in run 022 |

**Potential**: If Codex supports system-prompt injection, it could gain semi-automatic behavior.

### PATH Issue

| Check | Result | Notes |
|-------|--------|-------|
| `codex` in PATH | ❌ NO | Must use full path |
| Wrapper needed | ✅ | `~/bin/ocmaf-codex` for PYTHONPATH |

---

## OPENCLAW KNOWN LIMITS

### Environment Blocked (Run 024)

| Check | Result | Notes |
|-------|--------|-------|
| GitHub release | ❌ 404 | v2026.3.13-1 assets missing |
| Download URL | ❌ BROKEN | OpenClaw-2026.3.13.dmg not found |
| Real host proof | ❌ BLOCKED | Cannot install |
| MCP verified | ⚠️ UNKNOWN | Cannot test without install |
| Native hooks | ⚠️ UNKNOWN | Cannot test without install |
| Production path | **TBD** | Cannot determine |

**Impact**: Third host remains unverified. OpenClaw line closure blocked.

**Resolution**: OpenClaw team must fix GitHub release assets.

---

## CROSS-HOST KNOWN LIMITS

### Cross-Host Memory Sharing

| Check | Result | Notes |
|-------|--------|-------|
| Same SQLite | ✅ | All hosts write to same DB |
| Cross-host recall | ✅ | Works technically |
| Conflict resolution | ✅ SPECIFIED | FR-050~052 in spec.md |
| Cross-host UX | ✅ COMPLETE | Run 024 spec delivered |

**Status**: Cross-host UX spec is now COMPLETE (Run 024). Implementation remains.

### Synthetic vs Real Host Gap

| Check | Result | Notes |
|-------|--------|-------|
| Run 021 direct MCP | ❌ | Not real host (piping to python) |
| Run 022 real host | ✅ | `codex exec` = genuine host call |

**Lesson**: Direct MCP invocation ≠ real host proof. Must use actual host CLI.

---

## PRODUCTION GAPS

### P0 (Must Address)

| Gap | Impact | Notes |
|-----|--------|-------|
| OpenClaw unverified | Cannot claim "3-host support" | Env resolution needed (GitHub 404) |
| Codex Method B untested | Unknown if Codex can do semi-auto | Potential improvement |

### P1 (Should Address)

| Gap | Impact | Notes |
|-----|--------|-------|
| ~~Cross-host UX~~ | ✅ COMPLETE | **SPEC delivered (Run 024)** - implementation pending |
| Replay/eval | Cannot validate scoring | Framework needed |

### P2 (Nice to Have)

| Gap | Impact | Notes |
|-----|--------|-------|
| Vector search | Performance at scale | Not MVP priority |
| Web UI | UX improvement | Not core requirement | |

---

## SUMMARY TABLE

| Host | A1 | A2 | B | C | Production | Notes |
|------|----|----|---|-----|------------|-------|
| Claude | ✅ | ❌ | ✅ | ✅ | A1+B | A2 = side process (not supported) |
| Codex | ❌ | ❌ | ⚠️ | ✅ | C | A = not available; B = untested |
| OpenClaw | ❌ | ❌ | ❌ | ❌ | **BLOCKED** | Download URL 404 (Run 024) |

---

**These limits are FINAL and binding. OpenClaw BLOCKED until GitHub release fixed. Cross-host UX spec COMPLETE (Run 024).**
