# OpenClaw Memory Fabric（OCMF）
## 优化设计文档 v0.2

**文档状态**：Ready for Design Review  
**适用范围**：整个 OpenClaw 体系的统一记忆底座  
**设计目标**：在单机优先前提下，构建一个受人类记忆机制启发的、可回测、可自动优化、可并发安全写入的分层记忆系统。  

---

# 0. 文档目的

本文档用于在现有 v0.1 设计基线上，输出一份更适合进入工程实施阶段的正式设计稿。

本稿不再把“记忆架构”仅视为一个分层存储系统，而是将其升级为一个完整的 **记忆生命周期系统（Memory Lifecycle System）**：

- 不只回答“记忆存在哪一层”
- 还回答“记忆如何形成”
- “如何巩固、更新、抑制、归档、重建与纠偏”

本设计的目标不是机械模仿人类记忆外观，而是借鉴人类记忆中真正有效的机制：

1. 有限的工作记忆
2. 线索驱动的回忆
3. 快速写入与慢速巩固分离
4. 回忆不是整块读取，而是逐步重建
5. 记忆提取会改变后续记忆状态
6. 冲突与干扰必须被抑制，而不是一味强化

---

# 1. 背景与问题定义

## 1.1 背景

在 OpenClaw 中，以下信息会持续产生：

- 用户对话
- agent 输出
- 工具调用结果
- 任务与 stage 生命周期事件
- validator / reviewer 结论
- 代码修改记录
- 文档摘要与提炼结果
- 用户长期偏好
- 成功案例与失败案例
- 项目约束、验收标准与策略边界

如果这些信息只是：

- 平铺存储，或
- 依赖单一向量库做全局相似检索

会逐步出现以下问题：

1. **记忆污染**：不同项目、不同 agent、不同类型的内容互相串味。
2. **检索噪声**：高频低价值内容被过度召回，真正关键的记忆被淹没。
3. **缺乏可解释性**：无法说明为什么某条记忆被召回、为什么长期保留。
4. **缺乏长期演进能力**：系统无法形成“经验沉淀、案例抽取、失败避坑、自动纠偏”的闭环。
5. **并发写入风险**：多 agent 同时更新长期记忆时，容易出现脏写、覆盖与状态不一致。
6. **分层失真**：常被从底层“救火”的记忆长期待在低层，说明分层规则没有自我修复能力。

---

## 1.2 总体目标

构建一个统一的 OpenClaw 全局记忆底座，使系统具备以下能力：

1. 像人类一样形成分层记忆，而不是简单堆积内容。
2. 区分“正在思考的内容”和“长期保留的内容”。
3. 让高价值记忆常驻，低频记忆按需召回。
4. 支持从 episodic 中抽取 case，再从 case 中蒸馏 procedural。
5. 支持成功/失败案例的长期积累与优先复用。
6. 支持评分公式自动回测、自动调优与自动纠偏。
7. 支持多 agent 并发写入与并发蒸馏，但长期状态提交必须受控。
8. 检索路径应模拟“先模糊想起，再越想越清晰”的回忆过程。
9. 保留原始证据与版本链，支持追溯、回放与重新计算。

---

## 1.3 设计边界

已确认边界如下：

1. **作用范围**：整个 OpenClaw，而不是单一 agent 私有记忆。
2. **记忆对象**：全部纳入，包括对话、任务、日志、工具结果、规则、偏好、成功/失败案例等。
3. **部署策略**：单机优先。
4. **评分要求**：必须支持自动回测与自动优化，不接受纯静态死规则。
5. **并发要求**：不接受多 agent 直接乱写同一个长期记忆库。
6. **工程策略**：v1 不追求多机分布式，但要预留升级路径。
7. **证据要求**：raw event 必须可追溯、可重放、可复算。

---

# 2. 设计理念：从“分层存储”升级为“记忆生命周期系统”

## 2.1 核心思想

本设计不把记忆理解为“一个向量条目”，而把它定义为：

> 一个由原始事件、派生表示、层级位置、状态演化、检索轨迹与证据链共同构成的生命周期对象。

换句话说，一条记忆不是只回答“是什么”，而是同时回答：

- 来自哪里
- 当前可信度如何
- 处于什么状态
- 为什么会被召回
- 为什么在这一层
- 是否正在更新
- 是否与其他记忆冲突
- 是否应被压缩、降层、隔离或归档

---

## 2.2 六条顶层原则

### 原则 1：统一写入，分型管理
所有记忆先进入统一入口，再按类型、层级、分辨率与状态管理。

### 原则 2：工作记忆与长期记忆分离
当前任务真正“正在想”的内容，必须与长期常驻记忆包分离。

### 原则 3：原始事实与派生记忆分离
raw event 是底账；summary、embedding、tier、case、procedure 都是派生结果。

### 原则 4：在线轻处理，离线重巩固
在线侧优先保证写入与快速召回；重蒸馏、聚类、调参、压缩在后台完成。

### 原则 5：回忆是重建，不是整块读取
检索应按 cue → gist → detail → evidence 逐步展开。

### 原则 6：并发接收可以多写者，长期状态提交必须受控
允许多 agent 并发生产事件，但持久化状态更新必须由受控写者完成。

---

# 3. 需求定义

## 3.1 功能需求

### FR-1 统一记忆接入
所有 OpenClaw 运行过程中的记忆来源都必须进入统一写入通道。

### FR-2 多类型记忆支持
至少支持以下类型：
- preference
- semantic
- episodic
- procedural
- case_success
- case_failure
- policy_constraint

### FR-3 分层存储
至少支持以下层级：
- W0 working_set
- L0 core_pack
- L1 hot
- L2 warm
- L3 cold
- L4 archive
- Q quarantine

### FR-4 多分辨率表示
每条记忆必须支持以下表示层：
- cue
- gist
- detail
- evidence

### FR-5 状态管理
每条记忆必须具有独立状态，并支持状态迁移。

### FR-6 逐层检索与重建
检索必须支持“先模糊、后清晰、必要时追证”的重建式过程。

### FR-7 成功/失败案例优先复用
case_success 与 case_failure 在相关场景下应有独立优先级。

### FR-8 自动升层/降层/隔离
系统必须根据价值、冲突、复用情况、验证结果自动调整位置与状态。

### FR-9 自动回测与自动优化
评分体系必须支持 retrieval trace、replay/backtest、shadow weights、自动调优。

### FR-10 并发安全
支持多 agent 并发提交事件、并发蒸馏，但长期状态提交必须可控、可恢复、可回滚。

### FR-11 原始证据保留
无论压缩、摘要或蒸馏如何进行，关键记忆必须保留原始引用与 evidence replay 能力。

---

## 3.2 非功能需求

### NFR-1 可解释性
系统必须尽量能解释：
- 为什么这条记忆被召回
- 为什么它位于该层
- 为什么它被压缩、升层、降层或隔离

### NFR-2 可回放性
系统必须保留足够轨迹，用于重建评分、重建索引、排查问题与回测。

### NFR-3 并发稳定性
在多 producer 场景下，不应出现明显脏写、覆盖、错乱或崩溃。

### NFR-4 资源可控
首版应适合单机长期运行，避免不必要的重型基础设施。

### NFR-5 可演进性
未来可升级为 PostgreSQL 控制面、多机同步与更复杂的共享记忆结构。

---

# 4. 四轴模型

为了避免“层级”承担过多语义，正式设计采用 **四轴模型**：

1. Type Axis（类型轴）
2. Tier Axis（层级轴）
3. Resolution Axis（分辨率轴）
4. State Axis（状态轴）

---

## 4.1 Type Axis（类型轴）

### 1) preference
用户或系统偏好，例如表达风格、结构偏好、固定约束。

### 2) semantic
稳定事实、项目背景、术语映射、静态知识。

### 3) episodic
某次任务、会话、事件、执行轨迹本身。

### 4) procedural
可复用的方法、步骤、套路、流程。

### 5) case_success
经过验证的成功案例，强调“场景、方案、成功原因”。

### 6) case_failure
失败案例与避坑经验，强调“错误、后果、修复方式”。

### 7) policy_constraint
策略边界、验收规则、不可越过的约束。

---

## 4.2 Tier Axis（层级轴）

### W0 working_set
当前任务真正正在参与推理的最小上下文集合。

内容示例：
- 当前 query
- 当前 task plan
- 最近工具返回
- 当前 validator/reviewer 约束
- 少量即时命中的高置信记忆

特点：
- 极小
- 高频变化
- 会话内有效
- 不等于长期记忆

### L0 core_pack
当前项目默认常驻的小型高价值长期记忆包。

### L1 hot
高频复用、当前项目强相关、近期高命中记忆。

### L2 warm
中频有用，不常驻，但值得优先检索。

### L3 cold
低频、旧记忆、潜在有价值，但不应经常干扰上下文。

### L4 archive
证据层与归档层，保存原始对话、日志、原文档 chunk、原工具结果等。

### Q quarantine
冲突、不稳定、低可信或待仲裁记忆的隔离层。

---

## 4.3 Resolution Axis（分辨率轴）

### cue
一句线索式表示，用于模糊回忆与快速粗召回。

### gist
中短摘要，说明这条记忆是什么、为何重要。

### detail
较完整的细节重构表示，包含条件、因果、步骤、适用边界。

### evidence
原始证据层，支持回放、追溯与人工核验。

### 设计目标
当系统“想起一件事”时：
1. 先从 cue 找感觉
2. 再用 gist 缩小范围
3. 再用 detail 恢复结构
4. 最后必要时用 evidence 追证

---

## 4.4 State Axis（状态轴）

### candidate
刚形成的候选记忆，尚未证明长期价值。

### stable
已通过基本验证、可正常参与召回。

### active
近期高频被使用，处于活跃状态。

### reconsolidating
刚被提取且正在更新或重写。

### quarantined
冲突、不稳、低可信或待仲裁。

### deprecated
已被更新事实替代，但暂不删除。

### archived
只保留追证价值，不再主动参与常规检索。

---

# 5. 生命周期模型

## 5.1 状态机

```text
captured
  -> stabilized
  -> candidate
  -> consolidated
  -> active
  -> dormant
  -> archived

active
  -> reconsolidating
  -> stable / deprecated / quarantined
```

---

## 5.2 生命周期说明

### captured
原始事件刚进入系统，尚未完成解析。

### stabilized
基础字段、引用、摘要与索引材料已准备完毕，可被后续 worker 消费。

### candidate
已形成派生记忆，但尚未证明长期保留价值。

### consolidated
已通过复用、验证、回放或聚合，被正式纳入长期记忆体系。

### active
近期高频命中，适合提升权重或升层。

### dormant
暂时不活跃，但不应删除。

### reconsolidating
记忆被重新激活，正在被更新、改写或与新证据融合。

### quarantined
内容冲突、来源可疑、结论不稳，等待仲裁。

### deprecated
已被新版本替代，但需保留 lineage 与兼容窗口。

### archived
不再主动干预任务，但保留追证与历史回放价值。

---

# 6. 总体架构

建议采用：

# OpenClaw Memory Fabric（OCMF）/ Single-node / Adaptive Lifecycle

整体分为 6 个层：

1. Event Ingress Layer
2. Distillation & Feature Layer
3. Tiered Storage & State Layer
4. Retrieval & Reconstruction Layer
5. Replay & Optimization Layer
6. Audit & Governance Layer

---

## 6.1 Event Ingress Layer

由 `memoryd` 统一接收来自：
- 用户对话
- agent 输出
- tool 结果
- stage/task 生命周期事件
- review/validator 结论
- 成功/失败执行记录
- 文档处理结果

职责：
- 基础校验
- 生成全局 event_id
- 追加写入 raw event log
- 返回 ACK

原则：
- 只负责“记下来”
- 不在入口处做重蒸馏

---

## 6.2 Distillation & Feature Layer

由并行 worker 负责：
- cue/gist/detail 生成
- embedding 生成
- topics/entities 提取
- memory_type 识别
- case 候选识别
- procedure 候选抽取
- R / P / C / trust / interference 所需特征预计算

---

## 6.3 Tiered Storage & State Layer

负责：
- 分层存储
- 状态管理
- 版本化更新
- current pointer 维护
- quarantine 隔离

---

## 6.4 Retrieval & Reconstruction Layer

按 query intent 驱动：
- cue recall
- gist rerank
- detail reconstruct
- evidence replay

---

## 6.5 Replay & Optimization Layer

负责：
- retrieval trace 记录
- replay/backtest
- 自动优化权重
- shadow 部署新参数
- promotion / demotion / quarantine 建议

---

## 6.6 Audit & Governance Layer

负责：
- 记忆审计
- 解释输出
- 冲突仲裁
- 手工 pin / unpin
- 策略约束执行
- 指标看板

---

# 7. 检索路径：回忆不是读取，而是重建

## 7.1 核心原则

系统不应默认加载最完整内容，而应模拟人类回忆：

1. 先低成本模糊想起
2. 再逐步提升清晰度
3. 最后在必要时追证

这一路径既降低上下文成本，也更符合“思考过程”。

---

## 7.2 检索四阶段

### Phase 1: Cue Recall
从 query 中抽取线索：
- topics
- entities
- time band
- project scope
- success/failure/debug/research intent

只在 cue 表示上做快速粗召回。

### Phase 2: Gist Expansion
展开候选 gist：
- 这条记忆大概是什么
- 是否属于同类问题
- 是成功经验还是失败教训
- 是否值得进入下一阶段

### Phase 3: Detail Reconstruction
对高分候选取 detail：
- 适用条件
- 为什么成功/失败
- 关键步骤
- 风险与注意事项

### Phase 4: Evidence Replay
在 debug / review / high-risk 场景下，再去 archive 中拿原始证据：
- 原日志
- 原对话
- 原工具结果
- 原文档 chunk

---

## 7.3 检索设计意图

目标不是“始终拿最全”，而是：
- 先想起线索
- 再恢复骨架
- 最后必要时核验证据

这使得系统具备：
- 更小的上下文注入量
- 更强的可解释性
- 更接近人类回忆方式的多阶段检索行为

---

# 8. 评分体系

本系统不使用单一总分，而采用三类核心评分 + 若干修正机制。

核心评分：
- R(q, m)：检索评分
- P(m)：分层评分
- C(m)：巩固评分

关键修正项：
- trust
- interference penalty
- promotion debt
- redundancy penalty
- staleness penalty
- conflict penalty

---

## 8.1 检索评分 R(q, m)

回答的问题：

> 当前 query 下，这条记忆应排在多前面？

建议形式：

```text
R(q,m) = σ(
  a1*dense_similarity
+ a2*sparse_similarity
+ a3*cue_overlap
+ a4*gist_overlap
+ a5*topic_match
+ a6*entity_match
+ a7*project_match
+ a8*namespace_match
+ a9*memory_type_prior
+ a10*trust_score
+ a11*success_mode_boost
+ a12*failure_mode_boost
- a13*staleness_penalty
- a14*redundancy_penalty
- a15*interference_penalty
)
```

### 关键特征说明
- `dense_similarity`：向量近似度
- `sparse_similarity`：关键词/稀疏特征匹配
- `cue_overlap`：线索级命中程度
- `gist_overlap`：概要语义重合度
- `memory_type_prior`：不同意图下不同类型的先验权重
- `trust_score`：可信度
- `success_mode_boost`：当任务偏执行/复用时成功案例提权
- `failure_mode_boost`：当任务偏调试/避坑时失败案例提权
- `interference_penalty`：与其他更优候选高度相似但质量更差时降权

### 主要用途
- 粗召回后排序
- gist/detail rerank
- 决定是否进入 W0 working_set

---

## 8.2 分层评分 P(m)

回答的问题：

> 这条记忆长期应该待在哪一层？

建议形式：

```text
P(m) = σ(
  b1*reuse_7d
+ b2*reuse_30d
+ b3*cross_session_reuse
+ b4*cross_agent_reuse
+ b5*current_project_relevance
+ b6*success_lift
+ b7*failure_prevention_lift
+ b8*manual_pin
+ b9*stability_score
- b10*staleness_penalty
- b11*redundancy_penalty
- b12*storage_cost_penalty
- b13*conflict_penalty
)
```

### 关键增强机制

#### 1) Percentile Gating
层级切换不只看绝对阈值，也看同类型、同项目分布中的相对位置。

#### 2) Promotion Debt
如果某条 L3/L4 记忆在近窗口期内反复“从底层救火”，说明分层错了。系统应累计 promotion debt，并在达到阈值后强制升层。

#### 3) Deep-tier Rescue Tracking
必须记录低层记忆被召回后显著改善结果的情况，作为自动纠偏依据。

### 层级决策示意
- manual_pin 或 P >= θ0 -> L0
- P >= θ1 -> L1
- P >= θ2 -> L2
- P >= θ3 -> L3
- else -> L4

---

## 8.3 巩固评分 C(m)

回答的问题：

> 这条记忆是否该被压缩、合并、抽 case、蒸 procedural、降层或保留摘要？

建议形式：

```text
C(m) = σ(
  c1*cluster_density
+ c2*summarization_gain
+ c3*case_extraction_potential
+ c4*procedural_extraction_potential
+ c5*evidence_strength
+ c6*retrieval_reinforcement
- c7*contradiction_risk
- c8*novelty_loss
- c9*update_instability
)
```

### 主要用途
- 是否从 episodic 中抽取 case
- 是否从 case 中蒸 procedural
- 是否只保留 cue/gist
- 是否降层
- 是否合并重复记忆

### 核心原则
不是“老了就压缩”，而是“被理解过、被验证过、可抽象了才压缩”。

---

## 8.4 信任、冲突与干扰

### trust_score
由以下因素综合而成：
- 来源可靠性
- evidence 完整度
- validator 结果
- 重放成功率
- 被推翻历史

### conflict_penalty
当记忆与高可信新事实冲突时，不应直接删除，应先降权或进入 quarantine。

### interference_penalty
防止低质量相似记忆在检索时淹没高质量记忆。

---

# 9. 自动回测与自动优化

## 9.1 Retrieval Trace
每次检索都应记录至少以下字段：
- query_id
- project_id
- namespace
- query_text
- intent
- candidates
- retrieved_topk
- used_in_context
- final_task_outcome
- validator_outcome
- user_feedback
- deep_tier_rescue
- timing
- weight_snapshot_id

---

## 9.2 正负标签

### 正向标签
- 被召回后帮助完成任务
- 被注入上下文后 validator/pass rate 提升
- 类似任务再次出现时复用成功
- 从中抽出 procedure 后多次复用成功

### 负向标签
- 召回但无帮助
- 注入后增加噪声
- 过时或被后续事实推翻
- 本应高层却总从低层救回
- 与正确记忆强冲突

---

## 9.3 评估指标

建议至少保留：
- NDCG@10
- Precision@5
- Recall@10
- DeepRecallPenalty
- OverInjectionRate
- CaseReuseHitRate
- SuccessLift
- FailurePreventionLift
- PromotionDebtResolutionRate
- QuarantineFalsePositiveRate

---

## 9.4 优化目标

综合目标函数示意：

```text
J = a*NDCG@10
  + b*Precision@5
  + c*CaseReuseHitRate
  + d*SuccessLift
  + e*FailurePreventionLift
  - f*DeepRecallPenalty
  - g*OverInjectionRate
  - h*QuarantineFalsePositiveRate
```

---

## 9.5 自动调参闭环

建议流程：
1. 收集最近 7 天 / 30 天 retrieval trace
2. 用不同参数集 replay
3. 根据综合目标打分
4. 选出最优权重快照
5. 先 shadow 部署
6. 连续若干周期稳定后再切正式参数

---

# 10. 并发模型与一致性设计

## 10.1 核心原则
- 并发接收：多生产者
- 原始事件：强持久化
- 派生记忆：最终一致
- 当前运行工作集：快照一致
- 长期状态提交：单 shard 单写者

---

## 10.2 memoryd

本地守护进程，负责：
- 接收 memory event
- 基础校验
- 生成全局 event_id
- 追加写入 raw event log
- 返回 ack

### 注意
memoryd 只负责“记下来”，不负责重蒸馏。

---

## 10.3 Append-only Raw Event Log

所有原始事件只追加，不原地覆盖。

优点：
- 崩溃恢复简单
- 重放简单
- 幂等容易
- 更换评分公式后可重算
- 便于保留历史与 lineage

---

## 10.4 Distillation Workers

多个 worker 并行消费 raw event，负责：
- cue/gist/detail 生成
- entity/topic 提取
- case 候选识别
- embedding 计算
- 特征预计算
- 冲突候选检测

---

## 10.5 Shard Committer

真正更新长期记忆元数据层的写者不是所有 worker，而是按 shard 归属的 committer。

### shard key 建议
按 `hash(project_id + namespace + source_scope) % N` 切分。

### 每个 shard 负责
- 一个逻辑写者
- 一份 SQLite shard DB
- WAL 模式
- 短事务提交
- busy_timeout
- current pointer 原子切换

---

## 10.6 版本化更新

不直接覆盖旧摘要，而采用版本化：
- memory_id
- version
- base_event_range
- derived_from_hash
- current_pointer
- commit_ts

更新流程：
1. 生成新版本
2. 校验基线版本未变化
3. 原子切换 current pointer
4. 老版本保留观察窗口
5. 必要时回滚

---

## 10.7 一致性模型

- raw event：一旦 ack，不可丢
- derived memory：允许延迟若干秒/分钟后稳定
- W0 working_set：对一次任务使用同一快照版本
- L0 core_pack：按周期刷新，不在任务中途频繁漂移

---

# 11. 存储边界与技术职责

## 11.1 SQLite（控制面）

职责：
- metadata
- tier / state / score / version / trace / jobs
- shard commit log
- current pointers
- 审计与 replay 索引

不适合：
- 多写者直接乱写同一 DB 文件
- 作为全量原文档存储层

---

## 11.2 Qdrant（召回面）

职责：
- cue / gist / detail 的向量索引
- payload filter
- 分层召回
- 多阶段 rerank 前的候选生成

建议重点 payload：
- project_id
- namespace
- memory_type
- tier
- state
- trust_state
- source_scope

---

## 11.3 Filesystem（证据层）

职责：
- raw event archive
- 原日志
- 原对话
- 原始文档 chunk
- 快照备份
- replay dataset

原则：
- 尽量不可变
- 不过度重写原件
- 保留原始可追证能力

---

## 11.4 未来升级边界

当单机并发、数据规模、事务压力继续提升时：
- 控制面可升级 PostgreSQL
- Qdrant 可继续保留
- Filesystem 仍保留 archive 职责
- memoryd 接口保持不变

---

# 12. 核心 Schema 草案

## 12.1 memory_event

字段建议：
- event_id
- project_id
- namespace
- session_id
- agent_id
- source_kind
- event_type
- created_at
- content_raw_ref
- content_digest
- dedupe_key
- ingest_status
- source_scope
- importance_hint

---

## 12.2 memory_item

字段建议：
- memory_id
- version
- project_id
- namespace
- memory_type
- tier
- state
- cue_text
- gist_text
- detail_text_ref
- evidence_ref
- topics_json
- entities_json
- trust_state
- trust_score
- activation_features_json
- placement_features_json
- consolidation_features_json
- interference_features_json
- hit_count
- last_hit_at
- score_R_cache
- score_P
- score_C
- promotion_debt
- current_pointer
- derived_from_event_range
- created_at
- updated_at

---

## 12.3 retrieval_trace

字段建议：
- trace_id
- query_id
- project_id
- namespace
- intent
- query_text
- cue_candidates
- gist_candidates
- detail_selected
- evidence_loaded
- used_in_context
- deep_tier_rescue
- final_outcome
- validator_outcome
- feedback_label
- weight_snapshot_id
- latency_ms
- created_at

---

## 12.4 weight_snapshot

字段建议：
- snapshot_id
- version
- R_weights_json
- P_weights_json
- C_weights_json
- target_window
- objective_score
- shadow_status
- promoted_to_prod
- created_at

---

## 12.5 shard_commit_log

字段建议：
- commit_id
- shard_id
- event_id
- memory_id
- old_version
- new_version
- commit_status
- retry_count
- error_message
- created_at

---

## 12.6 conflict_case

字段建议：
- conflict_id
- project_id
- namespace
- memory_id_left
- memory_id_right
- conflict_type
- conflict_score
- arbitration_status
- resolution_note
- created_at

---

# 13. W0 / L0 的区别与生成策略

## 13.1 W0 working_set

W0 是任务级、瞬时、极小的正在思考集合。

来源：
- 当前 query
- 当前计划
- 当前工具结果
- 当轮召回 Top-K 中最值得进入上下文的内容

生成原则：
- 尽量小
- 强相关优先
- 本轮结束即可释放

---

## 13.2 L0 core_pack

L0 是项目级、相对稳定、默认常驻的小型长期记忆包。

来源：
- 当前项目关键目标
- 用户长期偏好
- 高频成功套路
- 高频失败告警
- 当前项目核心边界

生成原则：
- 比 W0 稳定
- 比 L1 更精选
- 不允许无限膨胀

---

## 13.3 为什么必须拆开

如果不区分 W0 与 L0，会出现：
- 当前任务噪声长期驻留
- 长期记忆与即时推理上下文混淆
- core pack 失控膨胀
- 无法解释到底什么是“正在想”，什么是“长期常驻”

---

# 14. 冲突、隔离与遗忘

## 14.1 Quarantine 不是垃圾桶

Q quarantine 不是删除区，而是：
- 冲突事实缓冲区
- 低可信自动抽取隔离区
- 不同 agent 矛盾结论待仲裁区
- 暂不应污染主检索流的内容收容区

---

## 14.2 遗忘不是删除

本系统中的“遗忘”优先表现为：
- 降层
- 降权
- 降分辨率
- 退出主动检索
- 仅保留证据与 lineage

只有在明确安全、明确可替代、明确无审计价值时才考虑清理。

---

## 14.3 干扰控制

必须显式控制以下风险：
- 低质量高频日志把关键经验淹没
- 相似但过时的方案干扰最新方案
- 不同项目内容在语义上高度接近但业务上不可混用

建议机制：
- interference penalty
- project/namespace 强过滤
- 冲突检测
- quarantine 优先隔离

---

# 15. 分阶段实施计划

## Phase 0：设计冻结

目标：冻结以下内容：
- 四轴模型
- 生命周期状态机
- R / P / C 公式与特征表
- schema
- shard 策略
- 版本化与恢复策略
- acceptance cases

---

## Phase 1：MVP

建议范围：
- memoryd
- append-only raw event log
- cue/gist/detail/evidence 表示框架
- R / P 两类评分
- W0 / L0 / L1 / L2 / L4
- Q quarantine 基础能力
- sharded SQLite + Qdrant + filesystem
- retrieval trace
- nightly replay + tuning

暂不做：
- 复杂 procedural 自动蒸馏
- graph memory
- 多机同步
- PostgreSQL 控制面
- 复杂跨项目桥接

---

## Phase 2：v1

增加：
- L3 cold
- C(m) 巩固评分
- episodic -> case 抽取
- case -> procedural 蒸馏
- shadow deployment of weights
- memory audit dashboard
- conflict arbitration workflow

---

## Phase 3：v2

增加：
- PostgreSQL 可插拔
- graph edges
- 跨项目桥接记忆
- agent 专属视图与共享视图并存
- 更高级别调参与预算控制
- 多机或多节点协同

---

# 16. 风险与应对

## 风险 1：评分自我强化错误
**应对**：shadow weights、人工 pin、过时记忆惩罚、冲突记忆扣权、手工回滚。

## 风险 2：低层记忆经常救火
**应对**：定义 DeepRecallPenalty 与 promotion debt，推动自动升层。

## 风险 3：并发蒸馏冲突
**应对**：append-only raw、版本化更新、shard committer、幂等键。

## 风险 4：检索链过慢
**应对**：默认只走 cue + gist；只有高风险/调试场景再开 detail/evidence。

## 风险 5：压缩失真
**应对**：raw_ref 永远保留，失败案例必须可追证。

## 风险 6：多项目串味
**应对**：project_id / namespace 强过滤，跨项目召回默认关闭。

## 风险 7：隔离过度
**应对**：追踪 QuarantineFalsePositiveRate，避免把有用记忆过度封存。

---

# 17. 验收标准

## 17.1 设计验收
- 明确四轴模型
- 明确 W0 与 L0 的区别
- 明确状态轴与生命周期状态机
- 明确 R/P/C 三类评分与修正机制
- 明确自动回测与调参闭环
- 明确并发安全结构
- 明确 cue/gist/detail/evidence 检索路径
- 明确 SQLite / Qdrant / filesystem 职责边界

---

## 17.2 功能验收
- 支持多 agent 并发提交 event
- 支持分层检索与重建式检索
- 支持 case_failure 优先命中
- 支持 retrieval trace
- 支持参数快照与 replay
- 支持 quarantine 基础流程
- 支持 promotion debt 累积与升层触发

---

## 17.3 质量验收
- DeepRecallPenalty 可观测下降
- 常救火的低层记忆能被升层
- L0 core_pack 可控不膨胀
- W0 working_set 保持小而稳定
- 失败经验可在类似场景复用
- 冲突记忆不会直接污染主检索流

---

# 18. Ready-for-Implementation Checklist

进入编码前，至少冻结以下内容：

1. memory_event schema
2. memory_item schema
3. retrieval_trace schema
4. conflict_case schema
5. shard 策略
6. versioning 策略
7. R / P / C 特征表
8. trust / interference / promotion_debt 计算规则
9. W0 生成策略
10. L0 生成策略
11. 失败恢复策略
12. smoke tests 与 acceptance cases

---

# 19. 项目定义建议

本项目应被定义为：

> 一个面向 OpenClaw 的、受人类记忆机制启发的、分层 + 生命周期 + 重建式检索的统一记忆底座。

而不是：

> 一个多层向量库 + 摘要系统。

两者的区别在于：

前者强调：
- 工作记忆
- 巩固
- 状态迁移
- 提取后更新
- 冲突隔离
- 自动纠偏
- 证据追溯

后者往往只会得到：
- 存得很多
- 想不起来
- 想起来的不准
- 准的解释不清
- 清的更新不了

---

# 20. 本轮建议结论

如果本项目准备正式进入实施阶段，建议立刻冻结以下三项：

1. **四轴模型 + W0/L0 拆分**
2. **生命周期状态机 + quarantine 机制**
3. **R/P/C + trust/interference/promotion_debt 特征表**

只要这三项冻结，后续 schema、实现拆包、memoryd、replay、nightly tuning、审计面板都可以顺利展开。

