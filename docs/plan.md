# OpenClaw Memory Fabric (OCMF) - 实现方案

**Branch**: `001-memory-fabric-spec` | **Date**: 2026-03-10 | **Spec**: docs/spec.md

**Input**: 基于 docs/constitution.md + docs/spec.md 生成

## Summary

本计划描述 OpenClaw Memory Fabric (OCMF) 的实现方案，采用单机优先架构，通过"多生产者 + 受控提交者 + 可重建底账"模型，实现跨 AI 工具的统一记忆系统。

**核心策略**:
- 协议优先：先定义 Event Envelope 和 API 协议，再实现具体功能
- 事件驱动：所有记忆可追溯到原始事件，支持完整重建
- 分层管理：working/hot/warm/cold/archive 五级分层 + 八种状态
- 低侵入接入：Wrapper / Hook / Proxy 三种接入模式

## Technical Context

| 维度 | 选择 | 说明 |
|------|------|------|
| **Language/Version** | Python 3.11+ | 优先选择，兼容性好 |
| **Primary Dependencies** | sqlite3, fts5, click, pydantic | 轻依赖，避免复杂框架 |
| **Storage** | SQLite + FTS5 | 优先，可插拔向量能力 |
| **Testing** | pytest | 标准 Python 测试框架 |
| **Target Platform** | Mac / Windows / Linux | 跨平台兼容 |
| **Project Type** | library + cli + local-service | 三种形态 |
| **Performance Goals** | recall P50<100ms, write<50ms | 见 spec 非功能需求 |
| **Constraints** | 单机优先，证据驱动 | 符合宪法要求 |
| **Scale/Scope** | 单用户/单机器，10k events | v1 MVP 目标 |

## Constitution Check

### GATE: Must pass before implementation

| 原则 | 检查项 | 状态 |
|------|--------|------|
| Protocol-First | Event Envelope 定义先于适配器 | ✅ |
| Event-Sourced | 所有写入走事件层，对象层可重建 | ✅ |
| Single Source of Truth | raw event log 是唯一写入目标 | ✅ |
| Controlled Commit | 单写者机制保护长期对象 | ✅ |
| Evidence-First | 关键操作必须记录证据 | ✅ |
| Explainable Recall | recall 返回 explain 信息 | ✅ |
| Tool-Agnostic | 不绑定单一工具 | ✅ |
| Single-Machine First | 单机优先架构 | ✅ |
| Human-in-the-Loop | 高风险动作需确认 | ✅ |
| Small and Testable | 阶段可交付、可验证 | ✅ |

### 复杂度追踪

无复杂度违规。所有实现遵循宪法原则。

## Project Structure

### Documentation (this feature)

```
specs/001-memory-fabric-spec/
├── plan.md              # 本文件
├── research.md          # Phase 0 研究输出
├── data-model.md        # Phase 1 数据模型
├── quickstart.md        # Phase 1 快速入门
├── contracts/           # Phase 1 接口契约
│   └── memory-api.yaml
└── tasks.md             # Phase 2 任务清单

docs/
├── constitution.md      # 宪法
├── spec.md              # 规格说明
├── plan.md              # 本方案
├── checklist.md         # 检查清单
└── analysis.md          # 分析报告

runs/                    # 运行证据目录
└── <run_id>/
    └── evidence.md

ops/
├── verify_smoke.sh      # 冒烟测试
└── rollback.md         # 回滚方案
```

### Source Code (repository root)

```
openclaw_memory_fabric/
├── src/
│   ├── ocmaf/
│   │   ├── __init__.py
│   │   ├── event/           # 事件层
│   │   │   ├── envelope.py  # Event Envelope 定义
│   │   │   ├── store.py     # 事件存储
│   │   │   └── types.py     # 事件类型
│   │   ├── object/          # 对象层
│   │   │   ├── builder.py   # 对象构建器
│   │   │   ├── model.py     # Memory Object 模型
│   │   │   └── lifecycle.py # 状态迁移
│   │   ├── retrieval/       # 检索层
│   │   │   ├── recall.py    # recall API
│   │   │   ├── scorer.py     # 评分
│   │   │   └── conflict.py  # 冲突检测
│   │   ├── api/             # API 层
│   │   │   ├── remember.py
│   │   │   ├── recall.py
│   │   │   └── manage.py
│   │   └── adapters/        # 适配器
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── openclaw.py
│   │       ├── claude_code.py
│   │       ├── codex_cli.py
│   │       └── script.py
│   │
│   └── cli/
│       └── main.py          # CLI 入口
│
├── tests/
│   ├── unit/
│   │   ├── test_event/
│   │   ├── test_object/
│   │   └── test_retrieval/
│   ├── integration/
│   │   ├── test_remember_recall.py
│   │   └── test_adapters.py
│   └── smoke/
│       └── test_basic.py
│
├── ops/
│   ├── verify_smoke.sh
│   └── rollback.md
│
└── pyproject.toml
```

## Phase 0: 协议与底账

### 目标

不同工具可统一写入，且可回放重建。

### 输入

- spec.md 功能需求 FR1-FR6
- constitution.md 协议优先原则

### 输出

1. **Event Envelope 定义** (`src/ocmaf/event/envelope.py`)
   - event_id, version, timestamp, source_tool
   - scope (user/workspace/project/session)
   - event_type, payload, evidence, links

2. **Raw Event Store** (`src/ocmaf/event/store.py`)
   - SQLite + append-only
   - 基础 CRUD + 按 scope/time 查询
   - event_id UUID 生成

3. **基础 Rebuild** (`src/ocmaf/object/builder.py`)
   - 从 event log 重建对象层
   - 幂等性保证

4. **CLI / SDK 框架** (`src/ocmaf/`, `src/cli/`)
   - `ocmaf remember --event <json>`
   - `ocmaf rebuild`
   - Python SDK: `from ocmaf import remember, recall`

5. **数据表**
   - `events` 表：原始事件存储
   - `event_metadata` 表：索引元数据

### 关键技术决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 事件 ID | UUID v4 | 分布式友好，本地生成 |
| 存储格式 | JSON in SQLite | 灵活、可查询 |
| 写入模式 | append-only | 保证不可变性 |
| 查询索引 | scope + timestamp | 满足基本查询需求 |

### 风险

| 风险 | 缓解 |
|------|------|
| 事件格式扩展困难 | 版本号 + 前向兼容设计 |
| 查询性能 | 后续添加 FTS5 索引 |

### 验证

- `ops/verify_smoke.sh` 包含事件写入测试
- `tests/unit/test_event/` 覆盖事件序列化和存储
- `runs/<run_id>/evidence.md` 记录实现证据

### Evidence

- `src/ocmaf/event/envelope.py` - Event Envelope 定义
- `src/ocmaf/event/store.py` - 事件存储实现
- `tests/unit/test_event/test_store.py` - 存储测试
- `ops/verify_smoke.sh` - 冒烟测试用例

---

## Phase 1: 最小可用记忆系统

### 目标

形成"写入-检索-解释-追证"闭环。

### 输入

- Phase 0 输出
- spec.md 功能需求 FR13-FR32

### 输出

1. **Remember/Recall API**
   - `remember(event)` - 写入事件
   - `recall(query, context)` - 语义检索
   - `recall_gist(query, context)` - 精简检索
   - `expand(memory_id)` - 展开详情
   - `explain(memory_id)` - 召回解释

2. **快捷写入方法**
   - `capture_chat_turn(user_msg, assistant_msg, meta)`
   - `capture_task_result(task, result, evidence)`
   - `capture_decision(decision, meta)`

3. **Tier/State 管理**
   - working/hot/warm/cold/archive 五级
   - active/latent/reinforced/decaying/superseded/conflicted/quarantined/archived 八状态
   - 自动 + 手动状态迁移

4. **检索链路**
   - cue → candidate set → conflict check → gist → detail → evidence
   - 基础 relevance scoring

5. **Consolidate**
   - 手动触发状态迁移
   - 对象聚合

### 关键技术决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 检索引擎 | FTS5 + 关键词 | 轻量，满足基本需求 |
| 向量检索 | 可选插件 | 后续按需添加 |
| 冲突检测 | 简单文本相似 + 规则 | v1 足够 |
| 评分 | relevance + freshness | 简单有效 |

### 风险

| 风险 | 缓解 |
|------|------|
| 检索质量不足 | 提供 explain，用户可反馈调整 |
| 冲突误判 | quarantine 机制隔离争议记忆 |

### 验证

- `tests/integration/test_remember_recall.py` - 完整流程测试
- 性能测试：recall P50 < 100ms
- AC-RE-001 到 AC-RE-004 覆盖

### Evidence

- `src/ocmaf/retrieval/recall.py` - recall 实现
- `src/ocmaf/retrieval/scorer.py` - 评分实现
- `tests/integration/test_remember_recall.py` - 集成测试

---

## Phase 2: 对象聚合与案例蒸馏

### 目标

让记忆不只是碎片，而是可复用对象。

### 输入

- Phase 1 输出
- spec.md 功能需求 FR7-FR12, FR26-FR29

### 输出

1. **Object Builder**
   - 从 events 聚合生成 Memory Object
   - 增量更新支持

2. **案例蒸馏**
   - episodic → case_success / case_failure
   - case → procedural (步骤/流程)

3. **Entity/Topic/Version/Link**
   - 实体抽象
   - 主题抽象
   - 版本历史
   - 对象关联

4. **生命周期管理**
   - supersede 机制
   - quarantine 隔离
   - archive 归档

### 关键技术决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 聚合粒度 | event_type 分组 | 简单有效 |
| 案例提取 | 规则 + 模式匹配 | 不依赖 LLM |
| 版本策略 | 事件链 + 快照 | 可追溯可重建 |

### 风险

| 风险 | 缓解 |
|------|------|
| 聚合质量 | 提供手动调整接口 |
| 版本膨胀 | 定期归档旧版本 |

### 验证

- AC-LH-001 到 AC-LH-004 覆盖
- `tests/integration/test_object_builder.py`

### Evidence

- `src/ocmaf/object/builder.py` - 构建器
- `src/ocmaf/object/lifecycle.py` - 生命周期
- `tests/integration/test_object_builder.py`

---

## Phase 3: 接入层与无痛接入

### 目标

做到前 recall、后 remember，像正常聊天一样自动记起。

### 输入

- Phase 1-2 输出
- spec.md 功能需求 FR33-FR37

### 输出

1. **适配器**
   - OpenClaw adapter
   - Claude Code adapter
   - Codex CLI adapter
   - Script agent adapter (Python SDK)
   - Web UI proxy/sidecar 方案

2. **接口形态**
   - Python SDK (`import ocmaf`)
   - CLI (`ocmaf recall --query "..."`)
   - 本地 HTTP 服务 (`localhost:8080`)

3. **无缝接入设计**
   见下方"接入设计"章节

### 关键技术决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 接入模式优先级 | Wrapper > Hook > Proxy | 侵入性递减 |
| SDK 形态 | 函数调用 + 上下文管理器 | 简单易用 |
| HTTP 框架 | Flask (轻量) | 满足需求 |

### 风险

| 风险 | 缓解 |
|------|------|
| 工具兼容性 | 抽象 base adapter |
| prompt 膨胀 | 限制注入内容长度 |

### 验证

- AC-TA-002 适配器接入测试
- 实际工具集成测试

### Evidence

- `src/ocmaf/adapters/` - 适配器实现
- `tests/integration/test_adapters.py` - 适配器测试

---

## Phase 4: 回放评估与自动调优

### 目标

验证系统真的比普通上下文拼接更有效。

### 输入

- Phase 3 输出
- spec.md 功能需求 FR30-FR32

### 输出

1. **Retrieval Traces**
   - 记录每次 recall 的输入输出
   - 用于分析和调试

2. **Benchmark 数据集**
   - 最小测试集
   - 覆盖典型场景

3. **Replay Eval**
   - 离线评估评分准确性
   - 分层健康分析

4. **在线/离线校准**
   - 在线轻评分
   - 离线重校准

### 关键技术决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 评估指标 | precision/recall/f1 | 标准可比较 |
| 校准频率 | 按需 + 定期 | 避免过度调优 |

### 风险

| 风险 | 缓解 |
|------|------|
| 数据不足 | 最小测试集 + smoke |
| 评估偏差 | 多种指标综合 |

### 验证

- AC-TA-001 replay_eval 输出测试
- AC-TA-004 verify_smoke.sh 通过

### Evidence

- `ops/verify_smoke.sh` - 冒烟测试
- `runs/<run_id>/evidence.md` - 评估证据

---

## 接入设计：如何让 AI 工具无痛接入

### 3.1 最小 SDK 长什么样

```python
# 方式 1: 简单函数调用
from ocmaf import remember, recall, init

# 初始化（单次）
init(
    storage_path="~/.ocmaf/memory.db",
    scope={"user_id": "user123", "workspace": "default"}
)

# 调用前 recall
context = recall("项目约束")  # 返回相关记忆

# 调用后 remember
remember(event_type="chat_turn", content="用户要求使用 async")

# 方式 2: 上下文管理器（推荐）
from ocmaf import MemorySession

with MemorySession(scope={"project_id": "my-project"}) as session:
    # 自动 recall 当前上下文
    context = session.get_context()

    # 任务完成后自动 remember
    session.complete_task(task_id="123", result="success")
```

### 3.2 recall 在何时调用

| 场景 | 调用时机 | 典型触发 |
|------|----------|----------|
| 工具启动 | 会话初始化 | `init()` 时自动 |
| 新任务开始 | 任务创建 | `task_start` hook |
| 用户新消息 | 消息接收 | `on_message` hook |
| 关键决策 | 决策前 | `before_decide` hook |

**自动 recall 策略**:
- 启动时：自动 recall 最近 5 条 hot/warm 记忆
- 任务开始：自动 recall 同项目相关约束
- 消息到达：自动 recall 当前 session 相关

### 3.3 remember 在何时调用

| 场景 | 调用时机 | 典型触发 |
|------|----------|----------|
| 对话轮次 | 每次响应 | `on_response` hook |
| 任务完成 | 任务结束 | `on_task_complete` hook |
| 关键决策 | 决策做出 | `on_decision` hook |
| 用户明确 | 用户指令 | `!remember` 命令 |

**自动 remember 策略**:
- 对话自动 capture_chat_turn
- 任务自动 capture_task_result
- 决策自动 capture_decision
- 约束/偏好自动提取

### 3.4 哪些信息应自动注入

| 信息类型 | 注入方式 | 长度限制 |
|----------|----------|----------|
| 项目约束 | system prompt 前缀 | 200 chars |
| 相关案例 | context 附加 | 500 chars |
| 风格偏好 | 自动注入 | 100 chars |
| 历史教训 | 触发式注入 | 300 chars |

**注入原则**:
- 最小化：只注入最相关的 3 条
- 分层：gist 注入，detail 按需
- 去重：已注入不重复

### 3.5 如何避免 prompt 膨胀

1. **分层注入**: gist (摘要) vs detail (详情)
2. **按需展开**: 用户明确询问时才 expand
3. **长度限制**: 单次注入不超过 1KB
4. **自动摘要**: 定期压缩长记忆

### 3.6 如何处理不同工具的 session/project/workspace 映射

| 工具 | session | project | workspace |
|------|---------|---------|-----------|
| OpenClaw | `session_id` | `project_path` | `workspace_id` |
| Claude Code | `conversation_id` | `git_root` | `claude_code_workspace` |
| Codex CLI | `run_id` | `cwd` | `codex_workspace` |
| Script | 用户指定 | 用户指定 | 用户指定 |

**映射规则**:
- 自动检测：优先使用工具提供的标识
- 显式配置：用户可覆盖默认值
- 跨工具：相同项目路径视为同一 project

### 3.7 如何让用户体验接近"正常聊天自动记起"

1. **零配置**: 安装即用，默认 scope 自动推断
2. **透明操作**: 后台自动 recall/remember，无需用户干预
3. **显式控制**: 用户可用 `!remember` / `!forget` 显式控制
4. **可解释**: 注入内容带来源说明，用户可知可删

---

## 测试策略

### 单元测试

- `tests/unit/test_event/` - 事件层
- `tests/unit/test_object/` - 对象层
- `tests/unit/test_retrieval/` - 检索层

### 集成测试

- `tests/integration/test_remember_recall.py` - 完整流程
- `tests/integration/test_adapters.py` - 适配器

### 冒烟测试

- `ops/verify_smoke.sh` - 基础功能验证

---

## Smoke/Verify 策略

### verify_smoke.sh 内容

```bash
#!/bin/bash
set -e

echo "=== OCMF Smoke Test ==="

# 1. 写入测试
echo "[1/5] Testing remember..."
ocmaf remember --event '{"event_type":"test","content":"hello"}'

# 2. 检索测试
echo "[2/5] Testing recall..."
ocmaf recall --query "hello"

# 3. 重建测试
echo "[3/5] Testing rebuild..."
ocmaf rebuild

# 4. 评分测试
echo "[4/5] Testing scoring..."
ocmaf replay-eval --dataset tests/smoke/eval.json

# 5. 清理
echo "[5/5] Cleanup..."
rm -rf ~/.ocmaf/test_*

echo "=== All smoke tests passed ==="
```

### 运行频率

- 每次 commit: CI 自动运行
- 每次 release: 完整测试
- 定期: 性能回归测试

---

## Rollback/Cleanup 策略

### rollback.md 内容

```markdown
# Rollback 方案

## 回滚场景

### 1. 数据损坏
- 现象：recall 返回错误数据
- 原因：对象层损坏
- 方案：执行 `ocmaf rebuild --full`

### 2. 版本升级
- 现象：新版本不兼容
- 方案：
  1. 备份事件数据
  2. 降级版本
  3. 执行 rebuild

### 3. 适配器故障
- 现象：特定工具接入失败
- 方案：
  1. 禁用该适配器
  2. 使用通用 SDK
```

---

## Evidence 策略

### runs/<run_id>/evidence.md 结构

```markdown
# Evidence: [功能名称]

**Run ID**: [run_id]
**Date**: [date]
**Phase**: [phase]

## 实现证据

### 代码
- [文件路径]: [变更说明]

### 测试
- [测试用例]: [结果]

### 验证
- [验证项]: [结果]
```

### 证据收集

- 每次实现完成后自动生成
- 手动补充关键决策说明
- 与 `ops/verify_smoke.sh` 结果关联

---

## Human-in-the-Loop 停点

| 场景 | 停点 | 操作 |
|------|------|------|
| 高风险动作 | 执行前 | 用户确认 |
| 冲突记忆召回 | 返回前 | 用户选择 |
| 敏感记忆跨域 | 共享前 | 用户授权 |
| 大规模删除 | 执行前 | 用户确认 |

---

## 风险闭环

| 风险 | 检测 | 缓解 | 验证 |
|------|------|------|------|
| 记忆污染 | conflict check | quarantine | replay_eval |
| 层级错位 | scoring 监控 | consolidate | 层级报告 |
| 作用域泄漏 | 边界检查 | 显式共享 | 隔离测试 |
| 并发损坏 | single-writer | 事务 | 并发测试 |
| 评分失真 | replay_eval | 校准 | benchmark |

---

## 里程碑

| Phase | 里程碑 | 预期交付 |
|-------|--------|----------|
| Phase 0 | 协议与底账 | Week 1-2 |
| Phase 1 | 最小可用 | Week 3-4 |
| Phase 2 | 对象聚合 | Week 5-6 |
| Phase 3 | 接入层 | Week 7-8 |
| Phase 4 | 评估调优 | Week 9-10 |

---

## 依赖选择与可替代方案

| 组件 | 推荐 | 替代 | 说明 |
|------|------|------|------|
| 存储 | SQLite + FTS5 | PostgreSQL + pgvector | v1 SQLite 足够 |
| HTTP | Flask | FastAPI | 轻量优先 |
| CLI | Click | argparse | 更简洁 |
| 向量 | 可选 | chromadb, faiss | 按需添加 |

---

## AC 映射

| Phase | AC 覆盖 |
|-------|----------|
| Phase 0 | AC-WR-001, AC-WR-003 |
| Phase 1 | AC-WR-002, AC-RE-001~004, AC-LH-001 |
| Phase 2 | AC-LH-002~004 |
| Phase 3 | AC-TA-002 |
| Phase 4 | AC-TA-001, AC-TA-003, AC-TA-004 |

---

---

# 下一阶段实现方案增补 (Phase 3A-4A)

**Date**: 2026-03-11 | **Based On**: MVP + Claude Code Adapter 实现完成

## 背景与当前状态

- **已完成**:
  - MVP 核心：Event Envelope, Memory Object, remember/recall API, SQLite 存储
  - Claude Code adapter 实现（`src/ocmaf/adapters/claude_code.py`）
  - before_response / after_response 自动闭环
  - Scope mapping 规则
  - Injection policy (gist 优先 + 长度限制)
  - 冒烟测试通过 (6/6 tests passed)
  - `runs/002-adapter-integration/evidence.md`

- **本增补目标**:
  - 将 Claude Code 经验抽象为通用 Adapter Contract
  - 规划第二接入目标
  - 设计 Cross-tool E2E 验证
  - 补充 Replay/Eval 能力

---

## Phase 3A: Adapter Contract 固化

### 目标

将 Claude Code 适配器的成功经验抽象为通用 Adapter Contract，使新工具接入只需实现最小接口集。

### 输入

- Claude Code adapter 实现 (`src/ocmaf/adapters/claude_code.py`)
- 现有 Adapter 基类 (`src/ocmaf/adapters/base.py`)
- Scope mapping 实现 (`src/ocmaf/adapters/scope_mapping.py`)

### 输出

#### 1. Adapter Contract 接口规范

```python
class Adapter(ABC):
    """通用 Adapter Contract - 所有工具适配器必须实现"""

    # === 必需接口 ===

    def get_name(self) -> str:
        """工具名称"""
        pass

    def get_scope_from_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """从工具上下文提取 scope

        Returns: {user, workspace, project, session, tool}
        """
        pass

    def before_response(self, query: str, context: Dict[str, Any]) -> str:
        """Recall Hook - 响应前调用

        Args:
            query: 用户查询/输入
            context: {user, workspace, project, session, tool, ...}

        Returns:
            injection_text: 要注入到 LLM 上下文的文本
        """
        pass

    def after_response(
        self,
        query: str,
        response: str,
        context: Dict[str, Any],
    ) -> str:
        """Remember Hook - 响应后调用

        Args:
            query: 用户查询/输入
            response: AI 响应
            context: {user, workspace, project, session, tool, ...}

        Returns:
            event_id: 记住的事件 ID，失败返回空字符串
        """
        pass

    # === 可选接口 ===

    def before_task(self, task: str, context: Dict[str, Any]) -> str:
        """任务执行前 recall (可选)"""
        pass

    def after_task(
        self,
        task: str,
        result: str,
        success: bool,
        context: Dict[str, Any],
    ) -> str:
        """任务执行后 remember (可选)"""
        pass

    def get_injection_policy(self) -> InjectionPolicy:
        """获取该工具的注入策略 (可选，默认全局策略)"""
        pass
```

#### 2. Context 最小字段规范

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `user` | string | Yes | 用户标识符 |
| `workspace` | string | No | 工作区标识符 |
| `project` | string | No | 项目标识符 |
| `session` | string | No | 会话标识符 |
| `tool` | string | Yes | 工具名称 |
| `timestamp` | string | No | ISO 8601 时间戳 |

#### 3. Scope Mapping 最小约定

```python
class ScopeMapper:
    """工具无关的 scope 映射器"""

    # 标准环境变量映射
    TOOL_ENV_MAPPING = {
        "claude-code": {
            "user": "CLAUDE_USER_ID",
            "workspace": "CLAUDE_WORKSPACE",
            "project": "CLAUDE_PROJECT",
            "session": "CLAUDE_SESSION_ID",
        },
        "openclaw": {
            "user": "OPENCLAW_USER_ID",
            "workspace": "OPENCLAW_WORKSPACE",
            "project": "OPENCLAW_PROJECT",
            "session": "OPENCLAW_SESSION_ID",
        },
        "codex-cli": {
            "user": "CODEX_USER",
            "workspace": "CODEX_WORKSPACE",
            "project": "CODEX_PROJECT",
            "session": "CODEX_SESSION",
        },
    }

    # 优先级：显式 context > 环境变量 > 默认值
```

#### 4. Injection Policy 最小约定

```python
class InjectionPolicy:
    """全局注入策略"""

    # 默认限制
    DEFAULT_MAX_LENGTH = 2000
    DEFAULT_MAX_MEMORIES = 5
    DEFAULT_PREFER_GIST = True

    # 分层限制
    LAYER_LIMITS = {
        "system": 500,
        "user": 1500,
        "tool": 2000,
    }

    # 全局策略注册表
    _global_policy: Optional["InjectionPolicy"] = None

    @classmethod
    def set_global_policy(cls, policy: "InjectionPolicy"):
        """设置全局策略，所有 adapter 默认使用"""
        cls._global_policy = policy
```

#### 5. 错误处理与降级策略

| 错误类型 | 降级行为 |
|----------|----------|
| 数据库连接失败 | 返回空 injection，不抛出 |
| Recall 超时 | 返回空 injection，记录日志 |
| Remember 失败 | 返回空 event_id，重试一次 |
| Scope 解析失败 | 使用默认值 {user: "default"} |
| Injection 超长 | 按 policy 截断 |

### 关键决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| Contract 稳定性 | 严格版本管理 | 避免频繁 breaking change |
| Context 扩展 | 允许工具自定义字段 | 灵活性与标准性平衡 |
| 错误策略 | Fail-open | 不阻塞主流程 |
| Policy 优先级 | 全局默认 + 工具override | 统一管理与个性化 |

### 风险

| 风险 | 缓解 |
|------|------|
| Contract 过度抽象 | 保持最小必需接口 |
| 工具定制逻辑膨胀 | 要求工具特定逻辑在 adapter 内，不污染核心 |
| Scope 映射漂移 | 单元测试覆盖所有映射规则 |

### AC

- [ ] AC-AD-001: 所有 adapter 实现 get_name/before_response/after_response
- [ ] AC-AD-002: Context 字段完整映射到 scope
- [ ] AC-AD-003: Injection policy 截断行为可验证
- [ ] AC-AD-004: 错误场景返回符合降级策略

### Evidence

- `src/ocmaf/adapters/base.py` - Contract 定义
- `src/ocmaf/adapters/scope_mapping.py` - Scope 映射
- `tests/unit/test_adapter_contract.py` - Contract 测试

### Rollback/Cleanup

- 如 Contract 变更，保留旧版本接口兼容 2 周
- 渐进式废弃旧接口

---

## Phase 3B: 第二适配器实现

### 目标

实现第二个工具适配器，完成跨工具记忆共享验证。

### 多工具接入分层策略

| Tier | 描述 | 工具示例 | 接入方式 |
|------|------|----------|----------|
| **Tier A** | 原生支持 hook 的工具 | Claude Code | 直接调用 adapter hooks |
| **Tier B** | 可 wrapper 的 CLI/agent | Codex CLI, Script | 包装 CLI 调用 |
| **Tier C** | 需 sidecar/proxy 的封闭工具 | 封闭 Web UI | HTTP 代理 |

#### 推荐接入顺序

| 优先级 | 工具 | Tier | 理由 |
|--------|------|------|------|
| 1 | Claude Code | A | ✅ 已完成，验证了 Contract |
| 2 | Codex CLI | B | CLI 包装简单，场景明确 |
| 3 | OpenClaw | A/B | 需要了解其 hook 机制 |
| 4 | Web UI proxy | C | 最复杂，最后做 |

### 第二适配目标建议: Codex CLI

**选择理由**:

1. **Tier B 适配简单**: 通过包装 CLI 调用即可接入
2. **场景明确**: Codex CLI 有明确的 run/task 概念
3. **复用 Contract**: 与 Claude Code 使用相同接口
4. **跨工具验证**: 实现后可验证 Claude Code ↔ Codex CLI 记忆互通

**依赖前提**:

- Adapter Contract 已固化 (Phase 3A)
- Codex CLI 已在本地安装并可用
- 了解 Codex CLI 的运行上下文（环境变量、工作目录等）

**最小闭环定义**:

```
Round 1: Codex CLI 执行任务 → remember(task_result)
Round 2: Claude Code 启动 → recall(相关任务经验) → 自动注入上下文
```

### 输入

- Phase 3A 输出的 Adapter Contract
- Codex CLI 运行环境和上下文

### 输出

#### Codex CLI Adapter

```python
class CodexCLIAdapter(Adapter):
    """Codex CLI 适配器"""

    def get_name(self) -> str:
        return "codex-cli"

    def get_scope_from_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 从 Codex CLI 环境变量提取
        return {
            "user": os.environ.get("CODEX_USER", "default"),
            "workspace": os.environ.get("CODEX_WORKSPACE"),
            "project": os.environ.get("CODEX_PROJECT", os.getcwd()),
            "session": os.environ.get("CODEX_SESSION_ID"),
            "tool": "codex-cli",
        }

    def before_response(self, query: str, context: Dict[str, Any]) -> str:
        # 使用 MemorySession recall
        ...

    def after_response(self, query: str, response: str, context: Dict[str, Any]) -> str:
        # 使用 capture_task_result 记录
        ...
```

### 关键决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| Codex CLI 集成方式 | 包装 CLI 调用 | 不修改 Codex CLI 源码 |
| Scope 映射 | cwd 作为 project | Codex CLI 无显式 project ID |
| 任务结果捕获 | 解析 CLI 输出 | 标准化任务结果格式 |

### 风险

| 风险 | 缓解 |
|------|------|
| Codex CLI 输出格式变化 | 适配器兼容多种格式 |
| 环境变量不可用 | 回退到默认值 |

### AC

- [x] AC-AD- Codex-001: Codex CLI adapter 实现 get_name/before_response/after_response
- [x] AC-AD- Codex-002: Scope 正确映射 Codex CLI 上下文
- [x] AC-AD- Codex-003: **必须显式透传 tool='codex-cli' 到 remember/recall 路径**
- [x] AC-AD- Codex-004: 任务结果正确转换为 event
- [x] AC-AD- Codex-005: 冒烟测试通过（包含 cross-tool 验证）

> **关键要求**: 所有 adapter **必须显式透传 tool 参数**，确保跨工具隔离正确工作。

### Evidence

- `src/ocmaf/adapters/codex_cli.py` - Codex CLI adapter
- `tests/integration/test_codex_adapter.py` - 集成测试
- `runs/<run_id>/evidence.md` - 实施证据

### Rollback/Cleanup

- 禁用 adapter 回退到通用 SDK

---

## Phase 3C: OpenClaw Adapter MVP

### 目标

实现第三个工具适配器 (OpenClaw)，完成三向 (tri-tool) 记忆隔离验证。

### 当前状态

- Claude Code adapter: ✅ 已完成
- Codex CLI adapter: ✅ 已完成
- test_codex_adapter.py hermetic: ✅ 已修复
- OPENCLAW_GATE: ✅ GO

### 多工具接入分层策略 (更新)

| Tier | 描述 | 工具示例 | 接入方式 |
|------|------|----------|----------|
| **Tier A** | 原生支持 hook 的工具 | Claude Code, OpenClaw | 直接调用 adapter hooks |
| **Tier B** | 可 wrapper 的 CLI/agent | Codex CLI, Script | 包装 CLI 调用 |
| **Tier C** | 需 sidecar/proxy 的封闭工具 | 封闭 Web UI | HTTP 代理 |

#### 接入顺序 (更新)

| 优先级 | 工具 | Tier | 状态 |
|--------|------|
| 1 | Claude Code | A ||------|------ ✅ 已完成 |
| 2 | Codex CLI | B | ✅ 已完成 |
| **3** | **OpenClaw** | **A** | **本轮实现** |
| 4 | Web UI proxy | C | 待后续 |

### 输入

- Phase 3B 输出的 Codex CLI adapter
- OpenClaw 运行环境和上下文
- 已验证的 Adapter Contract

### 输出

#### OpenClaw Adapter

```python
class OpenClawAdapter(Adapter):
    """OpenClaw 适配器"""

    def get_name(self) -> str:
        return "openclaw"

    def get_scope_from_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # 从 OpenClaw 环境变量提取
        return {
            "user": os.environ.get("OPENCLAW_USER_ID", context.get("user", "default")),
            "workspace": os.environ.get("OPENCLAW_WORKSPACE", context.get("workspace")),
            "project": os.environ.get("OPENCLAW_PROJECT", context.get("project")),
            "session": os.environ.get("OPENCLAW_SESSION_ID", context.get("session")),
            "tool": "openclaw",  # 必须显式透传
        }

    def before_response(self, query: str, context: Dict[str, Any]) -> str:
        scope = self.get_scope_from_context(context)
        with MemorySession(
            user=scope.get("user", "default"),
            workspace=scope.get("workspace"),
            project=scope.get("project"),
            session=scope.get("session"),
            tool=scope.get("tool"),  # 必须显式透传 tool='openclaw'
            db_path=self.db_path,
        ) as session:
            result = session.recall_gist(query, limit=self.injection_policy.max_memories)
            return self.injection_policy.apply(result)

    def after_response(self, query: str, response: str, context: Dict[str, Any]) -> str:
        scope = self.get_scope_from_context(context)
        with MemorySession(
            user=scope.get("user", "default"),
            workspace=scope.get("workspace"),
            project=scope.get("project"),
            session=scope.get("session"),
            tool=scope.get("tool"),  # 必须显式透传 tool='openclaw'
            db_path=self.db_path,
        ) as session:
            event_id = session.capture_chat_turn(
                user_msg=query,
                assistant_msg=response,
                source_tool="openclaw",
            )
            return event_id
```

### 关键要求

#### 必须显式透传 tool='openclaw'

所有 adapter 必须显式传递 tool 参数到 MemorySession，确保跨工具隔离正确工作：

| Adapter | tool 值 |
|---------|---------|
| ClaudeCodeAdapter | `'claude-code'` |
| CodexCLIAdapter | `'codex-cli'` |
| OpenClawAdapter | `'openclaw'` |

#### Tri-tool Integration 验证方案

实现后必须验证三向隔离：

```python
def test_tri_tool_isolation():
    """三向工具隔离测试"""

    # 1. Claude Code 写入
    cc_adapter = ClaudeCodeAdapter(db_path=temp_db)
    cc_adapter.after_response("Python preference", "Use Python", {"user": "u1", "project": "p1"})

    # 2. Codex CLI 写入
    codex_adapter = CodexCLIAdapter(db_path=temp_db)
    codex_adapter.after_response("Docker usage", "Use Docker", {"user": "u1", "project": "p1"})

    # 3. OpenClaw 写入
    openclaw_adapter = OpenClawAdapter(db_path=temp_db)
    openclaw_adapter.after_response("Rust preference", "Use Rust", {"user": "u1", "project": "p1"})

    # 4. 验证隔离
    # Claude Code recall → 不应召回 Codex/OpenClaw 的记忆
    cc_recall = cc_adapter.before_response("pref", {"user": "u1", "project": "p1"})
    assert "Docker" not in cc_recall
    assert "Rust" not in cc_recall

    # Codex recall → 不应召回 Claude/OpenClaw 的记忆
    codex_recall = codex_adapter.before_response("usage", {"user": "u1", "project": "p1"})
    assert "Python" not in codex_recall
    assert "Rust" not in codex_recall

    # OpenClaw recall → 不应召回 Claude/Codex 的记忆
    openclaw_recall = openclaw_adapter.before_response("pref", {"user": "u1", "project": "p1"})
    assert "Python" not in openclaw_recall
    assert "Docker" not in openclaw_recall
```

### 验证矩阵

| 场景 | 工具 A 写入 | 工具 B 召回 | 预期结果 |
|------|------------|------------|----------|
| 同 tool 召回 | Claude | Claude | ✅ 召回 |
| 同 tool 召回 | Codex | Codex | ✅ 召回 |
| 同 tool 召回 | OpenClaw | OpenClaw | ✅ 召回 |
| 跨 tool 隔离 | Claude | Codex | ❌ 不召回 |
| 跨 tool 隔离 | Claude | OpenClaw | ❌ 不召回 |
| 跨 tool 隔离 | Codex | OpenClaw | ❌ 不召回 |
| 跨 tool 隔离 | OpenClaw | Claude | ❌ 不召回 |

### 关键决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| OpenClaw 集成方式 | Hook/Middleware | 原生支持 hook 的 Tier A 工具 |
| Scope 映射 | 环境变量优先 | OpenClaw 提供完整环境变量 |
| tool 透传 | 显式传递 | 必须确保隔离正确 |

### 风险

| 风险 | 缓解 |
|------|------|
| OpenClaw 环境变量不可用 | 回退到默认值 |
| Hook 机制不兼容 | 提供 SDK fallback |

### AC

- [ ] AC-AD-OpenClaw-001: OpenClaw adapter 实现 get_name/before_response/after_response
- [ ] AC-AD-OpenClaw-002: Scope 正确映射 OpenClaw 上下文
- [ ] AC-AD-OpenClaw-003: **必须显式透传 tool='openclaw'**
- [ ] AC-AD-OpenClaw-004: Tri-tool isolation 测试通过
- [ ] AC-AD-OpenClaw-005: verify_smoke.sh 包含 OpenClaw 测试

### Evidence

- `src/ocmaf/adapters/openclaw.py` - OpenClaw adapter
- `tests/test_openclaw_adapter.py` - OpenClaw 适配器测试
- `tests/test_tri_tool_integration.py` - 三向隔离测试
- `ops/verify_smoke.sh` - 更新包含 OpenClaw
- `runs/<run_id>/evidence.md` - 实施证据

### Rollback/Cleanup

- 禁用 adapter 回退到通用 SDK
- 保留历史数据，不删除

---

## Phase 3D: Tri-tool Integration 验证

### 目标

验证三工具 (Claude Code ↔ Codex CLI ↔ OpenClaw) 记忆互通与隔离。

### 输入

- Claude Code adapter (已完成)
- Codex CLI adapter (已完成)
- OpenClaw adapter (Phase 3C 输出)
- 三工具的测试环境

### 输出

#### Tri-tool Integration 测试

```python
def test_tri_tool_full_matrix():
    """完整三向测试矩阵"""

    adapters = {
        "claude-code": ClaudeCodeAdapter(db_path=temp_db),
        "codex-cli": CodexCLIAdapter(db_path=temp_db),
        "openclaw": OpenClawAdapter(db_path=temp_db),
    }

    # 每个工具写入
    for tool_name, adapter in adapters.items():
        adapter.after_response(
            f"Remember: {tool_name} preference",
            f"Using {tool_name}",
            {"user": "u1", "project": "p1"}
        )

    # 每个工具召回 → 验证同 tool 召回，跨 tool 隔离
    for recall_tool, adapter in adapters.items():
        for write_tool in adapters.keys():
            result = adapter.before_response("preference", {"user": "u1", "project": "p1"})

            if recall_tool == write_tool:
                # 同 tool → 应该召回
                assert result != ""
            else:
                # 跨 tool → 不应召回
                assert result == "" or write_tool not in result
```

### 验证步骤

1. **准备**: 初始化空数据库
2. **写入**: 三个 adapter 分别写入
3. **召回**: 交叉验证召回结果
4. **隔离**: 确认跨工具不召回
5. **解释**: 验证 explain() 可追溯

### AC

- [ ] AC-TRI-001: 同 tool recall 命中率 > 80%
- [ ] AC-TRI-002: 跨 tool 隔离率 = 100%
- [ ] AC-TRI-003: Injection 长度 < 2000 chars
- [ ] AC-TRI-004: Explain 返回完整证据链

### Evidence

- `tests/test_tri_tool_integration.py` - 三向测试
- `runs/<run_id>/evidence.md`

---

## Phase 4B: Cross-tool E2E / Real Host Integration Validation

### 目标

进行三宿主 (Claude Code ↔ Codex CLI ↔ OpenClaw) 真实宿主最小集成验证，确保:
- 三宿主最小真实写入/召回 E2E 可工作
- same-tool recall 验证通过
- cross-tool 默认隔离验证通过
- 至少一个共享 project/session/fallback 场景验证

### 当前状态

- Claude Code adapter: ✅ 已完成
- Codex CLI adapter: ✅ 已完成
- OpenClaw adapter: ✅ 已完成
- Tri-tool integration tests: ✅ 已通过

### 输入

- Phase 3C 输出的三适配器
- Tri-tool 隔离测试结果
- 三宿主真实环境

### 输出

#### 1. 三宿主最小 E2E 场景矩阵

| 场景 | 工具 A | 工具 B | 验证点 |
|------|--------|--------|--------|
| 同 tool recall | Claude → Claude | 同一工具 recall | ✅ 召回 |
| 跨 tool 隔离 | Claude → Codex | 不同工具 | ❌ 不召回 |
| 跨 tool 隔离 | Claude → OpenClaw | 不同工具 | ❌ 不召回 |
| 跨 tool 隔离 | Codex → OpenClaw | 不同工具 | ❌ 不召回 |
| Project fallback | Claude → Codex | 同项目不同 session | 按配置召回 |
| Session fallback | Claude → Claude | 同项目不同 session | 按配置召回 |

#### 2. 真实宿主最小集成场景

**场景 1: Claude Code → Codex CLI**

```
1. 用户在 Claude Code 中定义项目规范
2. Claude Code after_response 记录规范到 memory
3. 用户切换到 Codex CLI 执行任务
4. Codex CLI before_response recall 同项目规范
5. 验证: 注入内容包含规范记忆
```

**场景 2: OpenClaw → Claude Code**

```
1. 用户在 OpenClaw 中记录设计决策
2. OpenClaw after_response 记录决策
3. 用户切换到 Claude Code 继续工作
4. Claude Code before_response recall 相关决策
5. 验证: 注入内容包含决策记忆
```

**场景 3: Same-tool Session Fallback**

```
1. Claude Code 会话 1 记录偏好
2. 会话 1 结束
3. Claude Code 会话 2 开始 (同项目)
4. before_response recall 同项目偏好
5. 验证: 按 fallback 策略召回
```

#### 3. E2E Evidence 规范

每个 E2E 测试必须记录:

```markdown
## E2E-XXX: [场景名称]

### 环境
- 工具版本
- 数据库状态
- 环境变量

### 执行步骤
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

### 预期结果
- [结果描述]

### 实际结果
- [实际输出]

### 判定
✅ PASS / ❌ FAIL

### Known Limits (如不通过)
- [限制说明]
- [绕过方案]
```

#### 4. 已知边界

| 边界项 | 说明 | 影响 |
|--------|------|------|
| 无真实网络 | 测试环境隔离 | E2E 有限 |
| 有限 session | 短时间测试 | fallback 不准 |
| 无多日持久 | 测试周期短 | 老化不测 |
| 单一数据库 | 无并发写入 | 并发不测 |

#### 5. 降级策略

| 失败场景 | 降级行为 |
|----------|----------|
| 宿主机不可用 | 回退到 mock |
| 环境变量缺失 | 使用默认值 |
| 数据库连接失败 | 返回空 injection |
| Recall 超时 | 返回空 injection |

### 验收 AC

- [ ] AC-E2E-001: 三宿主最小 E2E 可执行
- [ ] AC-E2E-002: Same-tool recall 验证通过
- [ ] AC-E2E-003: Cross-tool 隔离验证通过
- [ ] AC-E2E-004: Project/Session fallback 场景验证
- [ ] AC-E2E-005: Known Limits 文档化

### Evidence

- `tests/test_tri_tool_integration.py` - Tri-tool 测试
- `tests/test_e2e_real_host.py` - 真实宿主测试
- `runs/<run_id>/evidence.md` - E2E 证据
- `runs/<run_id>/known_limits.md` - 已知边界文档

---

## Phase 4C: Real Host Manual Integration Validation Run

### 目标

明确区分"合成测试"与"真实宿主验证"，在真实宿主环境中进行手工集成验证：

- 明确什么算"真实宿主验证"
- 明确什么仍然只是"合成测试"
- 在 Claude Code / Codex CLI / OpenClaw 真实宿主中进行最小手工验证
- 验证 same-tool recall / cross-tool isolation / fallback 在真实宿主中的行为

### 当前状态

- Phase 4B E2E 测试: ✅ 已通过 (合成测试)
- Tri-tool isolation: ✅ 已验证
- Fallback 场景: ✅ 已验证

### 合成测试 vs 真实宿主验证

| 维度 | 合成测试 (Phase 4B) | 真实宿主验证 (Phase 4C) |
|------|---------------------|------------------------|
| 执行环境 | pytest / Python | 真实 Claude Code / Codex / OpenClaw |
| 数据流 | adapter 调用 | 真实 hook 回调 |
| Scope 来源 | 手动传入 context | 真实环境变量 |
| Recall 来源 | 代码调用 | 真实用户触发 |
| 时序 | 同步执行 | 可能异步/事件驱动 |
| 隔离性 | tempfile 隔离 | 真实默认数据库 |

### 真实宿主手工验证场景

**验证方法**: 手工执行 + 观察结果 + 记录证据

| 场景 | 工具 | 验证点 | 预期结果 |
|------|------|--------|----------|
| Claude Code recall | Claude Code | 真实会话中 recall | 注入内容出现 |
| Claude Code remember | Claude Code | 真实响应后 remember | event 记录 |
| Codex CLI recall | Codex CLI | 真实 run 中 recall | 输出包含记忆 |
| OpenClaw recall | OpenClaw | 真实任务中 recall | 上下文包含记忆 |
| Cross-tool 隔离 | 多工具 | 工具 A 写入，B 不召回 | 无串扰 |

### 输入

- Phase 4B E2E 测试结果
- 三宿主真实环境 (Claude Code / Codex CLI / OpenClaw)
- 手工验证脚本或清单

### 输出

#### 1. 三宿主手工验证记录

每个宿主验证记录:
```markdown
## 宿主验证: [工具名]

### 环境
- 工具版本:
- 数据库路径: ~/.ocmaf/memory.db
- 环境变量:

### 执行步骤
1. [步骤 1 - 写入]
   命令:
   结果:

2. [步骤 2 - 召回]
   命令:
   结果:

### 判定
✅ PASS / ❌ FAIL

### 证据截图
[如有截图或日志]
```

#### 2. 真实宿主 vs 合成测试对比

| 验证项 | 合成测试结果 | 真实宿主结果 | 差异分析 |
|--------|-------------|--------------|----------|
| Same-tool recall | ✅ | 待验证 | - |
| Cross-tool isolation | ✅ | 待验证 | - |
| Fallback | ✅ | 待验证 | - |

#### 3. Known Gaps

记录真实宿主中发现的问题:
- 环境差异
- 配置问题
- 时序问题

### 验收 AC

- [ ] AC-RH-001: 至少一个真实 Claude Code 会话验证
- [ ] AC-RH-002: 至少一个真实 Codex CLI run 验证
- [ ] AC-RH-003: 至少一个真实 OpenClaw 任务验证
- [ ] AC-RH-004: Same-tool recall 在真实宿主中工作
- [ ] AC-RH-005: Cross-tool isolation 在真实宿主中工作
- [ ] AC-RH-006: 手工验证证据记录完整

### Evidence

- `runs/<run_id>/real_host_validation.md` - 手工验证记录
- `runs/<run_id>/real_vs_synthetic.md` - 对比分析
- `runs/<run_id>/known_issues.md` - 真实宿主问题

### 风险

| 风险 | 描述 | 缓解 |
|------|------|------|
| 环境配置复杂 | 真实宿主配置困难 | 提供配置清单 |
| 时序不确定 | 异步执行导致不确定性 | 多次验证 |
| 数据污染 | 真实数据库被污染 | 验证前备份 |

---

## 真实宿主验证定义（严格版）

### 三种验证类型边界

| 类型 | 定义 | 特征 |
|------|------|------|
| **Synthetic Test** | pytest 调用 adapter 函数 | tempfile DB, mock env, 纯代码执行 |
| **Manual Adapter Invocation** | 直接调用 adapter.before/after_response | 真实环境变量, 但仍是 Python 调用 |
| **Real Host Validation** | 通过真实工具二进制执行 | 真实 `claude`/`codex` 进程, 真实 hook, 真实环境 |

### 严格 Real Host Validation 要求

**才算 Real Host Validation**:
1. ✅ 验证 `which claude` 返回真实路径
2. ✅ 验证 `which codex` 返回真实路径
3. ✅ 通过真实工具的 hook 或回调触发 OCMF
4. ✅ 验证 OCMF 写入真实默认数据库
5. ✅ 在真实工具的输出/响应中观察到记忆效果

**不算 Real Host Validation**:
1. ❌ 只是 adapter-level Python 调用（仍是代码调用）
2. ❌ 只验证环境变量存在（没有真实进程）
3. ❌ 只验证 adapter 能读写数据库（没有通过真实工具）
4. ❌ 只在 pytest 中模拟环境变量

### OpenClaw 环境阻塞处理

当目标宿主的二进制不可用时:

1. **记录为环境阻塞**: `HOST_BLOCKED: <tool> - <reason>`
2. **明确阻塞原因**: `which <tool>` 返回空
3. **不标记为 FAIL**: 环境问题不是代码问题
4. **更新 known_limits.md**: 列出所有阻塞的宿主

---

## Phase 4D: Claude/Codex Real Host Validation Run

### 目标

针对 Codex 审核反馈，收敛 Phase 4C 的问题，明确真正的 Real Host Validation 标准，并执行 Claude/Codex 双宿主最小验证:

1. 严格区分 "真实宿主验证" vs "adapter-level manual invocation"
2. 验证 `claude` 二进制真实路径
3. 验证 `codex` 二进制真实路径
4. 至少一条 Claude same-tool real host recall
5. 至少一条 Codex same-tool real host recall
6. 至少一条 Claude ↔ Codex real host cross-tool 默认隔离
7. OpenClaw 环境阻塞说明

### 当前问题（来自 Codex 审核）

| 问题 | 描述 | 修复方向 |
|------|------|----------|
| 问题1 | Claude 验证仍是 adapter-level invocation | 必须通过真实 `claude` 进程触发 |
| 问题2 | Codex evidence 与机器事实不一致 | 当前机器存在 codex 二进制，需验证 |
| 问题3 | OpenClaw 应标记为环境阻塞 | 明确记录为 BLOCKED，非 FAIL |

### 真实宿主验证矩阵

| 验证项 | Claude | Codex | OpenClaw | 说明 |
|--------|--------|-------|----------|------|
| 二进制路径验证 | `which claude` | `which codex` | `which openclaw` | 基础前提 |
| Same-tool remember | 真实进程写入 | 真实进程写入 | BLOCKED | 核心功能 |
| Same-tool recall | 真实进程召回 | 真实进程召回 | BLOCKED | 核心功能 |
| Cross-tool isolation | Claude↔Codex | Claude↔Codex | BLOCKED | 隔离验证 |

### 输入

- Phase 4C 验证结果
- `which claude` 输出
- `which codex` 输出
- `which openclaw` 输出

### 输出

#### 1. 二进制路径验证证据

```bash
$ which claude
/Users/user/.local/bin/claude

$ which codex
/usr/local/bin/codex

$ which openclaw
openclaw not found  # BLOCKED
```

#### 2. Claude Real Host 验证

如果 `which claude` 成功:
- 通过 Claude Code 的 hook/回调触发 OCMF
- 验证 remember 写入真实数据库
- 验证 recall 召回内容出现在响应中

如果 `which claude` 失败:
- 标记为环境阻塞

#### 3. Codex Real Host 验证

如果 `which codex` 成功:
- 通过 Codex CLI 执行触发 OCMF
- 验证 remember 写入真实数据库
- 验证 recall 输出包含记忆内容

如果 `which codex` 失败:
- 标记为环境阻塞

#### 4. Cross-tool Isolation 验证

真实 Claude 写入 → 真实 Codex 召回 → 应该为空

#### 5. Evidence 规范

每个验证必须包含:
- 真实命令输出 (`$ which claude`)
- 真实环境变量 (`$ env | grep CLAUDE`)
- 真实输入/输出
- 退出码

```markdown
## Claude Real Host Validation

### Binary Check
$ which claude
/Users/user/.local/bin/claude
Exit code: 0

### Environment Check
$ env | grep CLAUDE
CLAUDE_PROJECT=/tmp/test-project
Exit code: 0

### Recall Result
[real output from Claude]
```

### 验收 AC

- [ ] AC-RH-STRICT-001: `which claude` 返回真实路径
- [ ] AC-RH-STRICT-002: `which codex` 返回真实路径（或标记 BLOCKED）
- [ ] AC-RH-STRICT-003: Claude same-tool real host recall 验证
- [ ] AC-RH-STRICT-004: Codex same-tool real host recall 验证（或标记 BLOCKED）
- [ ] AC-RH-STRICT-005: Claude ↔ Codex cross-tool isolation 验证
- [ ] AC-RH-STRICT-006: OpenClaw 明确标记为环境阻塞

### Evidence

- `runs/<run_id>/binary_verification.md` - 二进制路径证据
- `runs/<run_id>/claude_real_host.md` - Claude 真实宿主验证
- `runs/<run_id>/codex_real_host.md` - Codex 真实宿主验证
- `runs/<run_id>/cross_tool_real_host.md` - 跨工具真实隔离
- `runs/<run_id>/evidence.md` - 完整证据汇总
- `runs/<run_id>/known_limits.md` - 更新的限制说明

### 风险

| 风险 | 描述 | 缓解 |
|------|------|------|
| Claude hook 不可用 | 无法触发真实 recall | 尝试多种触发方式 |
| Codex CLI 配置复杂 | 环境配置困难 | 提供配置清单 |
| OpenClaw 阻塞 | 宿主不可用 | 明确记录为 BLOCKED |

---

## Phase 4E: Strict Claude/Codex Real Host Validation

### 目标

针对最新审核反馈，进一步明确"严格意义上的 Real Host Validation"，并执行精确验证:

1. **严格定义三种验证类型**
2. **纠偏 previous run 中的证据问题**
3. **实现 Claude real host write + recall**
4. **实现 Codex real host write + recall**
5. **实现 Claude ↔ Codex real host cross-tool isolation**
6. **记录 OpenClaw 环境阻塞**

### 三种验证类型的严格定义

| 类型 | 定义 | 是否本轮目标 |
|------|------|-------------|
| **Real Host Validation** | 通过真实二进制进程自动触发 OCMF recall/remember | ✅ 目标 |
| **Manual Adapter Invocation** | 直接调用 adapter.before/after_response（Python 代码） | ❌ 不是 |
| **Synthetic Test** | pytest 自动执行 adapter 调用 | ❌ 不是 |

### Real Host Validation 的严格要求

**才算 Real Host Validation**:
1. ✅ 用户在 Claude Code 中发起查询
2. ✅ OCMF 自动 recall 相关记忆
3. ✅ 记忆注入到 Claude Code 响应中
4. ✅ 用户看到包含记忆的响应
5. ✅ 记忆被写入数据库

**不算 Real Host Validation**:
1. ❌ 直接调用 `adapter.before_response(query, context)`
2. ❌ 在 Python 中手动设置 `os.environ["CLAUDE_*"]`
3. ❌ 在 pytest 中调用 adapter 函数

### 当前问题与修复

| 问题 | 描述 | 修复 |
|------|------|------|
| 问题1 | 之前的 real host 仍是 manual adapter invocation | 需要真实触发 |
| 问题2 | codex 证据与机器不一致 | 重新验证 `which codex` |
| 问题3 | Claude 无 hook 系统 | 需要探索触发方式 |

### Claude Real Host 最小场景

**目标**: 在 Claude Code 中触发 OCMF recall

**探索方案**:
1. **方案A**: 使用 Claude Code 的 MCP (Model Context Protocol)
2. **方案B**: 使用 claude CLI 的 plugin/extension 机制
3. **方案C**: 探索 Claude Code 的 `--mcp` flag

```bash
# 探索 Claude Code 支持的 hook 机制
claude --help | grep -i hook
claude --help | grep -i plugin
claude --help | grep -i mcp
claude --help | grep -i extend
```

### Codex Real Host 最小场景

**目标**: 通过 Codex CLI 触发 OCMF recall

**探索方案**:
1. 检查 Codex CLI 是否存在
2. 检查 Codex CLI 是否支持 hook/extension

```bash
# 检查 Codex CLI
which codex
codex --help
```

### Claude ↔ Codex Real Host Cross-tool 隔离

**目标**: 验证 Claude 写入的记忆不会被 Codex 召回

**步骤**:
1. 通过 Claude real host 方式写入记忆
2. 通过 Codex real host 方式尝试召回
3. 验证隔离（Codex 无法召回 Claude 内容）

### OpenClaw 环境阻塞

如果 OpenClaw 不可用，明确记录:

```markdown
## OpenClaw Status

**Binary Check**:
$ which openclaw
openclaw not found

**Status**: BLOCKED - OpenClaw not installed

**后续条件**: 安装 OpenClaw 后重新验证
```

### 证据规范

每个验证必须包含:

1. **Binary 证据**:
```bash
$ which claude
/Users/user/.local/bin/claude
Exit code: 0
```

2. **真实环境变量**:
```bash
$ env | grep -E "(CLAUDE|CODEX|OPENCLAW)"
CLAUDE_PROJECT=/tmp/test-project
```

3. **真实输入** (用户实际发出的查询):
```
用户查询: "如何实现 async/await?"
```

4. **真实输出** (包含记忆注入的响应):
```
响应: "根据之前的经验, async/await 可以..."
```

5. **数据库记录**:
```sql
SELECT * FROM memory_events WHERE project = '/tmp/test-project';
```

### 失败记录规范

如果验证失败，必须记录:

1. **失败原因**: 具体是什么失败了
2. **错误信息**: 真实的错误输出
3. **阻塞点**: 是架构限制还是环境问题
4. **后续建议**: 如何修复或绕过

### 输入

- Phase 4D 验证结果
- `which claude` 输出（重新验证）
- `which codex` 输出（重新验证）
- `which openclaw` 输出（重新验证）

### 输出

1. **Binary 验证证据**: 真实命令输出
2. **Claude Real Host 验证**: 成功/失败/阻塞
3. **Codex Real Host 验证**: 成功/失败/阻塞
4. **Cross-tool 隔离证据**: Claude↔Codex
5. **OpenClaw 阻塞记录**: 明确记录为 BLOCKED

### 验收 AC

- [ ] AC-STRICT-001: 明确区分 Real Host / Manual / Synthetic
- [ ] AC-STRICT-002: Claude real host write + recall
- [ ] AC-STRICT-003: Codex real host write + recall
- [ ] AC-STRICT-004: Claude ↔ Codex cross-tool isolation
- [ ] AC-STRICT-005: OpenClaw 阻塞记录

### Evidence

- `runs/<run_id>/binary_check.md` - 重新验证的 binary 证据
- `runs/<run_id>/claude_strict_real_host.md` - Claude 严格 real host 验证
- `runs/<run_id>/codex_strict_real_host.md` - Codex 严格 real host 验证
- `runs/<run_id>/cross_tool_strict.md` - 严格 cross-tool 验证
- `runs/<run_id>/evidence.md` - 完整证据
- `runs/<run_id>/known_limits.md` - 更新的限制说明

### 风险

| 风险 | 描述 | 缓解 |
|------|------|------|
| Claude 无 hook | 无法自动触发 recall | 探索 MCP/plugin 机制 |
| Codex 未安装 | 无法验证 | 标记为环境阻塞 |
| 架构限制 | 工具不支持外部集成 | 记录为架构限制 |

---

## Phase 4A: Replay/Eval 补强

### 目标

验证跨工具记忆互通，确保:

- 工具 A 写入后，工具 B 能自动 recall
- Scope 隔离正确，不串上下文
- Evidence 可追溯
- Injection 长度受控
- Recall 结果可解释

### 输入

- Claude Code adapter (已完成)
- Codex CLI adapter (Phase 3B 输出)
- 两工具的测试环境

### 输出

#### Cross-tool E2E 测试用例

```python
def test_cross_tool_recall():
    """跨工具 recall 测试"""

    # Step 1: Claude Code 写入
    cc_adapter = ClaudeCodeAdapter()
    cc_context = {
        "user": "test_user",
        "workspace": "test_ws",
        "project": "test_project",
        "session": "session_001",
    }

    # Claude Code 记住一个重要决策
    cc_adapter.after_response(
        query="如何处理 Python 项目的依赖?",
        response="使用 pyproject.toml 和 uv/poetry",
        context=cc_context,
    )

    # Step 2: Codex CLI recall
    codex_adapter = CodexCLIAdapter()
    codex_context = {
        "user": "test_user",  # 同一用户
        "workspace": "test_ws",  # 同一工作区
        "project": "test_project",  # 同一项目
        "session": "session_002",  # 新会话
    }

    # Codex CLI 应该能回忆起 Claude Code 的经验
    injection = codex_adapter.before_response(
        query="项目依赖管理最佳实践",
        context=codex_context,
    )

    # 验证
    assert "pyproject.toml" in injection or "Python" in injection
```

#### 验证矩阵

| 场景 | 验证点 | 预期结果 |
|------|--------|----------|
| 同用户同项目 | 跨工具 recall | 应能召回 |
| 同用户不同项目 | 跨工具 recall | 不应召回 |
| 不同用户 | 跨工具 recall | 不应召回 |
| Scope 泄漏 | 隔离测试 | 严格隔离 |

#### 具体验证步骤

1. **准备阶段**:
   - 初始化空数据库
   - 安装两个 adapter

2. **Round 1 (Claude Code)**:
   - 执行 `cc_adapter.after_response()`
   - 验证 event 已写入
   - 记录 event_id

3. **Round 2 (Codex CLI)**:
   - 执行 `codex_adapter.before_response()`
   - 验证 injection 包含 Round 1 内容
   - 验证 injection 长度 < 2000 chars

4. **验证阶段**:
   - 调用 `explain(memory_id)` 验证可追溯性
   - 检查 scope 隔离

5. **清理**:
   - 删除测试数据库

### 关键决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 测试隔离 | 独立 DB | 避免污染 |
| Scope 匹配 | 精确匹配 (user+project) | 严格隔离 |
| 验证指标 | 命中率 + 长度 + 可解释性 | 全面覆盖 |

### 风险

| 风险 | 缓解 |
|------|------|
| 测试环境不稳定 | Docker 容器化测试 |
| 时间相关 flaky | 固定时间窗口 |

### AC

- [ ] AC-E2E-001: 同用户同项目 recall 命中率 > 80%
- [ ] AC-E2E-002: Scope 隔离验证通过
- [ ] AC-E2E-003: Injection 长度 < 2000 chars
- [ ] AC-E2E-004: Explain 返回完整证据链
- [ ] AC-E2E-005: 测试退出码 0

### Evidence

- `tests/integration/test_cross_tool_e2e.py` - E2E 测试
- 测试输出日志
- `runs/<run_id>/evidence.md`

### Rollback/Cleanup

- 测试后清理测试数据库
- 回退到单工具测试

---

## Phase 4A: Replay/Eval 补强

### 目标

建立完整的评估体系，验证记忆系统效果。

### 输入

- Phase 3C E2E 测试结果
- 现有 retrieval 实现

### 输出

#### 1. Retrieval Trace 记录

```python
class RetrievalTrace:
    """检索轨迹记录"""

    trace_id: str
    timestamp: str
    query: str
    context: Dict[str, Any]

    # 输入
    keywords: List[str]
    scope: Dict[str, Any]

    # 输出
    candidate_count: int
    selected_memory_ids: List[str]
    injection_length: int

    # 评分
    relevance_scores: List[float]
    confidence_scores: List[float]
    freshness_scores: List[float]
```

**存储**: `retrieval_traces` 表

#### 2. Adapter Recall Quality Benchmark

```json
{
  "name": "adapter_recall_benchmark",
  "version": "1.0",
  "test_cases": [
    {
      "id": "tc001",
      "query": "项目依赖管理",
      "expected_memories": ["pyproject.toml", "poetry"],
      "scope": {"user": "test", "project": "test_project"},
      "max_injection_length": 2000
    }
  ],
  "metrics": [
    "recall_precision",
    "recall_latency",
    "injection_length",
    "conflict_detected"
  ]
}
```

#### 3. 跨工具 Recall 命中率

```
| 工具 A | 工具 B | 命中率 | 延迟 P50 | 延迟 P95 |
|--------|--------|--------|----------|----------|
| Claude Code | Codex CLI | 85% | 45ms | 120ms |
| Codex CLI | Claude Code | 80% | 50ms | 130ms |
```

#### 4. 错误注入 / 冲突注入测试

```python
def test_conflict_injection():
    """冲突检测测试"""

    # 写入两条冲突记忆
    adapter.after_response(
        "使用 Django",
        "推荐 Django 框架",
        context={"project": "web"}
    )
    adapter.after_response(
        "使用 Flask",
        "推荐 Flask 框架",
        context={"project": "web"}
    )

    # Recall 时应检测冲突
    result = adapter.before_response("Web 框架推荐", context)

    # 验证冲突标记
    assert any(m.state == State.CONFLICTED for m in result.memories)
```

#### 5. Prompt 膨胀守护指标

| 指标 | 阈值 | 告警 |
|------|------|------|
| 单次 injection 长度 | < 2000 chars | 警告 |
| 累计 injection 长度 | < 8000 chars/会话 | 警告 |
| 触发截断比例 | < 10% | 警告 |

### 关键决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| Trace 存储 | SQLite | 轻量，满足需求 |
| 评估频率 | 按需 + 定期 | 避免过度开销 |
| 膨胀指标 | 长度 + 截断率 | 可量化 |

### 风险

| 风险 | 缓解 |
|------|------|
| Trace 数据膨胀 | 定期归档/清理 |
| 评估主观性 | 多指标综合 |

### AC

- [ ] AC-EVAL-001: Trace 记录完整
- [ ] AC-EVAL-002: Benchmark 可执行
- [ ] AC-EVAL-003: 跨工具命中率可计算
- [ ] AC-EVAL-004: 冲突检测测试通过
- [ ] AC-EVAL-005: 膨胀指标可监控

### Evidence

- `ops/replay_eval.py` - 评估脚本
- `ops/benchmark/adapter_recall.json` - 测试集
- `runs/<run_id>/eval_report.md` - 评估报告

### Rollback/Cleanup

- 禁用评估模块不影响主流程

---

## 风险与技术债审查

### 当前实现后的潜在技术债与优先治理项

#### 1. Claude Code Adapter 专用逻辑过重 ⚠️ HIGH

**问题**: 当前 Claude Code adapter 包含部分硬编码逻辑，未来复用性受限

**位置**: `src/ocmaf/adapters/claude_code.py`

**治理建议**:
- 抽象公共逻辑到 base adapter
- 工具特定配置外部化
- 添加 adapter 配置 schema

#### 2. Adapter Contract 尚未抽象稳定 ⚠️ MEDIUM

**问题**: Contract 接口可能随新工具接入演进

**治理建议**:
- 严格版本管理 (semver)
- 保持最小必需接口
- 2 周过渡期废弃旧接口

#### 3. Recall 返回结构过于工具定制 ⚠️ MEDIUM

**问题**: RecallResult 包含工具特定字段

**位置**: `src/ocmaf/api/recall.py`

**治理建议**:
- 抽象通用 RecallResult
- 工具特定字段通过 extension

#### 4. Scope Mapping 可能漂移 ⚠️ MEDIUM

**问题**: 各工具环境变量映射规则分散

**治理建议**:
- 集中管理映射规则
- 单元测试覆盖所有组合
- 文档化每个工具的映射

#### 5. Injection Policy 缺少全局策略中心 ⚠️ LOW

**问题**: 当前 injection policy 分散在各 adapter

**治理建议**:
- 实现全局策略注册表
- 提供 CLI 配置全局策略
- 监控策略违规

### 技术债治理优先级

| 优先级 | 项目 | 预计工作量 |
|--------|------|----------|
| 1 | Scope Mapping 集中管理 | 1 day |
| 2 | Adapter Contract 文档化 | 0.5 day |
| 3 | 全局 Injection Policy | 1 day |
| 4 | RecallResult 抽象 | 2 days |

---

## 阶段总览

| Phase | 里程碑 | 输入 | 输出 | 预计工作量 | 状态 |
|-------|--------|------|------|----------|------|
| 3A | Adapter Contract 固化 | Claude Code adapter | Contract 规范 | 1-2 days | ✅ 已完成 |
| **3B** | **Codex CLI adapter** | **Phase 3A + Codex CLI** | **Codex CLI adapter** | **2-3 days** | **✅ 已完成** |
| 3C | Cross-tool E2E | Phase 3B | E2E 测试 | 1-2 days | - |
| 4A | Replay/Eval 补强 | Phase 3C | 评估能力 | 3-5 days | - |

---

## 里程碑

| Phase | 里程碑 | 预期交付 | 状态 |
|-------|--------|----------|------|
| Phase 3A | Adapter Contract 固化 | Week 1 | ✅ 已完成 |
| Phase 3B | Codex CLI adapter | Week 2 | ✅ 已完成 |
| Phase 3C | OpenClaw adapter | Week 2-3 | ✅ 已完成 |
| Phase 3D | Tri-tool Integration | Week 3 | ✅ 已完成 |
| Phase 4B | Cross-tool E2E | Week 3-4 | ✅ 已完成 |
| Phase 4C | Real Host Manual Validation | Week 4 | ✅ 已完成 |
| Phase 4D | Claude/Codex Real Host Validation | Week 4 | ✅ 已完成 |
| Phase 4E | Strict Claude/Codex Real Host | Week 4 | ✅ 已完成 |
| **Phase 4F** | **Minimal Real Host Bridge** | **Week 5** | ✅ 已完成 |
| Phase 4G | Real Host Bridge Integration | Week 5 | ✅ 已完成 |
| **Phase 5A** | **Claude Native Hook/Plugin Auto-Memory** | **Week 6** | ✅ 已完成 |
| **Phase 5B** | **Codex Real Host Capability Closure** | **Week 6-7** | ✅ 已完成 |
| **Phase 6A** | **Unified Host Matrix / Product Strategy** | **Week 7** | ✅ 已完成 |
| **Phase 6B** | **OpenClaw Line Closure** | **Week 8** | 🔶 BLOCKED (env) |
| **Phase 6C** | **Minimal Cross-Host UX Spec** | **Week 8** | ✅ 已完成 |
| **Phase 6D** | **Cross-Host UX Output Implementation** | **Week 9** | ✅ 已完成 |
| **Phase 6E** | **Host-Visible Output Integration** | **Week 10** | ✅ 已完成 |
| **Phase 6F** | **Stable Golden Examples** | **Week 11** | ✅ 已完成 |
| **Phase 6G** | **Regression Gate** | **Week 11** | ✅ 已完成 |
| **Phase 7A** | **Unified Entry Point** | **Week 12** | ✅ 已完成 |
| **Phase 7B** | **Automatic Memory Experience** | **Week 12-13** | ✅ 已完成 |
| **Phase 7C** | **Unified Install E2E** | **Week 13** | ✅ 已完成 |
| **Phase 7D** | **Real User Journey Test** | **Week 13** | 🔶 进行中 |
| **Phase 7E** | **Multi-Host Switching UX** | **Week 14** | 🔶 规划中 |
| Phase 4A | Replay/Eval 补强 | Week 4-5 | - |

> **当前状态**: Phase 7C ✅ → Phase 7D 🔶 进行中 → Phase 7E 🔶 规划中 - Real User Journey + Multi-Host Switching

---

## Phase 4F: Minimal Real Host Bridge (Claude/Codex)

**目标**: 实现最小真实宿主桥接路径，让 Claude 和 Codex 能通过真实入口触发 OCMF

### 背景

**问题陈述**:
- Synthetic 测试已通过 (45/45)
- Manual adapter invocation 可用但不是 Real Host
- Phase 4E 验证显示 Claude/Codex 均无法完成 Real Host Validation

**新发现**:
- Codex App 已安装，暴露可执行 `codex` 命令:
  - `which codex` → `/Applications/Codex.app/Contents/Resources/codex`
  - `codex --version` → `codex-cli 0.108.0-alpha.12`
- Claude Code 支持 MCP 机制 (`--mcp-config`)

**Phase 4E 结论**:
- Claude Real Host: ❌ 需要 MCP 服务器实现
- Codex Real Host: ⚠️ 新发现 - App 已安装，命令可用
- OpenClaw: ❌ 环境阻塞

### 为什么单纯 Manual Adapter Invocation 不够

| 维度 | Manual Adapter Invocation | Real Host Validation |
|------|---------------------------|---------------------|
| 触发方式 | 手动调用 Python 函数 | 工具自动触发 |
| 进程上下文 | 当前 Python 进程 | 真实工具进程 |
| 环境变量 | Mock 或手动设置 | 工具真实环境 |
| 自动化程度 | 需外部脚本 | 工具内建 |
| 验证意义 | 功能可用性 | 真实集成验证 |

**结论**: Manual adapter invocation 验证了"代码能工作"，但不能验证"工具能自动触发"

### 什么算"最小真实宿主桥接路径"

**定义**: 通过工具的真实入口（CLI 命令/MCP），让工具在正常使用时自动触发 OCMF recall/remember

**最小路径包含**:
1. **工具入口**: Claude/Codex 可执行命令
2. **桥接机制**: MCP Server / Wrapper Script / Environment Hook
3. **OCMF 调用**: recall (查询前) + remember (响应后)
4. **数据落库**: SQLite 事件存储
5. **Scope 隔离**: tool=user/workspace/project/session

**最小验证目标**:
- 1 次真实 Write (通过工具触发)
- 1 次 Same-tool Recall (通过同一工具触发)
- 1 次 Cross-tool Isolation (工具 A 写入，B 无法召回)

### 为什么优先考虑 MCP Bridge

**MCP 优势**:
1. **官方支持**: Claude/Codex 均原生支持 MCP 协议
2. **标准化**: 统一接口定义 (tools/capabilities)
3. **自动化**: 工具启动时自动加载
4. **隔离性**: 每个工具独立配置
5. **最小侵入**: 不修改工具源码

**等价桥接方式** (备选):
1. **Wrapper Script**: 包装 CLI 命令
2. **Environment Hook**: 通过环境变量触发
3. **IPC/Socket**: 工具进程与 OCMF 通信
4. **File-based Trigger**: 通过文件变化触发

### MCP Bridge / 等价桥接方式的最小约束

**必须满足**:
1. 不修改工具源码
2. 工具启动时自动加载桥接
3. recall 在工具处理前触发
4. remember 在工具响应后触发
5. 所有操作落库可查
6. 支持 scope 隔离
7. 错误时优雅降级

**禁止**:
1. 禁止自动执行高风险操作
2. 禁止绕过 scope 隔离
3. 禁止修改长期记忆对象

### Claude Real Host Bridge 最小目标

| 目标 | 描述 | 验证方式 |
|------|------|----------|
| Write | Claude 触发 remember | 观察事件写入 |
| Recall | Claude 触发 recall | 观察召回结果 |
| Same-tool | Claude→Claude 可召回 | 验证同工具隔离 |

**实现路径**:
1. 实现 MCP Server (ocmf-mcp-server)
2. 配置 `--mcp-config` 指向 MCP Server
3. MCP Server 实现 recall/remember 工具
4. 验证 Claude 交互时自动触发

### Codex Real Host Bridge 最小目标

| 目标 | 描述 | 验证方式 |
|------|------|----------|
| Write | Codex 触发 remember | 观察事件写入 |
| Recall | Codex 触发 recall | 观察召回结果 |
| Same-tool | Codex→Codex 可召回 | 验证同工具隔离 |

**实现路径**:
1. 检查 Codex MCP 支持
2. 实现 MCP Server 或等价桥接
3. 验证 Codex 交互时自动触发

### Claude ↔ Codex Cross-tool 真实 Bridge 验证

| 验证项 | Claude Write | Codex Recall | 预期结果 |
|--------|--------------|--------------|----------|
| 隔离验证 | Claude 写入 | Codex 召回 | ❌ 无结果 |
| 反向验证 | Codex 写入 | Claude 召回 | ❌ 无结果 |
| Same-tool Claude | Claude 写入 | Claude 召回 | ✅ 有结果 |
| Same-tool Codex | Codex 写入 | Codex 召回 | ✅ 有结果 |

### OpenClaw 环境阻塞规范

**当前状态**:
- OpenClaw binary 不存在
- 继续作为环境阻塞项

**记录方式**:
```
OPENCLAW_ENV_STATUS: ❌ BLOCKED (Not Installed)
```

**未来条件**:
- OpenClaw 安装后重新验证

### Strict Evidence 文件要求

**必须产出**:
1. `binary_check.md`: 所有 binary 探测原始输出
2. `claude_real_host.md`: Claude Real Host 证据
3. `codex_real_host.md`: Codex Real Host 证据
4. `cross_tool_real_host.md`: Cross-tool Real Host 证据
5. `evidence.md`: 综合证据 + FINAL_STATUS
6. `known_limits.md`: 已知限制

**每条证据必须包含**:
- 原始命令输出
- 退出码
- 数据库记录 (如有)
- recall 结果输出

### 风险与降级策略

| 风险 | 影响 | 降级策略 |
|------|------|----------|
| MCP Server 实现复杂 | 项目延期 | 降级到 Wrapper Script |
| Codex MCP 不支持 | 无法集成 | 使用 Environment Hook |
| Claude MCP 变化 | 功能失效 | 保持向后兼容 |
| Cross-tool 隔离失败 | 数据泄漏 | 立即告警 + 隔离 |

### Phase 4F 验收标准 (AC)

| AC-ID | 描述 | 验证方式 |
|-------|------|----------|
| AC-BRIDGE-001 | Claude 通过 MCP 触发一次 remember | 观察数据库事件 |
| AC-BRIDGE-002 | Claude 通过 MCP 触发一次 recall | 观察召回结果 |
| AC-BRIDGE-003 | Codex 通过桥接触发一次 remember | 观察数据库事件 |
| AC-BRIDGE-004 | Codex 通过桥接触发一次 recall | 观察召回结果 |
| AC-BRIDGE-005 | Claude→Codex 隔离验证 | 验证无交叉召回 |
| AC-BRIDGE-006 | OpenClaw 环境阻塞记录 | 文档化阻塞状态 |

### Phase 4F 本轮边界

**只做**:
- ✅ Claude 最小真实宿主桥接路径
- ✅ Codex 最小真实宿主桥接路径
- ✅ 至少一条 Claude↔Codex 默认隔离的真实验证
- ✅ Strict evidence 重建
- ✅ OpenClaw 环境阻塞记录

**不做**:
- ❌ 新 adapter (现有 adapter 已足够)

### Phase 4F 执行结果 (实际验证)

**已实现**:
- ✅ MCP Server: `src/ocmaf/bridge/mcp_server.py`
- ✅ Claude Write/Recall: 通过 MCP Server 成功
- ✅ Codex Write/Recall: 通过 MCP Server 成功
- ✅ Cross-tool Isolation: Claude 无法召回 Codex 记忆

**验证结果**:
```
Claude Write:
{"success": true, "event_id": "ba0b7b8c-21a3-4069-8fae-94bde1396af3"}

Claude Recall:
{"success": true, "count": 1, "memories": [...]}

Codex Recall (after Claude Write):
{"success": true, "count": 0, "memories": []}  # Isolation verified
```

**状态**:
- REAL_HOST_STATUS: ⚠️ BRIDGE_IMPLEMENTED
- CLAUDE_REAL_HOST: ⚠️ BRIDGE_IMPLEMENTED
- CODEX_REAL_HOST: ⚠️ BRIDGE_IMPLEMENTED
- OPENCLAW_ENV_STATUS: ❌ BLOCKED
- ❌ 新核心功能
- ❌ Replay/Eval
- ❌ Vector Search
- ❌ Web UI proxy
- ❌ OpenClaw 宿主深度集成
- ❌ 大规模 bridge 平台化

---

## AC 映射 (增补)

| Phase | AC | 说明 |
|-------|-----|------|
| 3A | AC-AD-001~004 | Adapter Contract |
| 3B | AC-AD-Codex-001~004 | Codex CLI adapter |
| 3C | AC-AD-OpenClaw-001~005 | OpenClaw adapter MVP |
| 3D | AC-TRI-001~004 | Tri-tool Integration |
| 4B | AC-E2E-001~005 | Cross-tool E2E |
| 4C | AC-RH-001~006 | Real Host Manual Validation |
| 4D | AC-RH-STRICT-001~006 | Claude/Codex Real Host Validation |
| 4E | AC-STRICT-001~005 | Strict Claude/Codex Real Host |
| **4F** | **AC-BRIDGE-001~006** | **Minimal Real Host Bridge** |
| **4G** | **AC-RHB-001~006** | **Real Host Bridge Integration** |
| 4A | AC-EVAL-001~005 | Replay/Eval |

---

## Phase 4G: Real Host Bridge Integration Validation

### 背景

Phase 4F 完成了 MCP Server 实现，但需要明确区分三种验证类型：

| 验证类型 | 定义 | 例子 |
|----------|------|------|
| **Real Host Bridge Validation** | 通过真实工具进程+MCP配置触发 OCMF | `claude --mcp-config '{"mcpServers":{"ocmf":{...}}}'` |
| **Direct MCP Server Invocation** | 直接运行 MCP Server，不通过工具的 MCP 配置 | `echo '...' | python3 -m ocmaf.bridge.mcp_server --tool claude-code` |
| **Synthetic Test** | pytest 自动执行 | `pytest tests/` |

**Phase 4F 状态**: MCP Server 已实现，但验证主要通过 Direct MCP Server Invocation 方式，未完成 Real Host Bridge Validation。

### 本轮目标

- 实现并验证真实 `claude --mcp-config` 路径触发 OCMF
- 实现并验证真实 `codex` MCP 配置路径触发 OCMF
- 生成严格可审计的 Real Host Bridge 证据
- 验证工具默认隔离在真实桥接路径下仍然有效

### 严格边界定义

**Real Host Bridge Validation** (本轮目标):
```
✅ claude --mcp-config '{"mcpServers":{"ocmf":{"command":"python3","args":["-m","ocmaf.bridge.mcp_server","--tool","claude-code"]}}}'
✅ codex mcp add ocmf python3 -m ocmaf.bridge.mcp_server --tool codex-cli
```

**Direct MCP Server Invocation** (不等于 Real Host):
```
⚠️ echo '{"method":"tools/call",...}' | python3 -m ocmaf.bridge.mcp_server --tool claude-code
```
- 这是 MCP Server 的功能验证
- 不代表真实工具能触发

**Synthetic Test** (不等于 Real Host):
```
✅ pytest tests/ -v
```
- 自动化测试，不经过真实工具进程

### Claude Real Bridge 场景

**目标**: 通过真实 Claude Code 进程 + MCP 配置触发 OCMF

**步骤**:
1. 准备 MCP Server 配置 JSON
2. 使用 `claude --mcp-config <json>` 启动 Claude
3. 在 Claude 会话中调用 `/remember` 或 `ocmf_remember` 工具
4. 验证数据库事件写入 (tool='claude-code')
5. 调用 `/recall` 或 `ocmf_recall` 工具
6. 验证召回结果

**证据要求**:
- 真实 `claude --mcp-config` 命令
- 真实工具输出
- 数据库事件记录 (event_id, source_tool='claude-code')
- 召回结果输出

### Codex Real Bridge 场景

**目标**: 通过真实 Codex 进程 + MCP 配置触发 OCMF

**步骤**:
1. Codex CLI 支持 `mcp add` 命令添加 MCP 服务器
2. 使用 Codex 添加 OCMF MCP Server
3. 在 Codex 会ocmf_remember话中调用 `` 工具
4. 验证数据库事件写入 (tool='codex-cli')
5. 调用 `ocmf_recall` 工具
6. 验证召回结果

**证据要求**:
- 真实 `codex mcp add` 命令
- 真实工具输出
- 数据库事件记录 (event_id, source_tool='codex-cli')
- 召回结果输出

### Cross-tool Real Bridge 隔离验证

**目标**: 在真实桥接路径下验证 Claude ↔ Codex 默认隔离仍然有效

**步骤**:
1. 通过 Claude 写入记忆 (tool='claude-code')
2. 通过 Codex 尝试召回
3. 验证 Codex 无法召回 Claude 记忆 (count=0)
4. 反向验证: Codex 写入 → Claude 召回
5. 验证 Claude 无法召回 Codex 记忆

**证据要求**:
- 两条隔离路径的完整命令和输出
- 数据库查询结果证明 tool 字段隔离

### Strict Evidence 文件要求

| 文件 | 内容 |
|------|------|
| `binary_check.md` | 当前机器 Claude/Codex/OpenClaw binary 状态 |
| `claude_real_host_bridge.md` | 真实 claude --mcp-config 路径证据 |
| `codex_real_host_bridge.md` | 真实 codex MCP 配置路径证据 |
| `cross_tool_real_host.md` | 真实桥接路径下的隔离验证 |
| `evidence.md` | 综合证据与最终状态 |
| `known_limits.md` | 已知限制与三种验证类型区分 |

### 验收标准 (AC)

| AC-ID | 描述 | 验证方式 |
|-------|------|----------|
| AC-RHB-001 | Claude 通过 `claude --mcp-config` 触发一次 remember | 数据库事件 + 工具输出 |
| AC-RHB-002 | Claude 通过真实 MCP 配置触发一次 recall | 召回结果 + 数据库 |
| AC-RHB-003 | Codex 通过 `codex mcp add` 触发一次 remember | 数据库事件 + 工具输出 |
| AC-RHB-004 | Codex 通过真实 MCP 配置触发一次 recall | 召回结果 + 数据库 |
| AC-RHB-005 | Claude→Codex 真实路径隔离验证 | 双向隔离测试 |
| AC-RHB-006 | 三种验证类型严格区分 | 文档化边界 |

### 本轮边界

**只做**:
- ✅ 真实 claude --mcp-config 路径验证
- ✅ 真实 codex MCP 配置路径验证
- ✅ 真实路径下的 cross-tool 隔离
- ✅ Strict evidence 重建

**不做**:
- ❌ 新 adapter
- ❌ 新核心功能
- ❌ Replay/Eval 扩展
- ❌ Vector Search
- ❌ OpenClaw 宿主集成

### 风险与降级

| 风险 | 影响 | 降级策略 |
|------|------|----------|
| Claude MCP 配置格式变化 | 无法触发 | 保持向后兼容 |
| Codex MCP 支持限制 | 无法触发 | 使用 Environment Hook |
| MCP Server stdio 协议问题 | 通信失败 | 检查日志，降级到直接调用 |

---

## Phase 5A: Claude Native Hook/Plugin Auto-Memory

**目标**: 实现真正的宿主原生 hooks/plugin 自动触发 remember/recall，而非继续停留在 system-prompt 半自动方案

### 背景

**问题陈述**:
- Phase 018-019 实现了 Claude Real Host Proof 和 Native Auto-Memory MVP
- 但当前 "Native Auto-Memory" 的核心是 `--system-prompt` 注入
- System-prompt 需要用户主动启动会话时加载，且依赖 Claude 遵循指令
- 这不等同于严格意义上的"方式 A：宿主原生 hooks/plugin 自动触发"

### 三种自动化方式边界定义

| 方式 | 定义 | 触发机制 | 可靠性 |
|------|------|----------|--------|
| **方式 A: Host-Native Hook/Plugin** | Claude 进程生命周期内的原生 hook 点 | 用户操作自动触发，无需显式调用工具 | 最高 |
| **方式 B: System-Prompt** | 通过 --system-prompt 注入行为指令 | 依赖 Claude 遵循指令，可能被忽略 | 中等 |
| **方式 C: Manual MCP** | 用户手动输入 ocmf_remember/ocmf_recall | 完全依赖用户主动 | 最低 |

**关键区分**:
- **方式 A** = 用户无感知自动触发（像 IDE 插件一样）
- **方式 B** = 用户启动时加载指令，但行为仍需 Claude "配合"
- **方式 C** = 用户完全手动操作

### 为什么 System-Prompt 是过渡方案

1. **非确定性**: Claude 可能不遵循所有自动记忆指令
2. **需要显式加载**: 每次启动需要指定 --system-prompt
3. **非原生**: 属于"注入指令"而非"原生能力"
4. **无 hook 点**: 无法在特定事件（如消息发送、任务完成）自动触发

### Claude 原生 Hook/Plugin 能力探测

#### 可用能力 (Claude 2.1.78)

| 能力 | 状态 | 说明 |
|------|------|------|
| `--plugin-dir` | ✅ 可用 | 插件目录加载 |
| `--debug hooks` | ✅ 可用 | Hook 调试模式 |
| `--pre-hook` | ❌ 不可用 | 无此选项 |
| `--post-hook` | ❌ 不可用 | 无此选项 |

#### 实际可用路径分析

**路径 1: Plugin 模式**
- Claude 支持 `--plugin-dir` 加载插件
- 需要研究插件结构和触发机制
- **状态**: 待探索

**路径 2: Debug Hooks**
- `claude --debug hooks` 显示 hooks 相关信息
- 可能是观察模式而非主动触发
- **状态**: 待探索

**路径 3: 环境变量注入**
- 通过环境变量传递记忆行为
- **状态**: 待探索

### Phase 5A 验收标准 (AC)

| AC-ID | 描述 | 验证方式 |
|-------|------|----------|
| AC-CHA-001 | 明确区分方式 A/B/C 的边界 | 文档化定义 |
| AC-CHA-002 | 探索 Claude 原生 plugin/hook 触发机制 | 实际命令输出 |
| AC-CHA-003 | 若 plugin/hook 不可用，明确降级记录 | 诚实记录限制 |
| AC-CHA-004 | 不把 system-prompt 方案标记为方式 A 成功 | 证据与文档一致 |
| AC-CHA-005 | 完成自动化验证证据 (若方式 A 可行) | 真实命令+输出+数据库 |

### Phase 5A 执行任务

1. **探索 Plugin 机制**
   - 研究 `--plugin-dir` 的实际工作方式
   - 查找 Claude 插件格式和示例
   - 验证插件是否能自动触发行为

2. **探索 Hook 机制**
   - 运行 `claude --debug hooks` 探索可用 hooks
   - 确认是否有消息前/后 hook 可用
   - 验证 hook 触发自动记忆的可行性

3. **诚实记录降级点**
   - 若 plugin/hook 均不可用于自动记忆
   - 明确记录当前最优方案（system-prompt）的限制
   - 不虚假标记为"方式 A 成功"

4. **验证证据**
   - 若实现自动触发: 真实命令 + 自动生成的事件 + SQLite 验证
   - 若降级: 明确标注为"方式 B"并记录原因

### Phase 5A 本轮边界

**只做**:
- ✅ Claude 原生 hooks/plugin 自动化探索
- ✅ 三种方式边界明确定义
- ✅ System-prompt 诚实标记为方式 B（非方式 A）
- ✅ 证据重建

**不做**:
- ❌ Codex 自动化（本轮只保持 proof/handshake）
- ❌ 新 memory core 功能
- ❌ Replay/Eval
- ❌ Vector Search
- ❌ Web UI proxy
- ❌ Cross-tool real host
- ❌ OpenClaw 深度集成

### 风险与降级

| 风险 | 影响 | 降级策略 |
|------|------|----------|
| Claude 无原生 auto-trigger hooks | 无法实现方式 A | 降级到 system-prompt (方式 B)，诚实记录 |
| Plugin 机制不支持自动触发 | 无法实现方式 A | 记录为"待探索"，保持手动 MCP 可用 |
| 探索时间过长 | 进度延迟 | 设定 1 周探索上限，超时诚实记录 |

---

## Phase 5B: Codex Real Host Capability Closure

**目标**: 完成 Codex 路线的真实宿主能力收敛，参照 Claude 路线的收口模式，给出 Codex 的最终判定

### 背景

**Claude 路线已收口**:
- Method A (native auto-trigger) = ✅ PASS (background collection)
- Pure Method A (native context injection) = ❌ FAIL
- Method B (system-prompt assisted) = ✅ PASS
- Production path = A + B

**Codex 路线待验证**:
- Codex 是否存在 host-native auto-trigger 路径？
- Codex MCP 是否可用？
- Codex 的最终 production path 是什么？

### Claude vs Codex 对照

| 维度 | Claude | Codex |
|------|--------|-------|
| Real host proof | ✅ 已完成 | 🔶 待验证 |
| MCP support | ✅ 可用 | 🔶 待验证 |
| Native auto-trigger | ✅ SessionStart/SessionEnd | 🔶 待验证 |
| Native context injection | ❌ 不支持 | 🔶 待验证 |
| System-prompt | ✅ 可用 | 🔶 待验证 |
| Production path | A + B | 🔶 待判定 |

### Phase 5B 验收标准 (AC)

| AC-ID | 描述 | 验证方式 |
|-------|------|----------|
| AC-CDX-001 | Codex real host proof 完成 | 真实 CLI 输出 + SQLite |
| AC-CDX-002 | Codex MCP tool 可发现 | /mcp 输出 |
| AC-CDX-003 | Codex MCP tool 可调用 | 真实 remember + recall |
| AC-CDX-004 | Codex native auto-trigger 边界明确 | 文档化 |
| AC-CDX-005 | Codex production path 判定 | Method A/B/C 分类 |

### Phase 5B 执行任务

1. **Codex real host proof**
   - 验证 `codex` 命令入口可用
   - 验证 Codex MCP 配置可用
   - 完成一次 real host remember
   - 完成一次 real host recall
   - SQLite 对账

2. **Codex native automation boundary**
   - 探索 Codex hooks/plugin 机制
   - 验证是否存在 native auto-trigger
   - 验证 native context injection 是否可能

3. **Codex production path 判定**
   - 参照 Claude 模式
   - 明确 Method A/B/C 边界
   - 输出最终 production path

### Phase 5B 本轮边界

**只做**:
- ✅ Codex real host proof
- ✅ Codex native automation boundary 验证
- ✅ Codex 最终 production path 判定
- ✅ evidence / known_limits 更新

**不做**:
- ❌ Claude 新实验（已收口）
- ❌ OpenClaw 深度集成
- ❌ Replay/Eval
- ❌ Vector Search
- ❌ Web UI proxy
- ❌ Cross-tool 产品化

### 风险与降级

| 风险 | 影响 | 降级策略 |
|------|------|----------|
| Codex MCP 不可用 | 无法实现 real host | 使用 environment variable 或 direct invocation |
| Codex hooks 限制 | 无法实现 native auto-trigger | 参照 Claude 模式，使用 B 或 C |
| Codex 行为异常 | 验证失败 | 记录限制，继续判定 |

### 与 Claude 路线的关系

- Claude 路线结论作为参照模式
- 不期望 Codex 与 Claude 完全一致
- 每个工具独立判定最终 production path
- 共同目标是实现跨工具统一记忆

---

## Phase 6A: Unified Host Matrix / Product Strategy Closure

**目标**: 整合 Claude / Codex / OpenClaw 三宿主验证结论，输出统一产品层策略，明确各宿主生产路径和后续工程优先级

### 背景

**Claude 路线已收口**:
- Method A1 (native auto-trigger) = ✅ VERIFIED (background collection)
- Method A2 (native context injection) = ❌ NOT SUPPORTED
- Method B (system-prompt assisted) = ✅ VERIFIED
- Method C (manual MCP) = ✅ VERIFIED
- **Production path = A1 + B** (A1 for collection, B for recall)

**Codex 路线已收口**:
- Method A (native auto-trigger) = ❌ NOT AVAILABLE (no hooks subsystem)
- Method B (system-prompt) = ⚠️ UNTESTED
- Method C (manual MCP) = ✅ VERIFIED
- **Production path = C** (fully manual MCP calls)

**OpenClaw 路线**:
- Status = ⚠️ 环境阻塞，未完成同等级验证
- 保留当前状态说明，不深挖

### Host Capability Matrix

| 维度 | Claude | Codex | OpenClaw |
|------|--------|-------|----------|
| **Real host proof** | ✅ | ✅ | ⚠️ |
| **MCP 可用** | ✅ | ✅ | ⚠️ |
| **Native hooks** | ✅ | ❌ | ⚠️ |
| **Auto-trigger (A1)** | ✅ | ❌ | ⚠️ |
| **Context injection (A2)** | ❌ | ❌ | ⚠️ |
| **System-prompt (B)** | ✅ | ⚠️ | ⚠️ |
| **Manual MCP (C)** | ✅ | ✅ | ⚠️ |
| **Production path** | **A1 + B** | **C** | **TBD** |

### Method Taxonomy (正式定义)

#### Method A1: Native Auto-Trigger (Background Collection)

| Property | Value |
|----------|-------|
| **Name** | A1 - Native auto-trigger |
| **Mechanism** | Host hooks call tools automatically |
| **Trigger** | Automatic (SessionStart, SessionEnd, etc.) |
| **User Input Required** | ❌ NO |
| **Claude Uses Results** | ❌ NO (side process) |
| **Memory Storage** | ✅ YES |
| **Supported hosts** | Claude only |

#### Method A2: Native Context Injection

| Property | Value |
|----------|-------|
| **Name** | A2 - Native context injection |
| **Mechanism** | Hook outputs affect LLM context |
| **Trigger** | Automatic |
| **Claude Uses Results** | ❌ NO |
| **Supported hosts** | None |

**A2 is NOT SUPPORTED in any known host.**

#### Method B: System-Prompt Assisted

| Property | Value |
|----------|-------|
| **Name** | B - System-prompt assisted |
| **Mechanism** | Instructions injected via system prompt |
| **Trigger** | Host follows injected instructions |
| **User Input Required** | ❌ NO (once configured) |
| **Host Uses Results** | ✅ YES |
| **Memory Storage** | ⚠️ Depends on host compliance |
| **Supported hosts** | Claude (verified), Codex (untested) |

#### Method C: Manual MCP

| Property | Value |
|----------|-------|
| **Name** | C - Manual MCP |
| **Mechanism** | User/agent explicitly calls ocmf_* tools |
| **Trigger** | Explicit tool invocation |
| **User Input Required** | ✅ YES |
| **Host Uses Results** | ✅ YES |
| **Supported hosts** | Claude (verified), Codex (verified) |

### Production Path Per Host

#### Claude - Recommended: A1 + B

| Phase | Method | Purpose |
|-------|--------|---------|
| Memory collection | A1 | Automatic background capture (hooks) |
| Context-aware recall | B | Claude uses memories in conversation |

**Why**: A1 provides automatic background collection without user input. B provides seamless recall where Claude actively uses memories.

**Neither Pure A nor Pure B is sufficient**:
- Pure A1: Claude doesn't read hook outputs (A2 not supported)
- Pure B: No automatic collection

#### Codex - Recommended: C

| Phase | Method | Purpose |
|-------|--------|---------|
| Memory collection | C | Manual ocmf_remember calls |
| Memory recall | C | Manual ocmf_recall calls |

**Why**: Codex has no native hooks. MCP is the only extension mechanism, requiring explicit tool calls.

**Note**: Method B (system-prompt) was not tested and could potentially enable semi-automatic behavior.

#### OpenClaw - Status: TBD

OpenClaw verification was blocked by environment issues. Production path to be determined pending resolution.

### Unified Product Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OCMF Memory Fabric                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Claude    │  │   Codex     │  │  OpenClaw   │        │
│  │  A1 + B     │  │     C       │  │    TBD      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                │                │                 │
│         ▼                ▼                ▼                 │
│  ┌─────────────────────────────────────────────────┐       │
│  │          Unified SQLite Event Store               │       │
│  │  source_tool: claude-code | codex-cli | openclaw │       │
│  └─────────────────────────────────────────────────┘       │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────┐       │
│  │     Memory Objects / Retrieval / Scoring          │       │
│  └─────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Recommended User Experience

#### For Claude Users

1. **Install**: `codex mcp add ocmf -- <wrapper>` (if using Codex)
2. **Configure**: Add OCMF hooks in `~/.claude/settings.json`
3. **Use**: Works automatically - memories captured and recalled without explicit calls
4. **Monitor**: Check `~/.claude/logs/` for hook execution logs

#### For Codex Users

1. **Install**: `codex mcp add ocmf -- ~/bin/ocmaf-codex`
2. **Use**: Manually call `ocmf_remember` after sessions
3. **Recall**: Manually call `ocmf_recall` at session start
4. **Future**: System-prompt injection could enable semi-automatic behavior

#### For OpenClaw Users

Status: TBD pending environment resolution.

### Engineering Priorities (Next Steps)

| Priority | Task | Rationale |
|----------|------|----------|
| P1 | Codex Method B testing | Could enable semi-auto for Codex |
| P1 | OpenClaw environment resolution | Unblock third host |
| P2 | Cross-tool memory sharing | User stories require it |
| P2 | Replay/eval framework | Validate scoring quality |
| P3 | Vector search integration | Performance at scale |
| P3 | Web UI proxy | UX improvement |

### What NOT To Do Next

- ❌ More single-host capability exploration (Claude/Codex done)
- ❌ New adapters for unannounced hosts
- ❌ Large-scale architecture changes
- ❌ Vector search before cross-tool is validated
- ❌ UI proxy before core is stable

### Known Limits

| Host | Limitation | Workaround |
|------|-----------|------------|
| Claude A2 | Hook outputs don't affect context | Use Method B for recall |
| Codex | No native hooks | Use Method C (manual) |
| Codex B | Not tested | Test system-prompt injection |
| OpenClaw | Environment blocked | Resolve env issues |

### Phase 6A 本轮边界

**只做**:
- ✅ Host capability matrix 定稿
- ✅ Production path per host 确定
- ✅ Method taxonomy 文档化
- ✅ Product strategy 明确
- ✅ Evidence/known_limits 同步

**不做**:
- ❌ New host experiments
- ❌ New core functionality
- ❌ Replay/eval implementation
- ❌ Vector search
- ❌ Web UI proxy
- ❌ OpenClaw deep integration

---

## Phase 6B: OpenClaw Line Closure

**目标**: 完成 OpenClaw 路线的最终收口判断，补全三宿主矩阵的最后一块

### 背景

**当前宿主状态**:

| Host | Status | Production Path |
|------|--------|----------------|
| Claude | ✅ CLOSED | A1 + B |
| Codex | ✅ CLOSED | C |
| OpenClaw | ⚠️ BLOCKED | TBD |

**OpenClaw 历史**:
- 早期 MVP 已完成 (`runs/006-openclaw-mvp/`)
- Real host proof 多次尝试未通过
- 环境阻塞点：配置/权限/命令入口问题
- 需要重新评估阻塞原因并解决

### OpenClaw Method Boundary 定义

| Method | Status | Notes |
|--------|--------|-------|
| A1 - Native auto-trigger | ⚠️ UNKNOWN | 未探索 |
| A2 - Native context injection | ⚠️ UNKNOWN | 未探索 |
| B - System-prompt | ⚠️ UNKNOWN | 未探索 |
| C - Manual MCP | ⚠️ UNKNOWN | 未探索 |
| **Production path** | **TBD** | 需要 real host proof 后判定 |

**Position**: 如果 OpenClaw 有原生 hooks，则可能是 Method A 候选宿主（类似 Claude）。但当前无法确认。

### OpenClaw Real Host Proof 最小目标

1. **确认命令入口**: `which openclaw` 或等价命令
2. **确认 MCP/hooks 可用性**: OpenClaw 支持什么扩展机制
3. **一次 real remember**: 通过真实 OpenClaw 宿主调用
4. **一次 real recall**: 通过真实 OpenClaw 宿主调用
5. **SQLite 对账**: source_tool='openclaw' 落库

### OpenClaw Real Host Proof 验收标准 (AC)

| AC-ID | 描述 | 验证方式 |
|-------|------|----------|
| AC-OCL-001 | OpenClaw 命令入口可用 | `which openclaw` + version |
| AC-OCL-002 | OpenClaw MCP/extension 可用 | 配置或发现 |
| AC-OCL-003 | Real remember 落库 | 真实调用 + SQLite |
| AC-OCL-004 | Real recall 召回 | 真实调用 + 匹配 |
| AC-OCL-005 | Method boundary 明确 | A/B/C 分类 |
| AC-OCL-006 | Production path 判定 | 最终路径确定 |

### Phase 6B 本轮边界

**只做**:
- ✅ OpenClaw real host proof
- ✅ OpenClaw method boundary 验证
- ✅ OpenClaw final production path 判定
- ✅ evidence/known_limits 更新

**不做**:
- ❌ Claude 新实验（已收口）
- ❌ Codex 新实验（已收口）
- ❌ 新 core 功能
- ❌ Replay/Eval
- ❌ Vector search

### 风险与降级

| 风险 | 影响 | 降级策略 |
|------|------|----------|
| OpenClaw 仍无法完成 real host proof | 无法收口 | 记录阻塞原因，维持 TBD |
| OpenClaw 无 MCP/hooks | 无法自动化 | 标记为"manual only"候选 |
| 环境问题无法解决 | 阻塞 | 升级问题，明确 OpenClaw 支持状态 |

---

## Phase 6C: Minimal Cross-Host UX Spec

**目标**: 制定跨宿主场景下的最小 UX 规范，解决"同一记忆被多宿主写入/召回"时的展示问题

### 背景

**当前状态**:
- Claude ✅ (A1+B) 写入 events
- Codex ✅ (C) 写入 events
- OpenClaw ⚠️ (TBD) 待写入

**问题**:
1. 同一项目被 Claude 和 Codex 都写过记忆，recall 时如何展示 provenance？
2. 不同宿主写入的同一内容冲突时，如何解释？
3. 用户如何理解"source_tool"字段的含义？
4. Cross-host recall 的 UX 应该如何描述？

### Cross-Host UX 规范范围

#### 1. Provenance Display（来源展示）

Recall 结果中应明确显示每条记忆的来源宿主：

```json
{
  "memory_id": "uuid-123",
  "content": "...",
  "source_tool": "claude-code",    // ← 必须展示
  "source_host": "Claude",           // ← 友好名称
  "event_type": "chat_turn"
}
```

**规则**:
- recall 结果必须包含 source_tool
- UI 应将 source_tool 映射为友好名称 (claude-code → "Claude", codex-cli → "Codex")
- 按宿主分组展示时必须有明确分隔

#### 2. Conflict Explanation（冲突解释）

当 recall 返回多个 source 的冲突内容时：

```json
{
  "conflict_detected": true,
  "candidates": [
    {"source_tool": "claude-code", "content": "...", "timestamp": "..."},
    {"source_tool": "codex-cli", "content": "...", "timestamp": "..."}
  ]
}
```

**规则**:
- 检测到 content 不一致时，标记 conflict_detected
- 同时展示所有冲突来源及其时间戳
- 让用户决定使用哪个

#### 3. Recall Hit Explanation（召回命中解释）

explain(memory_id) 必须说明为什么这条记忆被召回：

```json
{
  "memory_id": "uuid-123",
  "recall_query": "project constraints",
  "keywords_matched": ["project", "constraints"],
  "scope_match": {"project": "ocmf"},
  "reason": "keyword match + scope match"
}
```

**规则**:
- recall 返回的每条记忆必须有 explain 可查
- explain 必须说明匹配原因（keyword / scope / time）
- 跨宿主recall 需说明哪些宿主写入过

#### 4. Source Tool 字段规范

| source_tool 值 | 友好名称 | 说明 |
|----------------|----------|------|
| claude-code | Claude | Claude Code 宿主 |
| codex-cli | Codex | Codex CLI 宿主 |
| openclaw | OpenClaw | OpenClaw 宿主 |
| synthetic | Synthetic | 直接模块调用（非真实宿主） |

**规则**:
- 所有事件必须有 source_tool
- synthetic 测试产生的 source_tool='synthetic'
- 真实宿主写入的 source_tool 对应宿主名

### Cross-Host Recall 场景

#### Scenario 1: Claude 写入 → Codex 召回

```
User works on OCMF project in Claude
→ Events stored with source_tool='claude-code'

User switches to Codex
→ Calls ocmf_recall("OCMF project constraints")
→ Returns memories from Claude

UX: "From Claude: OCMF constraints..."
```

#### Scenario 2: Cross-host 冲突

```
Claude remembers: "Use pytest for testing"
Codex remembers: "Use unittest for testing"

ocmf_recall("testing framework")
→ conflict_detected: true
→ Show both with timestamps
→ User resolves
```

### Phase 6C 本轮边界

**只做**:
- ✅ Cross-host UX 规范编写（spec 格式）
- ✅ Provenance / conflict / explain 规则定义
- ✅ source_tool 字段规范
- ✅ 更新 docs/spec.md 中的相关章节

**不做**:
- ❌ 实现任何 UI 组件
- ❌ 实现任何 cross-host 逻辑
- ❌ replay/eval
- ❌ vector search
- ❌ Web UI proxy

### 与 spec.md 的关系

Phase 6C 的输出将更新 `docs/spec.md` 中的以下章节：
- FR8 检索链路（增加 cross-host 展示规则）
- FR9 explain()（明确 explain 必须包含 provenance）
- FR13 作用域隔离（增加 source_tool 维度）

---

## Phase 6D: Cross-Host UX Output Implementation

**目标**: 把已完成的 cross-host UX spec 从文档推进到最小可运行实现，优先落地 recall / explain 输出层

### 背景

Phase 6C 已完成 cross-host UX 规范编写（FR-047~FR-058 已写入 spec.md）。Phase 6D 的核心任务是把这套规范落到实际代码实现，使 recall / explain 输出能够正确展示 provenance 和 conflict 信息。

### 实现范围

#### recall 输出增强

| 规范引用 | 实现目标 | 状态 |
|----------|----------|------|
| FR-047 | recall 结果必须包含 source_tool 字段 | 待实现 |
| FR-048 | source_tool 映射到 friendly name | 待实现 |
| FR-049 | recall 结果按 source 分组（可选） | 待实现 |

**recall 输出目标格式**:
```python
{
    "query": "testing framework",
    "results": [
        {
            "memory_id": "uuid-1",
            "content": "Testing framework: pytest",
            "source_tool": "claude-code",
            "source_host_friendly": "Claude",
            "timestamp": "2026-03-20T10:30:00Z"
        },
        {
            "memory_id": "uuid-2",
            "content": "Testing framework: unittest",
            "source_tool": "codex-cli",
            "source_host_friendly": "Codex",
            "timestamp": "2026-03-20T09:15:00Z"
        }
    ],
    "conflict_detected": true,
    "candidates": [...]
}
```

#### explain 输出增强

| 规范引用 | 实现目标 | 状态 |
|----------|----------|------|
| FR-053 | explain() 必须返回 match_reasons | 待实现 |
| FR-054 | explain() 必须返回 source_tool / source_host_friendly | 待实现 |
| FR-055 | cross-host explain() 显示 also_written_by | 待实现 |

**explain 输出目标格式**:
```python
{
    "memory_id": "uuid-123",
    "recall_query": "OCMF constraints",
    "match_reasons": [
        {"type": "keyword", "matched": ["OCMF", "constraints"]},
        {"type": "scope", "matched": {"project": "ocmf"}}
    ],
    "source_tool": "claude-code",
    "source_host_friendly": "Claude",
    "event_timestamp": "2026-03-20T10:30:00Z",
    "explain": "Matched keywords 'OCMF', 'constraints' and scope project='ocmf'",
    "also_written_by": ["codex-cli"]  # if applicable
}
```

#### conflict detection 最小实现

| 规范引用 | 实现目标 | 状态 |
|----------|----------|------|
| FR-050 | 检测同一 entity 不同 source 的 content 冲突 | 待实现 |
| FR-051 | conflict response 包含所有 candidates | 待实现 |
| FR-052 | 用户负责 conflict resolution | N/A (UX 决策) |

**conflict detection 最小实现策略**:
1. Recall 时，检查候选结果的 content hash 是否相同但 content 不同
2. 若检测到冲突，设置 `conflict_detected: true`
3. 在 `candidates` 字段中返回所有冲突的记忆
4. **不自动消解**，由用户决定（FR-052）

#### source_tool 展示规范落地

| source_tool | Friendly Name | 展示要求 |
|-------------|---------------|----------|
| claude-code | Claude | 始终展示 friendly name |
| codex-cli | Codex | 始终展示 friendly name |
| openclaw | OpenClaw | 始终展示 friendly name（当可用时） |
| synthetic | Synthetic (Test) | 明确标注为测试数据 |

**展示规范**:
- 永远不显示 raw source_tool，必须映射到 friendly name
- Synthetic 数据必须与真实 host 数据明确区分

### implemented vs specified-only 边界说明

#### 本轮实现（Phase 6D）

| 功能 | 状态 | 说明 |
|------|------|------|
| recall 输出增加 source_tool | ✅ 实现 | 返回时包含字段 |
| recall 输出增加 source_host_friendly | ✅ 实现 | friendly name 映射 |
| recall 按 source 分组 | ❌ 不做 | Phase 6D 可选优化，Phase 2 再做 |
| explain 输出增加 match_reasons | ✅ 实现 | keyword/scope/time |
| explain 输出增加 provenance | ✅ 实现 | source_tool + friendly |
| explain 输出增加 also_written_by | ✅ 实现 | cross-host 场景 |
| conflict detection | ✅ 实现 | 最小实现（检测+响应） |
| conflict resolution | ❌ 不做 | 留待用户决策（UX） |

#### spec 中指定但本轮不实现

| 规范引用 | 内容 | 原因 |
|----------|------|------|
| FR-049 | 按 source 分组展示 | Phase 2 UX 优化项 |
| FR-052 | 用户 resolution UX | 属于 UI 层，Phase 2 再做 |
| FR-055 cross-host context | also_written_by 详情 | 可延后 |

### 本轮验收标准（AC）

| AC ID | 验收条件 | 验证方法 |
|--------|----------|----------|
| AC-XHOST-IMPL-001 | recall 结果包含 source_tool | 运行 recall，检查返回 JSON |
| AC-XHOST-IMPL-002 | recall 结果包含 source_host_friendly | 运行 recall，检查 friendly name |
| AC-XHOST-IMPL-003 | recall 同一 entity 不同 source 可检测 | synthetic 测试：两 host 写同一 entity |
| AC-XHOST-IMPL-004 | conflict_detected=true 当冲突存在 | synthetic 测试触发冲突 |
| AC-XHOST-IMPL-005 | explain() 返回 match_reasons | 运行 explain()，检查返回 |
| AC-XHOST-IMPL-006 | explain() 返回 source_tool | 运行 explain()，检查返回 |
| AC-XHOST-IMPL-007 | synthetic 记忆显示 Synthetic (Test) | synthetic recall 返回 friendly name |

### Phase 6D 本轮边界

**只做**:
- ✅ recall 输出增加 cross-host 字段（source_tool, source_host_friendly）
- ✅ explain 输出增加 provenance（match_reasons, source_tool）
- ✅ conflict detection 最小实现
- ✅ evidence / known_limits 更新

**不做**:
- ❌ OpenClaw 新实验（Phase 6B 已 blocked）
- ❌ Claude/Codex 新边界实验（已收口）
- ❌ Web UI 实现（属于 Phase 2）
- ❌ replay/eval（属于后续阶段）
- ❌ vector search（属于后续阶段）
- ❌ memory core 大改（本轮只改输出格式）

### 与 Phase 6C spec 的关系

Phase 6D 是 Phase 6C 规范的落地实现。spec.md 中的 FR-047~FR-058 是 Phase 6D 的实现目标：

| Spec 章节 | Phase 6D 实现任务 |
|----------|-------------------|
| FR-047 (provenance display) | recall 增加 source_tool 字段 |
| FR-048 (friendly name) | recall 增加 source_host_friendly 映射 |
| FR-050 (conflict detection) | recall 增加 conflict_detected |
| FR-051 (conflict response) | recall 增加 candidates 字段 |
| FR-053 (explain match_reasons) | explain 增加 match_reasons |
| FR-054 (explain provenance) | explain 增加 source_tool/friendly |
| FR-055 (cross-host explain) | explain 增加 also_written_by |

---

## Phase 6E: Host-Visible Output Integration

**目标**: 把 Phase 6D 完成的 API 输出层，推进到用户可见的输出展示层

### 背景

Phase 6D 已完成 recall / explain API 的 cross-host 字段增强（source_tool, friendly name, timestamp, match_reasons, conflict_detected, candidates 等）。Phase 6E 的核心任务是把这些 API 字段真正展示到用户可见的输出中。

**Phase 6D API 增强已完成**:
- recall 输出: source_tool, source_host_friendly, timestamp, conflict_detected, candidates
- explain 输出: match_reasons, source_tool, source_host_friendly, event_timestamp, also_written_by, explain text

**Phase 6E 用户可见输出目标**:
- 在 Claude / Codex 宿主路径中可见这些字段
- 不是 Web UI，而是宿主 CLI 的自然输出格式
- 最小化干扰，正常使用流程中自然可见

### 两条宿主路径的落地策略

#### Claude 路径 (A1 + B)

Claude 使用 Method A1（hooks 自动收集）+ Method B（system-prompt recall）。用户不直接调用 recall/explain，而是通过对话自然获得记忆。

**落地策略**:
1. Claude hooks 的 SessionStart/SessionEnd 自动调用 ocmf_remember
2. Claude 在对话中通过 system-prompt 注入 recall 结果
3. **本轮任务**: 确保注入的 recall 结果包含 provenance 信息

**用户可见形式**:
```
[Claude 自动] Recall 结果:
- "OCMF uses pytest" (From Claude, 10:30)
- "OCMF constraints: pytest, type hints" (From Claude, 10:25)
```
或当 conflict 存在时:
```
⚠️ CONFLICT: 不同宿主对同一问题有不同结论
- "Testing: pytest" (From Claude)
- "Testing: unittest" (From Codex)
```

#### Codex 路径 (C)

Codex 使用 Method C（手动 MCP 调用）。用户显式调用 `codex recall "query"` 或 `codex remember "content"`。

**落地策略**:
1. Codex MCP tool `ocmf_recall` 返回 JSON
2. Codex CLI 输出格式化后的结果
3. **本轮任务**: 确保返回的 JSON 包含 provenance 字段，并格式化展示

**用户可见形式**:
```
$ codex recall "testing framework"
---
From Claude:
  • "Testing framework: pytest" (2026-03-22 10:30)

From Codex:
  • "Testing framework: unittest" (2026-03-22 09:15)
---
⚠️ CONFLICT DETECTED
```

### recall 用户可见输出目标

**目标格式** (两种宿主路径):

| 宿主 | 输出形式 | 示例 |
|------|----------|------|
| Claude | System-prompt 注入文本 | "From Claude: OCMF uses pytest (10:30)" |
| Codex | CLI 格式化输出 | "From Claude: OCMF uses pytest (2026-03-22 10:30)" |

**recall 返回 JSON 字段** (Phase 6D 已实现):
```python
{
    "memories": [
        {
            "content": "Testing framework: pytest",
            "source_tool": "claude-code",
            "source_host_friendly": "Claude",
            "timestamp": "2026-03-22T10:30:00Z",
            "is_synthetic": False,
            ...
        }
    ],
    "conflict_detected": True,
    "candidates": [...],
    ...
}
```

**用户可见输出格式**:
```
From Claude:
  • "Testing framework: pytest" (2026-03-22 10:30)

From Codex:
  • "Testing framework: unittest" (2026-03-22 09:15)
```

### explain 用户可见输出目标

**目标格式**:

| 宿主 | 输出形式 | 示例 |
|------|----------|------|
| Claude | System-prompt 展示 | "Recalled because: keyword 'testing', scope project=OCMF" |
| Codex | CLI 格式化输出 | "Recall reason: keyword match + project scope" |

**explain 返回 JSON 字段** (Phase 6D 已实现):
```python
{
    "memory_id": "uuid-123",
    "match_reasons": [
        {"type": "keyword", "matched": ["testing", "framework"]},
        {"type": "scope", "matched": {"project": "OCMF"}}
    ],
    "source_tool": "claude-code",
    "source_host_friendly": "Claude",
    "event_timestamp": "2026-03-22T10:30:00Z",
    "also_written_by": ["codex-cli"],
    "explain": "Matched keywords: testing, framework; Source: Claude; Also written by: Codex"
}
```

**用户可见输出格式**:
```
Memory: "Testing framework: pytest"
Source: Claude (2026-03-22 10:30)
Recall: Matched keywords 'testing', 'framework' and scope project=OCMF
Also written by: Codex
```

### conflict 场景用户可见展示目标

**conflict detection 已实现** (Phase 6D):
- `conflict_detected: True`
- `candidates: [...]` 包含所有冲突记忆

**用户可见 conflict 输出**:
```
⚠️ CONFLICT DETECTED

同一问题有不同记忆：
  From Claude:
    • "Testing framework: pytest" (2026-03-22 10:30)

  From Codex:
    • "Testing framework: unittest" (2026-03-22 09:15)

Resolution: User decides which to use
```

### implemented vs UI-visible 边界说明

#### Phase 6D 实现（API 层）

| 功能 | 状态 | 说明 |
|------|------|------|
| recall API source_tool | ✅ 实现 | JSON 返回包含字段 |
| recall API friendly name | ✅ 实现 | JSON 返回包含字段 |
| recall API timestamp | ✅ 实现 | JSON 返回包含字段 |
| recall API conflict_detected | ✅ 实现 | JSON 返回包含字段 |
| recall API candidates | ✅ 实现 | JSON 返回包含字段 |
| explain API match_reasons | ✅ 实现 | JSON 返回包含字段 |
| explain API provenance | ✅ 实现 | JSON 返回包含字段 |
| explain API also_written_by | ✅ 实现 | JSON 返回包含字段 |

#### Phase 6E 实现（用户可见层）

| 功能 | 状态 | 说明 |
|------|------|------|
| Claude system-prompt 展示 | 待实现 | 确保 recall 结果含 provenance |
| Codex CLI 格式化输出 | 待实现 | 格式化 JSON 到可见格式 |
| Conflict 场景展示 | 待实现 | ⚠️ CONFLICT DETECTED 格式 |
| explain 场景展示 | 待实现 | Recall reason 可见 |

### 本轮验收标准（AC）

| AC ID | 验收条件 | 验证方法 |
|--------|----------|----------|
| AC-VIS-001 | Claude recall 结果可见 source/friendly/timestamp | 检查 system-prompt 注入内容 |
| AC-VIS-002 | Codex recall 输出包含 provenance 字段 | 运行 `codex recall` 检查输出 |
| AC-VIS-003 | Conflict 场景有明确提示 | 触发 conflict 检查输出格式 |
| AC-VIS-004 | explain 结果可见 match_reasons | 运行 explain 检查输出 |

### Phase 6E 本轮边界

**只做**:
- ✅ Claude system-prompt 注入 recall 结果的 provenance 展示
- ✅ Codex CLI recall 输出的 provenance 格式化
- ✅ Conflict 场景的可见提示
- ✅ explain 结果的可见展示
- ✅ evidence / known_limits 更新

**不做**:
- ❌ OpenClaw 新实验（Phase 6B 已 blocked）
- ❌ 新宿主能力验证（Claude/Codex 已收口）
- ❌ Web UI 实现（属于后续阶段）
- ❌ replay/eval（属于后续阶段）
- ❌ vector search（属于后续阶段）
- ❌ 新 memory core 大改（本轮只改输出格式）

---

## 最终产品架构的下一阶段优先级

### 优先级排序

| 优先级 | 阶段 | 任务 | 状态 |
|--------|------|------|------|
| **P0** | 6B | OpenClaw real host proof | 🔶 BLOCKED |
| **P0** | 6C | Cross-host UX spec | ✅ 已完成 |
| **P1** | 6D | Cross-host UX Output 实现 | ✅ 已完成 |
| **P1** | 6E | Host-Visible Output Integration | ✅ 已完成 |
| **P1** | 6F | Stable Golden Examples | ✅ 已完成 |
| **P1** | 6G | Regression Gate | ✅ 已完成 |
| **P1** | **7A** | **Unified Entry Point** | **规划中** |
| **P1** | **7B** | **Automatic Memory Experience** | **规划中** |
| **P2** | 后续 | Replay/eval 框架 | 待定 |
| **P2** | 后续 | Vector search | 待定 |
| **P2** | 后续 | Web UI proxy | 待定 |

### 明确不做

- ❌ 新的 Claude/Codex 能力实验（已收口）
- ❌ 新的 adapter 接入（除非用户明确需要）
- ❌ 大规模架构重构
- ❌ 分布式/多租户

---

## Phase 7A: Unified Entry Point

**目标**: 为所有宿主提供统一的 OCMF 入口，用户无需理解 MCP / host matrix / method taxonomy

### 背景

当前状态：
- Host matrix 已收口：Claude=A1+B, Codex=C, OpenClaw=BLOCKED
- Host-visible output 已成立：provenance / conflict / explain 可用户可见
- Regression guardrail 已建立：golden examples 保护已达成体验

问题：
- 当前用户需要理解复杂的 host/method/adapter 概念才能使用 OCMF
- 不同宿主有不同接入方式，没有统一入口
- 用户需要知道什么是 MCP、什么是 Method A/B/C

目标：
- 用户只需要知道"安装 OCMF"即可，无缝接入所有宿主
- 不需要理解底层 host matrix / method taxonomy
- 统一的 CLI 入口：`ocmaf <command>`

### 统一入口架构

#### 统一 CLI

```
$ ocmaf --help
OpenClaw Memory Fabric (OCMF) - Unified Memory for AI Tools

Commands:
  ocmaf install    Install for current host (auto-detects Claude/Codex)
  ocmaf status     Show current host and memory status
  ocmaf recall     Recall memories
  ocmaf explain    Explain memory provenance
  ocmaf config     Configure settings

$ ocmaf install
Detected host: Claude (Method A1+B)
Installing OCMF for Claude...
✓ Claude integration ready
✓ Memory: ON
✓ Auto-recall: ON
✓ Conflict detection: ON
```

#### 统一 Python SDK

```python
from ocmaf import install, remember, recall

# One-line install for current host
install()  # Auto-detects and configures

# After install, just use - no host awareness needed
remember("context from conversation")
memories = recall("what was I working on?")
```

#### 统一 MCP Server

- Single MCP server works for all MCP-capable hosts
- Host auto-detection at startup
- No user configuration needed

### 与现有 regression gate 集成

- `ocmaf install` 运行 regression gate 验证
- Regression gate 失败时提供清晰降级提示
- 用户不需要理解 regression gate 是什么

### Host-Specific Launch Strategy

| Host | Method | Launch | User Experience |
|------|--------|--------|----------------|
| Claude | A1+B | MCP auto-config | `ocmaf install` → Claude ready |
| Codex | C | MCP manual | `ocmaf install --host codex` |
| OpenClaw | BLOCKED | TBD | TBD when unblocked |

---

## Phase 7B: Automatic Memory Experience

**目标**: 用户安装 OCMF 后，默认获得"自动记忆体验"，无需显式调用 remember/recall

### 背景

当前状态：
- Host-visible output 已成立
- User-visible experiences: provenance, conflict, explain 已可展示

问题：
- 当前 recall/remember 仍需显式调用
- 用户需要知道"在对话前后要调用 ocmaf remember"
- 这是早期 adopter 模式，不是大众用户模式

目标：
- 默认开启自动记忆（session 开始/结束自动触发）
- 默认开启自动 recall（对话开始前自动注入上下文）
- 用户体验如同"AI 天然记得一切"

### 默认行为设计

#### Default Auto-Memory On

安装后默认行为：

```
# Session Start
OCMF Auto-Recall:
- Loading project context...
- Found 3 relevant memories:
  • From Claude: "Project uses pytest for testing" (2h ago)
  • From Claude: "Main entry is src/main.py" (1d ago)
  ⚠️ CONFLICT: 2 different approaches found (see help)

# During Session
OCMF Auto-Remember:
- ✓ Remembering conversation context...
- ✓ Remembering task outcomes...

# Session End
OCMF Auto-Remember:
- ✓ Consolidating session memories...
```

#### User Experience Principles

1. **零配置**: 安装后立即生效，无需配置
2. **无感**: 记忆发生但用户不需要知道细节
3. **可解释**: 用户问"为什么记得这个"时有答案
4. **可控制**: 用户可以关闭自动记忆

#### 配置分级

| Level | Name | Behavior |
|-------|------|----------|
| 0 | Off | 完全关闭 |
| 1 | Minimal | 只在显式调用时记忆 |
| 2 | Auto (Default) | 自动记忆 session |
| 3 | Full | 自动记忆 + 自动 recall |

### 与 Regression Gate 的关系

- Regression gate 保护已达成体验不被回退
- Phase 7B 是"增强用户体验"，不是改变已保护内容
- 新增功能不应破坏 regression gate

### 降级策略

| Situation | Behavior |
|-----------|----------|
| Regression gate fails | 警告但允许继续（dev mode） |
| MCP connection fails | 降级到 manual mode |
| Conflict detected | 显示 ⚠️ CONFLICT 但允许继续 |
| OpenClaw blocked | 跳过 OpenClaw，Claude/Codex 继续 |

---

## Regression Gate Integration Policy

### Gate 位置

- `ops/verify_smoke.sh` 包含 regression gate
- `ocmaf install` 时自动运行
- 可独立运行: `python3 runs/028-regression-gate/run_regression_gate.py`

### Gate 保护内容

| Experience | Key Patterns |
|------------|--------------|
| Conflict Detection | `⚠️ CONFLICT DETECTED`, `[Claude]`, `[Codex]` |
| Cross-Host Explain | `Source:`, `Also written by:`, `Match Reasons:` |
| Provenance Display | `From Claude`, `From Codex` |
| Injection Text | `(From Claude`, `⚠️ CONFLICT` |

### Gate 通过条件

- 4 个 golden example 全部 PASS
- 关键 pattern 存在
- 不要求 exact match（允许格式变化）

### Gate 失败处理

- 开发阶段：警告但不阻止
- Release 前：必须通过
- CI/CD：强制 gate 通过才能合并

---

## 用户侧体验原则

### 用户不需要理解

- ❌ MCP 是什么
- ❌ Method A/B/C 区别
- ❌ Host matrix
- ❌ Adapter protocol
- ❌ Event sourcing
- ❌ Conflict detection 算法

### 用户只需要知道

- ✅ `ocmaf install` 安装
- ✅ AI 会记得对话内容
- ✅ 可以问"为什么记得这个"
- ✅ 可以关闭自动记忆

### 设计原则

1. **Simple by default**: 默认配置开箱即用
2. **Explainable**: 用户问"为什么记得"时有答案
3. **Controllable**: 用户可以关闭/调整
4. **Reliable**: 自动记忆不需要用户干预

---

## 已知限制与降级策略

### 当前限制

| Limitation | Mitigation |
|------------|------------|
| OpenClaw BLOCKED | 跳过 OpenClaw，Claude/Codex 继续 |
| Semantic conflict detection | Title-based detection，足够 MVP |
| Real Claude system-prompt | MCP injection，足够当前需求 |
| Real Codex CLI | MCP injection，足够当前需求 |

### 降级路径

| Situation | Fallback |
|-----------|----------|
| Host not supported | 提示不支持，提供 manual mode |
| MCP not available | 降级到 CLI wrapper |
| Regression gate fails | 警告但不阻止 dev |
| Database locked | Retry with backoff |

---

## Phase 7A/7B 与现有工作的关系

### 继承已完成工作

| 已完成 | 继承方式 |
|--------|----------|
| Host matrix | 直接使用，不重新验证 |
| Claude Method A1+B | 作为 Claude launch method |
| Codex Method C | 作为 Codex launch method |
| Cross-host UX spec | 作为输出规范 |
| Host-visible output | 作为默认展示 |
| Golden examples | 由 regression gate 保护 |

### 不重复的工作

- Host capability 探测（已收口）
- Adapter contract（已定义）
- Event envelope protocol（已定义）
- Regression gate（已建立）

### 本轮新工作

- 统一入口 CLI/SDK
- 默认自动记忆行为
- Host auto-detection
- User-facing 配置分级

---

## Phase 7C: Unified Install E2E / Host Wiring Closure

**目标**: 把 unified entry 从"主线骨架"推进到"可信安装闭环"

### 背景

当前状态：
- Phase 7A 已完成 unified entry 骨架
- Phase 7B 已完成 auto-memory 行为设计
- Host matrix、method taxonomy、cross-host UX 已验证

问题：
- `ocmaf install` 骨架存在，但未真正串通 Claude A1+B / Codex C 已验证路径
- `unified status` 仅按 binary 存在性判断 host，可能误判
- Quickstart 与真实用户路径存在落差

目标：
- Unified install 真实可运行，能正确配置 Claude A1+B 和 Codex C
- Unified status 准确判断 host，不依赖 binary 存在性
- Quickstart 对应真实用户路径（不暴露实现细节）

### Unified Install Acceptance Criteria

| Criterion | Description | Verification |
|---------|-------------|--------------|
| AC-7C-INSTALL-001 | Claude install 生成正确的 MCP config | 文件内容验证 |
| AC-7C-INSTALL-002 | Claude install 配置 system-prompt recall 注入 | 配置文件验证 |
| AC-7C-INSTALL-003 | Codex install 生成正确的 MCP config | 文件内容验证 |
| AC-7C-INSTALL-004 | `ocmaf install` 运行 regression gate | gate PASS |
| AC-7C-INSTALL-005 | Install 失败时有清晰错误消息 | 错误可理解 |

### Unified Status Acceptance Criteria

| Criterion | Description | Verification |
|---------|-------------|--------------|
| AC-7C-STATUS-001 | 不依赖 binary 存在性判断 host | 使用 env vars |
| AC-7C-STATUS-002 | Claude env vars 正确识别 | CLAUDE_API_KEY 等 |
| AC-7C-STATUS-003 | Codex env vars 正确识别 | CODEX_API_KEY 或 binary |
| AC-7C-STATUS-004 | Unknown host 有清晰提示 | 用户可理解 |
| AC-7C-STATUS-005 | 显示 recommended method | 用户可理解 |

### Host Wiring Closure

#### Claude Wiring (Method A1+B)

```
ocmaf install --host claude
  ↓
1. 检测 CLAUDE_API_KEY env var
  ↓
2. 生成 ~/.claude/mcp_servers.json (如果不存在)
  ↓
3. 配置 OCMF MCP server
  ↓
4. 配置 system-prompt recall 注入 (B method)
  ↓
5. 验证连接
  ↓
6. 运行 regression gate
```

**验证点**：
- MCP config 格式正确
- System-prompt recall 注入配置存在
- OCMF_AUTO_MEMORY=1 默认开启

#### Codex Wiring (Method C)

```
ocmaf install --host codex
  ↓
1. 检测 CODEX_API_KEY env var 或 codex binary
  ↓
2. 生成 ~/.codex/mcp.json
  ↓
3. 配置 OCMF MCP server
  ↓
4. 验证连接
  ↓
5. 运行 regression gate
```

**验证点**：
- MCP config 格式正确
- Manual recall/remember 可用（Method C）

### Quickstart Truthfulness Rules

1. **不说慌**：Quickstart 描述的体验必须真实可复现
2. **不暴露细节**：不要求用户理解 MCP、method A/B/C、adapter protocol
3. **对应真实路径**：每个步骤都可执行，不存在"假设用户已配置"
4. **错误可理解**：失败消息对非技术用户友好

**Quickstart 承诺**：
- "安装后 Claude 会自动记得对话内容" → 必须真实
- "Codex 用户手动调用 recall" → 与 Method C 一致
- "运行 ocmaf install 即可" → 不需要额外配置

### Known Risks / Degraded Behavior

| Risk | Impact | Mitigation |
|------|--------|------------|
| Claude MCP config 冲突 | Install 失败 | 检测已有配置，提示用户 |
| Codex binary 不存在 | 误判 host | 检测 env var，不只靠 binary |
| Regression gate 失败 | Install 警告但不阻止 | 警告清晰，允许 dev mode |
| OpenClaw 仍 blocked | OpenClaw 无法安装 | 跳过，明确提示 blocked |

### 与 Phase 7A/7B 的关系

Phase 7A/7B 提供：
- Unified entry CLI 骨架
- Auto-memory 行为设计
- Host detection 逻辑

Phase 7C 补全：
- Install 真实可运行
- Status 准确判断
- Quickstart 真实可信

### 与 Regression Gate 的关系

- `ocmaf install` 必须运行 regression gate
- Gate 失败时警告但不阻止（dev mode）
- 用户不需要理解 gate 是什么

### 本轮不做

- ❌ OpenClaw 新实验
- ❌ 新 UX 字段
- ❌ replay/eval
- ❌ vector search
- ❌ Web UI
- ❌ 新 core 功能
- ❌ 新 golden 扩展

## Phase 7D: Real User Journey Test

### 背景

Phase 7C 完成了 unified install 的 wiring 修复和 identity fallback。OCMF 现在已经具备"可信安装闭环"能力：
- Claude 路径：A1+B，来源显示正确
- Codex 路径：C，来源显示正确
- unified install --host xxx 可用

但"安装能跑通"≠"用户旅程顺滑"。Phase 7D 的核心任务是验证真实用户旅程，识别实际卡点。

### 用户旅程测试目标

#### First Usable Memory Path Acceptance Criteria

一个真实用户按 quickstart 操作，应该能在 5 分钟内完成：

```
1. 安装：python3 -m pip install -e .
2. 初始化：ocmaf install --host claude
3. 记忆：ocmaf remember --content "我的第一个记忆"
4. 召回：ocmaf recall --query "我的"
5. 结果：看到 "From Claude: 我的第一个记忆"
```

**注意**：此步骤已更新为 phases 051-054 的 unified install 方案，不再需要 PYTHONPATH 或手动 source config。

**Acceptance Criteria**:
- AC-7D-FUM-001: 用户能在 5 分钟内完成 first usable memory path
- AC-7D-FUM-002: remember 后能看到 Source: Claude（或对应宿主）
- AC-7D-FUM-003: recall 后能看到 "From Claude" 而不是 "From Unknown" 或 "From cli"
- AC-7D-FUM-004: status 命令能看到正确的 memory count

### 实际卡点识别

#### Claude 路径用户卡点

| 卡点 | 描述 | 严重度 | 解决方案 |
|------|------|--------|----------|
| ~~PYTHONPATH~~ | ~~用户必须记住加 PYTHONPATH=src~~ | ~~HIGH~~ | **已解决**：phases 051-054 通过 bootstrap wrapper + global install 解决 |
| ~~source config~~ | ~~用户必须 source ~/.ocmf/config.sh~~ | ~~MEDIUM~~ | **已解决**：phase 052 通过 `_auto_source_config()` 自动加载 |
| MCP restart | Claude 需要 restart 才能加载新 MCP config | MEDIUM | 文档明确说明 |
| Unknown host | 运行时不在 Claude 环境，status 显示 unknown | LOW | 已通过 OCMF_SOURCE_TOOL fallback 修复 |

#### Codex 路径用户卡点

| 卡点 | 描述 | 严重度 | 解决方案 |
|------|------|--------|----------|
| ~~PYTHONPATH~~ | ~~同上~~ | ~~HIGH~~ | **已解决**：同 Claude 路径 |
| ~~source config~~ | ~~同上~~ | ~~MEDIUM~~ | **已解决**：同 Claude 路径 |
| auto-memory | Codex 不支持自动记忆，需要手动 recall/remember | HIGH | 文档明确说明 |
| Method C | 用户需要理解 Method C 是手动模式 | MEDIUM | quickstart 明确标注 |

### 用户旅程测试执行

#### Test Scenario: New User First Memory

```
E2E-7D-001: New User First Memory

Environment:
  - Fresh terminal
  - OCMF installed via pip install -e
  - No prior OCMF config

Steps:
  1. Run: python3 -m pip install -e .
  2. Run: ocmaf install --host claude
  3. Run: ocmaf remember --content "Using PostgreSQL for the database"
  4. Run: ocmaf recall --query "PostgreSQL"

Expected:
  - Step 2: "✓ Installation complete!"
  - Step 4: "✓ Remembered: <id>\n  Source: Claude"
  - Step 5: "Found 1 memories:\n\nFrom Claude:\n  • Using PostgreSQL for the database"

Actual: [TBD - to be filled after test]
判定: [PASS/FAIL]
```

### 验证清单

- [ ] First usable memory path executes without error
- [ ] Source shows correct host name (Claude/Codex, not Unknown/cli)
- [ ] Memory persists across CLI invocations
- [ ] Recall returns the remembered content
- [ ] No unexpected prompts or errors
- [ ] User can complete within 5 minutes

### Phase 7D 本轮边界

**只做**:
- quickstart 真实用户旅程测试
- Claude/Codex 两条路径真实操作验证
- 卡点记录与收敛建议
- evidence / known_limits 更新

**不做**:
- ❌ OpenClaw 新实验
- ❌ 新 core 功能
- ❌ replay/eval
- ❌ vector search
- ❌ Web UI

---

## Phase 7E: Multi-Host Switching UX

### 背景

当用户同时使用 Claude 和 Codex 时，~/.ocmf/config.sh 被用来存储当前宿主配置。但：

- Claude 使用时 source ~/.ocmf/config.sh → OCMF_SOURCE_TOOL=claude-code
- Codex 使用时 source ~/.ocmf/config.sh → OCMF_SOURCE_TOOL=codex-cli

如果用户在同一终端会话中切换宿主，会发生什么？OCMF 是否需要处理这种情况？

### Host Switching Experience Acceptance Criteria

#### Scenario: User Switches from Claude to Codex

```
Steps:
  1. User was using Claude
  2. User ran: source ~/.ocmf/config.sh (loaded claude-code)
  3. User switched to Codex terminal
  4. User ran: source ~/.ocmf/config.sh (still loads claude-code!)
  5. User ran: remember --content "Codex decision"

Expected Behavior:
  - Option A: OCMF 检测到 OCMF_SOURCE_TOOL 与实际环境不匹配，warning
  - Option B: 允许多宿主 config 并存，用户手动选择
  - Option C: 明确文档说明 config 是"安装时配置"不是"运行时检测"

Decision: [TBD - based on Phase 7D user testing]
```

### Multi-Host Config Architecture

#### Current State

```
~/.ocmf/
  config.sh          # 当前激活的配置（单一 active host）
  memory.db          # 共享的记忆存储
  claude/            # Claude 特定文件（未来）
  codex/             # Codex 特定文件（未来）
```

#### Potential Improvements

| 方案 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| A | Host-specific config: ~/.ocmf/claude.env, ~/.ocmf/codex.env | 清晰分离 | 需要选择机制 |
| B | Single config with host override: `source ~/.ocmf/config.sh --host claude` | 灵活 | 增加复杂度 |
| C | Runtime detection overwrites: 检测到 CODEX_API_KEY 时自动切换 | 无缝 | 可能覆盖用户意图 |

**Recommended**: Option A (host-specific config) with explicit sourcing

### Switching Verification Scenarios

#### Scenario: Cross-Host Memory Sharing

```
E2E-7E-001: Claude writes → Codex reads

Environment:
  - Claude installed and configured
  - Codex installed and configured
  - Shared ~/.ocmf/memory.db

Steps:
  1. Claude terminal: source ~/.ocmf/config.sh
  2. Claude terminal: remember --content "Use PostgreSQL"
  3. Codex terminal: source ~/.ocmf/config.sh
  4. Codex terminal: recall --query "PostgreSQL"

Expected:
  - Step 2: "Source: Claude"
  - Step 4: "From Claude: Use PostgreSQL"

判定: [PASS/FAIL/Untestable]
```

#### Scenario: Conflicting Memories

```
E2E-7E-002: Claude vs Codex conflicting decisions

Environment:
  - Shared memory.db

Steps:
  1. Claude: remember --content "Use PostgreSQL"
  2. Codex: remember --content "Use MongoDB"
  3. Claude: recall --query "database"

Expected:
  - Conflict detected
  - Shows both Claude and Codex versions

判定: [PASS/FAIL/Untestable]
```

### User Friction Logging Rules

When user testing reveals friction points, log them in evidence:

```
## User Friction Log

| ID | Scenario | Friction | Severity | Suggested Fix |
|----|----------|----------|----------|---------------|
| UF-001 | First memory | PYTHONPATH required | HIGH | Add wrapper script |
| UF-002 | Host switch | No warning when switching | MEDIUM | Add detection |
```

### Product Polish Priorities

Based on Phase 7D testing, identify top 3 polish items:

| Priority | Polish Item | Impact | Effort |
|----------|-------------|--------|--------|
| P1 | Wrapper script to avoid PYTHONPATH | High | Low |
| P2 | Host detection warning | Medium | Medium |
| P3 | Auto-config on first run | Medium | High |

### Phase 7E 本轮边界

**只做**:
- 多宿主切换体验验证
- 共享 memory.db 跨宿主 recall 测试
- 卡点记录与收敛建议
- evidence / known_limits 更新

**不做**:
- ❌ OpenClaw 新实验
- ❌ 新 core 功能
- ❌ 包装脚本实现（记录即可）
- ❌ replay/eval

---

**Version**: 1.18.0 | **Date**: 2026-03-22 | **Previous**: 1.17.0

**Phase 7A/7B Status**: Complete - Unified Entry Point + Automatic Memory Experience

**Phase 7C Status**: Complete - Unified Install E2E / Host Wiring Closure

**Phase 7D Status**: In Progress - Real User Journey Test

**Phase 7E Status**: Planned - Multi-Host Switching UX
