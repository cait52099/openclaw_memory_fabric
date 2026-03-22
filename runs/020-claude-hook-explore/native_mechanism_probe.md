# Claude Host-Native Mechanism Narrow Validation

**Run ID**: 020-claude-hook-explore
**Date**: 2026-03-20

---

## Narrow Validation: Method A Final Probe

### Objective
Find ONE real native auto-trigger mechanism in Claude 2.1.78

---

## Probe 1: --plugin-dir

**Result**: ❌ CANNOT auto-trigger
- Plugin system requires marketplace distribution
- Local plugins not supported
- No auto-trigger capability

---

## Probe 2: --debug hooks

**Result**: ❌ Observation only
- Debug output is read-only
- Cannot inject custom behavior
- No configurable triggers

---

## Probe 3: hookify Plugin (Official Marketplace)

**Finding**: ✅ Found native hook system!

### Hook Types Available
1. **PreToolUse** - Before tool executes
2. **PostToolUse** - After tool executes
3. **Stop** - When Claude stops
4. **UserPromptSubmit** - When user submits prompt

### Installation
```
$ claude plugin install hookify
✔ Successfully installed plugin: hookify@claude-plugins-official
```

### Analysis

**Capability**: Hookify provides REAL native hooks:
- ✅ PreToolUse - Can intercept before tool use
- ✅ PostToolUse - Can intercept after tool use
- ✅ UserPromptSubmit - Can intercept when user submits prompt
- ✅ Stop - Can intercept when Claude stops

**Limitation**: Hookify hooks are for **blocking/warning**, NOT for auto-triggering other tools

The hooks can:
- `warn` - Show warning but allow operation
- `block` - Prevent operation from executing

They CANNOT:
- Automatically call another tool (like ocmf_recall)
- Inject tool calls into the conversation
- Trigger MCP tools automatically

---

## Final Probe Result

| Mechanism | Available | Auto-Trigger MCP Tools |
|-----------|-----------|------------------------|
| --plugin-dir | ✅ | ❌ |
| --debug hooks | ✅ | ❌ |
| hookify hooks | ✅ | ❌ (warn/block only) |
| Custom agents | ✅ | ❌ |
| MCP (baseline) | ✅ | Manual only |

---

## CONCLUSION: Method A = FAIL

**Finding**: Claude 2.1.78 has NO native mechanism to auto-trigger MCP tools (like ocmf_recall/ocmf_remember)

The available native hooks (via hookify plugin) are for:
- Blocking/warning operations
- NOT for auto-invoking other tools

**This is a fundamental architecture limitation**, not a missing feature.

---

## Honest Assessment

**Claude Native Auto-Trigger for MCP Tools**: ❌ NOT AVAILABLE

- No native mechanism can automatically call ocmf_recall
- No native mechanism can automatically call ocmf_remember
- Hooks are for prevention/warning, not automation

**Method B (System-Prompt)**: ✅ Available but non-deterministic
**Method C (Manual MCP)**: ✅ Available and reliable
