#!/bin/bash
# Codex Setup Script for OCMF
# Method: C (Manual MCP)
# Auto-Memory: NOT Supported (manual recall/remember only)
#
# This configures Codex to use OCMF via MCP. Codex can then
# call 'ocmaf recall' and 'ocmaf remember' as MCP commands.

set -e

echo "=================================================="
echo "OCMF Codex Setup"
echo "Method: Manual MCP (C)"
echo "=================================================="

# Detect OCMF path (where this script is located)
OCMF_SETUP_DIR="$(cd "$(dirname "$0")" && pwd)"
OCMF_PATH="$(cd "$OCMF_SETUP_DIR/../.." && pwd)"

# Check if codex is available
if ! command -v codex &> /dev/null; then
    echo ""
    echo "⚠️  WARNING: 'codex' command not found"
    echo "   Codex CLI may not be installed."
    echo "   You can still configure OCMF and use it manually."
    echo ""
fi

# Check Codex MCP support
echo ""
echo "--- Step 1: Check Codex MCP Support ---"
if command -v codex &> /dev/null && codex --help 2>/dev/null | grep -i mcp > /dev/null; then
    echo "✓ Codex MCP support detected"
else
    echo "⚠️  Codex MCP support not confirmed"
    echo "   Will still create MCP config for manual setup."
fi

# Create OCMF config directory
OCMF_CONFIG_DIR="${HOME}/.ocmf"
OCMF_CONFIG="${OCMF_CONFIG_DIR}/config.sh"
mkdir -p "$OCMF_CONFIG_DIR"

echo ""
echo "--- Step 2: Create OCMF Config ---"
cat > "$OCMF_CONFIG" << 'HEREDOC_END'
# OCMF Configuration for Codex
# Source this file in your Codex environment: source ~/.ocmf/config.sh

# Auto-memory mode: 0=off (Codex: auto-memory NOT supported via Method C)
export OCMF_AUTO_MEMORY=0

# Default scope
export OCMF_SCOPE_USER="${USER}"
export OCMF_SCOPE_PROJECT="${PWD##*/}"

# Source tool identification - CODEX IDENTITY
export OCMF_SOURCE_TOOL="codex-cli"
export OCMF_HOST_METHOD="C"

# Memory store path
export OCMF_DB_PATH="${HOME}/.ocmf/memory.db"

# OCMF Python path (for imports)
export PYTHONPATH="${OCMF_PATH}/src:${PYTHONPATH}"

# OCMF installation path
export OCMF_PATH="${OCMF_PATH}"
HEREDOC_END
echo "✓ Created $OCMF_CONFIG"

# DEFENSIVE: Verify the config was written correctly
ACTUAL_TOOL="$(grep 'OCMF_SOURCE_TOOL=' "$OCMF_CONFIG" | head -1 | cut -d'"' -f2 2>/dev/null || echo 'UNKNOWN')"
if [ "$ACTUAL_TOOL" != "codex-cli" ]; then
    echo "✗ ERROR: Config verification failed!"
    echo "  Expected OCMF_SOURCE_TOOL=codex-cli"
    echo "  Got OCMF_SOURCE_TOOL=$ACTUAL_TOOL"
    echo "  This indicates a setup issue."
    exit 1
fi
echo "  ✓ Verified OCMF_SOURCE_TOOL=codex-cli"

echo ""
echo "--- Step 3: Create Codex MCP Configuration ---"
CODEX_MCP_DIR="${HOME}/.codex"
CODEX_MCP_CONFIG="${CODEX_MCP_DIR}/mcp.json"
mkdir -p "$CODEX_MCP_DIR"

echo "  Creating MCP config at $CODEX_MCP_CONFIG..."

# The MCP server entry point - using the full path with PYTHONPATH set
cat > "$CODEX_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "ocmf": {
      "command": "bash",
      "args": ["-c", "cd ${OCMF_PATH} && PYTHONPATH=${OCMF_PATH}/src python3 -m ocmaf.bridge.mcp_server --tool codex-cli"],
      "cwd": "${OCMF_PATH}"
    }
  }
}
EOF
echo "✓ Created $CODEX_MCP_CONFIG"

echo ""
echo "--- Step 4: Create Manual Recall/Remember Commands ---"
# Create helper script for manual recall/remember
CODEX_HELPERS="${OCMF_CONFIG_DIR}/codex_helpers.sh"
cat > "$CODEX_HELPERS" << EOF
# OCMF Codex Helper Commands
# Add these to your Codex startup or call manually
# Usage: source ~/.ocmf/codex_helpers.sh

# Remember a decision or fact
ocmf-remember() {
    local content="\$*"
    if [ -z "\$content" ]; then
        echo "Usage: ocmf-remember <content>"
        return 1
    fi
    PYTHONPATH=${OCMF_PATH}/src ocmaf remember --content "\$content"
}

# Recall relevant memories
ocmf-recall() {
    local query="\$*"
    if [ -z "\$query" ]; then
        echo "Usage: ocmf-recall <query>"
        return 1
    fi
    PYTHONPATH=${OCMF_PATH}/src ocmaf recall --query "\$query"
}

# Show memory status
ocmf-status() {
    PYTHONPATH=${OCMF_PATH}/src ocmaf unified status
}

# OCMF path
export OCMF_PATH="${OCMF_PATH}"
EOF
echo "✓ Created $CODEX_HELPERS"
echo ""
echo "  To use OCMF in Codex:"
echo "    1. Restart Codex to load MCP server"
echo "    2. Codex can now call 'ocmaf recall' and 'ocmaf remember'"
echo "  Or use CLI mode:"
echo "    source ~/.ocmf/codex_helpers.sh"
echo "    ocmf-recall \"my query\""
echo "    ocmf-remember \"my decision\""

echo ""
echo "--- Step 5: Integration Verification ---"

# Verify OCMF is importable with PYTHONPATH
PYTHONPATH="${OCMF_PATH}/src" python3 -c "from ocmaf.cli.unified import unified; print('✓ OCMF CLI importable')" 2>/dev/null || {
    echo "✗ OCMF CLI not importable"
    echo "  Run: pip install -e $OCMF_PATH"
    exit 1
}

# Verify host detection
PYTHONPATH="${OCMF_PATH}/src" python3 -c "
from ocmaf.cli.host_detection import get_host_info
info = get_host_info()
print(f'  Detected host: {info[\"detected_host\"]}')
print(f'  Method: {info[\"recommended_method\"]}')
print(f'  Auto-memory: {info[\"auto_memory_supported\"]}')
print(f'  Note: Codex requires CODEX_API_KEY env var to be detected')
" || echo "  ⚠️  Host detection verification skipped"

echo ""
echo "=================================================="
echo "✓ Codex Setup Complete"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Source the config: source ~/.ocmf/config.sh"
echo "  2. Restart Codex to load MCP server"
echo "  3. Run 'source ~/.ocmf/codex_helpers.sh && ocmf-status' to verify"
echo ""
echo "Method C (Manual MCP):"
echo "  - Codex uses OCMF via MCP commands"
echo "  - Auto-memory NOT supported (manual recall/remember only)"
echo "  - Run 'ocmaf recall' or 'ocmf-recall' manually"
