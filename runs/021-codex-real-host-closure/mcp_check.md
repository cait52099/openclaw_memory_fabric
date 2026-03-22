# Codex MCP Support Check

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-02

---

## MCP Support Verification

### codex --help | grep mcp

MCP-related subcommands found:
- `codex mcp` - Manage external MCP servers for Codex
- `codex mcp-server` - Start Codex as an MCP server (stdio)

### codex mcp subcommands

```
$ /Applications/Codex.app/Contents/Resources/codex mcp --help
Manage external MCP servers for Codex

Commands:
  list    List configured MCP servers
  get     Get MCP server config
  add     Add an MCP server
  remove  Remove an MCP server
  login   Manage login
  logout  Remove stored credentials
```

### codex mcp list

```
$ /Applications/Codex.app/Contents/Resources/codex mcp list
Name  Command  Args                                         Env  Cwd  Status   Auth
ocmf  python3  -m ocmaf.bridge.mcp_server --tool codex-cli  -    -    enabled  Unsupported
```

**Critical Finding**: OCMF MCP server is already configured and ENABLED in Codex.

### OCMF MCP Server Details

| Field | Value |
|-------|-------|
| Name | `ocmf` |
| Command | `python3` |
| Args | `-m ocmaf.bridge.mcp_server --tool codex-cli` |
| Env | - |
| Cwd | - |
| Status | **enabled** |
| Auth | Unsupported |

### codex mcp-server

```
$ /Applications/Codex.app/Contents/Resources/codex mcp-server --help
Start Codex as an MCP server (stdio)

Options:
  -c, --config <key=value>  Override configuration values
```

---

## OCMF MCP Server Tool Test

### Initialize + tools/list

```
$ echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}' | \
  python3 -m ocmaf.bridge.mcp_server --tool codex-cli

Response:
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05",
  "capabilities":{"tools":{}},"serverInfo":{"name":"ocmf-mcp","version":"0.1.0"}}}

{"jsonrpc":"2.0","id":2,"result":{"tools":[
  {"name":"ocmf_recall","description":"Recall relevant memories from OCMF",
   "inputSchema":{"type":"object","properties":{"query":{"type":"string","description":"Search query"}},"required":["query"]}},
  {"name":"ocmf_remember","description":"Store an event into OCMF memory",
   "inputSchema":{"type":"object","properties":{"content":{"type":"string"},"event_type":{"type":"string","enum":["chat_turn","task_result","decision"]}},"required":["content"]}},
  {"name":"ocmf_get_injection","description":"Get injection text for LLM context",
   "inputSchema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}}
]}}
```

**Tools Exposed**: 3
- `ocmf_recall` - Recall memories
- `ocmf_remember` - Store memories
- `ocmf_get_injection` - Get context injection text

---

## AC-CDX-002

- [x] Codex supports MCP configuration
- [x] `codex mcp` subcommand available
- [x] OCMF MCP server already configured and enabled
- [x] MCP tools correctly exposed via JSON-RPC

**Status**: ✅ PASS
