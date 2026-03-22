#!/bin/bash
# OCMF Verify Smoke Test
# Runs all P0 regression tests and smoke tests

set -e

echo "=================================================="
echo "OCMF Verify Smoke Test"
echo "=================================================="

# Change to project root
cd "$(dirname "$0")/.."

echo ""
echo "--- Running P0 Regression Tests ---"
python3 tests/test_p0_regression.py

echo ""
echo "--- Running Adapter Smoke Tests ---"
python3 ops/adapter_test.py

echo ""
echo "--- Running Codex Adapter Tests ---"
python3 tests/test_codex_adapter.py

echo ""
echo "--- Running Cross-Tool Integration Tests (Phase 3B.1) ---"
python3 tests/test_cross_tool_integration.py

echo ""
echo "--- Running OpenClaw Adapter Tests (Phase 3C) ---"
python3 tests/test_openclaw_adapter.py

echo ""
echo "--- Running Tri-Tool Integration Tests (Phase 3C) ---"
python3 tests/test_tri_tool_integration.py

echo ""
echo "--- Running Fallback / E2E Tests (Phase 4B) ---"
python3 tests/test_e2e_fallback.py

echo ""
echo "--- Running Golden Examples Regression Gate (Phase 6G) ---"
if [ -f "runs/028-regression-gate/run_regression_gate.py" ]; then
    python3 runs/028-regression-gate/run_regression_gate.py
    echo "✓ Regression gate passed"
else
    echo "⚠ Regression gate not found (skipping)"
fi

echo ""
echo "=================================================="
echo "All Smoke Tests Passed"
echo "=================================================="
