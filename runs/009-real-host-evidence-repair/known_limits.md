# OCMF Phase 4F Known Limits - Real Host vs Synthetic

**Run ID**: 009-real-host-evidence-repair
**Date**: 2026-03-12

---

## 验证类型定义（严格版）

### 三种验证类型

| 类型 | 定义 | 例子 |
|------|------|------|
| **Real Host Validation** | 通过真实二进制进程自动触发 OCMF | Claude Code 进程自动 recall |
| **Manual Adapter Invocation** | 直接调用 adapter 函数 | `adapter.before_response(query, ctx)` |
| **Synthetic Test** | pytest 自动执行 | `pytest tests/` |

### 本轮验证结果

| 类型 | Claude | Codex | OpenClaw |
|------|--------|-------|----------|
| Real Host Validation | ❌ 需要实现 MCP | ❌ 未安装 | ❌ 未安装 |
| Manual Adapter Invocation | ✅ 可用 | ❌ 未安装 | ❌ 未安装 |
| Synthetic Test | ✅ 45/45 | ⚠️ Mock | ⚠️ Mock |

---

## Binary 验证结果

### Claude Code

```
$ which claude
/Users/caihongwei/.local/bin/claude

$ claude --version
2.1.72 (Claude Code)
```

**状态**: ✅ BINARY_AVAILABLE

**集成机制**:
- `--mcp-config`: 加载 MCP 服务器
- `--plugin-dir`: 加载插件目录

**注意**: 需要实现 MCP 服务器才能实现 Real Host Validation

### Codex CLI

```
$ which codex
codex not found
```

**状态**: ❌ NOT_FOUND

### OpenClaw

```
$ which openclaw
openclaw not found
```

**状态**: ❌ NOT_FOUND

---

## Real Host 验证阻塞原因

### Claude Code - 需要新开发

**问题**: Claude Code 提供 MCP 机制，但需要实现 MCP 服务器

**影响**: 实现 MCP 服务器 = 新功能开发，超出验证范围

**需要**:
1. 实现符合 MCP 协议的服务器
2. 实现 recall/remember 工具
3. 配置 `--mcp-config`

**评估**: 这不是"验证"而是"开发新功能"

### Codex CLI - 环境阻塞

**问题**: Codex CLI 未安装

**状态**: 环境阻塞 ≠ 代码问题

### OpenClaw - 环境阻塞

**问题**: OpenClaw 未安装

**状态**: 环境阻塞 ≠ 代码问题

---

## Synthetic Test 状态

所有合成测试通过 (45/45):

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

## 本轮验收状态

| 验收项 | 状态 | 说明 |
|--------|------|------|
| Claude binary 验证 | ✅ 完成 | v2.1.72 |
| Codex binary 验证 | ❌ 阻塞 | 未安装 |
| OpenClaw binary 验证 | ❌ 阻塞 | 未安装 |
| Real Host write/recall | ❌ 阻塞 | 需要实现 MCP |
| Manual adapter invocation | ⚠️ 可用 | 不等于 Real Host |
| Cross-tool isolation | ⚠️ Synthetic | 45/45 测试通过 |
| evidence.md | ✅ 完成 | 完整记录 |
| known_limits.md | ✅ 完成 | 区分三种类型 |

---

## 区分: Real Host vs Manual vs Synthetic

### Real Host Validation (本轮无法完成)

- 需要真实二进制进程自动触发
- Claude Code 需要 MCP 服务器实现
- Codex CLI 未安装
- OpenClaw 未安装

### Manual Adapter Invocation (Claude 可用)

- 直接调用 adapter 函数
- 使用真实环境变量
- 手动设置上下文
- 不等于 Real Host Validation

### Synthetic Test (完整通过)

- pytest 自动执行
- 45/45 全部通过

---

## 后续建议

### Claude Code 集成

若要实现真正的 Real Host Validation，需要:
1. 实现 MCP 服务器 (新功能开发)
2. 或修改 Claude Code 源码 (非官方)

### Codex CLI

安装后重新验证

### OpenClaw

安装后重新验证

---

## 结论

**本轮结论**:
- Real Host Validation: ❌ 需要新开发 (Claude MCP)
- Manual Adapter Invocation: ⚠️ 可用但不等于是 Real Host
- Synthetic Test: ✅ 45/45 全部通过

**区分明确**:
- Real Host 需要进程自动触发
- Manual 是直接调用 adapter
- Synthetic 是 pytest

---

**Last Updated**: 2026-03-12
