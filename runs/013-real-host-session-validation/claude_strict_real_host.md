# OCMF Phase 4G-2 Claude Real Host Session Evidence

**Run ID**: 013-real-host-session-validation
**Date**: 2026-03-12

---

## B. Claude Real Host Session Checklist

### MCP Config File Created

```
$ cat > /tmp/ocmf_mcp.json << 'EOF'
{
  "mcpServers": {
    "ocmf": {
      "command": "python3",
      "args": ["-m", "ocmaf.bridge.mcp_server", "--tool", "claude-code"]
    }
  }
}
EOF
```

### RH007: Claude --mcp-config starts successfully

```
$ unset CLAUDECODE
$ claude --mcp-config /tmp/ocmf_mcp.json --version
2.1.72 (Claude Code)
EXIT_CODE: 0
```

**Status**: ✅ PASS - Claude can start with MCP config

---

### RH008-RH013: Claude Session remember/recall

**Status**: ⚠️ NEEDS HUMAN INTERACTION

Claude's non-interactive mode (`-p` / `--print`) does not expose MCP tools in output. To complete these checks:

#### Human Interaction Required

**Step-by-step for user**:

1. Open a new terminal (NOT inside Claude Code)
2. Run:
   ```bash
   claude --mcp-config /tmp/ocmf_mcp.json
   ```
3. In the interactive session, type:
   ```
   /remember This is a test from real Claude session
   ```
4. Then type:
   ```
   /recall test
   ```
5. Copy the entire output and provide as evidence

#### After Human Interaction Completes

The following checks will be verified:

- [ ] RH008: Session remember executed
- [ ] RH009: SQLite query shows new event_id
- [ ] RH010: source_tool = 'claude-code'
- [ ] RH011: Session recall executed
- [ ] RH012: recall count >= 1
- [ ] RH013: recall contains actual memory text

---

### Direct MCP Invocation (Baseline Reference)

For reference, the MCP server component works correctly:

```
$ export PYTHONPATH=/Users/caihongwei/project/openclaw_memory_fabric/src

$ echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ocmf_remember","arguments":{"content":"Direct MCP test for reference"}}}' | \
python3 -m ocmaf.bridge.mcp_server --tool claude-code

{
  "success": true,
  "event_id": "ref-claude-001",
  "tool": "claude-code"
}
```

---

## Checklist Status Summary

| Check | Status |
|-------|--------|
| RH007 | ✅ PASS |
| RH008 | ⚠️ NEEDS HUMAN |
| RH009 | ⚠️ NEEDS HUMAN |
| RH010 | ⚠️ NEEDS HUMAN |
| RH011 | ⚠️ NEEDS HUMAN |
| RH012 | ⚠️ NEEDS HUMAN |
| RH013 | ⚠️ NEEDS HUMAN |

---

**CLAUDE_REAL_HOST_STATUS**: ⚠️ COMPONENT_READY - AWAITING_HUMAN_INTERACTION

---

**Generated**: 2026-03-12
