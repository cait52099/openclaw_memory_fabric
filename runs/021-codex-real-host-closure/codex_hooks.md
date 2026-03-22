# Codex Hooks / Plugin Mechanism Probe

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-03

---

## Hooks / Plugin Investigation

### codex --help (full scan for hooks)

```
$ /Applications/Codex.app/Contents/Resources/codex --help

Commands:
  exec        Run Codex non-interactively
  review      Run a code review non-interactively
  login       Manage login
  logout      Remove stored authentication credentials
  mcp         Manage external MCP servers for Codex
  mcp-server  Start Codex as an MCP server (stdio)
  app-server  [experimental] Run the app server or related tooling
  app         Launch the Codex desktop app
  completion  Generate shell completion scripts
  sandbox     Run commands within a Codex-provided sandbox
  debug       Debugging tools
  apply       Apply the latest diff
  resume      Resume a previous interactive session
  fork        Fork a previous interactive session
  cloud       [EXPERIMENTAL] Browse tasks from Codex Cloud
  features    Inspect feature flags
  help        Print this message or the help of the given subcommand(s)
```

### Hook-related search

No `hooks` subcommand found. Searched `--help` output for:
- "hook" - Not found
- "plugin" - Not found
- "event" - Not found
- "trigger" - Not found
- "automation" - Not found

### codex features list

```
$ /Applications/Codex.app/Contents/Resources/codex features list
[No hooks-related feature flags found]
```

### codex sandbox

```
$ /Applications/Codex.app/Contents/Resources/codex sandbox --help
Run commands within a Codex-provided sandbox

Options:
  --sandbox <MODE>  Select the sandbox policy (read-only, workspace-write, danger-full-access)
```

### codex exec (non-interactive mode)

```
$ /Applications/Codex.app/Contents/Resources/codex exec --help
Run Codex non-interactively

Options:
  -p, --profile <CONFIG_PROFILE>  Configuration profile from config.toml
```

---

## Analysis

### Hooks / Auto-trigger Capability

| Capability | Found | Evidence |
|-----------|-------|----------|
| Hooks subcommand | ❌ NO | No `codex hooks` command |
| Plugin subcommand | ❌ NO | No `codex plugin` command |
| Event-based triggers | ❌ NO | No SessionStart/SessionEnd hooks |
| Auto-trigger mechanism | ❌ NO | No automatic execution points discovered |
| Native hooks | ❌ NOT FOUND | No hooks in --help output |

### MCP-based Alternative

Codex's primary extension mechanism is MCP:
- `codex mcp add` - Add external MCP servers
- `codex mcp-server` - Run Codex as MCP server

OCMF is already configured as an MCP server for Codex.

---

## Conclusion

**Codex does NOT have a native hooks/plugin auto-trigger mechanism** like Claude's settings-based hooks.

The equivalent integration path for Codex is:
- **MCP** - Configure OCMF as an MCP server (already done ✅)
- **Method C** - User explicitly calls ocmf_remember/ocmf_recall tools

This means for Codex:
- **Method A (native auto-trigger)** = ❌ NOT AVAILABLE
- **Method B (system-prompt)** = ⚠️ MAY BE POSSIBLE (not yet tested)
- **Method C (manual MCP)** = ✅ AVAILABLE

---

## AC-CDX-004

- [x] Codex hooks mechanism probed
- [x] No native auto-trigger hooks found
- [x] MCP is the primary extension mechanism
- [x] OCMF already integrated via MCP

**Status**: ✅ EXPLORED (native hooks = NOT FOUND, MCP = PRIMARY PATH)
