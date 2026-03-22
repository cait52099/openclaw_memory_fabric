# Codex MCP Check

**Run ID**: 022-codex-real-host-closure
**Date**: 2026-03-20
**Task**: MCP Configuration Verification

---

## MCP Configuration

### codex mcp list

```
$ /Applications/Codex.app/Contents/Resources/codex mcp list
Name  Command                            Args  Env  Cwd  Status   Auth
ocmf  /Users/caihongwei/bin/ocmaf-codex  -     -    -    enabled  Unsupported
```

### Wrapper Script

Created at `~/bin/ocmaf-codex`:
```bash
#!/bin/bash
export PYTHONPATH="/Users/caihongwei/project/openclaw_memory_fabric/src"
exec python3 -m ocmaf.bridge.mcp_server --tool codex-cli "$@"
```

### Why Wrapper Needed

Without PYTHONPATH, `python3 -m ocmaf.bridge.mcp_server` fails with import error because `ocmaf` module cannot be found. The wrapper sets PYTHONPATH before launching.

### Verification: codex exec shows mcp ready

```
mcp: ocmf starting
mcp: ocmf ready
mcp startup: ready: ocmf
```

---

## Summary

| Check | Result |
|-------|--------|
| MCP configured | ✅ Yes |
| OCMF server | ✅ configured |
| Status | enabled |
| Wrapper script | ✅ created |
| MCP handshake | ✅ successful |

---

**AC-CDX-002**: ✅ PASS
