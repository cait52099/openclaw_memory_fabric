# Claude Settings-Based Hooks - Working Configuration

**Run ID**: 020-claude-hook-explore
**Date**: 2026-03-20

---

## Working Auto-Memory Configuration

### Step 1: Create Auto-Memory Script

```bash
cat > /tmp/auto_memory.sh << 'EOF'
#!/bin/bash
export PYTHONPATH="/Users/caihongwei/project/openclaw_memory_fabric/src"

echo "=== Auto-memory hook triggered ===" >> /tmp/claude_hooks.log
date >> /tmp/claude_hooks.log

# Call ocmf_recall
echo "--- Calling ocmf_recall ---" >> /tmp/claude_hooks.log
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ocmf_recall","arguments":{"query":"OCMF test"}}}' | \
  python3 -m ocmaf.bridge.mcp_server --tool claude-code >> /tmp/claude_hooks.log 2>&1

# Call ocmf_remember
echo "--- Calling ocmf_remember ---" >> /tmp/claude_hooks.log
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"ocmf_remember","arguments":{"content":"Auto-remembered from SessionStart hook at $(date)"}}}' | \
  python3 -m ocmaf.bridge.mcp_server --tool claude-code >> /tmp/claude_hooks.log 2>&1

echo "=== Hook complete ===" >> /tmp/claude_hooks.log
EOF

chmod +x /tmp/auto_memory.sh
```

### Step 2: Add Hooks to Settings

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/tmp/auto_memory.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Step 3: Test

```bash
claude -p "hello"
```

---

## What Works

- ✅ SessionStart hook fires
- ✅ ocmf_recall is called
- ✅ ocmf_remember is called
- ✅ Event stored in SQLite

---

## Limitation

⚠️ Hook runs as side process - Claude doesn't automatically use recalled memories in context.
