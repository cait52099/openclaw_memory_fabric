# OCMF Known Limits - Claude Real Host Session

**Run ID**: 014-claude-session-validation
**Date**: 2026-03-12

---

## Summary

This run documents the current status of Claude Real Host Session Bridge validation.

---

## What Has Been Verified

### Binary Environment

- Claude binary: ✅ /Users/caihongwei/.local/bin/claude
- Claude version: ✅ 2.1.72
- MCP config: ✅ Created and verified

### MCP Integration

- Claude --mcp-config flag: ✅ Works
- MCP server can be configured: ✅ Yes

---

## What Needs Human Interaction

The following requires user to run Claude in interactive mode:

```
claude --mcp-config /tmp/ocmf_mcp.json
```

Then in the session:
- `/remember <content>`
- `/recall <query>`

---

## Validation Type Distinction

| Type | Example | Current Status |
|------|---------|---------------|
| Real Host Bridge | Interactive session with MCP config | ⏳ Needs human |
| Direct MCP Invocation | `echo '...' \| python3 -m ocmaf.bridge.mcp_server` | ✅ Works |
| Synthetic Test | `pytest tests/` | ✅ 45/45 PASS |

---

## Known Limitations

1. **Claude Non-Interactive Mode**: Claude `-p` mode does not expose MCP tools in output
2. **Human Interaction Required**: Real host validation requires interactive session

---

## Codex Status

- Codex binary: ✅ Available at /Applications/Codex.app/.../codex
- Codex MCP add: ✅ Works
- Codex handshake: ⚠️ Known issue from previous runs
- **This run**: NOT TESTED (focused on Claude only)

---

## OpenClaw Status

- OpenClaw binary: ❌ Not found
- Status: ❌ BLOCKED

---

## Next Steps

After human interaction completes:
1. Update claude_strict_real_host.md with real outputs
2. Run SQLite query to verify event_id
3. Update evidence.md with results
4. Determine FINAL_STATUS

---

**Last Updated**: 2026-03-12
