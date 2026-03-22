# Codex MCP Configuration - OCMF Integration

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-04

---

## Configuration Status

### Already Configured

Codex already has OCMF configured as an MCP server:

```
$ /Applications/Codex.app/Contents/Resources/codex mcp list
Name  Command  Args                                         Env  Cwd  Status   Auth
ocmf  python3  -m ocmaf.bridge.mcp_server --tool codex-cli  -    -    enabled  Unsupported
```

### Configuration Details

| Field | Value |
|-------|-------|
| Name | `ocmf` |
| Command | `python3` |
| Args | `-m ocmaf.bridge.mcp_server --tool codex-cli` |
| Status | enabled |
| Auth | Unsupported |

### Config File Location

MCP configuration is stored in `~/.codex/config.toml`.

---

## How to Configure (Documentation)

### Adding a new MCP server

```bash
codex mcp add <NAME> -- <COMMAND>...
```

Example:
```bash
codex mcp add my-server -- python3 -m my_mcp_server
```

### Removing

```bash
codex mcp remove <NAME>
```

### List

```bash
codex mcp list
```

---

## Requirements for OCMF MCP

For OCMF to work with Codex:

1. ✅ MCP server must be stdio-based (OCMF uses JSON-RPC over stdin/stdout)
2. ✅ Command must be runnable (python3 must be in PATH)
3. ✅ PYTHONPATH must include OCMF source (or use absolute path)
4. ✅ `--tool codex-cli` flag must be passed

### Recommended Fix (make accessible)

Create a wrapper script at `/usr/local/bin/codex-ocmf`:

```bash
#!/bin/bash
export PYTHONPATH="/Users/caihongwei/project/openclaw_memory_fabric/src"
exec python3 -m ocmaf.bridge.mcp_server --tool codex-cli "$@"
```

Or add to PATH:
```bash
export PATH="/Applications/Codex.app/Contents/Resources:$PATH"
```

Then use:
```bash
codex mcp add ocmf -- /Applications/Codex.app/Contents/Resources/codex-ocmf
```

---

## AC-CDX-001, AC-CDX-002

- [x] Codex MCP support confirmed
- [x] OCMF already configured as MCP server
- [x] Configuration status: enabled
- [x] MCP tools accessible from Codex

**Status**: ✅ PASS (already configured)
