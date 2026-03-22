# OpenClaw Real Host Entry Point

## Environment Variables

OpenClaw adapter uses the following environment variables to derive context:

| Env Variable | Description | Default |
|--------------|-------------|---------|
| `OPENCLAW_USER_ID` | User identifier | `default` |
| `OPENCLAW_WORKSPACE` | Workspace directory | None |
| `OPENCLAW_PROJECT` | Project path | None |
| `OPENCLAW_SESSION_ID` | Session identifier | None |
| `OPENCLAW_TASK_ID` | Current task identifier | None |

## Scope Mapping

The adapter maps context to memory scope as follows:

```python
{
    "user": OPENCLAW_USER_ID or "default",
    "workspace": OPENCLAW_WORKSPACE,
    "project": OPENCLAW_PROJECT,
    "session": OPENCLAW_SESSION_ID,
    "tool": "openclaw"  # Explicit tool isolation
}
```

## Integration Methods

### Method 1: Direct Adapter Usage (Tier A - Hook Level)

OpenClaw is a **Tier A** adapter - it integrates at the hook level with native support for callbacks.

```python
from ocmaf.adapters import OpenClawAdapter

adapter = OpenClawAdapter(db_path="/path/to/memory.db")

# Before generating response - recall relevant memories
injection = adapter.before_response(
    query="Your task description",
    context={}  # Uses OPENCLAW_* env vars automatically
)

# After generating response - remember the interaction
event_id = adapter.after_response(
    query="Your task",
    response="Task result",
    context={}  # Uses OPENCLAW_* env vars automatically
)
```

### Method 2: Standalone Functions

```python
from ocmaf.adapters.openclaw import get_recall_context, remember_interaction

# Recall before task
injection = get_recall_context(
    query="Implement user auth",
    user="user123",
    project="/path/to/project",
    session="session456",
    db_path="/path/to/memory.db"
)

# Remember chat interaction
event_id = remember_interaction(
    query="Your query",
    response="AI response",
    user="user123",
    project="/path/to/project",
    session="session456",
    db_path="/path/to/memory.db"
)
```

### Method 3: Hook Callback Integration (Native)

If OpenClaw supports custom hooks, register callbacks:

```python
# In OpenClaw's hook configuration
hooks:
  before_response:
    - module: ocmaf.adapters.openclaw
      function: before_response
  after_response:
    - module: ocmaf.adapters.openclaw
      function: after_response
```

Or programmatically:

```python
from ocmaf.adapters import OpenClawAdapter

# Register hooks with OpenClaw
def my_before_response(query, context):
    adapter = OpenClawAdapter()
    return adapter.before_response(query, context)

def my_after_response(query, response, context):
    adapter = OpenClawAdapter()
    return adapter.after_response(query, response, context)

# Register with OpenClaw runtime
openclaw.register_hook("before_response", my_before_response)
openclaw.register_hook("after_response", my_after_response)
```

## Verification Commands

```bash
# Check environment variables are set
echo $OPENCLAW_USER_ID
echo $OPENCLAW_WORKSPACE
echo $OPENCLAW_PROJECT
echo $OPENCLAW_SESSION_ID
echo $OPENCLAW_TASK_ID

# Test adapter initialization
python -c "from ocmaf.adapters import OpenClawAdapter; a = OpenClawAdapter(); print(a.get_name())"

# Test recall
python -c "
from ocmaf.adapters import OpenClawAdapter
adapter = OpenClawAdapter()
result = adapter.before_response('test task', {})
print('Recall result:', result)
"
```

## Database Path

Default: `~/.ocmaf/memory.db` (if db_path not specified)

Recommended: Use explicit path for production:
```python
adapter = OpenClawAdapter(db_path="/path/to/project/.ocmf/memory.db")
```

## Tool Isolation

The adapter explicitly sets `tool='openclaw'` to ensure:
- Memories created by OpenClaw are isolated from other tools
- Same-tool recall works correctly
- Cross-tool isolation is maintained (Claude Code / Codex CLI cannot recall OpenClaw memories by default)

## Tier Classification

OpenClaw is a **Tier A** adapter - it integrates at the hook level with native support for callbacks. This is the most seamless integration tier.

## Integration Example with OpenClaw

```python
# Within OpenClaw's execution context
import os
os.environ["OPENCLAW_PROJECT"] = "/path/to/project"
os.environ["OPENCLAW_SESSION_ID"] = "session-123"

from ocmaf.adapters import OpenClawAdapter

adapter = OpenClawAdapter(db_path="/path/to/memory.db")

# Get recall context before task execution
context = adapter.before_response(
    query="Refactor the authentication module",
    context={}
)
print("Relevant memories from past:", context)

# ... OpenClaw executes the task ...

# Remember the task result after execution
adapter.after_task(
    task="Refactor authentication module",
    result="Successfully split auth into separate service",
    success=True,
    context={}
)
```

## Fallback Behavior

If OPENCLAW_* environment variables are not set, the adapter falls back to:
- `user`: "default"
- `workspace`: None
- `project`: None (or passed via context)
- `session`: None (or passed via context)
- `tool`: "openclaw"

Always pass explicit context when possible for better memory organization.
