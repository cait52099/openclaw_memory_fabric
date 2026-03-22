# Native Auto-Memory Manual Test Guide

**Run ID**: 019-native-auto-memory
**Date**: 2026-03-19

---

## How to Test Auto-Memory in Interactive Session

### Step 1: Create Startup Script

```bash
#!/bin/bash
# auto-memory-start.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/Users/caihongwei/project/openclaw_memory_fabric"
SYSTEM_PROMPT_FILE="$PROJECT_ROOT/runs/019-native-auto-memory/auto_memory_system_prompt.md"
MCP_CONFIG="/tmp/ocmf_mcp.json"

# Verify files exist
if [ ! -f "$SYSTEM_PROMPT_FILE" ]; then
    echo "Error: System prompt file not found: $SYSTEM_PROMPT_FILE"
    exit 1
fi

if [ ! -f "$MCP_CONFIG" ]; then
    echo "Error: MCP config not found: $MCP_CONFIG"
    exit 1
fi

# Start Claude with auto-memory system prompt
claude --mcp-config "$MCP_CONFIG" \
       --system-prompt "$(cat "$SYSTEM_PROMPT_FILE")"
```

### Step 2: Run the Script

```bash
chmod +x auto-memory-start.sh
./auto-memory-start.sh
```

### Step 3: Verify in Session

Once in the interactive session:

1. **Check MCP tools**:
   ```
   /mcp
   ```
   Expected output should show:
   - Ocmf MCP Server
   - Status: connected
   - Tools: ocmf_recall, ocmf_remember, ocmf_get_injection

2. **Test auto-recall**:
   Start the conversation by asking about a project you've worked on before. The system prompt instructs Claude to automatically call `ocmf_recall` at the start.

3. **Test auto-remember**:
   Mention important information like:
   - "Remember that I prefer Python 3.11+"
   - "The project uses pytest for testing"
   - "Important constraint: always use type hints"
   The system prompt instructs Claude to automatically call `ocmf_remember`.

4. **Verify in SQLite**:
   ```bash
   sqlite3 /tmp/ocmf_bridge_test.db "SELECT event_id, payload_json FROM events ORDER BY timestamp DESC LIMIT 5;"
   ```

---

## Expected Behavior

### At Session Start
Claude should automatically call `ocmf_recall` with a query based on the project context.

### During Conversation
When you mention:
- Important constraints or requirements
- Solutions to problems
- Preferences or patterns
- Key decisions

Claude should automatically call `ocmf_remember` to store this information.

### At Session End
Before you say goodbye, Claude should summarize key decisions and call `ocmf_remember` to store the summary.

---

## Troubleshooting

### MCP Tools Not Visible

1. Check MCP config: `cat /tmp/ocmf_mcp.json`
2. Verify Python path: The config includes PYTHONPATH
3. Test MCP server: `PYTHONPATH=/Users/caihongwei/project/openclaw_memory_fabric/src python3 -m ocmaf.bridge.mcp_server --tool claude-code`

### Auto-Memory Not Triggering

1. Verify system prompt is loaded: The startup should show the system prompt
2. Check session is interactive: Auto-memory requires interactive mode
3. Manually test: Ask Claude "What memories do you have about this project?"

---

**Generated**: 2026-03-19
