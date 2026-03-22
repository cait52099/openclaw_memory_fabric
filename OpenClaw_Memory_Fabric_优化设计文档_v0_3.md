# OpenClaw Memory Fabric 优化设计文档 v0.3

## 1. 文档目标

本文档用于定义一个**兼容各类 AI 工具的统一记忆模块**（Memory Fabric），支持：

- 多 AI 工具 / 多 agent 接入
- 单机优先、可演进到多机
- 分层记忆与生命周期管理
- 像“正常聊天一样”自然触发记忆
- 可追溯、可解释、可回放、可调优

本文档在 v0.2 思路上进一步收敛，重点补强：

- 跨工具兼容层
- 统一记忆事件协议
- 并发安全写入模型
- 冲突消解与遗忘机制
- 无痛接入模式
- 对话式自动回忆体验

---

## 2. 设计目标

### 2.1 总体目标

构建一个 Tool-agnostic 的 Memory Fabric，使 OpenClaw、Claude Code、Codex CLI、ChatGPT 类工作流、本地脚本、IDE 插件等都能通过统一方式接入记忆系统。

### 2.2 核心能力

1. **统一写入**：不同工具都可将事件写入统一记忆协议。
2. **统一检索**：不同工具都能以一致方式检索可用记忆。
3. **渐进回忆**：支持 cue → gist → detail → evidence 的回忆流程。
4. **分层管理**：支持 working / hot / warm / cold / archive 等层级。
5. **生命周期控制**：支持强化、衰减、替代、隔离、归档。
6. **回测优化**：根据真实使用行为优化评分与分层策略。
7. **证据驱动**：所有高价值记忆支持来源与证据追踪。

### 2.3 用户体验目标

最终接入效果应尽量接近：

- 用户正常聊天
- AI 无需手动“查库”感知
- 在需要时自动想起相关上下文
- 想起的内容先给摘要，再在必要时展开细节与证据

---

## 3. 非目标

当前阶段不追求：

- 一开始就做分布式多机一致性集群
- 完全替代向量数据库或知识图谱
- 完全无判断地永久保存所有历史聊天
- 在 v1 就实现所有外部 SaaS 深度双向同步
- 让任意第三方 AI 原生修改长期记忆状态

---

## 4. 核心设计原则

### 4.1 事件先行，状态后建
所有接入工具只写原始事件，不直接修改长期记忆对象。

### 4.2 单机优先，重建优先
首版优先保证稳定、可调试、可回放、可重建。

### 4.3 记忆不是日志堆积
记忆是经过筛选、聚合、蒸馏、迁移后的可用知识资产。

### 4.4 检索不是一次命中
回忆是逐步重建，不是单次全文召回。

### 4.5 长期记忆必须受控提交
多 agent 可并发产生事件，但长期状态提交必须经过受控 consolidator。

### 4.6 评分规则必须可回测
任何分层或升降级策略都必须支持 replay / backtest / tuning。

### 4.7 证据优先于自信
高价值记忆要能追溯来源，避免“记错但说得很像真的”。

---

## 5. 系统抽象层次

## 5.1 Compatibility Layer（兼容层）
负责让不同 AI 工具以统一方式接入。

接入对象分为三类：

### A. Agent Runtime
- OpenClaw
- Claude Code
- Codex CLI
- ChatGPT Agent / 浏览器工作流
- 自定义 agent runner

### B. IDE / Workspace Tools
- VS Code / Cursor / Claude Code 环境
- Shell / Terminal 工具
- Git hooks / CI
- 本地开发脚本

### C. External Knowledge Producers
- 文件系统 watcher
- Git commit / diff
- 浏览器 session
- 日历 / 邮件 / IM / 笔记
- 爬虫 / API 抓取器

## 5.2 Memory Core（记忆核心）
核心负责：

- 事件接收
- 对象聚合
- 打分
- 分层
- 检索
- 冲突处理
- 回放评估

## 5.3 Recall Runtime（回忆运行时）
负责在实际聊天 / 执行时：

- 接收 query / task cue
- 召回相关记忆
- 生成摘要上下文
- 在需要时展开细节与证据

---

## 6. 记忆四轴模型

## 6.1 Type Axis（记忆类型）

- episodic：单次事件 / 会话 / 任务经历
- semantic：稳定事实 / 概念 / 约束
- procedural：流程 / 方法 / 操作套路
- preference：用户偏好 / 风格 /习惯
- case_success：成功案例
- case_failure：失败案例
- policy：规则 / 红线 / 约束

## 6.2 Tier Axis（存储层级）

- working：当前工作集
- hot：近期高频高价值
- warm：中期可用
- cold：低频保留
- archive：仅归档或审计

## 6.3 Resolution Axis（分辨率）

- cue：触发线索
- gist：概要
- detail：详细内容
- evidence：证据与来源

## 6.4 State Axis（状态）

- active
- latent
- reinforced
- decaying
- superseded
- conflicted
- quarantined
- archived

---

## 7. 统一记忆事件协议

这是跨工具兼容的第一优先级。

### 7.1 Event Envelope

```json
{
  "event_id": "evt_20260310_xxx",
  "timestamp": "2026-03-10T15:00:00+08:00",
  "source": {
    "tool": "claude_code",
    "agent_id": "reviewer_01",
    "session_id": "sess_xxx",
    "workspace_id": "p009_memory_fabric",
    "project_id": "p009"
  },
  "kind": "task_result",
  "type_axis": "episodic",
  "resolution": "detail",
  "content": {
    "title": "task completed",
    "text": "...",
    "structured": {}
  },
  "links": {
    "parent_event_id": "evt_xxx",
    "task_id": "task_001",
    "run_id": "run_20260310_xxx"
  },
  "evidence": {
    "files": [],
    "logs": [],
    "commands": []
  },
  "policy": {
    "privacy": "workspace",
    "retention_hint": "normal"
  }
}
```

### 7.2 最小必填字段

- event_id
- timestamp
- source.tool
- source.session_id
- kind
- content.text 或 content.structured

### 7.3 常见事件类型

- chat_turn
- task_start
- task_result
- failure
- fix_applied
- decision
- preference_update
- document_ingested
- file_changed
- recall_feedback
- retrieval_trace

---

## 8. Identity 设计

为避免跨工具接入后的身份冲突，必须拆成三层：

### 8.1 Event ID
原始事件唯一 ID。

### 8.2 Memory Object ID
多个事件聚合后的记忆对象 ID。

### 8.3 Entity / Topic ID
跨会话、跨工具聚合的实体 / 主题 ID。

建议命名：

- evt_*：事件
- mem_*：记忆对象
- ent_*：实体 / 主题
- case_*：案例
- proc_*：流程

---

## 9. 并发写入与提交模型

## 9.1 总体模型
采用：**多生产者 + 单提交者 + 可重放日志**

### Producers
多个 agent / 工具 / 脚本并发写入 raw events。

职责：
- append only
- 不直接修改长期记忆对象
- 不直接变更 tier / state

### Consolidator / Committer
受控单写者，负责：

- 事件聚合
- 对象生成
- 分数更新
- tier 迁移
- 状态迁移
- 版本链维护
- 索引更新

### Rebuilder
必要时基于 raw event log 重建：

- memory objects
- score 表
- index
- replay traces

## 9.2 这样设计的原因

- 降低多 agent 并发脏写风险
- 提高可解释性
- 支持回滚和重建
- 支持以后迁移数据库而不丢语义

---

## 10. 记忆对象与蒸馏

### 10.1 原始事件不是最终记忆
系统需要将原始事件聚合为更稳定的记忆对象。

### 10.2 主要对象类型

- Session Summary
- Project Constraint
- User Preference
- Success Case
- Failure Case
- Procedural Recipe
- Entity Fact
- Decision Record

### 10.3 蒸馏方向

- episodic → case_success / case_failure
- 多个 case → procedural
- 多轮对话 → stable preference
- 多次重复事实 → semantic memory

---

## 11. 评分系统

## 11.1 两层评分

### Online Fast Score
在线快速评分，用于初始放层与实时召回。

候选特征：

- recency
- frequency
- reuse_count
- validation_pass
- user_pin
- source_reliability
- task_success_relation
- contradiction_risk

### Offline Calibrated Score
离线回测评分，用于校准在线权重。

重点分析：

- 哪些冷层记忆经常被救火召回
- 哪些热层记忆经常召回但最终无用
- 哪些案例真正提高任务成功率
- 哪些 procedural 已经过时

## 11.2 核心目标
让记忆位置越来越接近真实使用价值，而不是人工拍脑袋固定权重。

---

## 12. 检索与回忆流程

推荐检索链路：

`cue -> candidate set -> conflict check -> gist -> detail -> evidence`

### 12.1 cue
从当前问题 / 任务 / 对话上下文中提取线索。

### 12.2 candidate set
从 semantic + FTS + vector + entity link 中召回候选集合。

### 12.3 conflict check
在进入主上下文前进行冲突校验：

- 是否存在新版本替代
- 是否已过时
- 是否和当前项目 / 工作区不匹配
- 是否与用户最新偏好冲突
- 是否处于 quarantined / conflicted 状态

### 12.4 gist
先返回简要记忆摘要，减少上下文占用。

### 12.5 detail
仅在需要时展开详细步骤、历史案例、限制条件。

### 12.6 evidence
对关键结论给出证据链，例如：

- 文件路径
- 原始消息
- 任务日志
- 测试结果
- commit / diff

---

## 13. 遗忘、衰减与失效机制

### 13.1 不主张直接删除
除非有明确隐私或用户删除请求，大多数记忆优先采用：

- suppress
- decay
- supersede
- quarantine
- archive

### 13.2 动作定义

- **suppress**：暂不参与默认召回
- **decay**：长期少用自动降权
- **supersede**：被新版本替代
- **quarantine**：冲突严重或可信度不足，隔离待审
- **archive**：仅用于回放 / 审计 / 追溯

### 13.3 这样做的目的
避免系统无限膨胀，同时保留可审计性。

---

## 14. 无痛接入设计

这是系统最终是否“像正常聊天一样能记起来”的关键。

## 14.1 接入原则

所有 AI 工具都不要感知复杂内部结构，而只接 2 类接口：

### A. 写入接口
在会话中自动或半自动写入：

- chat turn
- task result
- failure / fix
- preference update
- important decision

### B. 检索接口
在每轮对话开始前或生成前调用：

- recall(query, session, project, user)

## 14.2 推荐接入方式分三档

### 档位 1：最无痛（Wrapper 模式）
把原本对模型的调用包一层：

1. 用户输入进入 wrapper
2. wrapper 先调 recall
3. 把摘要记忆拼进 system/context
4. 调原模型回答
5. 回答后抽取新事件并 remember

适合：
- OpenClaw
- 自己的 agent runtime
- CLI 工具
- 本地自动化脚本

### 档位 2：插件模式（Middleware / Hook）
在工具已有生命周期钩子中插入：

- before_prompt → recall
- after_response → remember
- after_task → consolidate signal

适合：
- Claude Code 工作流
- Codex CLI orchestration
- VS Code / Cursor 插件环境

### 档位 3：旁路模式（Proxy / Sidecar）
如果某些工具不方便改内部逻辑，可以做代理层：

- 聊天请求先过本地代理
- 代理做 recall + remember
- 再转发到原工具/模型

适合：
- 封闭型工具
- 浏览器自动化场景
- Web UI 类 AI 工具

---

## 15. 最方便的调用方式

目标是让调用方只会两件事：

## 15.1 写入

```python
memory.remember(event)
```

或更简单：

```python
memory.capture_chat_turn(user_msg, assistant_msg, meta)
memory.capture_task_result(task, result, evidence)
```

## 15.2 检索

```python
ctx = memory.recall(
    query=user_msg,
    session_id=session_id,
    project_id=project_id,
    user_id=user_id
)
```

返回建议：

```json
{
  "gist": ["用户偏好中文输出", "项目 p009 需证据驱动", "上次失败点在并发提交"],
  "detail_refs": ["mem_xxx", "case_xxx"],
  "evidence_refs": ["run_xxx/logs/..."],
  "injection_text": "Relevant memory: ..."
}
```

调用方只需把 `injection_text` 拼进上下文即可。

---

## 16. 如何做到“像正常聊天一样就能记起来”

关键不是让模型自己学会记忆，而是让 runtime 自动做两件事：

### 16.1 自动 recall
每次收到用户消息时，根据：

- 当前 query
- 当前 project
- 当前 workspace
- 当前会话
- 当前用户

自动召回最相关 gist。

### 16.2 自动 remember
每次回答结束后，自动抽取：

- 新偏好
- 新约束
- 新成功案例
- 新失败案例
- 新决策

写入 event store。

## 16.3 用户侧体验
最终用户不需要说：

- “去查一下记忆库”
- “请加载上次项目背景”
- “请记住这个偏好”

而是系统默认：

- 在该记得的时候自动记得
- 在不该打扰的时候不乱插话
- 在需要更精确时再展开细节

---

## 17. 推荐 API 抽象

建议统一成以下核心接口：

### 17.1 Remember API

- remember(event)
- remember_batch(events)
- capture_chat_turn(...)
- capture_task_result(...)
- capture_decision(...)

### 17.2 Recall API

- recall(query, context)
- recall_gist(query, context)
- expand(memory_id)
- explain(memory_id)

### 17.3 Lifecycle API

- reinforce(memory_id)
- suppress(memory_id)
- supersede(old_id, new_id)
- quarantine(memory_id)
- archive(memory_id)

### 17.4 Ops API

- consolidate()
- replay(run_id)
- backtest(dataset)
- stats()

---

## 18. 推荐实现栈（v1）

### 18.1 存储

- SQLite：元数据 / 状态 / 关系表
- SQLite FTS5：全文索引
- sqlite-vec 或 LanceDB / Qdrant（本地可选）：向量召回
- 文件系统：raw events / evidence / snapshots / replay traces

### 18.2 原因

- 单机友好
- 易调试
- 易打包
- 易回放
- 易迁移

---

## 19. 建议目录结构

```text
memory-fabric/
├─ docs/
│  ├─ constitution.md
│  ├─ spec.md
│  ├─ plan.md
│  ├─ checklist.md
│  └─ analysis.md
├─ memory/
│  ├─ adapters/
│  ├─ ingestion/
│  ├─ objects/
│  ├─ scoring/
│  ├─ retrieval/
│  ├─ replay/
│  ├─ conflict/
│  └─ storage/
├─ data/
│  ├─ raw_events/
│  ├─ evidence/
│  ├─ snapshots/
│  └─ indexes/
├─ tasks/
│  ├─ tasks.md
│  └─ tasks.json
├─ ops/
│  ├─ verify_smoke.sh
│  ├─ replay_eval.py
│  └─ rollback.md
└─ runs/
   └─ <run_id>/
      ├─ evidence.md
      └─ logs/
```

---

## 20. 评估指标

## 20.1 写入类

- event append 成功率
- 并发写入无损率
- 重放后一致性

## 20.2 检索类

- Top-k 命中率
- 关键记忆召回率
- 噪声率
- 证据追溯成功率

## 20.3 层级健康类

- 高频记忆误落冷层比例
- 热层无效记忆比例
- quarantine 命中质量

## 20.4 任务收益类

- 任务成功率提升
- reviewer 修改轮次下降
- 重复错误率下降
- 成功案例复用率上升

---

## 21. 分阶段推进建议

## Phase 0：协议与底账

交付：
- 统一事件协议
- raw append log
- SQLite 元数据表
- 基础 replay

验收：
- 不同工具写入协议成功
- 回放可重建事件流
- 并发 producer 不丢数据

## Phase 1：最小可用记忆系统

交付：
- type / tier / state 基础模型
- working / hot / warm / cold
- cue / gist / detail / evidence
- 简单评分与检索

验收：
- 完成写入 → 检索 → 追证闭环
- 可解释召回原因
- 能做基础升降层

## Phase 2：案例蒸馏与冲突处理

交付：
- success / failure case
- procedural distillation
- conflict check
- supersede / quarantine

验收：
- 成功失败案例可独立召回
- procedural 可复用
- 冲突对象不会污染主召回链

## Phase 3：回测与自动调优

交付：
- retrieval traces
- replay benchmark
- scoring tuning
- 层级健康分析

验收：
- 能输出调优前后对比
- 能发现低层救火记忆
- 能建议权重优化

---

## 22. 风险与防护

### 22.1 主要风险

- 记忆污染
- 高频低价值信息淹没关键记忆
- 跨工具身份混乱
- 旧规则与新规则冲突
- 自动写入过多导致噪声爆炸
- 检索链路过重导致对话延迟变高

### 22.2 防护措施

- 统一事件协议
- 统一 identity
- 单提交者模型
- gist 优先注入
- 高风险对象需 evidence 支持
- recall trace 记录与回测
- suppress / quarantine / supersede 机制

---

## 23. 最终建议

这个系统值得推进，但不要一开始做成“大而全”。

最优策略是：

1. 先做统一协议和可重建底账
2. 再做最小 recall/remember 闭环
3. 再做案例蒸馏与冲突控制
4. 最后做自动回测调优

真正的“无痛接入”关键不在于模型多聪明，而在于：

- 所有工具都能统一写入事件
- 所有工具都能统一调用 recall
- recall 的输出足够轻，能直接注入上下文
- remember 的触发足够自动，不要求用户显式操作

一旦这四点成立，用户就会感觉：

> 系统像正常聊天一样，会自然地记得以前的事情。

---

## 24. 当前版本结论

### 可实现性
可实现，且工程上有明确路径。

### 优先级最高的补强项

1. 统一记忆事件协议
2. 兼容层与接入模型
3. Identity 体系
4. 并发提交模型
5. 冲突消解与失效机制
6. 回测评估体系

### 推荐下一步
直接进入：

- constitution
- spec
- plan
- tasks
- implement

将该文档转化为可执行工程制品。
