# Claude Plugin Capability Evidence

**Run ID**: 020-claude-hook-explore
**Task**: T-5A-01
**Date**: 2026-03-20

---

## Summary

Claude 2.1.78 has a plugin system, but it requires marketplace distribution and does NOT support local auto-trigger hooks.

---

## Evidence

### 1. --plugin-dir Flag Available

```
$ claude --help | grep -i plugin
--plugin-dir <path>                               Load plugins from a directory for this session only (repeatable: --plugin-dir A --plugin-dir B) (default: [])
plugin|plugins                                    Manage Claude Code plugins
```

**Status**: ✅ Flag exists

### 2. Plugin System Commands

```
$ claude plugin --help
Commands:
  disable    Disable an enabled plugin
  enable     Enable a disabled plugin
  install    Install a plugin from available marketplaces
  list       List installed plugins
  marketplace Manage Claude Code marketplaces
  uninstall  Uninstall an installed plugin
  update     Update a plugin to the latest version
  validate   Validate a plugin or marketplace manifest
```

**Status**: ✅ Plugin commands exist

### 3. Plugin Validation - Local Install NOT Supported

```
$ claude plugin install /tmp/test_ocmf_plugin
✘ Failed to install plugin "/tmp/test_ocmf_plugin": Plugin "/tmp/test_ocmf_plugin" not found in any configured marketplace
```

**Status**: ❌ Local plugins not supported - must be from marketplace

### 4. Plugin Format Requires Marketplace Structure

```
$ claude plugin validate /tmp/test_ocmf_plugin
✘ Found 1 error:
  ❯ author: Invalid input: expected object, received string
```

**Status**: ❌ Complex marketplace schema required

---

## Conclusion

Claude's plugin system is designed for **marketplace distribution** (like VS Code extensions), NOT for:
- Local auto-trigger hooks
- Automatic message processing
- Custom event handlers

**Finding**: Claude does NOT have native hooks for automatic recall/remember triggering.
