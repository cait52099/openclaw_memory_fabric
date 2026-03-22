# Codex Binary Check

**Run ID**: 022-codex-real-host-closure
**Date**: 2026-03-20
**Task**: Real Host Binary Verification

---

## Binary Check

### which codex (PATH)

```
$ which codex
codex not found
EXIT:1
```

**Result**: Not in PATH. Use full path.

### Full Path Check

```
$ /Applications/Codex.app/Contents/Resources/codex --version
codex-cli 0.116.0-alpha.10
EXIT:0
```

### codex exec Works

```
$ /Applications/Codex.app/Contents/Resources/codex exec --skip-git-repo-check --full-auto "echo test"
OpenAI Codex v0.116.0-alpha.10 (research preview)
model: gpt-5.4
provider: openai
...
```

---

## Summary

| Check | Result |
|-------|--------|
| Binary exists | ✅ Yes |
| Full path | `/Applications/Codex.app/Contents/Resources/codex` |
| Version | `codex-cli 0.116.0-alpha.10` |
| In PATH | ❌ No |
| Executable | ✅ Yes |
| `codex exec` works | ✅ Yes |

---

**AC-CDX-001**: ✅ PASS
