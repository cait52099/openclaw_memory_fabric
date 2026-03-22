# OCMF Product Strategy - Per-Host Production Paths

**Run ID**: 023-unified-host-matrix
**Date**: 2026-03-22
**Status**: FINAL

---

## PURPOSE

This document defines the official product strategy for OCMF deployment across supported hosts. It answers: which host uses which path, how users experience "auto-memory," and what OCMF's role is in each deployment.

---

## PRODUCT POSITIONING

**OCMF**: A unified memory fabric that provides persistent, retrievable, explainable memory across AI tools.

**Core promise**: "Your AI remembers what you work on, across every tool you use."

**Key differentiator**: Unlike tool-specific memory solutions, OCMF uses a unified event store that works across Claude, Codex, and eventually other hosts.

---

## PER-HOST PRODUCTION PATHS

### Claude: Recommended Path = A1 + B

**Experience**: Users configure once, then memory just works.

#### What happens automatically (A1):
1. User starts Claude session
2. `SessionStart` hook fires → calls `ocmf_remember` with session context
3. During session, hook can auto-collect decisions/constraints
4. User ends session → `SessionEnd` hook fires → final `ocmf_recall` + `ocmf_remember`

#### What happens via system prompt (B):
1. Claude receives system prompt with memory retrieval instructions
2. Claude calls `ocmf_recall` with relevant query
3. Claude reads the recall results and uses them in its responses
4. Memory is seamlessly integrated into the conversation

#### User setup required:
1. Configure `~/.claude/settings.json` with OCMF hooks
2. Add OCMF MCP server to settings
3. That's it — no manual memory calls needed

#### What users say:
> "Claude automatically remembers my project constraints and recalls them when I work on related tasks."

---

### Codex: Recommended Path = C (Manual MCP)

**Experience**: Users explicitly call memory tools, like using a shared notepad.

#### What users do:
1. At session start: `/codex recall <project>` to get context
2. During work: `/codex remember <decision>` after important moments
3. At session end: `/codex remember <summary>` for future sessions

#### User setup required:
1. `codex mcp add ocmf -- ~/bin/ocmaf-codex`
2. Learn the ocmf_remember/ocmf_recall commands
3. Be intentional about calling them

#### What users say:
> "I call `/codex remember` after key decisions, and `/codex recall` when starting new sessions."

#### Future potential:
If Codex Method B (system-prompt) is verified, Codex could gain semi-automatic behavior similar to Claude.

---

### OpenClaw: Status = TBD

**Current status**: Environment blocked, not verified.

**Potential**: If OpenClaw has native hooks, it could become the primary Method A host (like Claude).

**Action needed**: Resolve environment issues to determine path.

---

## UNIFIED STORAGE LAYER

Despite different trigger mechanisms, all hosts write to the same unified storage:

```
┌──────────────────────────────────────────────────────┐
│                  OCMF SQLite                         │
│                                                      │
│  events table:                                       │
│  event_id | source_tool | event_type | payload      │
│  ─────────────────────────────────────────────────  │
│  uuid-1  | claude-code  | chat_turn  | {...}       │
│  uuid-2  | codex-cli    | chat_turn  | {...}       │
│  uuid-3  | openclaw     | decision   | {...}       │
│                                                      │
│  → All hosts share the same memory store            │
│  → Cross-host recall is possible                     │
└──────────────────────────────────────────────────────┘
```

**Benefit**: Memories from Claude are available to Codex, and vice versa.

---

## HOW TO DESCRIBE "AUTO-MEMORY" TO USERS

### For Claude users:
> "OCMF automatically captures your session context using Claude's native hooks. Your constraints, decisions, and patterns are stored without manual effort. When relevant, Claude recalls them in conversation."

### For Codex users:
> "OCMF provides memory tools you can call during your workflow. After key decisions or at session boundaries, use `ocmf_remember` to save context and `ocmf_recall` to retrieve it for future sessions."

### For OpenClaw users (future):
> "OCMF captures your OpenClaw session activity automatically, making your project history and constraints available across all your AI tools."

---

## OCMF'S ROLE PER HOST

| Role | Claude | Codex | OpenClaw |
|------|--------|-------|----------|
| **Trigger mechanism** | Native hooks (A1) | Manual calls (C) | TBD |
| **Memory retrieval** | System-prompt (B) | Manual calls (C) | TBD |
| **Storage engine** | OCMF SQLite | OCMF SQLite | OCMF SQLite |
| **User effort** | Minimal (setup once) | Moderate (explicit calls) | TBD |
| **Automation level** | High | Low | TBD |

---

## USER ONBOARDING FLOWS

### Claude Onboarding (5 minutes)
1. Install OCMF: `pip install ocmaf`
2. Configure hooks: Copy settings.json snippet from docs
3. Configure MCP: Add OCMF to Claude's MCP config
4. Done — memory works automatically

### Codex Onboarding (5 minutes)
1. Install OCMF: `pip install ocmaf`
2. Configure MCP: `codex mcp add ocmf -- ~/bin/ocmaf-codex`
3. Learn the commands: `ocmf_remember`, `ocmf_recall`
4. Be intentional — call tools after key moments

---

## ENGINEERING PRIORITIES

| Priority | Task | Rationale |
|----------|------|----------|
| **P0** | Maintain Claude A1+B stability | Production path confirmed |
| **P0** | Maintain Codex C stability | Production path confirmed |
| **P1** | Test Codex Method B | Could reduce user effort for Codex |
| **P1** | Resolve OpenClaw environment | Unblock third host |
| **P2** | Cross-host memory sharing UX | Key product differentiator |
| **P2** | Replay/eval framework | Validate scoring quality |
| **P3** | Vector search | Performance at scale |

---

## WHAT NOT TO DO

- ❌ Build new host adapters without user demand
- ❌ Claim Method A support for hosts that don't have it
- ❌ Promise "auto-memory" for Codex (it requires manual calls)
- ❌ Expand cross-tool features before both Claude and Codex paths are stable
- ❌ Add vector search before basic retrieval is validated at scale

---

## SUCCESS METRICS

| Host | Metric | Target |
|------|--------|--------|
| Claude | Hook uptime | >99% of sessions |
| Claude | Memory recall hit rate | >80% of relevant queries |
| Codex | Manual recall frequency | User-reported |
| Cross-host | Claude → Codex recall | User-reported |

---

## FINAL OUTPUT

| Metric | Value |
|--------|-------|
| **FINAL_STATUS** | **PASS** |
| **CLAUDE_PRODUCTION_PATH** | **A1 + B** |
| **CODEX_PRODUCTION_PATH** | **C** |
| **OPENCLAW_PRODUCTION_PATH** | **TBD** |
| **UNIFIED_STORAGE** | **YES** (all hosts share SQLite) |
