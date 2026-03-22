# OCMF Phase 4F Strict Real Host Evidence

**Run ID**: 009-real-host-evidence-repair
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

## Binary Verification Results

### Claude Code

```
$ which claude
/Users/caihongwei/.local/claude
Exit code: 0

$ claude --version
2.1.72 (Claude Code)
Exit code: 0
```

**Status**: ✅ BINARY_AVAILABLE

### Codex CLI

```
$ which codex
codex not found
Exit code: 1
```

**Status**: ❌ NOT_FOUND

### OpenClaw

```
$ which openclaw
openclaw not found
Exit code: 1
```

**Status**: ❌ NOT_FOUND

---

## Three-Way Strict Validation Type Distinction

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
| Codex CLI | ⚠️ Mock Only | 不等于 Real Host |
| OpenClaw | ⚠️ Mock Only | 不等于 Real Host |

**定义**: pytest 自动执行

**当前状态**: ✅ 45/45 通过

---

## Claude Real Host Analysis

### Binary Status

- **Binary**: ✅ /Users/caihongwei/.local/bin/claude
- **Version**: 2.1.72 (Claude Code)

### MCP Mechanism

Claude Code 提供 `--mcp-config` 参数：

```
$ claude --help | grep mcp
      --mcp-config PATH    Path to MCP configuration file
```

**问题**: 需要实现 MCP 服务器才能触发 OCMF

**评估**: 实现 MCP 服务器 = 新功能开发，超出验证范围

### CLAUDE_REAL_HOST: ❌ BLOCKED (Requires MCP Implementation)

- Binary exists: ✅
- MCP support: ✅ (--mcp-config flag available)
- Real host integration: ❌ Requires MCP server implementation

---

## Codex Real Host Analysis

### Binary Status

- **Binary**: ❌ NOT_FOUND
- **Installation**: ❌ NOT_INSTALLED

### CODEX_REAL_HOST: ❌ BLOCKED (Not Installed)

- Binary exists: ❌
- Real host integration: ❌

---

## OpenClaw Real Host Analysis

### Binary Status

- **Binary**: ❌ NOT_FOUND
- **Installation**: ❌ NOT_INSTALLED

### OPENCLAW_REAL_HOST: ❌ BLOCKED (Not Installed)

- Binary exists: ❌
- Real host integration: ❌

---

## Cross-Tool Analysis

### Real Host Cross-Tool

**Status**: ❌ BLOCKED

**原因**:
1. Claude Code: 需要 MCP 服务器实现
2. Codex CLI: 未安装
3. 两工具均无法完成 real host validation

### Synthetic Cross-Tool

**Status**: ✅ 45/45 PASS

**注意**: 这是 SYNTHETIC，不是 REAL HOST

---

## Strict Evidence Summary

### Real Host Validation Evidence

| Requirement | Claude | Codex | OpenClaw |
|-------------|--------|-------|----------|
| Binary exists | ✅ | ❌ | ❌ |
| Integration mechanism | ⚠️ MCP available | ❌ N/A | ❌ N/A |
| Real host trigger | ❌ BLOCKED | ❌ BLOCKED | ❌ BLOCKED |

### Manual Adapter Invocation Evidence

| Requirement | Claude | Codex | OpenClaw |
|-------------|--------|-------|----------|
| Adapter available | ✅ | ❌ | ❌ |
| Can be called | ✅ | ❌ | ❌ |

### Synthetic Test Evidence

| Requirement | Claude | Codex | OpenClaw |
|-------------|--------|-------|----------|
| Tests pass | ✅ 45/45 | ⚠️ Mock | ⚠️ Mock |

---

## REAL_HOST_STATUS: ❌ BLOCKED

| Tool | Binary | Integration Mechanism | Real Host Status |
|------|--------|---------------------|-----------------|
| Claude Code | ✅ v2.1.72 | MCP (需实现服务器) | ❌ 需要新开发 |
| Codex CLI | ❌ Not Found | N/A | ❌ BLOCKED |
| OpenClaw | ❌ Not Found | N/A | ❌ BLOCKED |

---

## CLAUDE_REAL_HOST: ❌ MCP_POTENTIAL_REQUIRES_IMPLEMENTATION

- Binary exists: ✅
- MCP support: ✅ (--mcp-config flag available)
- Real host integration: ❌ Requires MCP server implementation

---

## CODEX_REAL_HOST: ❌ BLOCKED (Not Installed)

- Binary exists: ❌
- Real host integration: ❌

---

## OPENCLAW_REAL_HOST: ❌ BLOCKED (Not Installed)

- Binary exists: ❌
- Real host integration: ❌

---

## SYNTHETIC_TEST_STATUS: ✅ PASS (45/45)

---

## CROSS_TOOL_STATUS: ❌ BLOCKED (Both Tools Blocked)

- Claude: ❌ BLOCKED (MCP required)
- Codex: ❌ BLOCKED (Not installed)
- Cross-tool isolation: ❌ Cannot verify

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
- claude_real_host_status.md: Claude real host 状态分析
- claude_strict_real_host.md: Claude 严格证据
- codex_strict_real_host.md: Codex 和 OpenClaw 严格证据
- cross_tool_strict.md: Cross-tool 严格证据

---

**Evidence Generated**: 2026-03-12
**Status**: Phase 4F Complete - Real Host BLOCKED
