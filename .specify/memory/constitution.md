# OpenClaw Memory Fabric (OCMF) Constitution

## Core Principles

### I. Protocol-First
所有功能实现必须先定义统一的协议（Memory Event Envelope / Recall API / Remember API），再开发适配器和 UI。协议是所有接入方的共同契约，必须保持稳定和可扩展。

### II. Event-Sourced
所有长期记忆必须可追溯到原始事件。任何记忆对象的最终状态都必须能够通过重放相关事件来重建，确保记忆系统的可审计性和可追溯性。

### III. Single Source of Truth
Raw append-only event log 是底账，是唯一可信来源。记忆对象层从 event log 重建而来，可重放、可重建，但不直接作为写入目标。

### IV. Controlled Commit
多生产者（多个 AI 工具）可以并发写入事件，但长期对象状态的更新必须通过受控提交机制（single-writer / controlled committer），避免并发冲突和数据不一致。

### V. Evidence-First
关键动作（决策、召回、调优）必须有证据链支撑。所有重要操作必须记录证据，输出必须可验收、可追溯。

### VI. Explainable Recall
召回过程必须可解释。不做不可审计的黑盒注入。每次召回必须说明为何召回、来源是什么、证据链是什么。

### VII. Tool-Agnostic
架构设计不绑定任何单一 AI 工具。必须支持 OpenClaw、Claude Code、Codex CLI、脚本 agent、Web UI proxy 等多种工具的平等接入。

### VIII. Single-Machine First
第一阶段优先单机架构，确保稳定性和可靠性。多机/云化方案在单机验证成熟后再考虑。

### IX. Human-in-the-Loop on Risk
风险红线必须停在人工确认点。本项目默认禁止自动执行支付、购票、删除数据、生产环境变更、账号操作等高风险动作。

### X. Small and Testable
任务必须小、可执行、可验收。每次实现必须产出 runs/&lt;run_id&gt;/evidence.md，确保有交付物可验证。

## Terminology

| 术语 | 定义 |
|------|------|
| Event | 原始记忆事件，是写入系统的最小单位 |
| Memory Object | 由 events 聚合而成的长期记忆对象 |
| Entity/Topic | 跨事件的实体或主题 |
| Tier | 记忆分层：working / hot / warm / cold / archive |
| Resolution | 召回精度：cue / gist / detail / evidence |
| State | 记忆状态：active / latent / reinforced / decaying / superseded / conflicted / quarantined / archived |
| Recall | 基于线索检索并重建相关记忆的过程 |
| Remember | 将会话/任务/决策/证据写入记忆系统的过程 |
| Consolidation | 从 raw events 聚合并更新长期对象层的过程 |
| Replay/Backtest | 回放历史轨迹评估评分和分层效果 |

## Non-Goals

- **NG1**: 第一阶段不做分布式多机一致性系统
- **NG2**: 第一阶段不做云端 SaaS 多租户产品
- **NG3**: 第一阶段不追求复杂 UI 先行，优先保证协议、写入、检索、回放与接入
- **NG4**: 第一阶段不强依赖某一家模型厂商或单一 agent runtime
- **NG5**: 第一阶段不把所有外部系统（邮箱/IM/浏览器/日历）一次性全接完，只要求架构可扩展

## Constraints

### 技术栈
- 语言：Python 3.11+
- 存储：SQLite（优先）+ FTS5 + 可选本地向量检索
- 平台：Mac / Windows / Linux 兼容
- 接口形态：Python SDK + CLI + 本地 HTTP 服务

### 运行环境
- 单机优先，本地开发环境优先
- 需适配用户现有 OpenClaw / Claude Code / Codex CLI 工作流

### 依赖限制
- 尽量轻依赖，避免引入复杂分布式基础设施
- 向量能力可插拔，不强制绑定

## Risks

### 高风险动作
本项目默认禁止自动执行以下高风险动作，若未来涉及，必须 Human-in-the-loop：
- 支付/购票
- 删除数据
- 生产环境变更
- 账号操作

### 合规/权限限制
- 必须支持权限边界、workspace/project/user 作用域隔离
- 不得默认跨作用域泄漏敏感上下文
- 不得把 private memory 自动暴露给不相关 agent

## Requirements (Must Have)

1. 统一 Memory Event Envelope
2. 统一 Recall API / Remember API
3. Raw append-only event log + 可重建对象层
4. Type / Tier / Resolution / State 四轴模型
5. 检索链路支持 cue → candidate set → conflict check → gist → detail → evidence
6. 多生产者写入、受控提交者更新长期状态
7. 基础评分 + 离线 replay/backtest 校准
8. explainability：说明为何召回、为何升层/降层/隔离
9. 证据驱动：关键决策、召回、调优必须能追证
10. 提供无痛接入 adapter 方案与最小 SDK

## Requirements (Should Have)

1. SQLite + FTS5 + 可选本地向量检索
2. 统一 CLI / 本地服务模式
3. OpenClaw / Claude Code / Codex CLI 的 adapter 示例
4. runs/&lt;run_id&gt;/evidence.md 自动落证
5. replay benchmark 脚本与最小 smoke

## Prohibitions

1. 工具直接写长期记忆对象表，绕过统一事件层
2. 无版本链、无证据、不可重建的黑盒记忆写入
3. 在 recall 时无冲突检查就直接注入互相矛盾内容
4. 高风险动作自动执行
5. 架构强耦合到某单一 AI 工具内部

## Change Strategy

- 所有重大架构变更必须更新 docs/constitution.md、docs/spec.md、docs/plan.md
- 协议字段如需破坏性升级，必须定义版本号与兼容策略
- 每次实现必须产出 runs/&lt;run_id&gt;/evidence.md
- 先保证协议稳定，再扩展接入面和高级功能

## Governance

### 宪法优先
本宪法文件优先于所有其他实践准则。所有 spec/plan/tasks/implement 必须遵循本宪法，不得发生冲突。

### 修订流程
- 重大修订需要更新版本号
- 所有修订必须记录变更原因
- 修订后需要确保与其他 design artifacts 保持一致

### 版本号规则
- MAJOR：向后不兼容的原则移除或重新定义
- MINOR：新增原则或实质性扩展指导
- PATCH：澄清、措辞、非语义性改进

### 合规检查
- 所有 PR/代码审查必须验证与本宪法的合规性
- 复杂度必须有充分理由
- 使用本宪法作为运行时开发指导的依据

---

**Version**: 1.0.0 | **Ratified**: 2026-03-10 | **Last Amended**: 2026-03-10
