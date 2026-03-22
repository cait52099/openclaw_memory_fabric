# Claude Line Final Position

**Run ID**: 020-claude-hook-explore
**Date**: 2026-03-20
**Status**: FINAL - CLOSED

---

## EXECUTIVE SUMMARY

This document establishes the final, authoritative position on Claude's native automation capabilities for OCMF. It resolves the Method A/B debate and defines the recommended production path.

---

## A. CLAUDE METHOD A - VERIFIED (成立部分)

### What IS Established

| Capability | Status | Evidence |
|------------|--------|----------|
| Official settings-based hooks path | ✅ VERIFIED | `settings_hooks_config.md` |
| SessionStart hook fires | ✅ VERIFIED | `hooks_trigger_log.md` |
| SessionEnd hook fires | ✅ VERIFIED | `hooks_trigger_log.md` |
| Native auto-trigger (no user input) | ✅ VERIFIED | `hooks_trigger_log.md` |
| ocmf_recall auto-called | ✅ VERIFIED | `sqlite_reconciliation.md` |
| ocmf_remember auto-called | ✅ VERIFIED | `sqlite_reconciliation.md` |
| Background auto-memory | ✅ VERIFIED | Events in SQLite |

### Configuration
```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "/tmp/auto_memory.sh", "timeout": 30 }] }],
    "SessionEnd": [{ "hooks": [{ "type": "command", "command": "/tmp/auto_memory.sh", "timeout": 30 }] }]
  }
}
```

---

## B. CLAUDE METHOD A - NOT ESTABLISHED (未成立部分)

### What is NOT Established

| Capability | Status | Reason |
|------------|--------|--------|
| Pure native context injection | ❌ FAIL | Hooks run as side processes |
| Hook outputs in Claude context | ❌ FAIL | Claude doesn't read hook tool outputs |
| Seamless auto-recall in conversation | ❌ FAIL | Results don't affect current response |

### Reason
Claude hooks execute as **side processes** - their outputs (including MCP tool responses) are NOT automatically injected into Claude's conversation context.

---

## C. CLAUDE METHOD B - VERIFIED

| Capability | Status | Evidence |
|------------|--------|----------|
| System-prompt injection | ✅ VERIFIED | Run 019 |
| Claude follows auto-memory instructions | ✅ VERIFIED | Run 019 |
| Context-aware recall | ✅ VERIFIED | Claude uses recalled info |

---

## D. RECOMMENDED PRODUCTION PATH

### Final Recommendation: A + B

| Component | Method | Role |
|-----------|--------|------|
| Background memory collection | **Method A** | Auto-capture decisions, constraints, patterns |
| Context-aware recall | **Method B** | Inject relevant memories into conversation |

### Rationale
- Method A: Handles automatic background collection without user intervention
- Method B: Handles context injection so Claude actually USES the memories

**Neither method alone is sufficient** - A provides auto-storage, B provides seamless recall.

---

## E. TERMINOLOGY CLOSURE (术语收口)

The following terms are now **definitive** in this project:

| Term | Definition | Claude Support |
|------|------------|----------------|
| **Native auto-trigger** | Hooks auto-call tools without user input | ✅ A |
| **Native context injection** | Hook outputs automatically affect Claude's context | ❌ NOT SUPPORTED |
| **System-prompt assisted automation** | Claude follows injected instructions | ✅ B |
| **Manual MCP** | User explicitly calls tools | ✅ C |
| **Synthetic test** | Automated tests via pytest | ✅ |

### Prohibited Shorthand
- ❌ "Claude Method A" can NOT mean "fully native auto-memory"
- ❌ Must always specify: "native auto-trigger" vs "native context injection"
- ❌ Must always specify: "Method A" vs "Method B" vs "Method A+B"

---

## F. FINAL VERDICT

| Metric | Status |
|--------|--------|
| **FINAL_STATUS** | **CLOSED** |
| **CLAUDE_METHOD_A** | **PASS** (native auto-trigger) |
| **CLAUDE_PURE_METHOD_A** | **FAIL** (native context injection) |
| **CLAUDE_METHOD_B** | **PASS** |
| **RECOMMENDED_PATH** | **A + B** |

---

## G. EVIDENCE CHAIN

| Evidence File | Purpose |
|---------------|---------|
| `settings_hooks_config.md` | Official schema configuration |
| `hooks_trigger_log.md` | Both events triggered verification |
| `sqlite_reconciliation.md` | Events stored in database |
| `method_boundary.md` | A/B/C distinction |
| `evidence.md` | Final evidence summary |
| `known_limits.md` | Limitations documented |
| **This file** | Final position closure |

---

## H. WHAT THIS MEANS FOR OCMF

1. **Claude CAN do automatic background memory collection** (Method A)
2. **Claude CANNOT seamlessly inject memories without system-prompt** (Pure A fails)
3. **Claude CAN do seamless recall with system-prompt** (Method B works)
4. **Best path: A + B combination** (A for collection, B for recall)

---

**This position is FINAL and binding for the OCMF project.**
**No further debate on Claude native capabilities is productive.**
