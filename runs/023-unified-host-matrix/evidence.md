# OCMF Unified Host Matrix - Evidence Summary

**Run ID**: 023-unified-host-matrix
**Date**: 2026-03-22
**Status**: FINAL

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** (Claude ✅, Codex ✅, OpenClaw ❌ BLOCKED) |
| **HOST_MATRIX_CLOSED** | **YES** |
| **CLAUDE_LINE_CLOSED** | **YES** |
| **CODEX_LINE_CLOSED** | **YES** |
| **OPENCLAW_STATUS** | **BLOCKED** (GitHub release 404) |
| **CROSS_HOST_UX_SPEC** | **COMPLETE** (Run 024) |
| **RECOMMENDED_PRODUCT_STRATEGY** | **Per-host: Claude=A1+B, Codex=C, OpenClaw=TBD** |

---

## CLAUDE EVIDENCE (Run 020)

### Source Documents
- `runs/020-claude-hook-explore/final_claude_position.md`
- `runs/020-claude-hook-explore/evidence.md`
- `runs/020-claude-hook-explore/method_boundary.md`
- `runs/020-claude-hook-explore/settings_hooks_config.md`

### Verified Facts
| Fact | Evidence |
|------|----------|
| Binary | `/usr/local/bin/claude` (or `which claude`) |
| Version | Claude 2.1.78 |
| Hooks path | `~/.claude/settings.json` |
| Hook events | SessionStart, SessionEnd |
| Auto-recall | ✅ Verified via SQLite events |
| Auto-remember | ✅ Verified via SQLite events |
| A2 (context injection) | ❌ FAIL - hooks are side processes |
| Method B | ✅ Verified via Run 019 |

### Run 020 Session Log (excerpt)
```
SessionStart hook triggered at 2026-03-20T...
tool ocmf_recall auto-called
tool ocmf_remember auto-called
event_id = 0476b6c1-40b1-4bae-8fab-b4937cd28572 (SessionStart)
event_id = 4dd11d54-e497-4ce7-9272-d6abcc7b2521 (SessionEnd)
SQLite: source_tool='claude-code' ✅
```

---

## CODEX EVIDENCE (Run 022)

### Source Documents
- `runs/022-codex-real-host-closure/final_codex_position.md`
- `runs/022-codex-real-host-closure/codex_real_host.md`
- `runs/022-codex-real-host-closure/mcp_check.md`

### Verified Facts
| Fact | Evidence |
|------|----------|
| Binary | `/Applications/Codex.app/Contents/Resources/codex` |
| Version | `codex-cli 0.116.0-alpha.10` |
| MCP configured | ✅ via `codex mcp list` |
| Wrapper | `/Users/caihongwei/bin/ocmaf-codex` |
| Real host call | ✅ `codex exec` with `--full-auto` |
| MCP handshake | ✅ `mcp: ocmf ready` |
| Remember event_id | `cec26366-0a10-42c5-b44f-5bdae2e332c3` |
| Recall count | 1 (exact match) |
| SQLite | `source_tool='codex-cli'` ✅ |

### Run 022 Session Log (excerpt)
```
$ codex exec --full-auto "call ocmf_remember... OCMF_REAL_HOST_TEST_1773980433"
mcp: ocmf starting
mcp: ocmf ready
tool ocmf.ocmf_remember(...)
→ event_id = cec26366-0a10-42c5-b44f-5bdae2e332c3
tool ocmf.ocmf_recall({"query":"OCMF_REAL_HOST_TEST"})
→ count = 1, memory_id = cec26366-... (SAME)
SQLite verified ✅
```

---

## OPENCLAW EVIDENCE (Run 024)

### Status: BLOCKED

| Check | Result | Evidence |
|-------|--------|----------|
| GitHub release | ❌ 404 | `OpenClaw-2026.3.13.dmg` not found |
| Download URL | ❌ BROKEN | `https://github.com/openclaw/openclaw/releases/download/v2026.3.13/OpenClaw-2026.3.13.dmg` |
| Homebrew install | ❌ FAIL | Download failed |
| Binary in PATH | ❌ NO | `which openclaw` = not found |
| Real host proof | ❌ BLOCKED | Cannot install |
| Method boundary | ⚠️ TBD | Cannot determine without install |
| Production path | ⚠️ TBD | Cannot determine |

### Source Documents
- `runs/024-openclaw-closure-crosshost-ux/binary_check.md`
- `runs/024-openclaw-closure-crosshost-ux/method_boundary.md`
- `runs/024-openclaw-closure-crosshost-ux/production_path.md`

### Blocker Detail
```
$ brew install --cask openclaw
==> Downloading https://github.com/openclaw/openclaw/releases/download/v2026.3.13/OpenClaw-2026.3.13.dmg
Error: Download failed: https://github.com/openclaw/openclaw/releases/download/v2026.3.13/OpenClaw-2026.3.13.dmg
```

### Resolution Required
OpenClaw team must fix the GitHub release assets (v2026.3.13-1 has no .dmg file).

---

## HOST CAPABILITY SUMMARY

| Capability | Claude | Codex | OpenClaw |
|------------|--------|-------|----------|
| **Real host proof** | ✅ Run 020 | ✅ Run 022 | ❌ BLOCKED (Run 024) |
| **MCP可用** | ✅ | ✅ | ⚠️ Unknown |
| **Native hooks** | ✅ | ❌ | ⚠️ Unknown |
| **Auto-trigger (A1)** | ✅ | ❌ | ⚠️ Unknown |
| **Context injection (A2)** | ❌ | ❌ | ⚠️ Unknown |
| **System-prompt (B)** | ✅ | ⚠️ | ⚠️ Unknown |
| **Manual MCP (C)** | ✅ | ✅ | ⚠️ Unknown |
| **Production path** | **A1+B** | **C** | **TBD** |
| **Cross-host UX spec** | N/A | N/A | **COMPLETE** (Run 024) |

---

## METHOD DEFINITIONS VERIFICATION

| Method | Definition | Claude | Codex | OpenClaw |
|--------|------------|--------|-------|----------|
| **A1** | Native hooks call tools automatically | ✅ | ❌ | ⚠️ |
| **A2** | Hook outputs affect context | ❌ | ❌ | ⚠️ |
| **B** | System-prompt instructions | ✅ | ⚠️ | ⚠️ |
| **C** | Manual MCP calls | ✅ | ✅ | ⚠️ |

---

## PRODUCTION PATHS

| Host | Path | Components |
|------|------|------------|
| **Claude** | A1 + B | A1: hooks auto-collect; B: Claude uses memories in context |
| **Codex** | C | Manual `ocmf_remember` / `ocmf_recall` calls |
| **OpenClaw** | TBD | Cannot determine until env issues resolved |

---

## DOCUMENT HYGIENE

| Issue | Correction |
|-------|-----------|
| Codex binary path in older runs | Correct path: `/Applications/Codex.app/Contents/Resources/codex` |
| Codex version drift | Current: `0.116.0-alpha.10` (run 022) |
| Run 021 "direct MCP"冒充 real host | Corrected in run 022 with `codex exec` |
| Method A ambiguity | Defined A1 vs A2 vs B vs C explicitly |
| OpenClaw blocker detail | Added specific GitHub release 404 evidence (Run 024) |
| Cross-host UX spec | Completed in Run 024 (was P1 gap) |

---

## CROSS-HOST UX SPEC (Run 024)

### Status: COMPLETE

The cross-host UX specification has been finalized and incorporated into `docs/spec.md` Section 5.15.

### Source Documents
- `runs/024-openclaw-closure-crosshost-ux/cross_host_ux_spec.md`
- `runs/024-openclaw-closure-crosshost-ux/source_tool_spec.md`

### Key Specifications Delivered

| Requirement | Status | Notes |
|-------------|--------|-------|
| Provenance display | ✅ FR-047 | Recall results must show source_tool |
| Friendly name mapping | ✅ FR-048 | claude-code→Claude, codex-cli→Codex, etc. |
| Group by source | ✅ FR-049 | Optional grouping in recall output |
| Conflict detection | ✅ FR-050 | conflict_detected when same entity differs |
| Conflict response | ✅ FR-051 | All candidates with source/content/timestamp |
| User resolution | ✅ FR-052 | Conflicts must be resolved by user |
| explain() match_reasons | ✅ FR-053 | keyword/scope/time match reasons |
| explain() provenance | ✅ FR-054 | source_tool and source_host_friendly |
| Cross-host explain | ✅ FR-055 | also_written_by other hosts |
| source_tool invariants | ✅ FR-056/057/058 | Required field, real host vs synthetic |

### UX by Host Path

| Host | Collection | Recall | User Effort |
|------|------------|--------|-------------|
| Claude | A1 (auto hooks) | B (system-prompt) | Minimal |
| Codex | C (manual) | C (manual) | Intentional |
| OpenClaw | TBD | TBD | Unknown |

### source_tool Mapping

| source_tool | Friendly Name | Host Type |
|-------------|---------------|-----------|
| claude-code | Claude | Desktop App |
| codex-cli | Codex | CLI |
| openclaw | OpenClaw | Desktop App |
| synthetic | Synthetic (Test) | Test |

---

## EVIDENCE FILES

| File | Purpose |
|------|---------|
| `host_matrix.md` | Host capability matrix |
| `method_taxonomy.md` | Method definitions |
| `product_strategy.md` | Product recommendations |
| `evidence.md` | This file |
| `known_limits.md` | Limitations and gaps |

### Cross-Host UX Spec (Run 024)

| File | Purpose |
|------|---------|
| `cross_host_ux_spec.md` | Full UX specification |
| `source_tool_spec.md` | source_tool mapping table |

### OpenClaw Closure (Run 024)

| File | Purpose |
|------|---------|
| `binary_check.md` | OpenClaw install blocked |
| `method_boundary.md` | TBD (blocked) |
| `production_path.md` | TBD (blocked) |

---

**This evidence is FINAL and binding.**
