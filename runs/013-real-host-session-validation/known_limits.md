# OCMF Phase 4G-2 Known Limits - Real Host Session Bridge

**Run ID**: 013-real-host-session-validation
**Date**: 2026-03-12

---

## Summary

This run documents the current status of Real Host Session Bridge validation after attempting to complete the checklist items.

---

## Three-Way Validation Type Distinction

| Type | Definition | Status |
|------|------------|--------|
| Real Host Bridge | Through real tool interactive session + MCP config | ⚠️ Needs Human |
| Direct MCP Invocation | Direct execution of MCP server via stdio | ✅ Verified |
| Synthetic Test | pytest automated execution | ✅ 45/45 PASS |

---

## Current Status by Category

### Binary / Environment

| Check | Status |
|-------|--------|
| Claude binary | ✅ Available |
| Claude MCP config | ✅ Works |
| Codex binary | ✅ Available |
| Codex MCP add | ✅ Works |
| OpenClaw | ❌ BLOCKED |

### Claude Session

| Check | Status | Note |
|-------|--------|------|
| --mcp-config starts | ✅ | Verified |
| Session remember | ⚠️ | Needs human |
| SQLite event | ⚠️ | Needs human |
| Session recall | ⚠️ | Needs human |

**Limitation**: Claude `-p` (non-interactive) mode doesn't expose MCP tools.

### Codex Session

| Check | Status | Note |
|-------|--------|------|
| mcp add | ✅ | Verified |
| Session remember | ⚠️ | MCP handshake fails |
| SQLite event | ⚠️ | Needs human |
| Session recall | ⚠️ | MCP handshake fails |

**Limitation**: Codex MCP client fails to handshake with OCMF server.

### Cross-tool

| Check | Status |
|-------|--------|
| Isolation (direct MCP) | ✅ Verified |

---

## What is NOT Real Host Bridge

### Direct MCP Invocation

```bash
# This is DIRECT MCP invocation, NOT Real Host Bridge
echo '{"method":"tools/call",...}' | python3 -m ocmaf.bridge.mcp_server --tool claude-code
```

This is component verification, not session-level validation.

### Synthetic Test

```bash
# This is SYNTHETIC test, NOT Real Host Bridge
pytest tests/
```

---

## Human Interaction Required

### For Claude Session Validation

1. Open a new terminal (NOT inside Claude Code)
2. Run: `claude --mcp-config /tmp/ocmf_mcp.json`
3. In session, type: `/remember This is a test from real Claude session`
4. In session, type: `/recall test`
5. Copy output as evidence

### For Codex Session Validation

The MCP handshake issue must be resolved first. Options:
1. Fix MCP server implementation to be compatible with Codex
2. Use alternative integration method

---

## Evidence Files

| File | Status |
|------|--------|
| binary_check.md | ✅ Complete |
| claude_strict_real_host.md | ⚠️ Partial |
| codex_strict_real_host.md | ⚠️ Partial |
| cross_tool_strict.md | ⚠️ Via direct MCP |
| evidence.md | ✅ Complete |
| known_limits.md | ✅ Complete |

---

## Conclusions

**REAL_HOST_STATUS**: ⚠️ PARTIAL

- Claude: ⚠️ Component ready, needs human interaction
- Codex: ⚠️ MCP handshake issue
- OpenClaw: ❌ BLOCKED
- Cross-tool: ✅ Isolation verified (component level)
- Synthetic: ✅ 45/45

**Next Steps**:
1. Complete Claude human interaction
2. Resolve Codex MCP handshake issue
3. Re-validate with full session evidence

---

**Last Updated**: 2026-03-12
