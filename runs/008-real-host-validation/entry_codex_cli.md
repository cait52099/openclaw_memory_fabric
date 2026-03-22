# Codex CLI Real Host Entry Point

## Environment Variables

Codex CLI adapter uses the following environment variables to derive context:

| Env Variable | Description | Default |
|--------------|-------------|---------|
| `CODEX_USER` | User identifier | `default` |
| `CODEX_WORKSPACE` | Workspace directory | None |
| `CODEX_PROJECT` | Project path (defaults to cwd) | `os.getcwd()` |
| `CODEX_SESSION_ID` | Session identifier | None |
| `CODEX_RUN_ID` | Current run identifier | None |

## Scope Mapping

The adapter maps context to memory scope as follows:

```python
{
    "user": CODEX_USER or "default",
    "workspace": CODEX_WORKSPACE,
    "project": CODEX_PROJECT or os.getcwd(),
    "session": CODEX_SESSION_ID,
    "tool": "codex-cli"  # Explicit tool isolation
}
```

## Integration Methods

### Method 1: Direct Adapter Usage

```python
from ocmaf.adapters import CodexCLIAdapter

adapter = CodexCLIAdapter(db_path="/path/to/memory.db")

# Before generating response - recall relevant memories
injection = adapter.before_response(
    query="Your task description",
    context={}  # Uses CODEX_* env vars automatically
)

# After generating response - remember the interaction
event_id = adapter.after_response(
    query="Your task",
    response="Task result",
    context={}  # Uses CODEX_* env vars automatically
)
```

### Method 2: Standalone Functions

```python
from ocmaf.adapters.codex_cli import (
    get_recall_context,
    remember_interaction,
    remember_task_result
)

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

# Remember task result
event_id = remember_task_result(
    task="Implement auth",
    result="Successfully implemented JWT auth",
    success=True,
    user="user123",
    project="/path/to/project",
    session="session456",
    db_path="/path/to/memory.db"
)
```

### Method 3: CLI Wrapper Script

Create a wrapper script `ocodex-memory`:

```bash
#!/bin/bash
# Codex CLI memory wrapper

SUBCOMMAND=$1
shift

case $SUBCOMMAND in
    recall)
        python -c "
from ocmaf.adapters.codex_cli import get_recall_context
import os, json
query = '$1'
result = get_recall_context(query)
print(result)
"
        ;;
    remember)
        # Remember interaction after Codex completes
        python -c "
from ocmaf.adapters.codex_cli import remember_interaction
import os
"
        ;;
esac
```

## Verification Commands

```bash
# Check environment variables are set
echo $CODEX_USER
echo $CODEX_WORKSPACE
echo $CODEX_PROJECT
echo $CODEX_SESSION_ID
echo $CODEX_RUN_ID

# Test adapter initialization
python -c "from ocmaf.adapters import CodexCLIAdapter; a = CodexCLIAdapter(); print(a.get_name())"

# Test recall
python -c "
from ocmaf.adapters import CodexCLIAdapter
adapter = CodexCLIAdapter()
result = adapter.before_response('implement login', {})
print('Recall result:', result)
"
```

## Database Path

Default: `~/.ocmaf/memory.db` (if db_path not specified)

Recommended: Use explicit path for production:
```python
adapter = CodexCLIAdapter(db_path="/path/to/project/.ocmf/memory.db")
```

## Tool Isolation

The adapter explicitly sets `tool='codex-cli'` to ensure:
- Memories created by Codex CLI are isolated from other tools
- Same-tool recall works correctly
- Cross-tool isolation is maintained (Claude Code cannot recall Codex memories by default)

## Tier Classification

Codex CLI is a **Tier B** adapter (CLI wrapper) - it wraps CLI calls rather than integrating at the hook level. The adapter provides a programmatic interface that can be called before/after Codex CLI runs.

## Integration Example with Codex CLI

```python
# Before running Codex CLI command
import os
os.environ["CODEX_PROJECT"] = "/path/to/project"
os.environ["CODEX_SESSION_ID"] = "session-123"

from ocmaf.adapters import CodexCLIAdapter

adapter = CodexCLIAdapter(db_path="/path/to/memory.db")

# Get recall context before task
context = adapter.before_response(
    query="Fix authentication bug",
    context={}
)
print("Relevant memories:", context)

# ... Run Codex CLI command ...

# Remember the task result
adapter.after_task(
    task="Fix authentication bug",
    result="Fixed JWT token expiry issue",
    success=True,
    context={}
)
```
