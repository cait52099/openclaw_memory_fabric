# Changelog - OpenClaw Memory Fabric (OCMF)

All notable changes to this project are documented in this file.

---

## [0.1.0] - 2026-03-22 (Current Version)

### Development Status
**Alpha** - Not formally released to package indexes

### Phase Summary

| Phase | Description | Status |
|-------|-------------|--------|
| 001-034 | Early development | Internal |
| 035-050 | Trusted User Journey verification | ✓ PASS |
| 051 | Bootstrap wrapper (remove PYTHONPATH friction) | ✓ PASS |
| 052 | Global install (`pip install -e .` + entry point) | ✓ PASS |
| 053 | Shell/PATH polish (new shell validation) | ✓ PASS |
| 054 | Quickstart final polish | ✓ PASS |
| 055 | Release/distribution documentation alignment | ✓ PASS |
| 056 | Formal release readiness | Current |

### Completed Features

#### Core Memory Protocol
- [x] Unified Memory Event Envelope
- [x] Raw append-only event store
- [x] Memory Object aggregation layer
- [x] Entity/Topic/Version/Link models
- [x] Scope isolation (user/workspace/project/session)

#### Core APIs
- [x] `remember(event)` - Store memories
- [x] `recall(query, context)` - Retrieve memories
- [x] `explain(memory_id)` - Memory provenance
- [x] `status` - Show memory count
- [x] `doctor` - Setup verification

#### Host Integration
- [x] Claude integration (Method A1 + B)
- [x] Codex integration (Method C)
- [x] Cross-host memory sharing
- [x] Source attribution (Claude/Codex)

#### Installation & UX
- [x] Development install: `python3 -m pip install -e .`
- [x] Global `ocmaf` command
- [x] Auto-config sourcing
- [x] Quickstart documentation
- [x] Trusted user journey verified

### Known Limitations

| Issue | Status | Notes |
|-------|--------|-------|
| Identity drift root cause | Not identified | Never reproduced in testing |
| OpenClaw support | Blocked | GitHub release unavailable |
| PyPI formal release | Not published | Development install only |
| Semantic conflict detection | Not implemented | Would need embeddings |
| Auto-memory on Codex | Not supported | Manual recall/remember only |

### Friction Points (Not Blockers)

| Issue | Workaround |
|-------|------------|
| Claude restart required after install | Restart Claude after `ocmaf install` |
| Config overwrites on host switch | Re-run `ocmaf install --host ...` |
| Codex no auto-memory | Use `ocmaf remember/recall` manually |

---

## [Unreleased] - Future Plans

### Planned Features
- [ ] PyPI formal release
- [ ] Semantic conflict detection
- [ ] OpenClaw integration (blocked on GitHub release)
- [ ] Vector search option
- [ ] Replay/backtest tools
- [ ] Web UI

### Requirements for Formal Release
- [ ] README.md at project root
- [ ] CHANGELOG.md (this file)
- [ ] Automated tests
- [ ] Release workflow
- [ ] Version tagging

---

## Phase Details

### Phase 035-050: Trusted User Journey
- Claude clean-home verification
- Codex clean-home verification
- Host switching verification
- Determinism verification
- **Result**: Trusted user journey confirmed

### Phase 051: Bootstrap Wrapper
- Created `ocmaf` bootstrap wrapper
- Removed need for manual `PYTHONPATH=src`
- **Result**: PYTHONPATH friction eliminated

### Phase 052: Global Install
- Fixed `pyproject.toml` entry point
- Added `_auto_source_config()` function
- Enabled `pip install -e .` + global `ocmaf` command
- **Result**: Development install fully working

### Phase 053: Shell/PATH Polish
- New shell session validation
- Quickstart alignment
- Doc hygiene fixes
- **Result**: Shell integration polished

### Phase 054: Quickstart Polish
- Unified install command: `python3 -m pip install -e .`
- Python-direct path moved to Troubleshooting/Advanced
- Main quickstart: 3 steps (Install → First Use → Daily Usage)
- **Result**: Quickstart finalized

### Phase 055: Release/Distribution Polish
- Updated docs/plan.md to remove old install patterns
- Marked PYTHONPATH/source config friction as resolved
- Clarified release status (not yet formally released)
- **Result**: Documentation aligned

### Phase 056: Formal Release Readiness (Current)
- README.md at project root
- CHANGELOG.md at project root
- Release checklist
- Non-publish release rehearsal
- **Goal**: Prepare for eventual formal release

---

## Version History

| Version | Date | Status |
|---------|------|--------|
| 0.1.0 | 2026-03-22 | Current (Alpha, not formally released) |

---

## Migration Notes

### For Users (v0.1.0)

**Current install method:**
```bash
python3 -m pip install -e /path/to/openclaw_memory_fabric
ocmaf install --host claude  # or --host codex
```

**NOT YET AVAILABLE:**
```bash
pip install ocmaf  # Not published yet
```

---

## Contact & Support

For issues or questions, see:
- [Documentation](docs/)
- [Quickstart](docs/quickstart.md)
- Phase evidence in `runs/<run_id>/`
