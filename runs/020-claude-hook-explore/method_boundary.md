# OCMF Claude Method Boundaries - Final Definition

**Run ID**: 020-claude-hook-explore
**Date**: 2026-03-20
**Status**: FINAL - TERMINOLOGY CLOSED

---

## PURPOSE

This document establishes definitive, unambiguous terminology for Claude native automation methods. These terms are binding for the OCMF project.

---

## METHOD DEFINITIONS (FINAL)

### Method A: Native Auto-Trigger

| Property | Definition |
|----------|------------|
| **Name** | Native auto-trigger |
| **Mechanism** | Claude settings-based hooks |
| **Trigger** | Automatic (SessionStart, SessionEnd, etc.) |
| **User Input Required** | ❌ NO |
| **Claude Uses Results** | ❌ NO (side process) |
| **Memory Storage** | ✅ YES |
| **Claude Status** | ✅ VERIFIED |

### Method B: System-Prompt Assisted

| Property | Definition |
|----------|------------|
| **Name** | System-prompt assisted |
| **Mechanism** | --system-prompt with instructions |
| **Trigger** | Claude follows injected instructions |
| **User Input Required** | ❌ NO (once configured) |
| **Claude Uses Results** | ✅ YES |
| **Memory Storage** | ⚠️ Depends on Claude compliance |
| **Claude Status** | ✅ VERIFIED |

### Method C: Manual MCP

| Property | Definition |
|----------|------------|
| **Name** | Manual MCP |
| **Mechanism** | User types ocmf_* commands |
| **Trigger** | User explicitly calls tools |
| **User Input Required** | ✅ YES |
| **Claude Uses Results** | ✅ YES |
| **Claude Status** | ✅ VERIFIED |

---

## CLAUDE METHOD A - SUBTYPES

### A1: Native Auto-Trigger (Background Collection)

| Property | Value |
|----------|-------|
| **Name** | A1 - Native auto-trigger |
| **Claude Support** | ✅ VERIFIED |
| **Context Injection** | ❌ NO |
| **Use Case** | Background memory collection |

### A2: Native Context Injection

| Property | Value |
|----------|-------|
| **Name** | A2 - Native context injection |
| **Claude Support** | ❌ NOT VERIFIED |
| **Context Injection** | N/A |
| **Use Case** | N/A |

**A2 is NOT SUPPORTED in Claude 2.1.78**

---

## COMBINATION PATHS

### A + B (Recommended)

| Component | Method | Claude Support |
|-----------|--------|----------------|
| Background collection | A1 | ✅ VERIFIED |
| Context injection | B | ✅ VERIFIED |
| **Combined** | **A1 + B** | **✅ RECOMMENDED** |

### Pure A

| Component | Method | Claude Support |
|-----------|--------|----------------|
| Background collection | A1 | ✅ VERIFIED |
| Context injection | A2 | ❌ NOT VERIFIED |
| **Pure A** | **FAIL** | ❌ |

---

## TERMINOLOGY RULES (BINDING)

### ❌ PROHIBITED SHORTHAND

- ❌ "Claude Method A" alone is ambiguous - must specify A1 or A2
- ❌ "Native auto-memory" alone is ambiguous - must specify auto-trigger vs context injection
- ❌ "Method A works" without qualification

### ✅ REQUIRED QUALIFICATION

When discussing Claude Method A, you MUST specify:

| If you mean... | Use this term... |
|----------------|-----------------|
| Hooks auto-call tools | "Method A1 - native auto-trigger" |
| Hook outputs affect Claude context | "Method A2 - native context injection" (NOT SUPPORTED) |
| Both components together | "Method A1 + A2" (A2 not supported) |
| Background collection + context | "Method A + B" |

---

## FINAL VERDICT

| Term | Definition | Claude Status |
|------|------------|--------------|
| **Native auto-trigger (A1)** | Hooks call tools automatically | ✅ VERIFIED |
| **Native context injection (A2)** | Hook outputs affect context | ❌ NOT SUPPORTED |
| **System-prompt assisted (B)** | Claude follows instructions | ✅ VERIFIED |
| **Manual MCP (C)** | User calls tools | ✅ VERIFIED |
| **Recommended path** | **A1 + B** | ✅ VERIFIED |

---

## PRODUCTION RECOMMENDATION

| Phase | Method | Purpose |
|-------|--------|---------|
| Memory collection | A1 | Automatic background capture |
| Memory recall | B | Claude uses memories |

**Neither Pure A nor Pure B is sufficient** - A1+B is required for full functionality.

---

**This terminology is FINAL and binding.**
