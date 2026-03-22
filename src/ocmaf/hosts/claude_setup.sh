#!/bin/bash
# Claude Setup Script for OCMF
# Method: A1 (Native Hooks) + B (System-Prompt)
# Auto-Memory: Supported via CLI commands
#
# IMPORTANT: This configures OCMF environment. For Claude to actually
# use OCMF for auto-recall, you need to either:
# 1. Use MCP commands: ocmaf recall/remember
# 2. Configure Claude's system prompt manually to include recall results
#
# This script sets up the FOUNDATION for A1+B but full auto-recall
# requires additional Claude-side configuration.

set -e

echo "=================================================="
echo "OCMF Claude Setup"
echo "Method: A1 (Native Hooks) + B (System-Prompt)"
echo "=================================================="

# Detect OCMF path (where this script is located)
OCMF_SETUP_DIR="$(cd "$(dirname "$0")" && pwd)"
OCMF_PATH="$(cd "$OCMF_SETUP_DIR/../.." && pwd)"

# Check if already configured
MCP_CONFIG_DIR="${HOME}/.claude"
MCP_CONFIG="${MCP_CONFIG_DIR}/mcp_servers.json"
OCMF_CONFIG_DIR="${HOME}/.ocmf"
OCMF_CONFIG="${OCMF_CONFIG_DIR}/config.sh"

echo ""
echo "--- Step 1: Create OCMF Config Directory ---"
mkdir -p "$OCMF_CONFIG_DIR"
echo "✓ Created $OCMF_CONFIG_DIR"

echo ""
echo "--- Step 2: Create OCMF Config (A1+B Foundation) ---"
cat > "$OCMF_CONFIG" << 'HEREDOC_END'
# OCMF Configuration for Claude
# Source this file in your Claude environment: source ~/.ocmf/config.sh

# Auto-memory mode: 0=off, 1=on
# Note: Full auto-recall requires Claude-side system-prompt configuration
export OCMF_AUTO_MEMORY=1

# Default scope (can be overridden per project)
export OCMF_SCOPE_USER="${USER}"
export OCMF_SCOPE_PROJECT="${PWD##*/}"

# Source tool identification - CLAUDE IDENTITY
export OCMF_SOURCE_TOOL="claude-code"
export OCMF_HOST_METHOD="A1+B"

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
if [ "$ACTUAL_TOOL" != "claude-code" ]; then
    echo "✗ ERROR: Config verification failed!"
    echo "  Expected OCMF_SOURCE_TOOL=claude-code"
    echo "  Got OCMF_SOURCE_TOOL=$ACTUAL_TOOL"
    echo "  This indicates a setup issue."
    exit 1
fi
echo "  ✓ Verified OCMF_SOURCE_TOOL=claude-code"

echo ""
echo "--- Step 3: Claude MCP Configuration (Optional) ---"
echo ""
echo "  MCP allows Claude to call 'ocmaf recall' and 'ocmaf remember' directly."
echo "  Without MCP, you can still use OCMF manually via CLI."
echo ""

if [ -d "$MCP_CONFIG_DIR" ]; then
    echo "  Claude config directory found: $MCP_CONFIG_DIR"

    # Check if MCP config already exists
    if [ -f "$MCP_CONFIG" ]; then
        echo "  MCP config exists: $MCP_CONFIG"

        # Use Python to safely merge OCMF into existing config
        echo "  Merging OCMF into existing MCP config..."
        python3 - "$MCP_CONFIG" "$OCMF_PATH" << 'PYEOF'
import json
import sys

config_path = sys.argv[1]
ocmf_path = sys.argv[2]

# Read existing config
with open(config_path, 'r') as f:
    config = json.load(f)

# Ensure mcpServers exists
if "mcpServers" not in config:
    config["mcpServers"] = {}

# Add OCMF if not present
if "ocmf" not in config["mcpServers"]:
    config["mcpServers"]["ocmf"] = {
        "command": "python3",
        "args": ["-m", "ocmaf.bridge.mcp_server", "--tool", "claude-code"],
        "cwd": ocmf_path
    }
    print("  ✓ Added OCMF to existing MCP config")
else:
    print("  ✓ OCMF already in MCP config")

# Write back
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
PYEOF
        echo "✓ Merged MCP config"
    else
        echo "  Creating MCP config with OCMF server..."
        cat > "$MCP_CONFIG" << EOF
{
  "mcpServers": {
    "ocmf": {
      "command": "python3",
      "args": ["-m", "ocmaf.bridge.mcp_server", "--tool", "claude-code"],
      "cwd": "${OCMF_PATH}"
    }
  }
}
EOF
        echo "✓ Created $MCP_CONFIG"
    fi
else
    echo "  ⚠️  Claude config directory not found: $MCP_CONFIG_DIR"
    echo "  MCP configuration is optional."
fi

echo ""
echo "--- Step 4: Integration Verification ---"

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
" || echo "  ⚠️  Host detection verification skipped"

echo ""
echo "=================================================="
echo "✓ Claude Setup Complete"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Source the config: source ~/.ocmf/config.sh"
echo "  2. Run 'PYTHONPATH=src ocmaf unified status' to verify"
echo "  3. Auto-memory is enabled by default (OCMF_AUTO_MEMORY=1)"
echo ""
echo "Usage modes:"
echo "  A. MCP mode (recommended for full integration):"
echo "     - Claude can call 'ocmaf recall' and 'ocmaf remember' directly"
echo "     - Requires adding OCMF to Claude's MCP servers"
echo ""
echo "  B. CLI mode (manual):"
echo "     - Run 'PYTHONPATH=src ocmaf recall --query ...' manually"
echo "     - Copy/paste results into conversation"
echo ""
echo "For auto-recall (Method A1+B):"
echo "  - MCP mode: Claude calls recall automatically at session start"
echo "  - CLI mode: User manually runs ocmaf and includes results"
