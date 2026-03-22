# OpenClaw Memory Fabric (OCMF) - 基线规格说明

**Feature Branch**: `001-memory-fabric-spec`
**Created**: 2026-03-10
**Status**: Draft
**Input**: 用户描述 - 构建兼容各 AI 工具的统一记忆模块

## 1. 问题定义

### 1.1 当前多 AI 工具记忆割裂的核心问题

当前不同 AI 工具（如 OpenClaw、Claude Code、Codex CLI、脚本 agent、Web UI 自动化）之间的上下文、偏好、项目历史、成功/失败经验彼此割裂，导致：

- 重复说明：每次切换工具都需要重新说明项目背景和约束
- 重复踩坑：在一个工具中失败的经验无法传递给其他工具
- 上下文丢失：跨工具切换时记忆丢失，无法连续工作

### 1.2 为什么普通 RAG / 向量库不足以解决该问题

普通 RAG / 向量库存在以下局限性：

- **无结构化检索**：仅支持相似度匹配，无法实现多维度筛选（作用域、状态、时间）
- **无分层管理**：无法区分 working memory、hot、warm、cold、archive 等层级
- **无冲突检测**：无法检测和消解互相矛盾的记忆
- **无证据链**：无法追溯记忆来源和决策依据
- **无生命周期**：无法自动管理记忆的 decay、reinforce、supersede 状态

### 1.3 为什么需要 Memory Fabric 而不是单一知识库

Memory Fabric 的核心价值：

- **事件驱动**：所有记忆可追溯到原始事件，支持重建
- **分层存储**：根据使用频率和时效性自动分层
- **冲突消解**：自动检测和标记矛盾记忆
- **证据驱动**：关键决策必须有证据支撑
- **多工具接入**：统一协议支持多种 AI 工具接入

## 2. 目标

### 2.1 跨工具统一记忆接入

定义统一的 Memory Event Envelope 和 Recall/Remember API，使 OpenClaw、Claude Code、Codex CLI、脚本 agent、Web UI proxy 等工具可以通过统一接口接入。

### 2.2 像正常聊天一样自然 recall

实现智能上下文感知 recall，基于当前会话自动检索相关历史，而非显式查询。

### 2.3 会话、项目、偏好、案例、程序性知识、证据可沉淀

支持多种记忆类型：会话上下文、项目配置、用户偏好、成功案例、程序性知识（步骤/流程）、决策证据。

### 2.4 可重建、可解释、可调优

- 可重建：所有长期对象可从 raw events 重建
- 可解释：每次召回需说明来源和理由
- 可调优：通过 replay/backtest 评估和调整评分/分层规则

## 3. 非目标

- **NG1**: 不做分布式多机一致性系统（单机优先）
- **NG2**: 不做厂商绑定（不依赖单一模型厂商）
- **NG3**: 不做大而全 UI 先行（优先保证核心功能）
- **NG4**: 不做一次性全量外部系统集成（架构可扩展即可）

## 4. 用户故事

### User Story 1 - OpenClaw 项目连续性 (Priority: P1)

作为 OpenClaw 用户，我希望在继续同一项目时，系统能自动想起上次约束、失败点和当前状态。

**Why this priority**: 这是核心价值主张，解决记忆割裂的首要场景。

**Independent Test**: 可以在单一项目中测试：写入项目约束 -> 关闭会话 -> 重新打开 -> 验证约束是否被正确 recall。

**Acceptance Scenarios**:

1. **Given** 用户在项目中设定了约束（如"不使用第三方认证库"），**When** 用户重新打开同一项目，**Then** 系统自动 recall 该约束
2. **Given** 用户在某次任务中失败并记录了失败原因，**When** 用户执行类似任务，**Then** 系统提醒之前的失败点
3. **Given** 用户完成了项目阶段性目标，**When** 用户继续工作，**Then** 系统展示当前状态和待办

---

### User Story 2 - Claude Code 任务上下文 (Priority: P1)

作为 Claude Code 用户，我希望实现任务时自动带入项目 spec、既往修复经验和风格偏好。

**Why this priority**: 提升开发效率，避免重复说明项目背景。

**Independent Test**: 可以独立测试：写入项目 spec -> 执行新任务 -> 验证 spec 是否被自动带入上下文。

**Acceptance Scenarios**:

1. **Given** 用户创建了项目 spec（如 API 设计规范），**When** 用户开始新任务，**Then** 系统自动 recall 相关 spec
2. **Given** 用户之前修复过某个 bug 并记录了方案，**When** 用户遇到类似问题，**Then** 系统提供历史修复经验
3. **Given** 用户有代码风格偏好（如"使用 async/await"），**When** 用户生成代码，**Then** 系统遵循该偏好

---

### User Story 3 - 脚本 agent 简易接入 (Priority: P2)

作为 Codex CLI / 脚本 agent 用户，我希望无需学习复杂 API，只在调用前 recall、调用后 remember 即可。

**Why this priority**: 降低接入门槛，使脚本 agent 也能享受记忆系统能力。

**Independent Test**: 可以用最小脚本测试：调用 recall -> 验证返回 -> 调用 remember -> 验证写入。

**Acceptance Scenarios**:

1. **Given** 脚本 agent 调用 `recall(query)`，**When** 存在相关记忆，**Then** 返回匹配的记忆内容
2. **Given** 脚本 agent 调用 `remember(event)`，**When** 事件格式正确，**Then** 事件被成功写入
3. **Given** 脚本 agent 调用快捷方法 `capture_task_result()`，**When** 任务完成，**Then** 自动生成事件并写入

---

### User Story 4 - 评分与分层调优 (Priority: P2)

作为系统维护者，我希望通过 replay/backtest 判断评分和分层规则是否有效。

**Why this priority**: 确保记忆系统长期健康运行，需要评估和优化机制。

**Independent Test**: 可以用历史数据回放测试：准备测试数据集 -> 运行 replay_eval -> 查看评分报告。

**Acceptance Scenarios**:

1. **Given** 维护者准备历史事件数据，**When** 运行 replay_eval，**Then** 输出评分准确率、分层健康度等指标
2. **Given** 维护者发现评分偏低，**When** 调整评分规则并重新评估，**Then** 可以看到调整前后的差异
3. **Given** 存在过时记忆，**When** 系统自动执行分层调整，**Then** 过时记忆被降层或归档

---

### User Story 5 - 记忆审计与追溯 (Priority: P3)

作为审计者，我希望知道某段记忆为何被召回、来自何处、是否已过时或被替代。

**Why this priority**: 满足合规和审计需求，确保记忆系统可解释。

**Independent Test**: 可以测试任意记忆的 explain 功能。

**Acceptance Scenarios**:

1. **Given** 用户查看某条被召回的记忆，**When** 调用 explain(memory_id)，**Then** 显示记忆来源、创建时间、关联事件、状态
2. **Given** 某记忆已被新记忆替代，**When** 查看旧记忆，**Then** 显示 superseded 状态和替代者链接
3. **Given** 存在冲突记忆，**When** 查看冲突记忆，**Then** 显示冲突标记和相关证据

---

### Edge Cases

- 跨工具作用域泄漏：确保不同工具的记忆严格隔离
- 空结果处理：recall 无结果时返回空列表而非错误
- 并发写入冲突：多工具同时写入同一对象时的处理
- 超大上下文：单次 recall 返回过多结果时的分页处理

## 5. 功能需求

### 5.1 统一 Memory Event Envelope

- **FR-001**: 系统 MUST 定义统一的 Event Envelope 格式，包含 event_id、timestamp、source_tool、scope、event_type、payload、evidence 等字段
- **FR-002**: 系统 MUST 支持事件版本号，用于协议兼容性管理
- **FR-003**: 系统 MUST 验证事件格式，拒绝不符合规范的写入

### 5.2 Raw Append-Only Event Store

- **FR-004**: 系统 MUST 使用 append-only 方式存储原始事件，保证事件不可变性
- **FR-005**: 系统 MUST 为每个事件生成唯一 event_id（推荐 UUID）
- **FR-006**: 系统 MUST 支持事件按时间范围、作用域、事件类型过滤查询

### 5.3 Memory Object 聚合层

- **FR-007**: 系统 MUST 提供 Memory Object 聚合层，从 raw events 重建对象状态
- **FR-008**: 系统 MUST 支持 rebuild 操作，从 event log 重建整个对象层
- **FR-009**: 系统 MUST 支持对象层增量更新，避免全量重建

### 5.4 Entity / Topic / Version / Link 模型

- **FR-010**: 系统 MUST 支持 Entity（实体）和 Topic（主题）抽象
- **FR-011**: 系统 MUST 记录对象版本，支持版本历史追溯
- **FR-012**: 系统 MUST 支持对象间 Link（关联），支持证据链构建

### 5.5 Recall API

- **FR-013**: 系统 MUST 提供 recall(query, context) 接口，支持语义检索
- **FR-014**: 系统 MUST 提供 recall_gist(query, context) 接口，返回精简版本
- **FR-015**: 系统 MUST 支持 expand(memory_id) 接口，获取记忆完整详情
- **FR-016**: 系统 MUST 支持 explain(memory_id) 接口，说明召回原因和来源

### 5.6 Remember API

- **FR-017**: 系统 MUST 提供 remember(event) 接口，写入单个事件
- **FR-018**: 系统 MUST 验证写入权限，确保符合作用域隔离要求

### 5.7 快捷写入方法

- **FR-019**: 系统 MUST 提供 capture_chat_turn(user_msg, assistant_msg, meta) 方法
- **FR-020**: 系统 MUST 提供 capture_task_result(task, result, evidence) 方法
- **FR-021**: 系统 MUST 提供 capture_decision(decision, meta) 方法
- **FR-022**: 系统 MUST 自动提取关键信息（如约束、偏好、失败点）并结构化存储

### 5.8 检索链路

- **FR-023**: 系统 MUST 实现完整检索链路：cue → candidate set → conflict check → gist → detail → evidence
- **FR-024**: 系统 MUST 在 conflict check 阶段检测互相矛盾的记忆
- **FR-025**: 系统 MUST 在返回结果中包含 evidence 引用

### 5.9 Tier/State Lifecycle 管理

- **FR-026**: 系统 MUST 支持 Tier 分层：working / hot / warm / cold / archive
- **FR-027**: 系统 MUST 支持 State 状态：active / latent / reinforced / decaying / superseded / conflicted / quarantined / archived
- **FR-028**: 系统 MUST 自动执行 tier/state 状态迁移
- **FR-029**: 系统 MUST 提供 consolidate() 接口，手动触发状态迁移

### 5.10 Scoring 与 Replay/Backtest

- **FR-030**: 系统 MUST 提供在线轻评分机制（ relevance_score、confidence_score、freshness_score）
- **FR-031**: 系统 MUST 提供 replay_eval() 接口，离线评估评分和分层规则
- **FR-032**: 系统 MUST 支持评分规则可配置和动态调整

### 5.11 适配器层

- **FR-033**: 系统 MUST 提供 OpenClaw 适配器
- **FR-034**: 系统 MUST 提供 Claude Code 适配器
- **FR-035**: 系统 MUST 提供 Codex CLI 适配器
- **FR-036**: 系统 MUST 提供脚本 agent 适配器（Python SDK）
- **FR-037**: 系统 MUST 提供 Web UI proxy 适配器

### 5.12 作用域隔离

- **FR-038**: 系统 MUST 支持 user/workspace/project/session 四级作用域
- **FR-039**: 系统 MUST 严格隔离不同作用域的记忆
- **FR-040**: 系统 MUST 支持跨作用域显式共享（如显式授权）

### 5.13 证据追溯与 Run 目录

- **FR-041**: 系统 MUST 支持证据关联，记录每个记忆的来源事件
- **FR-042**: 系统 MUST 在 runs/<run_id>/evidence.md 落盘证据文件
- **FR-043**: 系统 MUST 自动生成 run 目录，记录每次执行的输入输出

### 5.14 Rebuild 功能

- **FR-044**: 系统 MUST 提供 rebuild() 接口，从 raw events 重建对象层
- **FR-045**: 系统 MUST 提供 rebuild(index_only=True) 选项，仅重建索引
- **FR-046**: 系统 MUST 在重建过程中保持数据一致性

### 5.15 Cross-Host UX（跨宿主体验）

#### 5.15.1 Provenance Display（来源展示）

- **FR-047**: recall 结果必须包含 source_tool 字段，标识记忆来源宿主
- **FR-048**: recall 结果必须将 source_tool 映射为友好名称（claude-code → Claude, codex-cli → Codex, openclaw → OpenClaw, synthetic → Synthetic）
- **FR-049**: recall 结果应按 source_host 分组展示（可选）

#### 5.15.2 Conflict Explanation（冲突解释）

- **FR-050**: 当 recall 检测到同一实体不同来源内容冲突时，必须标记 conflict_detected=true
- **FR-051**: 冲突响应必须包含所有冲突来源的 content、source_tool、timestamp
- **FR-052**: 冲突必须由用户最终决定，不自动选优

#### 5.15.3 Recall Hit Explanation（召回命中解释）

- **FR-053**: explain(memory_id) 必须返回 match_reasons，说明为何被召回（keyword/scope/time）
- **FR-054**: explain(memory_id) 必须返回 source_tool 和 source_host_friendly
- **FR-055**: 跨宿主 recall 的 explain 必须说明 also_written_by 其他宿主

#### 5.15.4 source_tool 字段规范

| source_tool | Friendly Name | 说明 |
|-------------|---------------|------|
| claude-code | Claude | Claude Code 桌面应用 |
| codex-cli | Codex | Codex CLI |
| openclaw | OpenClaw | OpenClaw 桌面应用 |
| synthetic | Synthetic (Test) | 直接模块调用，非真实宿主 |

- **FR-056**: 所有事件必须有 source_tool 字段
- **FR-057**: synthetic 测试产生的 source_tool='synthetic'
- **FR-058**: source_tool 不可变

#### 5.15.5 User Experience by Host Path

**Claude (A1 + B - Automatic)**:
> "OCMF 自动使用 Claude hooks 捕获你的项目上下文。约束、决策、模式无需手动操作即可自动存储。"

**Codex (C - Manual)**:
> "OCMF 提供你在工作流中调用的记忆工具。在关键决策后使用 `ocmf_remember` 保存上下文，在会话开始时使用 `ocmf_recall` 检索。"

**OpenClaw (TBD - 待确定)**:
> 取决于 OpenClaw 验证结果。

## 6. 非功能需求

### 6.1 可重建性

- 所有 Memory Object 必须能从 raw events 100% 重建
- 重建过程必须是幂等的

### 6.2 可追溯性

- 每个记忆必须可追溯到原始事件
- 必须支持事件链完整遍历

### 6.3 可解释性

- 每次 recall 必须返回 explain 信息
- 必须说明为何召回、如何评分、证据来源

### 6.4 低侵入接入

- 适配器必须最小化对宿主工具的代码修改
- Wrapper 模式要求零代码修改

### 6.5 单机稳定性

- 必须保证单机环境下的稳定运行
- 必须处理异常退出和恢复

### 6.6 并发安全

- 多工具并发写入时必须保证数据一致性
- 必须实现受控提交机制（single-writer）

### 6.7 可扩展性

- 存储层必须支持插件化（SQLite/向量库）
- 适配器必须可扩展新工具类型

### 6.8 性能目标

| 指标 | 目标值 |
|------|--------|
| Recall P50 | < 100ms |
| Recall P95 | < 500ms |
| Write Latency | < 50ms |
| Full Rebuild (10k events) | < 30s |
| Concurrent Writers | >= 5 |

### 6.9 兼容性

- 必须支持 Mac / Windows / Linux
- Python 版本 >= 3.11

### 6.10 可测试性

- 必须提供 verify_smoke.sh 冒烟测试脚本
- 每个模块必须有独立测试用例

## 7. 核心数据模型

### 7.1 ID 类型

| ID 类型 | 格式 | 说明 |
|---------|------|------|
| Event ID | UUID | 原始事件唯一标识 |
| Memory Object ID | UUID | 聚合后对象唯一标识 |
| Entity ID | UUID | 实体唯一标识 |
| Topic ID | UUID | 主题唯一标识 |
| Run ID | timestamp + uuid | 运行实例唯一标识 |

### 7.2 Event Envelope 字段

```json
{
  "event_id": "uuid",
  "version": "1.0",
  "timestamp": "ISO8601",
  "source_tool": "string",
  "scope": {
    "user_id": "string",
    "workspace_id": "string",
    "project_id": "string",
    "session_id": "string"
  },
  "event_type": "chat_turn | task_result | decision | preference | constraint | evidence",
  "payload": {
    "content": "string",
    "metadata": {}
  },
  "evidence": ["event_id"],
  "links": ["memory_object_id"]
}
```

### 7.3 Memory Object 字段

```json
{
  "memory_id": "uuid",
  "entity_id": "uuid",
  "topic_id": "uuid",
  "version": "int",
  "tier": "working | hot | warm | cold | archive",
  "state": "active | latent | reinforced | decaying | superseded | conflicted | quarantined | archived",
  "resolution": "cue | gist | detail | evidence",
  "content": "string",
  "score": {
    "relevance": 0.0,
    "confidence": 0.0,
    "freshness": 0.0
  },
  "created_from": ["event_id"],
  "superseded_by": "memory_id",
  "supersedes": ["memory_id"],
  "conflict_with": ["memory_id"],
  "scope": {},
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### 7.4 Tier / Resolution / State 枚举

**Tier（分层）**:
- working: 当前工作上下文
- hot: 高频访问
- warm: 中频访问
- cold: 低频访问
- archive: 归档存储

**Resolution（精度）**:
- cue: 召回提示
- gist: 概要信息
- detail: 详细信息
- evidence: 完整证据链

**State（状态）**:
- active: 活跃
- latent: 潜在可用
- reinforced: 被强化
- decaying: 衰减中
- superseded: 被替代
- conflicted: 冲突
- quarantined: 隔离
- archived: 归档

## 8. 核心接口

### 8.1 Remember 接口

```python
def remember(event: Event) -> EventResult:
    """
    写入单个记忆事件。
    - 验证事件格式
    - 写入 raw event store
    - 触发对象层更新（异步）
    """
    pass
```

### 8.2 Recall 接口

```python
def recall(query: str, context: Context) -> RecallResult:
    """
    基于语义检索记忆。
    - cue: 解析查询意图
    - candidate set: 获取候选集
    - conflict check: 检测冲突
    - gist: 返回概要
    - evidence: 附带证据引用
    """
    pass

def recall_gist(query: str, context: Context) -> List[Gist]:
    """
    仅返回精简概要，跳过详细内容和冲突检查。
    适用于快速上下文填充。
    """
    pass
```

### 8.3 Expand/Explain 接口

```python
def expand(memory_id: str) -> MemoryObject:
    """
    获取记忆完整详情。
    """
    pass

def explain(memory_id: str) -> Explanation:
    """
    返回记忆的可解释信息：
    - 为何被召回
    - 来源事件
    - 当前状态
    - 相关联的记忆
    """
    pass
```

### 8.4 快捷写入接口

```python
def capture_chat_turn(user_msg: str, assistant_msg: str, meta: dict) -> EventResult:
    """
    捕获对话轮次，自动提取关键信息。
    """
    pass

def capture_task_result(task: str, result: dict, evidence: list) -> EventResult:
    """
    捕获任务结果，记录成功/失败经验和证据。
    """
    pass

def capture_decision(decision: str, meta: dict) -> EventResult:
    """
    捕获决策及其上下文。
    """
    pass
```

### 8.5 管理接口

```python
def consolidate() -> ConsolidationResult:
    """
    手动触发状态迁移和对象聚合。
    """
    pass

def rebuild(full: bool = False) -> RebuildResult:
    """
    从 raw events 重建对象层。
    - full=True: 全量重建
    - full=False: 仅重建索引
    """
    pass

def replay_eval(test_dataset: list) -> EvalResult:
    """
    离线评估评分和分层规则。
    """
    pass
```

## 9. 接入模式

### 9.1 Wrapper 模式

**适用工具**: Claude Code、Codex CLI（支持自定义 prompt 或配置文件）

**优点**: 零代码修改，完全透明

**缺点**: 功能受限，无法精细控制

**推荐顺序**: 1（最优先）

### 9.2 Hook / Middleware 模式

**适用工具**: OpenClaw、脚本 agent（支持 hook 机制）

**优点**: 侵入性低，可拦截关键节点

**缺点**: 需要宿主工具支持 hook

**推荐顺序**: 2

### 9.3 Proxy / Sidecar 模式

**适用工具**: Web UI proxy、需要网络代理的工具

**优点**: 完全透明，可拦截所有请求

**缺点**: 配置复杂，需要网络层面支持

**推荐顺序**: 3

## 10. 架构模块

```
adapters/           # 适配器层
  ├── openclaw/
  ├── claude_code/
  ├── codex_cli/
  ├── script/
  └── webui/

ingestion/          # 事件摄取
  ├── validator/
  ├── enricher/
  └── dispatcher/

raw_event_store/   # 原始事件存储
  ├── store/
  └── query/

object_builder/     # 对象构建
  ├── aggregator/
  ├── linker/
  └── versioner/

scoring/            # 评分模块
  ├── relevance/
  ├── confidence/
  └── freshness/

retrieval/         # 检索模块
  ├── cue_parser/
  ├── candidate/
  └── ranker/

conflict/           # 冲突检测
  ├── detector/
  └── resolver/

replay/             # 回放评估
  ├── recorder/
  └── evaluator/

storage/            # 存储层
  ├── sqlite/
  └── vector/       # 可选

ops/                # 运维脚本
  ├── verify_smoke.sh
  └── rollback.md
```

## 11. 约束与边界

### 11.1 禁止事项

- **CB-001**: 不允许接入工具直接改长期对象层，必须通过事件层
- **CB-002**: 不允许 recall 跳过冲突检查
- **CB-003**: 高风险动作（支付/删除/生产变更）必须人工确认
- **CB-004**: 默认单机优先，不支持分布式模式
- **CB-005**: 默认证据驱动，关键操作必须有证据

### 11.2 边界条件

- 单次 recall 返回最多 20 条结果（可配置）
- 单个事件最大 1MB
- 作用域层级：user > workspace > project > session

## 12. 风险与缓解

| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| 记忆污染 | 低质量或错误记忆被召回 | 证据链校验 + 冲突检测 |
| 层级错位 | 记忆被错误分层 | 自动评分 + 定期 consolidate |
| 冲突召回 | 互相矛盾的记忆同时召回 | conflict check + 标记 |
| 过时规则 | 旧规则污染新任务 | version 管理 + supersede |
| 并发损坏 | 多工具写入导致状态损坏 | single-writer + 事务 |
| 作用域泄漏 | 敏感记忆被错误暴露 | 严格隔离 + 显式共享 |
| 评分失真 | 评分规则偏离实际 | replay_eval 定期校准 |
| 数据不足 | Replay 测试数据不足 | 最小测试用例 + smoke |

## 13. 验收标准 (AC)

### 13.1 写入类 AC

| AC ID | 标准 | 验证方法 |
|-------|------|----------|
| AC-WR-001 | remember(event) 成功写入并返回 event_id | 调用接口并验证返回 |
| AC-WR-002 | capture_* 方法正确提取关键信息 | 构造输入并验证 payload |
| AC-WR-003 | 作用域隔离：跨作用域无法访问 | 多作用域测试 |
| AC-WR-004 | 并发写入不损坏数据 | 5 并发写入测试 |

### 13.2 检索类 AC

| AC ID | 标准 | 验证方法 |
|-------|------|----------|
| AC-RE-001 | recall 返回相关记忆，P50 < 100ms | 性能测试 |
| AC-RE-002 | recall_gist 返回精简结果 | 验证返回格式 |
| AC-RE-003 | conflict check 检测冲突记忆 | 构造冲突数据测试 |
| AC-RE-004 | explain 返回完整解释信息 | 验证返回字段 |

### 13.3 层级健康类 AC

| AC ID | 标准 | 验证方法 |
|-------|------|----------|
| AC-LH-001 | consolidate 正确执行状态迁移 | 观察 tier/state 变化 |
| AC-LH-002 | rebuild 可完整重建对象层 | 清空对象层后 rebuild |
| AC-LH-003 | 过时记忆自动降层或归档 | 时间推进测试 |
| AC-LH-004 | superseded 标记正确传递 | 验证新旧记忆状态 |

### 13.4 任务收益类 AC

| AC ID | 标准 | 验证方法 |
|-------|------|----------|
| AC-TA-001 | replay_eval 输出评分报告 | 运行评估并验证输出 |
| AC-TA-002 | 适配器成功接入目标工具 | 实际工具集成测试 |
| AC-TA-003 | runs/<run_id>/evidence.md 正确生成 | 检查文件内容 |
| AC-TA-004 | verify_smoke.sh 冒烟测试通过 | 运行脚本并验证 |

## 14. Evidence

### 14.1 证据映射

每个关键模块和接口必须能在 plan/tasks/implement 中映射到证据：

| 模块/接口 | 证据文件 | 验证方式 |
|-----------|----------|----------|
| Event Envelope | runs/<run_id>/evidence.md | 验证字段完整性 |
| Recall API | ops/verify_smoke.sh | 性能测试用例 |
| Conflict Check | tasks/tasks.md | 测试用例覆盖 |
| Rebuild | ops/verify_smoke.sh | 重建测试用例 |
| Adapters | runs/<run_id>/evidence.md | 实际工具测试 |
| Scoring | tasks/tasks.md | replay_eval 输出 |

### 14.2 证据输出路径

- **runs/<run_id>/evidence.md**: 每次实现的证据文档
- **ops/verify_smoke.sh**: 冒烟测试脚本
- **docs/constitution.md**: 宪法（已存在）
- **docs/spec.md**: 本规格说明
- **docs/plan.md**: 实现计划（待生成）
- **docs/checklist.md**: 检查清单（待生成）
- **docs/analysis.md**: 分析报告（待生成）
- **tasks/tasks.md**: 任务清单（待生成）
- **tasks/tasks.json**: 任务 JSON（待生成）
- **ops/rollback.md**: 回滚方案（待生成）

## 15. Assumptions

- 用户环境已有 Python 3.11+
- 用户需要单机本地部署
- 向量检索作为可选功能，不强制要求
- 首批适配器仅支持 OpenClaw、Claude Code、Codex CLI
