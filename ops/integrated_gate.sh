#!/bin/bash
# OCMF Integrated Regression Gate
#
# This script integrates the Phase 6G regression gate with主线变更流程.
# It runs before commits or deployments to ensure no regression in:
# - recall output (source_tool, friendly name, timestamp)
# - explain output (match_reasons, provenance)
# - conflict detection output

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

GATE_STATUS="PASS"
GATE_FAILED=""

echo "=================================================="
echo "OCMF Integrated Regression Gate"
echo "=================================================="

# Check if regression gate script exists
GATE_SCRIPT="runs/028-regression-gate/run_regression_gate.py"
if [ ! -f "$GATE_SCRIPT" ]; then
    echo ""
    echo "⚠️  WARNING: Regression gate script not found"
    echo "   $GATE_SCRIPT"
    echo "   Skipping regression check"
    echo ""
    exit 0
fi

echo ""
echo "--- Running Regression Gate ---"

# Run the regression gate
if python3 "$GATE_SCRIPT"; then
    echo ""
    echo -e "${GREEN}✓ REGRESSION GATE: PASS${NC}"
else
    GATE_STATUS="FAIL"
    GATE_FAILED="Regression gate failed"
    echo ""
    echo -e "${RED}✗ REGRESSION GATE: FAIL${NC}"
    echo ""
    echo "Regression gate detected output drift."
    echo ""
    echo "Options:"
    echo "  1. Review the changes that caused the drift"
    echo "  2. Update golden examples if the drift is intentional"
    echo "  3. Fix the underlying code to match golden"
    echo ""
    echo "To update golden examples:"
    echo "  python3 runs/027-stable-golden-examples/generate_golden_examples.py"
fi

echo ""
echo "=================================================="

# Return status based on gate result
if [ "$GATE_STATUS" = "FAIL" ]; then
    exit 1
fi

exit 0
