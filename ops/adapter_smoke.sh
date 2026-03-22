#!/bin/bash
# Adapter Smoke Test - Verify recall/remember closed loop

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_DIR/.ocmaf/test_adapter.db"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================"
echo "OCMF Adapter Smoke Test"
echo "============================================"

# Clean up old test DB
rm -f "$DB_PATH"
mkdir -p "$(dirname "$DB_PATH")"

# Export Python path
export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local name="$1"
    local cmd="$2"
    echo -n "Testing: $name ... "
    if eval "$cmd" > /tmp/test_output.txt 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "Output:"
        cat /tmp/test_output.txt
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

echo ""
echo "=== Phase 1: Basic Import ==="

run_test "Import SDK" \
    'python3 -c "from ocmaf.sdk import MemorySession; print(\"OK\")"'

run_test "Import Adapter" \
    'python3 -c "from ocmaf.adapters import ClaudeCodeAdapter; print(\"OK\")"'

echo ""
echo "=== Phase 2: Memory Session ==="

run_test "Create session and remember" \
    "python3 -c '
from ocmaf.sdk import MemorySession

with MemorySession(user='test_user', db_path='$DB_PATH') as session:
    event_id = session.capture_chat_turn(
        \"What is Python?\",
        \"Python is a programming language.\",
        source_tool='test'
    )
    print(f\"Event ID: {event_id}\")
print(\"OK\")
'"

run_test "Recall after remember" \
    "python3 -c '
from ocmaf.sdk import MemorySession

with MemorySession(user='test_user', db_path='$DB_PATH') as session:
    session.capture_chat_turn(
        \"How do I use lists in Python?\",
        \"You can create lists with brackets: my_list = [1, 2, 3]\",
        source_tool='test'
    )
    result = session.recall(\"Python list\")
    print(f\"Found {len(result.memories)} memories\")
print(\"OK\")
'"

echo ""
echo "=== Phase 3: Adapter Hooks ==="

run_test "Claude Code adapter before_response" \
    'python3 -c "
from ocmaf.adapters.claude_code import ClaudeCodeAdapter

adapter = ClaudeCodeAdapter(db_path=\"$DB_PATH\")
injection = adapter.before_response(\"test query\", {\"user\": \"test_user\"})
print(f\"Injection length: {len(injection)}\")
print(\"OK\")
"'

run_test "Claude Code adapter after_response" \
    'python3 -c "
from ocmaf.adapters.claude_code import ClaudeCodeAdapter

adapter = ClaudeCodeAdapter(db_path=\"$DB_PATH\")
event_id = adapter.after_response(
    \"Test query\",
    \"Test response\",
    {\"user\": \"test_user\"}
)
print(f\"Event ID: {event_id}\")
print(\"OK\")
"'

echo ""
echo "=== Phase 4: Closed Loop Test ==="

run_test "Complete recall->response->remember->recall loop" \
    'python3 -c "
from ocmaf.adapters.claude_code import ClaudeCodeAdapter

adapter = ClaudeCodeAdapter(db_path=\"$DB_PATH\")
context = {\"user\": \"test_user\", \"session\": \"test_session\"}

query1 = \"How do I create a Python class?\"
response1 = \"Use the class keyword: class MyClass:\"

injection1 = adapter.before_response(query1, context)
print(f\"Round 1 injection: {len(injection1)} chars\")

event_id = adapter.after_response(query1, response1, context)
print(f\"Round 1 remembered: {event_id}\")

query2 = \"Show me a Python class example\"
injection2 = adapter.before_response(query2, context)
print(f\"Round 2 injection: {len(injection2)} chars\")

print(\"Closed loop: OK\")
"'

echo ""
echo "=== Phase 5: Scope Mapping ==="

run_test "Scope mapping from context" \
    'python3 -c "
from ocmaf.adapters.scope_mapping import get_scope_mapper

mapper = get_scope_mapper(\"claude-code\")
scope = mapper.map_from_context({
    \"user\": \"my_user\",
    \"workspace\": \"my_workspace\",
    \"project\": \"my_project\",
    \"session\": \"my_session\"
})

assert scope[\"user\"] == \"my_user\"
assert scope[\"workspace\"] == \"my_workspace\"
assert scope[\"project\"] == \"my_project\"
assert scope[\"session\"] == \"my_session\"
print(\"OK\")
"'

echo ""
echo "=== Phase 6: Injection Policy ==="

run_test "Injection policy truncation" \
    'python3 -c "
from ocmaf.adapters.base import InjectionPolicy

policy = InjectionPolicy(max_length=100)
text = \"A\" * 200
truncated = policy.truncate(text)
assert len(truncated) < 210
assert \"...\" in truncated
print(\"OK\")
"'

run_test "Layer-based injection policy" \
    'python3 -c "
from ocmaf.adapters.base import InjectionPolicy

system_policy = InjectionPolicy.for_layer(\"system\")
user_policy = InjectionPolicy.for_layer(\"user\")

assert system_policy.max_length < user_policy.max_length
print(f\"System limit: {system_policy.max_length}\")
print(f\"User limit: {user_policy.max_length}\")
print(\"OK\")
"'

# Clean up
rm -f "$DB_PATH"

echo ""
echo "============================================"
echo "Test Results"
echo "============================================"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
