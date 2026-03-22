# OCMF Cross-Host UX Specification

**Run ID**: 024-openclaw-closure-crosshost-ux
**Date**: 2026-03-22
**Status**: FINAL
**Task**: T-6C-01

---

## PURPOSE

This document defines the minimum UX specification for cross-host memory scenarios in OCMF. It addresses how memories from different hosts (Claude, Codex, OpenClaw) are displayed when recalled across host boundaries.

---

## 1. PROVENANCE DISPLAY

### Rule: Every recalled memory MUST display its source

When a user calls `ocmf_recall`, every returned memory MUST show:

```json
{
  "memory_id": "uuid-123",
  "content": "Use pytest for testing",
  "source_tool": "claude-code",
  "source_host_friendly": "Claude",
  "event_type": "chat_turn",
  "timestamp": "2026-03-20T10:30:00Z"
}
```

### Friendly Name Mapping

| source_tool | Friendly Name | Description |
|-------------|---------------|-------------|
| claude-code | Claude | Claude Code desktop app |
| codex-cli | Codex | Codex CLI |
| openclaw | OpenClaw | OpenClaw desktop app |
| synthetic | Synthetic | Direct module test (not real host) |

### Display Format

In text output or UI, memories should be grouped or labeled by source:

```
From Claude:
  • "Use pytest for testing" (2026-03-20)

From Codex:
  • "Use pytest for testing" (2026-03-19)
```

---

## 2. CROSS-HOST RECALL SCENARIO

### Scenario: Claude Writes → Codex Recalls

```
User works on OCMF project in Claude:
1. Claude SessionStart hook fires → ocmf_remember session context
2. During session, Claude auto-collects decisions
3. User ends session → SessionEnd hook → more remembers

User switches to Codex:
1. User runs: codex recall "OCMF project constraints"
2. Returns memories from Claude with source_tool='claude-code'
3. Display shows: "From Claude: OCMF constraints..."

What user sees:
─────────────────────────────────────────────
Recall Results for "OCMF project constraints"
─────────────────────────────────────────────

From Claude:
  • "OCMF uses SQLite + FTS5 for storage" (today)
  • "Project constraints: pytest, type hints" (today)

From Codex:
  (no memories from Codex yet)
─────────────────────────────────────────────
```

### Scenario: Cross-Host Conflict

```
Claude remembers: "Testing framework: pytest"
Codex remembers: "Testing framework: unittest"

User calls: ocmf_recall("testing framework")

Display:
─────────────────────────────────────────────
Recall Results for "testing framework"
─────────────────────────────────────────────

⚠️ CONFLICT DETECTED

From Claude:
  • "Testing framework: pytest" (2026-03-20 10:30)

From Codex:
  • "Testing framework: unittest" (2026-03-20 09:15)

Resolution: User chooses which to use
─────────────────────────────────────────────
```

---

## 3. CONFLICT EXPLANATION

### When Conflicts Are Detected

A conflict is detected when:
- Same memory (by content hash) has different values from different sources
- Recall returns multiple candidates with overlapping scope but different content

### Conflict Response Format

```json
{
  "query": "testing framework",
  "conflict_detected": true,
  "candidates": [
    {
      "source_tool": "claude-code",
      "source_host_friendly": "Claude",
      "content": "Testing framework: pytest",
      "timestamp": "2026-03-20T10:30:00Z",
      "memory_id": "uuid-1"
    },
    {
      "source_tool": "codex-cli",
      "source_host_friendly": "Codex",
      "content": "Testing framework: unittest",
      "timestamp": "2026-03-20T09:15:00Z",
      "memory_id": "uuid-2"
    }
  ],
  "resolution_required": true
}
```

### Resolution Options

1. **User picks**: Show both, user decides which to use
2. **Latest wins**: Show newest by timestamp (configurable)
3. **Source priority**: Claude > Codex > OpenClaw (configurable)

---

## 4. RECALL HIT EXPLANATION (explain)

### Rule: explain() MUST return why a memory was recalled

Every `explain(memory_id)` response MUST include:

```json
{
  "memory_id": "uuid-123",
  "recall_query": "OCMF constraints",
  "match_reasons": [
    {
      "type": "keyword",
      "matched": ["OCMF", "constraints"]
    },
    {
      "type": "scope",
      "matched": {"project": "ocmf"}
    }
  ],
  "source_tool": "claude-code",
  "source_host_friendly": "Claude",
  "event_timestamp": "2026-03-20T10:30:00Z",
  "explain": "Matched keywords 'OCMF', 'constraints' and scope project='ocmf'"
}
```

### Cross-Host explain() Additions

When explaining a cross-host recall:

```json
{
  "memory_id": "uuid-123",
  "also_written_by": ["codex-cli"],
  "cross_host_context": "This constraint was also remembered by Codex in session xyz"
}
```

---

## 5. USER EXPERIENCE BY HOST PATH

### Claude (A1 + B - Automatic)

**User Experience**: "Memory just works"

1. User configures once in `~/.claude/settings.json`
2. Claude automatically captures decisions and context
3. Claude uses memories in conversation (via system-prompt)
4. User doesn't need to think about memory

**User-facing description**:
> "OCMF automatically remembers your project context using Claude's hooks. Your constraints, decisions, and patterns are captured without manual effort."

### Codex (C - Manual)

**User Experience**: "Memory as a tool"

1. User explicitly calls `ocmf_remember` after key moments
2. User explicitly calls `ocmf_recall` at session start
3. Memory is intentional and user-driven

**User-facing description**:
> "OCMF provides memory tools you call during your workflow. After key decisions, use `ocmf_remember` to save context, and `ocmf_recall` at session start to retrieve it."

### OpenClaw (TBD - Unknown)

**User Experience**: Unknown until OpenClaw is verified

---

## 6. SOURCE_TOOL FIELD SPECIFICATION

### Database Schema

The `source_tool` field in events table:

```sql
source_tool TEXT NOT NULL  -- 'claude-code', 'codex-cli', 'openclaw', 'synthetic'
```

### Required Invariants

1. **Every event MUST have source_tool** - no exceptions
2. **Real host calls MUST use host identifier** - claude-code, codex-cli, openclaw
3. **Synthetic tests MUST use 'synthetic'** - not fake host names
4. **source_tool is immutable** - once set, cannot be changed

### Display Pipeline

```
events.source_tool
    ↓
Map to friendly name
    ↓
Include in recall output
    ↓
Group by source (optional)
    ↓
Display to user
```

---

## 7. MINIMAL VIABLE CROSS-HOST UX

### Must Have (MVP)

- [x] Recall results show source_tool for each memory
- [x] source_tool maps to friendly name
- [x] Conflict detection when same-entity has different content
- [x] explain() returns why memory was recalled
- [x] Timestamps shown for all memories

### Should Have (v1.1)

- [ ] Group memories by source in recall output
- [ ] "From Claude" / "From Codex" section headers
- [ ] Cross-host context in explain()

### Nice to Have (v2.0)

- [ ] Visual distinction per source (icons, colors)
- [ ] Source priority configuration
- [ ] Auto-merge suggestions for conflicts

---

## 8. SPEC CHAPTER UPDATES

This UX spec should update `docs/spec.md`:

- **FR8** (Retrieval): Add cross-host display rules
- **FR9** (explain): Add provenance and match_reason requirements
- **FR13** (Scope): Add source_tool as a scope dimension

---

## 9. RELATIONSHIP TO HOST PATHS

| Host | Collection Method | Recall Method | User Effort |
|------|-----------------|--------------|-------------|
| Claude | A1 (auto hooks) | B (system-prompt) | Minimal |
| Codex | C (manual) | C (manual) | Intentional |
| OpenClaw | TBD | TBD | Unknown |

The UX spec applies to ALL hosts uniformly for the recall/explain output format.

---

## FINAL OUTPUT

| Metric | Value |
|--------|-------|
| CROSS_HOST_UX_SPEC_READY | ✅ YES (this document) |
| Provenance display | ✅ Specified |
| Conflict explanation | ✅ Specified |
| Recall hit explanation | ✅ Specified |
| User experience by path | ✅ Specified |
| source_tool specification | ✅ Specified |

---

**This spec is FINAL and should be implemented in retrieval module.**
