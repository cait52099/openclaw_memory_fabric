# Claude Code Real Host Entry Point

## Environment Variables

Claude Code adapter uses the following environment variables to derive context:

| Env Variable | Description | Default |
|--------------|-------------|---------|
| `CLAUDE_USER_ID` | User identifier | `default` |
| `CLAUDE_WORKSPACE` | Workspace directory | None |
| `CLAUDE_PROJECT` | Project path | None |
| `CLAUDE_SESSION_ID` | Session identifier | None |

## Scope Mapping

The adapter maps context to memory scope as follows:

```python
{
    "user": CLAUDE_USER_ID or "default",
    "workspace": CLAUDE_WORKSPACE,
    "project": CLAUDE_PROJECT,
    "session": CLAUDE_SESSION_ID,
    "tool": "claude-code"  # Explicit tool isolation
}
```

## Integration Methods

### Method 1: Direct Adapter Usage

```python
from ocmaf.adapters import ClaudeCodeAdapter

adapter = ClaudeCodeAdapter(db_path="/path/to/memory.db")

# Before generating response - recall relevant memories
injection = adapter.before_response(
    query="Your query here",
    context={}  # Uses CLAUDE_* env vars automatically
)

# After generating response - remember the interaction
event_id = adapter.after_response(
    query="Your query",
    response="AI response",
    context={}  # Uses CLAUDE_* env vars automatically
)
```

### Method 2: Standalone Functions

```python
from ocmaf.adapters.claude_code import get_recall_context, remember_interaction

# Recall
injection = get_recall_context(
    query="Your query",
    user="user123",
    project="/path/to/project",
    session="session456",
    db_path="/path/to/memory.db"
)

# Remember
event_id = remember_interaction(
    query="Your query",
    response="AI response",
    user="user123",
    project="/path/to/project",
    session="session456",
    db_path="/path/to/memory.db"
)
```

### Method 3: Hook Integration (Native)

If Claude Code supports custom hooks, integrate at:

- **before_response**: Call `adapter.before_response(query, context)`
- **after_response**: Call `adapter.after_response(query, response, context)`

## Verification Commands

```bash
# Check environment variables are set
echo $CLAUDE_USER_ID
echo $CLAUDE_WORKSPACE
echo $CLAUDE_PROJECT
echo $CLAUDE_SESSION_ID

# Test adapter initialization
python -c "from ocmaf.adapters import ClaudeCodeAdapter; a = ClaudeCodeAdapter(); print(a.get_name())"

# Test recall
python -c "
from ocmaf.adapters import ClaudeCodeAdapter
adapter = ClaudeCodeAdapter()
result = adapter.before_response('test query', {})
print('Recall result:', result)
"
```

## Database Path

Default: `~/.ocmaf/memory.db` (if db_path not specified)

Recommended: Use explicit path for production:
```python
adapter = ClaudeCodeAdapter(db_path="/path/to/project/.ocmf/memory.db")
```

## Tool Isolation

The adapter explicitly sets `tool='claude-code'` to ensure:
- Memories created by Claude Code are isolated from other tools
- Same-tool recall works correctly
- Cross-tool isolation is maintained
