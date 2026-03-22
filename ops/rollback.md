# OCMF Rollback Guide

**Last Updated**: 2026-03-11
**Version**: 1.0

---

## Overview

This document describes rollback procedures for OCMF (OpenClaw Memory Fabric) including P0 fixes and adapter changes.

---

## Rollback Scenarios

### Scenario 1: Adapter Contract Changes (P0-A)

**Problem**: Adapter contract changes break existing adapters.

**Rollback**:
1. Revert changes to `src/ocmaf/adapters/base.py`
2. Restore previous `AdapterProtocol` definition
3. Run smoke tests: `python3 ops/adapter_test.py`

**Warning**: This may break adapter interoperability.

---

### Scenario 2: Scope Isolation Issues (P0-B)

**Problem**: Scope filtering incorrect, memories leak across projects.

**Rollback**:
1. Revert `src/ocmaf/storage/memory_store.py` query changes
2. Revert `src/ocmaf/storage/event_store.py` query changes
3. Clear database: `rm ~/.ocmaf/memory.db`
4. Re-run tests

---

### Scenario 3: Recall Fallback Issues (P0-C)

**Problem**: Fallback returns wrong memories or doesn't work.

**Rollback**:
1. Revert `src/ocmaf/api/recall.py` fallback logic
2. Clear cache: `rm ~/.ocmaf/memory.db`
3. Run fallback tests: `python3 -c "from tests.test_p0_regression import *; TestP0RecallFallback().test_session_to_project_fallback()"`

---

### Scenario 4: Explain Failures (P0-D)

**Problem**: explain() returns errors or crashes.

**Rollback**:
1. Revert `src/ocmaf/api/recall.py` explain() method
2. Run explain tests: `python3 tests/test_p0_regression.py`

---

### Scenario 5: EventStore Query Issues (P0-E)

**Problem**: Query returns wrong events or fails.

**Rollback**:
1. Revert `src/ocmaf/storage/event_store.py` query method to use LIKE
2. Clear database: `rm ~/.ocmaf/memory.db`
3. Run query tests: `python3 -c "from tests.test_p0_regression import *; TestP0EventStoreQuery().test_query_uses_json_extract()"`

---

## Emergency Rollback

### Full System Rollback

If all else fails:

```bash
# 1. Backup current database
cp ~/.ocmaf/memory.db ~/.ocmaf/memory.db.backup

# 2. Clear database (fresh start)
rm ~/.ocmaf/memory.db

# 3. Re-run smoke tests
python3 ops/adapter_test.py

# 4. If tests fail, restore backup
cp ~/.ocmaf/memory.db.backup ~/.ocmaf/memory.db
```

---

## Database Migration Rollback

If schema changes cause issues:

```bash
# Backup data
sqlite3 ~/.ocmaf/memory.db ".backup memory_backup.db"

# Restore if needed
sqlite3 memory_backup.db ".restore ~/.ocmaf/memory.db"
```

---

## Contact

For issues with rollback, contact the OCMF team.
