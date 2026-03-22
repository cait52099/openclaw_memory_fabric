# OCMF Claude Line - Known Limits

**Run ID**: 020-claude-hook-explore
**Date**: 2026-03-20
**Status**: FINAL - CLAUDE LINE CLOSED

---

## FINAL STATUS: CLAUDE LINE CLOSED

---

## KNOWN LIMITS - CLAUDE METHOD A

### ✅ VERIFIED (Native Auto-Trigger)

| Capability | Status | Evidence |
|------------|--------|----------|
| Official settings hooks path | ✅ Verified | settings_hooks_config.md |
| SessionStart hook | ✅ Verified | hooks_trigger_log.md |
| SessionEnd hook | ✅ Verified | hooks_trigger_log.md |
| Auto recall | ✅ Verified | SQLite events |
| Auto remember | ✅ Verified | SQLite events |
| Background collection | ✅ Verified | Events stored |

### ❌ NOT VERIFIED (Native Context Injection)

| Capability | Status | Reason |
|------------|--------|--------|
| Native context injection | ❌ FAIL | Hooks are side processes |
| Hook outputs in Claude context | ❌ FAIL | Claude doesn't read hook outputs |
| Seamless auto-recall | ❌ FAIL | Results don't affect response |

---

## KNOWN LIMITS - CLAUDE METHOD B

### ✅ VERIFIED

| Capability | Status | Evidence |
|------------|--------|----------|
| System-prompt injection | ✅ Verified | Run 019 |
| Auto-memory instructions | ✅ Verified | Run 019 |
| Context-aware recall | ✅ Verified | Claude uses recalled info |

---

## KNOWN LIMITS - PRODUCTION PATH

### Recommended: A + B Combination

| Component | Method | Limitation |
|-----------|--------|------------|
| Background collection | A | Claude doesn't use outputs |
| Context-aware recall | B | Requires system-prompt |

**Note**: Neither method alone is sufficient. Method A provides auto-storage, Method B provides seamless recall.

---

## TERMINOLOGY CLARIFICATION

### What "Claude Method A" CAN mean:
- ✅ Native auto-trigger (hooks call tools without user input)
- ✅ Background auto-memory (automatic memory collection)

### What "Claude Method A" CANNOT mean (without qualification):
- ❌ "Fully native auto-memory" (context injection doesn't work)
- ❌ "Seamless auto-recall" (requires Method B)

### Required Qualification:
When referring to Claude Method A, ALWAYS specify:
- "native auto-trigger" vs "native context injection"
- "background collection" vs "context injection"

---

## SUMMARY

| Method | Native Auto-Trigger | Native Context Injection | System-Prompt |
|--------|-------------------|------------------------|---------------|
| **A** | ✅ VERIFIED | ❌ NOT VERIFIED | N/A |
| **B** | N/A | N/A | ✅ VERIFIED |
| **A+B** | ✅ | ✅ | ✅ |

---

**Claude line is CLOSED. These limits are final.**
