# OCMF Phase 3B.1 审计分歧对齐报告

**Date**: 2026-03-11
**Purpose**: 核对 Speckit 与 Codex 审计结论差异，明确代码事实，为 Phase 3B.1 修正提供依据

---

## 一、审计结论对比

| 维度 | Speckit/Claude Code 结论 | Codex 结论 | 代码事实 |
|------|--------------------------|------------|----------|
| FINAL_STATUS | PASS | 阶段性 PASS | **阶段性 PASS** |
| SECOND_ADAPTER_GATE | GO | NO-GO | **NO-GO** |
| ClaudeCodeAdapter tool 透传 | 已有 | 未显式透传 | **未显式透传** |
| CodexCLIAdapter tool 透传 | ✅ 实现 | ✅ 实现 | **✅ 已实现** |
| Cross-tool 测试 | 有 | 无真正断言 | **无真正断言** |
| verify_smoke 包含 Codex | 已更新 | 未更新 | **未更新** |

---

## 二、代码事实核对

### 2.1 ClaudeCodeAdapter - ❌ 未显式透传 tool

**问题位置**: `src/ocmaf/adapters/claude_code.py:76-82`

```python
# Create memory session
with MemorySession(
    user=scope.get("user", "default"),
    workspace=scope.get("workspace"),
    project=scope.get("project"),
    session=scope.get("session"),
    db_path=self.db_path,
) as session:
```

**问题**: `tool` 参数未传递给 MemorySession！

**对比 CodexCLIAdapter** (`src/ocmaf/adapters/codex_cli.py:72-80`):
```python
with MemorySession(
    user=scope.get("user", "default"),
    workspace=scope.get("workspace"),
    project=scope.get("project"),
    session=scope.get("session"),
    tool=scope.get("tool"),  # ✅ 已传递
    db_path=self.db_path,
) as session:
```

### 2.2 Cross-tool 测试 - ❌ 无真正断言

**问题位置**: `tests/test_codex_adapter.py:49-73`

```python
def test_cross_tool_isolation():
    """Verify cross-tool isolation works with Codex CLI."""
    adapter = CodexCLIAdapter()

    # Write with tool='codex-cli'
    event_id = adapter.after_response(
        "Remember this: Python preference",
        "Sure, I'll remember Python preference",
        {"user": "test", "project": "test_proj"}
    )
    assert event_id, "Should create event"

    # Try to recall with tool='claude-code'
    cc_adapter = ClaudeCodeAdapter()
    cc_result = cc_adapter.before_response(
        "Python preference",
        {"user": "test", "project": "test_proj"}
    )

    # Since different tool, should find nothing or different result
    # This validates tool isolation works
    # ⚠️ 没有 assert！测试没有验证任何东西！
```

### 2.3 verify_smoke.sh - ❌ 未包含 Codex

**问题位置**: `ops/verify_smoke.sh`

```bash
# grep -i codex 结果: 无匹配
```

verify_smoke.sh 未包含：
- Codex CLI adapter 测试
- Cross-tool integration 测试

---

## 三、冲突点清单

| # | 冲突点 | Speckit 声称 | Codex 判定 | 代码事实 |
|---|--------|-------------|------------|----------|
| 1 | ClaudeCodeAdapter tool 透传 | 已实现 | 未显式透传 | ❌ 未传递到 MemorySession |
| 2 | Cross-tool 测试 | 有 | 无真正断言 | ❌ 无 assert |
| 3 | verify_smoke Codex | 已更新 | 未更新 | ❌ 无 codex 测试 |
| 4 | 双适配器阶段 | 已进入 | 未进入 | **未进入** |
| 5 | OpenClaw 启动 | 可开始 | 不应开始 | **不应开始** |

---

## 四、Phase 3B.1 目标与边界

### 4.1 唯一目标

修复两个硬阻塞，使双适配器达到合格标准：

1. **ClaudeCodeAdapter 显式透传 tool='claude-code'**
   - 修复位置: `src/ocmaf/adapters/claude_code.py`
   - 在 before_response 和 after_response 中添加 `tool=scope.get("tool")` 到 MemorySession

2. **真正可验证的 Cross-tool Integration + verify 纳入**
   - 修复测试断言: `tests/test_codex_adapter.py::test_cross_tool_isolation`
   - 更新 verify_smoke.sh: 添加 Codex adapter 测试

### 4.2 边界声明

**本轮只修**:
- ✅ ClaudeCodeAdapter tool 透传
- ✅ Cross-tool 测试断言
- ✅ verify_smoke 纳入

**本轮禁止**:
- ❌ OpenClaw adapter
- ❌ Web UI proxy
- ❌ replay/eval
- ❌ 向量搜索
- ❌ 冲突检测增强

---

## 五、当前项目状态正式判定

```
FINAL_STATUS: 阶段性 PASS
SECOND_ADAPTER_GATE: NO-GO
PHASE_STATUS: Phase 3B 完成，但需 Phase 3B.1 修正
```

**原因**:
1. ClaudeCodeAdapter 未显式透传 tool，导致跨工具隔离在真实场景下可能失效
2. Cross-tool 测试无真正断言，无法验证隔离正确性
3. verify_smoke.sh 未纳入 Codex adapter 测试

---

## 六、启动 OpenClaw adapter 前必须满足的最小条件

| 条件 | 验收方式 | 状态 |
|------|----------|------|
| ClaudeCodeAdapter 显式透传 tool | 代码审查 | ❌ 待修复 |
| Cross-tool 测试有真正断言 | 测试审查 | ❌ 待修复 |
| verify_smoke 包含 Codex | 执行验证 | ❌ 待修复 |
| 双向 cross-tool 隔离验证通过 | 集成测试 | ❌ 待修复 |
| P0 regression 不退化 | 测试执行 | ✅ 已通过 |

---

## 七、Phase 3B.1 任务清单

| Task | 内容 | 文件 |
|------|------|------|
| T-3B.1-01 | ClaudeCodeAdapter before_response 添加 tool 透传 | adapters/claude_code.py |
| T-3B.1-02 | ClaudeCodeAdapter after_response 添加 tool 透传 | adapters/claude_code.py |
| T-3B.1-03 | Cross-tool 测试添加真正断言 | tests/test_codex_adapter.py |
| T-3B.1-04 | verify_smoke.sh 添加 Codex 测试 | ops/verify_smoke.sh |
| T-3B.1-05 | 双向 cross-tool 隔离验证 | tests/test_*.py |
| T-3B.1-06 | 更新 evidence.md | runs/004-codex-fix/evidence.md |

---

## 八、结论

**当前状态**: 尚未进入"合格的双适配器阶段"

**下一步**: Phase 3B.1 修正包（仅修复上述两个硬阻塞）

**OpenClaw adapter 启动条件**: Phase 3B.1 完成后重新评估

---

## 九、Phase 3B.1a Test Hermetic Fix 分析

**Run ID**: 005-test-hermetic-fix
**Date**: 2026-03-11
**Phase**: 3B.1a - Test Infrastructure Correction

### 9.1 背景

Phase 3B.1 功能修复已完成，但 Codex 审核发现测试基础设施存在不可忽视的问题：

1. **test_codex_adapter.py 非 hermetic** - 写入默认数据库 ~/.ocmaf/memory.db
2. **verify_smoke.sh 在干净环境可能失败** - 依赖已有数据
3. **evidence.md 略有夸大** - 声称 7/7 但未验证隔离性

### 9.2 代码事实

**默认数据库状态**:
```bash
$ ls -la ~/.ocmaf/memory.db
-rw-r--r--  1 caihongwei  staff  102400  Mar 11 20:40 memory.db

$ sqlite3 ~/.ocmaf/memory.db "SELECT COUNT(*) FROM events;"
24
```

**test_codex_adapter.py 问题**:
```python
# 第 20 行 - 未提供 db_path
adapter = CodexCLIAdapter()  # 使用默认 ~/.ocmaf/memory.db
```

### 9.3 判定

| 维度 | 状态 | 说明 |
|------|------|------|
| 功能正确性 | ✅ PASS | ClaudeCodeAdapter 已正确透传 tool |
| 跨工具隔离 | ✅ PASS | cross-tool 测试已验证 |
| 测试 hermetic | ❌ FAIL | test_codex_adapter.py 写入默认数据库 |
| verify 可重现 | ⚠️ UNCLEAN | 依赖已有数据 |
| OPENCLAW_GATE | ❌ NO-GO | 测试基础设施不合格 |

### 9.4 Phase 3B.1a 唯一目标

**必须修复**:
- [ ] T-3B1a-01: test_codex_adapter.py 改为 tempfile（与 test_cross_tool_integration.py 一致）
- [ ] T-3B1a-02: 运行 verify_smoke.sh 确认全绿
- [ ] T-3B1a-03: 更新 evidence.md 准确反映 hermetic 状态

**禁止改变**:
- ❌ 不修功能代码
- ❌ 不新增 adapter
- ❌ 不改接口
- ❌ 不动 test_cross_tool_integration.py（已 hermetic）

### 9.5 GO 判定

**当前**: NO-GO ❌

**达到 GO 条件**:
1. test_codex_adapter.py 使用 tempfile
2. 所有测试可独立运行
3. verify_smoke.sh 在干净环境可全绿
4. evidence 准确反映测试属性

---

**Analysis Updated**: 2026-03-11
**Status**: Ready for Phase 3B1a Implementation
