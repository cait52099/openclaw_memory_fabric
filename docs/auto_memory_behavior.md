# OCMF Auto-Memory Behavior Specification

**Run ID**: 029-unified-entry
**Date**: 2026-03-22
**Status**: Implemented
**Task Type**: PRODUCT DESIGN

---

## Overview

Auto-memory is an optional behavior where the OCMF system automatically recalls relevant memories at session start and remembers key events at session end, without requiring the user to manually invoke recall/remember commands.

## Design Goals

1. **Zero-friction memory**: Users don't need to remember to recall/remember
2. **Non-intrusive**: Memory operations happen silently in background
3. **Configurable**: Users can disable or adjust behavior
4. **Transparent**: Users can see what was recalled/remembered

## Auto-Memory Levels

| Level | Session Start | Session End | Description |
|-------|--------------|-------------|-------------|
| 0 | Off | Off | No automatic operations |
| 1 | Recall relevant | Off | Auto-recall at start only |
| 2 | Off | Remember key | Auto-remember at end only |
| 3 | Recall relevant | Remember key | Full auto-memory (recommended) |

## Session Start Auto-Recall

### Trigger Conditions (Level 1, 3)

- Session ID changes (new session detected)
- User has history (previous memories exist)
- OCMF_AUTO_MEMORY=1 or OCMF_AUTO_MEMORY=3

### Recall Query Strategy

1. **Scope-based**: Use current project/user/workspace as context
2. **Recent-first**: Prioritize recently created memories
3. **Keyword extraction**: Extract keywords from session context
4. **Conflict detection**: If conflicts detected, surface warning

### Output Handling

- Results are injected into system context (not displayed to user unless conflicts)
- Conflicts are surfaced as warnings
- Provenance is included but abbreviated

## Session End Auto-Remember

### Trigger Conditions (Level 2, 3)

- Session ending (detected via signal or timeout)
- OCMF_AUTO_MEMORY=2 or OCMF_AUTO_MEMORY=3

### What Gets Remembered

1. **Key decisions**: Extracted from conversation
2. **Facts stated**: User-provided facts about project
3. **Preferences**: Explicitly mentioned preferences
4. **Context summary**: Brief session summary

### Extraction Strategy

- Look for explicit decision markers ("decided to", "choosing", "will use")
- Detect factual statements ("the project uses X", "we agreed on Y")
- Avoid: questions, casual conversation, already remembered content

## Conflict Handling

When auto-recall detects conflicts:

```
⚠️ CONFLICT DETECTED
Memory from different sources disagree on this topic:

[Claude] "We decided to use PostgreSQL"
[Codex]  "SQLite is the database choice"

Review before continuing.
```

## Host Support Matrix

| Host | Auto-Recall | Auto-Remember | Notes |
|------|------------|--------------|-------|
| Claude | ✓ Supported | ✓ Supported | Method A1+B |
| Codex | ✗ Not supported | ✗ Not supported | Method C only |
| OpenClaw | ⚠️ BLOCKED | ⚠️ BLOCKED | GitHub release unavailable |

## Environment Variables

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| OCMF_AUTO_MEMORY | 0, 1, 2, 3 | 0 | Auto-memory level |
| OCMF_RECALL_LIMIT | number | 10 | Max memories to recall |
| OCMF_SESSION_TIMEOUT | seconds | 300 | Idle time before session end |

## Fallback Behavior

If auto-memory fails:

1. **Recall failure**: Log error, continue without memories
2. **Remember failure**: Queue for retry, don't lose data
3. **Conflict detection failure**: Skip conflict check, recall anyway

## User Control

Users can always:

1. Disable auto-memory: `export OCMF_AUTO_MEMORY=0`
2. Manual recall: `ocmaf recall <query>`
3. Manual remember: `ocmaf remember --content "..."`
4. View status: `ocmaf unified status`

## Implementation Notes

- Auto-recall runs asynchronously (doesn't block session start)
- Auto-remember runs on session end signal
- Both operations are best-effort (failures don't block user)
- Evidence is always written to runs/<run_id>/ for audit

## Evidence

This specification is implemented in:

- `src/ocmaf/api/auto_recall.py` - Auto-recall implementation
- `src/ocmaf/api/auto_remember.py` - Auto-remember implementation
- `src/ocmaf/cli/host_detection.py` - Host capability detection
- `src/ocmaf/hosts/claude_setup.sh` - Claude auto-memory enablement

---

**Status**: Implemented as specified
**Next**: User can enable with `export OCMF_AUTO_MEMORY=3`
