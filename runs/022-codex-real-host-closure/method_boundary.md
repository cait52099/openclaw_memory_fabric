# OCMF Codex Method Boundaries - Final Definition

**Run ID**: 022-codex-real-host-closure
**Date**: 2026-03-20
**Status**: FINAL - TERMINOLOGY CLOSED

---

## PURPOSE

This document establishes definitive, unambiguous terminology for Codex native automation methods. These terms are binding for the OCMF project.

---

## METHOD DEFINITIONS (FINAL)

### Method A: Native Auto-Trigger

| Property | Definition |
|----------|------------|
| **Name** | Native auto-trigger |
| **Mechanism** | Codex internal hooks / event-based triggers |
| **Trigger** | Automatic (SessionStart, SessionEnd, etc.) |
| **User Input Required** | ❌ NO |
| **Codex Uses Results** | ❌ NO (if existed, would be side process) |
| **Memory Storage** | ✅ YES (if existed) |
| **Codex Status** | ❌ NOT AVAILABLE |

**Codex has NO native hooks or auto-trigger mechanism.**

### Method B: System-Prompt Assisted

| Property | Definition |
|----------|------------|
| **Name** | System-prompt assisted |
| **Mechanism** | Instructions injected via system prompt |
| **Trigger** | Codex follows injected instructions |
| **User Input Required** | ❌ NO (once configured) |
| **Codex Uses Results** | ✅ YES |
| **Codex Status** | ⚠️ UNTESTED |

**Codex Method B = NOT TESTED in this run.**

### Method C: Manual MCP

| Property | Definition |
|----------|------------|
| **Name** | Manual MCP |
| **Mechanism** | Codex explicitly calls ocmf_* tools via MCP |
| **Trigger** | User/agent explicitly calls tools |
| **User Input Required** | ✅ YES |
| **Codex Uses Results** | ✅ YES |
| **Codex Status** | ✅ VERIFIED |

---

## CODEX METHOD A - NOT AVAILABLE

Unlike Claude (which has settings-based hooks), Codex has NO native event hooks.

| Capability | Claude | Codex |
|-----------|--------|-------|
| SessionStart hook | ✅ | ❌ |
| SessionEnd hook | ✅ | ❌ |
| PreToolUse hook | ✅ | ❌ |
| PostToolUse hook | ✅ | ❌ |
| Native auto-trigger | ✅ | ❌ |

---

## TERMINOLOGY RULES (BINDING)

### ❌ PROHIBITED SHORTHAND

- ❌ "Codex Method A" alone is ambiguous - Codex has NO Method A
- ❌ "Codex native auto-memory" - Codex has no native automation
- ❌ "Codex auto-trigger" - Not available

### ✅ REQUIRED QUALIFICATION

| If you mean... | Use this term... |
|----------------|-----------------|
| Codex calls OCMF tools manually | "Codex Method C - Manual MCP" |
| (Not applicable) | "Codex Method A" = DOES NOT EXIST |
| (Not applicable) | "Codex Method B" = NOT TESTED |

---

## FINAL VERDICT

| Term | Definition | Codex Status |
|------|------------|--------------|
| **Native auto-trigger (A)** | Codex hooks call tools automatically | ❌ NOT AVAILABLE |
| **System-prompt assisted (B)** | Codex follows injected instructions | ⚠️ NOT TESTED |
| **Manual MCP (C)** | Codex calls tools via MCP | ✅ VERIFIED |
| **Recommended path** | **Method C** | ✅ VERIFIED |

---

**This terminology is FINAL and binding.**
