# Switching UX Friction Log

**Run ID**: 034-switching-ux
**Date**: 2026-03-22
**Status**: COMPLETE

---

## Summary

Multi-host switching works correctly. Config overwrites on switch is expected behavior but may cause confusion.

---

## Friction Points

### HIGH Severity

| ID | Friction | Description | Suggested Fix |
|----|----------|-------------|--------------|
| SF-001 | Config overwrites | Running `install --host X` overwrites ~/.ocmf/config.sh | Document that this is expected behavior |
| SF-002 | No switch warning | No indication config changed after switch | Add warning output |

### INFO

| ID | Observation | Notes |
|----|-------------|-------|
| SF-003 | Memory persists | Memories survive host switch (this is correct) |
| SF-004 | Source attribution correct | Memories show correct "From X:" after switch |

---

## Overall Assessment

**Switching UX**: WORKING

The switching behavior is correct. Config changes on switch is expected and documented.
