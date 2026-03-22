# OpenClaw Binary Check

**Run ID**: 024-openclaw-closure-crosshost-ux
**Date**: 2026-03-22
**Task**: T-6B-01

---

## Binary Check

### which openclaw

```
$ which openclaw
openclaw not found
EXIT:1
```

**Result**: Not in PATH.

### Application Search

```
$ ls /Applications/*openclaw*
No matches found

$ ls ~/Library/Caches/Homebrew/cask/openclaw*
No cached installer

$ ls /opt/homebrew/Caskroom/openclaw*
No matches found
```

### Homebrew Check

```
$ brew info openclaw
==> openclaw: 2026.3.13 (auto_updates)
https://openclaw.ai/
Not installed
```

**Status**: OpenClaw is available in Homebrew Cask but NOT installed.

### Download Attempt

```
$ brew install --cask openclaw
Error: Download failed on Cask 'openclaw' with message:
Download failed: https://github.com/openclaw/openclaw/releases/download/v2026.3.13/OpenClaw-2026.3.13.dmg
```

### GitHub Release Check

```
$ curl https://api.github.com/repos/openclaw/openclaw/releases/latest
Latest: v2026.3.13-1

$ curl -sL "https://github.com/openclaw/openclaw/releases/download/v2026.3.13-1/OpenClaw-2026.3.13.dmg"
Not Found (404)
```

**Result**: GitHub release assets are missing/broken.

---

## Summary

| Check | Result |
|-------|--------|
| Binary in PATH | ❌ NO |
| OpenClaw.app installed | ❌ NO |
| Homebrew available | ✅ YES |
| Download URL | ❌ BROKEN (404) |
| Install possible | ❌ NO |

---

## AC-OCL-001

- [x] OpenClaw environment checked
- [x] Binary not available
- [x] Download URL broken

**Status**: ❌ BLOCKED - Cannot proceed with real host proof

---

## Blocker Documentation

| Item | Value |
|-------|-------|
| Blocker type | Download URL broken |
| GitHub release | v2026.3.13-1 |
| Expected DMG | OpenClaw-2026.3.13.dmg |
| Actual response | 404 Not Found |
| Resolution needed | OpenClaw team must fix release assets |
