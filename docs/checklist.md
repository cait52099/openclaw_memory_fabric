# OCMF 实现质量检查清单

**Purpose**: 面向实现前/实现中/实现后的质量检查清单
**Created**: 2026-03-10
**Feature**: OpenClaw Memory Fabric (OCMF)
**Based On**: docs/constitution.md, docs/spec.md, docs/plan.md

## 1. 协议与数据模型检查

- [ ] CHK001 - Event Envelope 是否定义了所有必需字段（event_id, version, timestamp, source_tool, scope, event_type, payload, evidence, links）？ [Completeness, Spec §7.2]
- [ ] CHK002 - Event Envelope 的 scope 是否支持 user/workspace/project/session 四级隔离？ [Completeness, Spec §7.2]
- [ ] CHK003 - event_id 是否使用 UUID 格式以确保全局唯一性？ [Clarity, Spec §7.1]
- [ ] CHK004 - timestamp 是否使用 ISO 8601 格式以支持时区和时间比较？ [Clarity, Spec §7.2]
- [ ] CHK005 - Memory Object 是否包含 tier/state/resolution 三轴模型？ [Completeness, Spec §7.3]
- [ ] CHK006 - Memory Object 的 score 是否包含 relevance/confidence/freshness 三个维度？ [Completeness, Spec §7.3]
- [ ] CHK007 - 是否定义了 superseded_by 和 conflict_with 字段用于处理记忆更新和冲突？ [Completeness, Spec §7.3]
- [ ] CHK008 - event_type 是否明确定义了枚举值（chat_turn, task_result, decision, preference, constraint, evidence）？ [Clarity, Spec §7.2]
- [ ] CHK009 - Tier 枚举是否包含 working/hot/warm/cold/archive 五级？ [Completeness, Spec §7.4]
- [ ] CHK010 - State 枚举是否包含 active/latent/reinforced/decaying/superseded/conflicted/quarantined/archived 八种状态？ [Completeness, Spec §7.4]

## 2. 存储与可重建检查

- [ ] CHK011 - 事件存储是否采用 append-only 模式以保证不可变性？ [Completeness, Const. §III]
- [ ] CHK012 - 是否所有 Memory Object 都可从 raw events 100% 重建？ [Completeness, Spec §6.1]
- [ ] CHK013 - rebuild 操作是否幂等（多次执行结果一致）？ [Clarity, Spec §6.1]
- [ ] CHK014 - rebuild 是否支持全量重建和增量重建两种模式？ [Completeness, Plan §Phase 0]
- [ ] CHK015 - 事件表是否建立了 scope 和 timestamp 的索引以支持高效查询？ [Performance, Plan §Phase 0]
- [ ] CHK016 - 是否定义了 event_metadata 表用于存储索引元数据？ [Completeness, Plan §Phase 0]

## 3. Recall/Remember 接口检查

- [ ] CHK017 - remember(event) 接口是否验证事件格式并返回 event_id？ [Completeness, Spec §FR-017]
- [ ] CHK018 - recall(query, context) 接口是否实现完整的 cue → candidate → conflict → gist → detail → evidence 链路？ [Completeness, Spec §FR-023]
- [ ] CHK019 - recall_gist 是否返回精简版本而跳过详细内容和冲突检查？ [Clarity, Spec §FR-014]
- [ ] CHK020 - expand(memory_id) 是否返回记忆完整详情？ [Completeness, Spec §FR-015]
- [ ] CHK021 - explain(memory_id) 是否说明召回原因、来源事件、当前状态和关联记忆？ [Completeness, Spec §FR-016]
- [ ] CHK022 - capture_chat_turn 方法是否自动提取关键信息并结构化存储？ [Completeness, Spec §FR-019]
- [ ] CHK023 - capture_task_result 方法是否支持记录成功/失败经验和证据？ [Completeness, Spec §FR-020]
- [ ] CHK024 - capture_decision 方法是否捕获决策及其上下文？ [Completeness, Spec §FR-021]

## 4. Tier/State/Resolution 生命周期检查

- [ ] CHK025 - 是否定义了 Tier 迁移规则（working → hot → warm → cold → archive）？ [Completeness, Plan §Phase 1]
- [ ] CHK026 - 是否支持自动 tier/state 状态迁移？ [Completeness, Spec §FR-028]
- [ ] CHK027 - 是否提供 consolidate() 接口手动触发状态迁移？ [Completeness, Spec §FR-029]
- [ ] CHK028 - State 迁移是否定义了 ACTIVE ↔ LATENT ↔ DECAYING → SUPERSEDED/ARCHIVED 规则？ [Completeness, Plan §Phase 2]
- [ ] CHK029 - 是否支持 reinforced 状态用于标记被强化的记忆？ [Completeness, Spec §7.4]
- [ ] CHK030 - 是否支持 quarantine 机制隔离争议记忆？ [Completeness, Plan §Phase 2]

## 5. 冲突消解检查

- [ ] CHK031 - conflict check 阶段是否检测互相矛盾的记忆？ [Completeness, Spec §FR-024]
- [ ] CHK032 - 是否在返回结果中包含 evidence 引用？ [Completeness, Spec §FR-025]
- [ ] CHK033 - recall 结果是否标记 conflict_with 字段？ [Clarity, Plan §Phase 1]
- [ ] CHK034 - 冲突记忆是否被自动 quarantine 隔离？ [Completeness, Spec §7.4]
- [ ] CHK035 - 是否支持 superseded 机制标记被替代的记忆？ [Completeness, Plan §Phase 2]

## 6. Adapter 接入检查

- [ ] CHK036 - 是否提供 OpenClaw adapter 实现？ [Completeness, Spec §FR-033]
- [ ] CHK037 - 是否提供 Claude Code adapter 实现？ [Completeness, Spec §FR-034]
- [ ] CHK038 - 是否提供 Codex CLI adapter 实现？ [Completeness, Spec §FR-035]
- [ ] CHK039 - 是否提供 Python SDK（script agent）适配器？ [Completeness, Spec §FR-036]
- [ ] CHK040 - 是否提供 Web UI proxy/sidecar 方案？ [Completeness, Spec §FR-037]
- [ ] CHK041 - SDK 是否支持函数调用和上下文管理器两种形态？ [Clarity, Plan §接入设计]
- [ ] CHK042 - 适配器是否采用 Wrapper > Hook > Proxy 的优先顺序？ [Consistency, Plan §Phase 3]

## 7. 作用域与权限边界检查

- [ ] CHK043 - 是否支持 user/workspace/project/session 四级作用域？ [Completeness, Spec §FR-038]
- [ ] CHK044 - 是否严格隔离不同作用域的记忆？ [Completeness, Spec §FR-039]
- [ ] CHK045 - 是否支持跨作用域显式共享（需用户授权）？ [Completeness, Spec §FR-040]
- [ ] CHK046 - 是否防止 private memory 自动暴露给不相关 agent？ [Completeness, Const. §合规]
- [ ] CHK047 - 写入权限是否验证符合作用域隔离要求？ [Completeness, Spec §FR-018]

## 8. 性能与稳定性检查

- [ ] CHK048 - Recall P50 延迟是否 < 100ms？ [Measurability, Spec §6.8]
- [ ] CHK049 - Recall P95 延迟是否 < 500ms？ [Measurability, Spec §6.8]
- [ ] CHK050 - Write 延迟是否 < 50ms？ [Measurability, Spec §6.8]
- [ ] CHK051 - Full Rebuild (10k events) 是否 < 30s？ [Measurability, Spec §6.8]
- [ ] CHK052 - 是否支持 >= 5 个并发写入器？ [Completeness, Spec §6.8]
- [ ] CHK053 - 是否实现了 single-writer 受控提交机制？ [Completeness, Const. §IV]
- [ ] CHK054 - 是否保证单机环境下的稳定运行和异常恢复？ [Completeness, Spec §6.5]

## 9. Replay/Backtest 检查

- [ ] CHK055 - 是否记录 retrieval_traces 用于分析和调试？ [Completeness, Plan §Phase 4]
- [ ] CHK056 - 是否定义了 benchmark 数据集？ [Completeness, Plan §Phase 4]
- [ ] CHK057 - replay_eval 是否输出评分准确率等指标？ [Completeness, Spec §FR-031]
- [ ] CHK058 - 是否支持在线轻评分（relevance/confidence/freshness）？ [Completeness, Spec §FR-030]
- [ ] CHK059 - 是否支持离线校准以调整评分规则？ [Completeness, Spec §FR-032]
- [ ] CHK060 - 是否提供层级健康分析报告？ [Completeness, Plan §Phase 4]

## 10. Verify/Evidence 检查

- [ ] CHK061 - 是否提供 verify_smoke.sh 冒烟测试脚本？ [Completeness, Spec §6.10]
- [ ] CHK062 - smoke 测试是否覆盖 remember/recall/rebuild/eval 核心功能？ [Completeness, Plan §Smoke]
- [ ] CHK063 - 每次实现是否产出 runs/<run_id>/evidence.md？ [Completeness, Const. §Change Strategy]
- [ ] CHK064 - evidence.md 是否记录代码变更、测试结果、验证项？ [Completeness, Plan §Evidence]
- [ ] CHK065 - 是否每个关键模块都有对应的 evidence 映射？ [Completeness, Spec §14.1]

## 11. Rollback/Cleanup 检查

- [ ] CHK066 - 是否定义了 rollback.md 回滚方案？ [Completeness, Plan §Rollback]
- [ ] CHK067 - 数据损坏场景是否有 rebuild --full 回滚方案？ [Completeness, Plan §Rollback]
- [ ] CHK068 - 版本升级不兼容是否有回滚方案？ [Completeness, Plan §Rollback]
- [ ] CHK069 - 适配器故障是否有降级方案？ [Completeness, Plan §Rollback]
- [ ] CHK070 - 是否定义了大规模删除的人工确认流程？ [Completeness, Const. §IX]

## 12. Human-in-the-Loop 检查

- [ ] CHK071 - 高风险动作（支付/购票/删除/生产变更）是否必须人工确认？ [Completeness, Const. §IX]
- [ ] CHK072 - 冲突记忆召回是否在返回前需要用户选择？ [Completeness, Plan §Human-in-the-Loop]
- [ ] CHK073 - 敏感记忆跨域共享是否需要用户授权？ [Completeness, Plan §Human-in-the-Loop]
- [ ] CHK074 - 是否禁止自动执行高风险动作？ [Completeness, Const. §Prohibitions]
- [ ] CHK075 - 是否定义了明确的 Human-in-the-loop 停点清单？ [Completeness, Plan §Human-in-the-Loop]

## 13. Adapter Contract 检查

- [ ] CHK076 - 是否所有 adapter 都实现了 get_name/before_response/after_response 接口？ [Completeness, Plan §Phase 3A]
- [ ] CHK077 - Context 字段是否正确映射到 scope？ [Completeness, Plan §Phase 3A]
- [ ] CHK078 - Injection policy 是否支持截断和分层限制？ [Clarity, Plan §Phase 3A]
- [ ] CHK079 - 错误场景是否遵循 fail-open 降级策略？ [Completeness, Plan §Phase 3A]
- [ ] CHK080 - Scope mapping 是否支持环境变量自动推断？ [Completeness, Plan §Phase 3A]

## 14. Cross-tool E2E 检查

- [ ] CHK081 - 同用户同项目 recall 命中率是否 > 80%？ [Measurability, Plan §Phase 3C]
- [ ] CHK082 - 不同项目 scope 隔离是否严格？ [Completeness, Plan §Phase 3C]
- [ ] CHK083 - Injection 长度是否 < 2000 chars？ [Measurability, Plan §Phase 3C]
- [ ] CHK084 - Explain 是否返回完整证据链？ [Completeness, Plan §Phase 3C]
- [ ] CHK085 - Cross-tool E2E 测试是否可独立运行？ [Clarity, Plan §Phase 3C]

## 15. Replay/Eval 检查

- [ ] CHK086 - 是否记录 retrieval_traces 用于分析？ [Completeness, Plan §Phase 4A]
- [ ] CHK087 - 是否定义 adapter recall quality benchmark？ [Completeness, Plan §Phase 4A]
- [ ] CHK088 - 跨工具 recall 命中率是否可计算？ [Measurability, Plan §Phase 4A]
- [ ] CHK089 - 冲突注入测试是否验证冲突检测？ [Completeness, Plan §Phase 4A]
- [ ] CHK090 - Prompt 膨胀指标是否可监控？ [Measurability, Plan §Phase 4A]

## 16. P0 Fix Gate Checklist

本章节专门用于 P0 修复验收，每个 Gate 必须全部通过才能进入下一阶段或第二适配器。

### 16.1 Adapter Contract Gate (P0-A)

- [X] CHK091 - get_name() 接口是否返回统一的工具名称字符串？ [T-P0-02]
- [X] CHK092 - get_scope_from_context() 是否返回完整的 scope dict (user/workspace/project/session/tool)？ [T-P0-03]
- [X] CHK093 - before_response(query, context) -> str 接口签名是否未被破坏？ [T-P0-03]
- [X] CHK094 - after_response(query, response, context) -> str 接口签名是否未被破坏？ [T-P0-03]
- [X] CHK095 - 所有 adapter 是否使用统一的 Context 最小字段定义？ [T-P0-03]
- [X] CHK096 - 错误降级是否遵循 fail-open 策略（不阻塞主流程）？ [T-P0-04]

### 16.2 Scope End-to-End Gate (P0-B)

- [X] CHK097 - tool 字段是否已添加到 events 表 schema？ [T-P0-08]
- [X] CHK098 - tool 字段是否已添加到 memory_objects 表 schema？ [T-P0-08]
- [X] CHK099 - EventStore.query() 是否支持 tool 过滤？ [T-P0-08]
- [X] CHK100 - MemoryStore.query() 是否支持 tool 过滤？ [T-P0-08]
- [X] CHK101 - 不同 tool 的记忆是否严格隔离（跨 tool 检索返回空）？ [T-P0-09]
- [X] CHK102 - scope matrix 测试是否覆盖 user/workspace/project/session/tool 所有组合？ [T-P0-10]

### 16.3 Recall Fallback Gate (P0-C)

- [X] CHK103 - recall 是否支持 session miss -> project fallback？ [T-P0-12]
- [X] CHK104 - recall 是否支持 project miss -> workspace fallback？ [T-P0-12]
- [X] CHK105 - recall 是否支持 workspace miss -> user fallback？ [T-P0-12]
- [X] CHK106 - fallback 策略是否可通过配置调整（至少代码常量级）？ [T-P0-13]
- [X] CHK107 - cross-session 同项目召回测试是否通过？ [T-P0-14]
- [X] CHK108 - recall trace 是否包含 fallback_level 字段记录回退来源？ [T-P0-15]

### 16.4 Explainability Gate (P0-D)

- [X] CHK109 - explain(memory_id) 合法输入是否返回完整结构（memory/source_events/related_memories/state_info）？ [T-P0-17]
- [X] CHK110 - explain() 是否能正确加载 source_events（追溯到原始事件）？ [T-P0-17]
- [X] CHK111 - explain(memory_id) 非法输入（如不存在 ID）是否返回明确错误而非抛异常？ [T-P0-18]
- [X] CHK112 - explain() 输出是否 JSON-serializable（无 datetime 等复杂类型）？ [T-P0-19]
- [X] CHK113 - explain 单元测试是否覆盖合法/非法两种输入？ [T-P0-18]

### 16.5 EventStore.query(scope) Gate (P0-E)

- [X] CHK114 - EventStore.query(scope) 是否已摆脱脆弱的 JSON LIKE 字符串匹配？ [T-P0-21]
- [X] CHK115 - scope 查询是否使用可靠的 JSON 提取或拆列方案？ [T-P0-22]
- [X] CHK116 - 事件表是否建立了 scope 相关索引？ [T-P0-22]
- [X] CHK117 - event query 测试是否验证精确匹配（不误召回）？ [T-P0-24]
- [X] CHK118 - 复杂 scope 查询（如 user= A, project= B）是否返回正确结果？ [T-P0-23]

### 16.6 Smoke / Evidence Gate (P0-F)

- [ ] CHK119 - verify_smoke.sh 是否覆盖 5 个 P0 核心功能？ [T-P0-25]
- [ ] CHK120 - adapter_test.py 是否包含 scope 相关测试？ [T-P0-25]
- [ ] CHK121 - P0 regression test 套件是否可独立运行？ [T-P0-26]
- [ ] CHK122 - ops/rollback.md 是否已更新 P0 相关回滚场景？ [T-P0-29]

### 16.7 Second Adapter Go/No-Go Gate

- [ ] CHK123 - evidence.md 是否明确列出已验证项？ [T-P0-30]
- [ ] CHK124 - evidence.md 是否明确列出未验证项？ [T-P0-30]
- [ ] CHK125 - evidence.md 是否明确列出已知限制？ [T-P0-30]
- [ ] CHK126 - evidence.md 是否明确写出 second-adapter gate 判定（PASS/NO-GO）？ [T-P0-30]
- [ ] CHK127 - 是否所有 P0 Gate 检查项均已通过（CHK091~CHK126）？ [T-P0-30]

---

## 总结

| 章节 | 检查项数量 | 覆盖范围 |
|------|------------|----------|
| 协议与数据模型 | 10 | Event Envelope, Memory Object, 枚举定义 |
| 存储与可重建 | 6 | append-only, rebuild, 索引 |
| Recall/Remember | 8 | 核心接口, 快捷方法 |
| Tier/State/Resolution | 6 | 状态迁移, consolidate |
| 冲突消解 | 5 | conflict check, superseded |
| Adapter 接入 | 7 | 5种适配器, SDK形态 |
| 作用域与权限 | 5 | 四级隔离, 跨域共享 |
| 性能与稳定性 | 7 | 性能目标, 并发安全 |
| Replay/Backtest | 6 | traces, benchmark, 评分 |
| Verify/Evidence | 5 | smoke, evidence.md |
| Rollback/Cleanup | 5 | 回滚方案, 清理 |
| Human-in-the-Loop | 5 | 停点, 风险确认 |
| Adapter Contract | 5 | 通用接口, scope mapping, injection policy |
| Cross-tool E2E | 5 | 跨工具 recall, scope 隔离 |
| Replay/Eval | 5 | traces, benchmark, 膨胀监控 |
| **P0 Fix Gate** | **37** | **P0 修复验收专用** |

**总计**: 159 条检查项 (127 + 32)

**使用说明**:
- 实现前：对照检查项确认需求完整
- 实现中：逐项验证实现符合规范
- 实现后：检查清单作为验收依据

**P0 Fix Gate 使用说明**:
- CHK091~CHK126: P0 修复验收检查项
- CHK127: 全部 P0 Gate 通过判定
- 只有 CHK091~CHK126 全部通过，才能进入第二适配器阶段
- evidence.md 必须明确写出 second-adapter gate 判定

---

## 14. Real Host Session Evidence Checklist

**Purpose**: 真实宿主会话级 bridge 验收检查清单，用于指导人工交互实证 run
**Based On**: runs/012-real-host-bridge-validation/evidence.md, known_limits.md

### A. Binary / Environment

- [ ] RH001 - 是否执行了 `which claude` 并记录了真实路径？ [Evidence]
- [ ] RH002 - 是否执行了 `claude --version` 并记录了版本号？ [Evidence]
- [ ] RH003 - 是否执行了 `which codex` 并记录了真实路径？ [Evidence]
- [ ] RH004 - 是否执行了 `codex --version` 并记录了版本号？ [Evidence]
- [ ] RH005 - 是否执行了 `which openclaw` 并明确记录为 BLOCKED？ [Evidence]
- [ ] RH006 - 所有 binary 检查是否与当前机器事实一致？ [Evidence]

### B. Claude Real Host Session 闭环

- [ ] RH007 - 是否通过真实 `claude --mcp-config ...` 启动了 Claude 会话？ [Evidence]
- [ ] RH008 - 是否在 Claude 会话内实际触发了 remember（/remember 或 ocmf_remember）？ [Evidence]
- [ ] RH009 - 是否通过 sqlite 查询验证了数据库中有新写入的 event_id？ [Evidence]
- [ ] RH010 - 写入事件的 `source_tool` 字段是否为 `claude-code`？ [Evidence]
- [ ] RH011 - 是否在 Claude 会话内实际触发了 recall（/recall 或 ocmf_recall）？ [Evidence]
- [ ] RH012 - recall 结果的 count 是否 >= 1？ [Evidence]
- [ ] RH013 - recall 结果是否包含之前写入的记忆内容（真实文本）？ [Evidence]

### C. Codex Real Host Session 闭环

- [ ] RH014 - 是否执行了 `codex mcp list` 确认 MCP 服务器已添加？ [Evidence]
- [ ] RH015 - 是否在 Codex 会话内实际触发了 ocmf_remember 工具？ [Evidence]
- [ ] RH016 - 是否通过 sqlite 查询验证了数据库中有新写入的 event_id？ [Evidence]
- [ ] RH017 - 写入事件的 `source_tool` 字段是否为 `codex-cli`？ [Evidence]
- [ ] RH018 - 是否在 Codex 会话内实际触发了 ocmf_recall 工具？ [Evidence]
- [ ] RH019 - recall 结果的 count 是否 >= 1？ [Evidence]
- [ ] RH020 - recall 结果是否包含之前写入的记忆内容（真实文本）？ [Evidence]

### D. Cross-tool Real Host Isolation

- [ ] RH021 - 是否有真实的 Claude 写 → Codex recall 命令和输出？ [Evidence]
- [ ] RH022 - Claude 写 → Codex recall 的结果 count 是否为 0？ [Evidence]
- [ ] RH023 - 是否有真实的 Codex 写 → Claude recall 命令和输出？ [Evidence]
- [ ] RH024 - Codex 写 → Claude recall 的结果 count 是否为 0？ [Evidence]
- [ ] RH025 - 是否有 sqlite 查询结果证明 tool 字段隔离？ [Evidence]
- [ ] RH026 - 是否没有使用占位 event_id（必须是真实 UUID）？ [Evidence]

### E. Evidence Hygiene

- [ ] RH027 - binary_check.md 是否与当前机器事实一致？ [Evidence]
- [ ] RH028 - claude_strict_real_host.md 是否包含真实会话级证据（不只是 COMPONENT_READY）？ [Evidence]
- [ ] RH029 - codex_strict_real_host.md 是否包含真实会话级证据（不只是 COMPONENT_READY）？ [Evidence]
- [ ] RH030 - cross_tool_strict.md 是否基于真实宿主路径（不只是 direct MCP invocation）？ [Evidence]
- [ ] RH031 - evidence.md 是否严格区分了 real host bridge / direct MCP / manual adapter / synthetic test？ [Evidence]
- [ ] RH032 - known_limits.md 是否明确标注了哪些项需要人工交互？ [Evidence]

---

## 总结（更新）

| 章节 | 检查项数量 | 覆盖范围 |
|------|------------|----------|
| 协议与数据模型 | 10 | Event Envelope, Memory Object, 枚举定义 |
| 存储与可重建 | 6 | append-only, rebuild, 索引 |
| Recall/Remember | 8 | 核心接口, 快捷方法 |
| Tier/State/Resolution | 6 | 状态迁移, consolidate |
| 冲突消解 | 5 | conflict check, superseded |
| Adapter 接入 | 7 | 5种适配器, SDK形态 |
| 作用域与权限 | 5 | 四级隔离, 跨域共享 |
| 性能与稳定性 | 7 | 性能目标, 并发安全 |
| Replay/Backtest | 6 | traces, benchmark, 评分 |
| Verify/Evidence | 5 | smoke, evidence.md |
| Rollback/Cleanup | 5 | 回滚方案, 清理 |
| Human-in-the-Loop | 5 | 停点, 风险确认 |
| Adapter Contract | 5 | 通用接口, scope mapping, injection policy |
| Cross-tool E2E | 5 | 跨工具 recall, scope 隔离 |
| Replay/Eval | 5 | traces, benchmark, 膨胀监控 |
| P0 Fix Gate | 37 | P0 修复验收专用 |
| **Real Host Session** | **32** | **会话级 bridge 验收** |
