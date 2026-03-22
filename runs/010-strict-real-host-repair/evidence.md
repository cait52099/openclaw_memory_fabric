# OCMF Phase 4F Strict Real Host Evidence

**Run ID**: 010-strict-real-host-repair
**Date**: 2026-03-12
**Phase**: 4F - Strict Real Host Evidence Repair

---

## Executive Summary

Phase 4F 执行严格证据修复，明确区分三种验证类型。

**关键发现**:
- Claude Code binary: ✅ 存在 (v2.1.72)
- Claude Code Real Host: ❌ 需要 MCP 服务器实现
- Codex CLI: ❌ 未安装
- OpenClaw: ❌ 未安装
- Cross-tool: ❌ 两工具均阻塞

---

## 1. Binary Verification Results

### Claude Code

```
$ which claude
/Users/caihongwei/.local/bin/claude
EXIT_CODE: 0

$ claude --version
2.1.72 (Claude Code)
EXIT_CODE: 0
```

**Status**: ✅ BINARY_AVAILABLE

### Codex CLI

```
$ which codex
codex not found
EXIT_CODE: 1
```

**Status**: ❌ NOT_FOUND

### OpenClaw

```
$ which openclaw
openclaw not found
EXIT_CODE: 1
```

**Status**: ❌ NOT_FOUND

---

## 2. Three-Way Strict Validation Type Distinction

### Real Host Validation

| Tool | Status | Reason |
|------|--------|--------|
| Claude Code | ❌ BLOCKED | 需要 MCP 服务器实现 (新功能开发) |
| Codex CLI | ❌ BLOCKED | 未安装 |
| OpenClaw | ❌ BLOCKED | 未安装 |

**定义**: 通过真实二进制进程自动触发 OCMF

**当前状态**: ❌ 所有工具均阻塞

---

### Manual Adapter Invocation

| Tool | Status | Note |
|------|--------|------|
| Claude Code | ✅ AVAILABLE | 不等于 Real Host |
| Codex CLI | ❌ NOT_AVAILABLE | 未安装 |
| OpenClaw | ❌ NOT_AVAILABLE | 未安装 |

**定义**: 直接调用 adapter 函数

**当前状态**: ⚠️ 仅 Claude Code 可用

---

### Synthetic Test

| Tool | Status | Note |
|------|--------|------|
| Claude Code | ✅ 45/45 PASS | 不等于 Real Host |
| Codex CLI | ⚠️ 7/7 Mock | 不等于 Real Host |
| OpenClaw | ⚠️ 6/6 Mock | 不等于 Real Host |

**定义**: pytest 自动执行

**当前状态**: ✅ 45/45 通过

---

## 3. Claude Real Host Analysis

### Binary Status

- **Binary**: ✅ /Users/caihongwei/.local/bin/claude
- **Version**: 2.1.72 (Claude Code)

### MCP Mechanism

```
$ claude --help 2>&1 | grep -i mcp
      --mcp-config PATH    Path to MCP configuration file
```

**Problem**: 需要实现 MCP 服务器才能触发 OCMF

**Assessment**: 实现 MCP 服务器 = 新功能开发，超出验证范围

### Real Host Write/Recall Attempt

**Status**: ❌ CANNOT COMPLETE - BLOCKED

**Reason**:
1. Claude Code 没有自动触发 OCMF 的 hook 系统
2. 需要实现 MCP 服务器（新功能开发）
3. 用户在 Claude Code 中输入内容时不会自动调用外部程序

---

## 4. Codex Real Host Analysis

### Binary Status

- **Binary**: ❌ NOT_FOUND
- **Installation**: ❌ NOT_INSTALLED

### Real Host Write/Recall Attempt

**Status**: ❌ CANNOT COMPLETE - BLOCKED

**Reason**: Codex CLI 未安装

---

## 5. OpenClaw Status

### Binary Status

- **Binary**: ❌ NOT_FOUND
- **Installation**: ❌ NOT_INSTALLED

**Status**: ❌ BLOCKED (Not Installed)

---

## 6. Cross-Tool Analysis

### Real Host Cross-Tool

**Status**: ❌ BLOCKED

**Reason**:
1. Claude Code: 需要 MCP 服务器实现
2. Codex CLI: 未安装
3. 两工具均无法完成 real host validation

### Synthetic Cross-Tool

**Status**: ✅ 4/4 PASS

---

## 7. Synthetic Test Results

```bash
$ python3 -m pytest tests/ -v
============================== 45 passed in 0.20s ==============================
```

| Test Suite | Tests | Passed |
|-----------|-------|--------|
| P0 Regression | 16 | 16/16 |
| Adapter Smoke | 6 | 6/6 |
| Codex Adapter | 7 | 7/7 |
| Cross-Tool | 4 | 4/4 |
| OpenClaw Adapter | 6 | 6/6 |
| Tri-Tool Integration | 9 | 9/9 |
| Fallback / E2E | 3 | 3/3 |

---

## FINAL STATUS

### REAL_HOST_STATUS: ❌ BLOCKED

| Tool | Binary | Integration Mechanism | Real Host Status |
|------|--------|---------------------|-----------------|
| Claude Code | ✅ v2.1.72 | MCP (需实现服务器) | ❌ 需要新开发 |
| Codex CLI | ❌ Not Found | N/A | ❌ BLOCKED |
| OpenClaw | ❌ Not Found | N/A | ❌ BLOCKED |

### CLAUDE_REAL_HOST: ❌ BLOCKED

- Binary exists: ✅
- MCP support: ✅ (--mcp-config flag available)
- Real host integration: ❌ Requires MCP server implementation

### CODEX_REAL_HOST: ❌ BLOCKED (Not Installed)

- Binary exists: ❌
- Real host integration: ❌

### OPENCLAW_ENV_STATUS: ❌ BLOCKED (Not Installed)

- Binary exists: ❌
- Real host integration: ❌

### SYNTHETIC_TEST_STATUS: ✅ PASS (45/45)

---

## FINAL_STATUS: ⚠️ REAL_HOST_BLOCKED

**原因**:
1. Claude Code: 需要实现 MCP 服务器 (超出范围)
2. Codex CLI: 未安装
3. OpenClaw: 未安装
4. Synthetic tests: 全部通过 ✅

**严格区分**:
- Real Host: ❌ 所有工具均阻塞
- Manual Adapter: ⚠️ 仅 Claude 可用
- Synthetic Test: ✅ 45/45 通过

---

## Evidence Files Reference

- binary_check.md: 原始 binary 探测结果
- claude_strict_real_host.md: Claude 严格证据
- codex_strict_real_host.md: Codex 和 OpenClaw 严格证据
- cross_tool_strict.md: Cross-tool 严格证据
- known_limits.md: 已知限制文档

---

**Evidence Generated**: 2026-03-12
**Status**: Phase 4F Complete - Real Host BLOCKED
