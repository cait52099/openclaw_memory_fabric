#!/bin/bash
# test-auto-memory-setup.sh
# Quick verification that auto-memory setup is correct

set -e

PROJECT_ROOT="/Users/caihongwei/project/openclaw_memory_fabric"
SYSTEM_PROMPT_FILE="$PROJECT_ROOT/runs/019-native-auto-memory/auto_memory_system_prompt.md"
MCP_CONFIG="/tmp/ocmf_mcp.json"

echo "=== OCMF Auto-Memory Setup Verification ==="
echo

# Check 1: System prompt file exists
echo "1. Checking system prompt file..."
if [ -f "$SYSTEM_PROMPT_FILE" ]; then
    echo "   ✅ System prompt file exists: $SYSTEM_PROMPT_FILE"
else
    echo "   ❌ System prompt file not found: $SYSTEM_PROMPT_FILE"
    exit 1
fi

# Check 2: MCP config exists
echo "2. Checking MCP config..."
if [ -f "$MCP_CONFIG" ]; then
    echo "   ✅ MCP config exists: $MCP_CONFIG"
else
    echo "   ❌ MCP config not found: $MCP_CONFIG"
    echo "   Run: cat > $MCP_CONFIG << 'EOF'"
    echo '   {"mcpServers":{"ocmf":{"command":"python3","args":["-m","ocmaf.bridge.mcp_server","--tool","claude-code"],"env":{"PYTHONPATH":"/Users/caihongwei/project/openclaw_memory_fabric/src"}}}}'
    exit 1
fi

# Check 3: Claude available
echo "3. Checking Claude..."
if command -v claude &> /dev/null; then
    CLAUDE_VERSION=$(claude --version 2>&1 | head -1)
    echo "   ✅ Claude available: $CLAUDE_VERSION"
else
    echo "   ❌ Claude not found in PATH"
    exit 1
fi

# Check 4: System prompt flag available
echo "4. Checking system prompt flag..."
if claude --help 2>&1 | grep -q "system-prompt"; then
    echo "   ✅ --system-prompt flag available"
else
    echo "   ❌ --system-prompt flag not found"
    exit 1
fi

# Check 5: MCP config flag available
echo "5. Checking MCP config flag..."
if claude --help 2>&1 | grep -q "mcp-config"; then
    echo "   ✅ --mcp-config flag available"
else
    echo "   ❌ --mcp-config flag not found"
    exit 1
fi

# Check 6: System prompt content
echo "6. Checking system prompt content..."
if grep -q "ocmf_recall" "$SYSTEM_PROMPT_FILE" && \
   grep -q "ocmf_remember" "$SYSTEM_PROMPT_FILE"; then
    echo "   ✅ System prompt contains auto-memory rules"
else
    echo "   ❌ System prompt missing auto-memory rules"
    exit 1
fi

# Check 7: Database exists
echo "7. Checking database..."
if [ -f "/tmp/ocmf_bridge_test.db" ]; then
    echo "   ✅ Database exists: /tmp/ocmf_bridge_test.db"
else
    echo "   ⚠️  Database not found (will be created on first use)"
fi

echo
echo "=== All Checks Passed ==="
echo
echo "To start auto-memory session, run:"
echo "  claude --mcp-config $MCP_CONFIG --system-prompt \"\$(cat $SYSTEM_PROMPT_FILE)\""
echo
echo "Or use the provided script:"
echo "  $PROJECT_ROOT/runs/019-native-auto-memory/auto-memory-start.sh"
