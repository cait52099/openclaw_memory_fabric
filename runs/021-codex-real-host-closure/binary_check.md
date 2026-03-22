# Codex Binary Check

**Run ID**: 021-codex-real-host-closure
**Date**: 2026-03-20
**Task**: T-5B-01

---

## Binary Check

### which codex

```
$ which codex
codex not found
EXIT:1
```

**Result**: NOT in PATH. Binary exists at full path instead.

### Full Path Check

```
$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.116.0-alpha.1
EXIT:0
```

**Result**: ✅ Binary available at full path.

### Binary Details

```
$ ls -la /Applications/Codex.app/Contents/Resources/codex
-rwxr-xr-x@  1 caihongwei  staff  116908768  3 19 08:46 codex
```

**Size**: ~117 MB

---

## Summary

| Check | Result |
|-------|--------|
| Binary exists | ✅ Yes |
| Full path | `/Applications/Codex.app/Contents/Resources/codex` |
| Version | `codex-cli 0.116.0-alpha.1` |
| In PATH | ❌ No |
| Executable | ✅ Yes |

---

## AC-CDX-001

- [x] Codex binary exists and is executable
- [x] Version confirmed: 0.116.0-alpha.1
- [x] Real host proof: Can be invoked directly

**Status**: ✅ PASS
