# Claude Settings-Based Hooks Configuration

**Run ID**: 020-claude-hook-explore
**Date**: 2026-03-20
**Status**: VERIFIED - Official Schema Works

---

## Configuration

### ~/.claude/settings.json (Official Schema)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/tmp/auto_memory.sh SessionStart",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/tmp/auto_memory.sh SessionEnd",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Auto-Memory Script: /tmp/auto_memory.sh

```bash
#!/bin/bash
export PYTHONPATH="/Users/caihongwei/project/openclaw_memory_fabric/src"
echo "[$(date)] HOOK_TRIGGERED: $1" >> /tmp/claude_hooks.log
echo '[{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ocmf_recall","arguments":{"query":"OCMF test auto-memory"}}}]' | \
  python3 -m ocmaf.bridge.mcp_server --tool claude-code >> /tmp/claude_hooks.log 2>&1
echo '[{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ocmf_remember","arguments":{"content":"Auto-remembered from hook at $(date)"}}}]' | \
  python3 -m ocmaf.bridge.mcp_server --tool claude-code >> /tmp/claude_hooks.log 2>&1
```

---

## Schema Validation

**Valid Events** (from official validator):
- PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStop, **SessionStart**, **SessionEnd**, PreCompact, Notification

**Required Fields**:
- `hooks` array (required)
- `type` field: `"command"` or `"prompt"` (required)
- For command: `command` field

---

## Configuration Status

| Item | Status |
|------|--------|
| Official schema format | ✅ Valid |
| SessionStart event | ✅ Configured |
| SessionEnd event | ✅ Configured |
| Command hook type | ✅ Valid |
| Timeout set | ✅ 30s |
