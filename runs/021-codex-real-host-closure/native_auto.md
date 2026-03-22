# Codex Native Auto-Trigger Verification

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-08

---

## Native Automation Boundary

### Investigation Results

#### 1. Hooks / Event Triggers

| Checked | Found |
|---------|-------|
| `codex hooks` command | ❌ NOT FOUND |
| `codex plugin` command | ❌ NOT FOUND |
| `codex events` command | ❌ NOT FOUND |
| Hook-related feature flags | ❌ NOT FOUND |
| SessionStart/SessionEnd hooks | ❌ NOT FOUND |
| PreToolUse/PostToolUse hooks | ❌ NOT FOUND |

#### 2. MCP as Auto-Trigger Alternative

MCP servers in Codex are NOT auto-triggered. They must be explicitly invoked by the model.

#### 3. Sandbox / Background Execution

```
$ codex sandbox --help
Run commands within a Codex-provided sandbox

Options:
  --sandbox <MODE>  Select the sandbox policy (read-only, workspace-write, danger-full-access)
```

Sandbox is for running model-generated commands, not for hooking into Codex lifecycle.

#### 4. Features List

```
$ codex features list
[No auto-trigger / hooks-related features]
```

---

## Codex Native Auto-Trigger Status

### Compared to Claude

| Capability | Claude | Codex |
|-----------|--------|-------|
| SessionStart hook | ✅ YES | ❌ NO |
| SessionEnd hook | ✅ YES | ❌ NO |
| PreToolUse hook | ✅ YES | ❌ NO |
| PostToolUse hook | ✅ YES | ❌ NO |
| Native auto-trigger | ✅ YES | ❌ NO |
| MCP extension | ✅ (via tools) | ✅ YES |

### Codex Equivalent

Codex does NOT have native auto-trigger hooks. Its primary extension mechanism is MCP, which requires explicit model invocation.

---

## Conclusion

**Codex native auto-trigger (Method A equivalent) = ❌ NOT AVAILABLE**

For Codex:
- **Method A (native auto-trigger)**: ❌ NOT POSSIBLE
- **Method B (system-prompt)**: ⚠️ Possible but not tested
- **Method C (manual MCP)**: ✅ VERIFIED

This is a fundamental architectural difference between Claude and Codex.

---

## AC-CDX-004

- [x] Native hooks investigated
- [x] No auto-trigger mechanism found
- [x] MCP is the only extension path
- [x] Clear boundary documented

**Status**: ✅ VERIFIED (native auto-trigger = NOT AVAILABLE)
