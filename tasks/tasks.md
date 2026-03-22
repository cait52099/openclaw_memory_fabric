# OCMF Phase 7C: Unified Install E2E / Host Wiring Closure 任务清单

**Project**: OpenClaw Memory Fabric (OCMF)
**Run ID**: 030-unified-install-e2e
**Goal**: 把 unified entry 推进到可信安装闭环，完成真实的 install -> status -> usable memory path
**Boundary**: 本轮只做 install / status / host wiring / quickstart 对齐 / evidence 更新

---

## 背景

Claude 路线已收口 (Run 020)：
- Method A1 (native auto-trigger) = ✅ PASS
- Pure Method A (native context injection) = ❌ FAIL
- Method B (system-prompt assisted) = ✅ PASS
- Production path = A1 + B

Codex 路线已收口 (Run 022)：
- Method A = ❌ NOT AVAILABLE (no hooks)
- Method B = ⚠️ UNTESTED
- Method C (manual MCP) = ✅ PASS
- Production path = C

OpenClaw 路线 BLOCKED (Run 024)：
- GitHub release 404，无法安装
- OpenClaw real host proof = BLOCKED
- OpenClaw production path = TBD

Cross-Host UX Spec 已完成 (Run 024)：
- provenance / conflict / explain 规范已定义 (FR-047~FR-058)
- spec.md 已更新 Section 5.15

Phase 6D 本轮任务：
- 把 cross-host UX spec 从文档推进到可运行实现
- 优先落地 recall / explain 输出层

---

## 任务清单

### A. Codex Binary / MCP / Handshake 能力核实

- [x] T-5B-01 [P] 验证 Codex 命令入口可用性
  - **任务名称**: 验证 Codex 命令入口可用性
  - **目标**: 确认 codex 命令可用
  - **输入**: `which codex`, `codex --version`
  - **输出**: Codex binary 证据
  - **步骤**:
    1. 执行 `which codex`
    2. 执行 `codex --version`
    3. 记录退出码和输出
  - **Evidence**: runs/021-codex-real-host-closure/binary_check.md
  - **AC**: AC-CDX-001
  - **风险**: Codex 未安装
  - **Human-in-the-loop**: 否

- [x] T-5B-02 [P] 验证 Codex MCP 支持
  - **任务名称**: 验证 Codex MCP 支持
  - **目标**: 确认 Codex 支持 MCP 配置
  - **输入**: `codex --help | grep mcp`
  - **输出**: MCP 可用性证据
  - **步骤**:
    1. 执行 `codex --help | grep -i mcp`
    2. 测试 `codex mcp` 子命令
    3. 记录 MCP 配置方式
  - **Evidence**: runs/021-codex-real-host-closure/mcp_check.md
  - **AC**: AC-CDX-002
  - **风险**: MCP 不可用
  - **Human-in-the-loop**: 否

- [x] T-5B-03 探测 Codex hooks / plugin 机制
  - **任务名称**: 探测 Codex hooks / plugin 机制
  - **目标**: 了解 Codex 是否支持 hooks 或 plugin
  - **输入**: Codex 帮助文档、codex hooks
  - **输出**: Codex hooks 分析
  - **步骤**:
    1. 执行 `codex --help` 查看 hooks 相关选项
    2. 测试 `codex hooks` 子命令 (如存在)
    3. 记录发现的 hook 点
  - **Evidence**: runs/021-codex-real-host-closure/codex_hooks.md
  - **AC**: AC-CDX-004
  - **风险**: hooks 不可用
  - **Human-in-the-loop**: 否

---

### B. Codex Real Host Proof

- [x] T-5B-04 [P] Codex MCP 配置 OCMF
  - **任务名称**: Codex MCP 配置 OCMF
  - **目标**: 配置 Codex 使用 OCMF MCP Server
  - **输入**: Codex MCP 配置方式
  - **输出**: Codex MCP 配置结果
  - **步骤**:
    1. 确定 Codex MCP 配置路径
    2. 创建 MCP 配置 JSON
    3. 添加 OCMF MCP Server
  - **Evidence**: runs/021-codex-real-host-closure/mcp_config.md
  - **AC**: AC-CDX-001, AC-CDX-002
  - **风险**: MCP 配置格式错误
  - **Human-in-the-loop**: 否

- [x] T-5B-05 Codex real host remember
  - **任务名称**: Codex real host remember
  - **目标**: 通过真实 Codex CLI 触发一次 remember
  - **输入**: 配置好的 Codex MCP
  - **输出**: SQLite 事件记录
  - **步骤**:
    1. 在 Codex 会话中调用 ocmf_remember
    2. 记录 event_id
    3. 验证 SQLite 落库
  - **Evidence**: runs/021-codex-real-host-closure/remember_test.md
  - **AC**: AC-CDX-001, AC-CDX-003
  - **风险**: MCP 调用失败
  - **Human-in-the-loop**: 否

- [x] T-5B-06 Codex real host recall
  - **任务名称**: Codex real host recall
  - **目标**: 通过真实 Codex CLI 触发一次 recall
  - **输入**: Codex MCP + remember 结果
  - **输出**: Recall 结果
  - **步骤**:
    1. 在 Codex 会话中调用 ocmf_recall
    2. 验证能召回 remember 的内容
    3. 记录召回结果
  - **Evidence**: runs/021-codex-real-host-closure/recall_test.md
  - **AC**: AC-CDX-001, AC-CDX-003
  - **风险**: Recall 失败
  - **Human-in-the-loop**: 否

---

### C. Codex Same-Tool Remember + Recall 闭环

- [x] T-5B-07 [P] Codex same-tool 闭环验证
  - **任务名称**: Codex same-tool 闭环验证
  - **目标**: 验证 Codex 可以 recall 自己 remember 的内容
  - **输入**: Codex MCP
  - **输出**: 闭环证据
  - **步骤**:
    1. Codex remember 特定内容
    2. Codex recall 相同上下文
    3. 验证能召回
  - **Evidence**: runs/021-codex-real-host-closure/closed_loop.md
  - **AC**: AC-CDX-003
  - **风险**: 闭环不工作
  - **Human-in-the-loop**: 否

---

### D. Codex Native Automation Boundary

- [x] T-5B-08 验证 Codex native auto-trigger
  - **任务名称**: 验证 Codex native auto-trigger
  - **目标**: 确认 Codex 是否支持 native hooks
  - **输入**: Codex hooks 探测结果
  - **输出**: Auto-trigger 边界
  - **步骤**:
    1. 分析 T-5B-03 的 hooks 探测结果
    2. 尝试配置一个 auto-trigger
    3. 测试是否能自动触发
  - **Evidence**: runs/021-codex-real-host-closure/native_auto.md
  - **AC**: AC-CDX-004
  - **风险**: hooks 限制
  - **Human-in-the-loop**: 否

- [x] T-5B-09 判定 Codex production path
  - **任务名称**: 判定 Codex production path
  - **目标**: 明确 Codex 最终 production path
  - **输入**: 所有验证结果
  - **输出**: Method A/B/C 分类
  - **步骤**:
    1. 汇总 real host proof 结果
    2. 汇总 native automation 结果
    3. 判定 production path
  - **Evidence**: runs/021-codex-real-host-closure/production_path.md
  - **AC**: AC-CDX-005
  - **风险**: 无法判定
  - **Human-in-the-loop**: 是 (确认最终分类)

---

### E. SQLite 对账与证据固化

- [x] T-5B-10 [P] SQLite 对账
  - **任务名称**: SQLite 对账
  - **目标**: 验证所有 Codex 事件正确落库
  - **输入**: Codex 测试产生的所有事件
  - **输出**: 对账报告
  - **步骤**:
    1. 查询所有 source_tool='codex-cli' 的事件
    2. 验证 event_id 连续性
    3. 验证 content 正确性
  - **Evidence**: runs/021-codex-real-host-closure/sqlite_reconciliation.md
  - **AC**: AC-CDX-001
  - **风险**: 对账失败
  - **Human-in-the-loop**: 否

---

### F. 最终 Codex Position 文档

- [x] T-5B-11 [P] 创建 final_codex_position.md
  - **任务名称**: 创建 final_codex_position.md
  - **目标**: 输出 Codex 最终收口文档
  - **输入**: 所有验证结果
  - **输出**: final_codex_position.md
  - **步骤**:
    1. 汇总 Codex Method A/B/C 判定
    2. 明确 production path
    3. 写入文档
  - **Evidence**: runs/021-codex-real-host-closure/final_codex_position.md
  - **AC**: AC-CDX-005
  - **风险**: 文档不完整
  - **Human-in-the-loop**: 是 (确认收口)

- [x] T-5B-12 更新 evidence.md 和 known_limits.md
  - **任务名称**: 更新 evidence.md 和 known_limits.md
  - **目标**: 同步项目证据
  - **输入**: final_codex_position.md
  - **输出**: 更新的证据文件
  - **步骤**:
    1. 更新 runs/021-codex-real-host-closure/evidence.md
    2. 更新 runs/021-codex-real-host-closure/known_limits.md
  - **Evidence**: runs/021-codex-real-host-closure/evidence.md
  - **AC**: 所有 AC
  - **风险**: 文档不一致
  - **Human-in-the-loop**: 否

---

## 并行任务说明

以下任务可并行执行:

- T-5B-01, T-5B-02, T-5B-03 (能力探测)
- T-5B-10, T-5B-11 (证据)
- T-5B-01, T-5B-04 (MCP 配置)

---

## 执行顺序

1. **Phase 1** (可并行): T-5B-01, T-5B-02, T-5B-03 - 能力探测
2. **Phase 2**: T-5B-04 - MCP 配置
3. **Phase 3**: T-5B-05, T-5B-06 - Real host proof
4. **Phase 4**: T-5B-07 - Same-tool 闭环
5. **Phase 5**: T-5B-08, T-5B-09 - Native automation + path
6. **Phase 6**: T-5B-10, T-5B-11, T-5B-12 - 证据

---

## Human-in-the-loop 场景

- T-5B-09: 确认最终 production path
- T-5B-11: 确认收口文档

---

## 验收标准映射

| AC-ID | 相关任务 |
|--------|----------|
| AC-CDX-001 | T-5B-01, T-5B-05, T-5B-06, T-5B-10 |
| AC-CDX-002 | T-5B-02, T-5B-04 |
| AC-CDX-003 | T-5B-05, T-5B-06, T-5B-07 |
| AC-CDX-004 | T-5B-03, T-5B-08 |
| AC-CDX-005 | T-5B-09, T-5B-11, T-5B-12 |

---

## 成功标准

- **OpenClaw Real Host Proof**: 真实 openclaw 宿主触发 remember + recall = ✅
- **OpenClaw Production Path**: 明确 Method A/B/C = ✅
- **Cross-Host UX Spec**: 明确 provenance / conflict / explain 规则 = ✅

---

## Phase 6B: OpenClaw Line Closure

### A. OpenClaw Binary / Env / Host Entry

- [ ] T-6B-01 [P] 验证 OpenClaw 命令入口可用性
  - **任务名称**: 验证 OpenClaw 命令入口可用性
  - **目标**: 确认 openclaw 命令可用
  - **输入**: `which openclaw`, `openclaw --version`
  - **输出**: OpenClaw binary 证据
  - **步骤**:
    1. 执行 `which openclaw` 或等效命令
    2. 记录 OpenClaw 版本和路径
    3. 确认环境是否可用
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/binary_check.md
  - **AC**: AC-OCL-001
  - **风险**: OpenClaw 环境阻塞
  - **Human-in-the-loop**: 否

### B. OpenClaw Real Host Proof

- [ ] T-6B-02 [P] 探测 OpenClaw MCP / extension 机制
  - **任务名称**: 探测 OpenClaw MCP / extension 机制
  - **目标**: 了解 OpenClaw 支持什么扩展机制
  - **输入**: OpenClaw 帮助文档
  - **输出**: OpenClaw extension 分析
  - **步骤**:
    1. 查找 OpenClaw 支持的扩展机制
    2. 测试 MCP 或 hooks 配置
    3. 记录扩展点
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/extension_check.md
  - **AC**: AC-OCL-002
  - **风险**: OpenClaw 无 MCP/hooks
  - **Human-in-the-loop**: 否

- [ ] T-6B-03 OpenClaw real host remember
  - **任务名称**: OpenClaw real host remember
  - **目标**: 通过真实 OpenClaw 宿主触发一次 remember
  - **输入**: OpenClaw extension 配置
  - **输出**: SQLite 事件记录
  - **步骤**:
    1. 通过 OpenClaw 会话调用 ocmf_remember
    2. 记录 event_id
    3. 验证 SQLite 落库
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/remember_test.md
  - **AC**: AC-OCL-003
  - **风险**: MCP/extension 调用失败
  - **Human-in-the-loop**: 否

- [ ] T-6B-04 OpenClaw real host recall
  - **任务名称**: OpenClaw real host recall
  - **目标**: 通过真实 OpenClaw 宿主触发一次 recall
  - **输入**: OpenClaw extension + remember 结果
  - **输出**: Recall 结果
  - **步骤**:
    1. 在 OpenClaw 会话中调用 ocmf_recall
    2. 验证能召回 remember 的内容
    3. 记录召回结果
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/recall_test.md
  - **AC**: AC-OCL-003
  - **风险**: Recall 失败
  - **Human-in-the-loop**: 否

### C. OpenClaw Same-Tool Remember + Recall 闭环

- [ ] T-6B-05 [P] OpenClaw same-tool 闭环验证
  - **任务名称**: OpenClaw same-tool 闭环验证
  - **目标**: 验证 OpenClaw 可以 recall 自己 remember 的内容
  - **输入**: OpenClaw extension
  - **输出**: 闭环证据
  - **步骤**:
    1. OpenClaw remember 特定内容
    2. OpenClaw recall 相同上下文
    3. 验证能召回
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/closed_loop.md
  - **AC**: AC-OCL-003
  - **风险**: 闭环不工作
  - **Human-in-the-loop**: 否

### D. OpenClaw Method Boundary + Production Path

- [ ] T-6B-06 判定 OpenClaw method boundary
  - **任务名称**: 判定 OpenClaw method boundary
  - **目标**: 明确 OpenClaw 的 A/B/C 边界
  - **输入**: 所有 OpenClaw 验证结果
  - **输出**: Method boundary 文档
  - **步骤**:
    1. 分析 OpenClaw extension 机制
    2. 判定是否有 native hooks
    3. 判定是否有 system-prompt 支持
    4. 确定 method boundary
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/method_boundary.md
  - **AC**: AC-OCL-005
  - **风险**: 边界无法判定
  - **Human-in-the-loop**: 是

- [ ] T-6B-07 判定 OpenClaw production path
  - **任务名称**: 判定 OpenClaw production path
  - **目标**: 明确 OpenClaw 最终 production path
  - **输入**: 所有验证结果
  - **输出**: Production path 文档
  - **步骤**:
    1. 汇总 real host proof 结果
    2. 判定 production path
    3. 记录最终分类
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/production_path.md
  - **AC**: AC-OCL-005, AC-OCL-006
  - **风险**: 无法判定
  - **Human-in-the-loop**: 是

### E. OpenClaw Final Position + Evidence

- [ ] T-6B-08 [P] 创建 final_openclaw_position.md
  - **任务名称**: 创建 final_openclaw_position.md
  - **目标**: 输出 OpenClaw 最终收口文档
  - **输入**: 所有验证结果
  - **输出**: final_openclaw_position.md
  - **步骤**:
    1. 汇总 OpenClaw Method A/B/C 判定
    2. 明确 production path
    3. 写入文档
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/final_openclaw_position.md
  - **AC**: AC-OCL-006
  - **风险**: 文档不完整
  - **Human-in-the-loop**: 是

- [ ] T-6B-09 更新 evidence.md 和 known_limits.md
  - **任务名称**: 更新 evidence.md 和 known_limits.md
  - **目标**: 同步 OpenClaw 证据
  - **输入**: final_openclaw_position.md
  - **输出**: 更新的证据文件
  - **步骤**:
    1. 更新 runs/024-openclaw-closure-crosshost-ux/evidence.md
    2. 更新 runs/024-openclaw-closure-crosshost-ux/known_limits.md
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/evidence.md
  - **AC**: AC-OCL-006
  - **风险**: 文档不一致
  - **Human-in-the-loop**: 否

---

## Phase 6C: Minimal Cross-Host UX Spec

### A. Cross-Host UX Specification

- [ ] T-6C-01 [P] 编写 cross_host_ux_spec.md
  - **任务名称**: 编写 cross_host_ux_spec.md
  - **目标**: 制定跨宿主 UX 规范
  - **输入**: host_matrix.md, product_strategy.md
  - **输出**: cross_host_ux_spec.md
  - **步骤**:
    1. 定义 provenance display 规则
    2. 定义 conflict explanation 规则
    3. 定义 recall hit explanation 规则
    4. 定义 source_tool 字段规范
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/cross_host_ux_spec.md
  - **AC**: AC-XHOST-001
  - **风险**: 规范不完整
  - **Human-in-the-loop**: 是

- [ ] T-6C-02 [P] 定义 source_tool 展示规范
  - **任务名称**: 定义 source_tool 展示规范
  - **目标**: 明确 source_tool 到友好名称的映射
  - **输入**: Cross-host UX spec
  - **输出**: source_tool 规范文档
  - **步骤**:
    1. 列出所有已知的 source_tool 值
    2. 定义友好名称映射
    3. 定义展示格式
  - **Evidence**: runs/024-openclaw-closure-crosshost-ux/source_tool_spec.md
  - **AC**: AC-XHOST-002
  - **风险**: 映射不完整
  - **Human-in-the-loop**: 否

### B. Spec Updates

- [ ] T-6C-03 更新 docs/spec.md 相关章节
  - **任务名称**: 更新 docs/spec.md 相关章节
  - **目标**: 将 cross-host UX 规范同步到 spec
  - **输入**: cross_host_ux_spec.md
  - **输出**: 更新的 docs/spec.md
  - **步骤**:
    1. 更新 FR8 检索链路（cross-host 展示）
    2. 更新 FR9 explain()（provenance）
    3. 更新 FR13 作用域隔离（source_tool 维度）
  - **Evidence**: docs/spec.md
  - **AC**: AC-XHOST-001
  - **风险**: spec 不一致
  - **Human-in-the-loop**: 否

### C. Final Integration

- [ ] T-6C-04 [P] 更新统一 evidence 和 known_limits
  - **任务名称**: 更新统一 evidence 和 known_limits
  - **目标**: 将 OpenClaw + Cross-Host UX 结果同步到统一文档
  - **输入**: 所有 Phase 6B/6C 输出
  - **输出**: 更新的 evidence.md, known_limits.md
  - **步骤**:
    1. 更新 runs/023-unified-host-matrix/evidence.md
    2. 更新 runs/023-unified-host-matrix/known_limits.md
    3. 确认与 host_matrix 一致
  - **Evidence**: runs/023-unified-host-matrix/evidence.md
  - **AC**: AC-XHOST-001, AC-OCL-006
  - **风险**: 文档不一致
  - **Human-in-the-loop**: 否

---

## Phase 6D: Cross-Host UX Output Implementation

**Run ID**: 025-cross-host-ux-output
**日期**: 2026-03-22
**目标**: 把 cross-host UX spec 从文档推进到可运行实现

### A. recall 输出增强

- [x] T-6D-01 recall 结果增加 source_tool 字段
  - **任务名称**: recall 结果增加 source_tool 字段
  - **目标**: recall API 返回包含 source_tool 字段
  - **输入**: 当前 recall 实现 (src/ocmaf/retrieval/recall.py)
  - **输出**: 修改后的 recall.py，增加 source_tool 字段
  - **步骤**:
    1. 找到 recall.py 中的结果组装代码
    2. 从 event 中提取 source_tool 字段
    3. 在返回结果中包含 source_tool
  - **Evidence**: src/ocmaf/retrieval/recall.py
  - **AC**: AC-XHOST-IMPL-001
  - **风险**: 不破坏现有 recall 逻辑
  - **Human-in-the-loop**: 否

- [x] T-6D-02 [P] recall 结果增加 source_host_friendly 映射
  - **任务名称**: recall 结果增加 source_host_friendly 映射
  - **目标**: recall API 返回包含 friendly host name
  - **输入**: source_tool 值
  - **输出**: 修改后的 recall.py，增加 source_host_friendly
  - **步骤**:
    1. 定义 FRIENDLY_NAMES 映射字典
    2. 在结果组装时调用映射函数
    3. 确保 synthetic → "Synthetic (Test)"
  - **Evidence**: src/ocmaf/retrieval/recall.py
  - **AC**: AC-XHOST-IMPL-002
  - **风险**: 映射值不正确
  - **Human-in-the-loop**: 否

- [x] T-6D-03 recall 结果增加 timestamp 字段
  - **任务名称**: recall 结果增加 timestamp 字段
  - **目标**: recall API 返回包含 event timestamp
  - **输入**: event 数据
  - **输出**: 修改后的 recall.py，增加 timestamp 字段
  - **步骤**:
    1. 从 event 中提取 timestamp
    2. 在返回结果中包含 timestamp
  - **Evidence**: src/ocmaf/retrieval/recall.py
  - **AC**: AC-XHOST-IMPL-001
  - **风险**: timestamp 格式不统一
  - **Human-in-the-loop**: 否

### B. explain 输出增强

- [x] T-6D-04 explain() 增加 match_reasons 字段
  - **任务名称**: explain() 增加 match_reasons 字段
  - **目标**: explain() 返回为什么记忆被召回
  - **输入**: 当前 explain() 实现
  - **输出**: 修改后的 retrieval/explain.py，增加 match_reasons
  - **步骤**:
    1. 分析 recall 时使用的匹配逻辑
    2. 提取 keyword 匹配和 scope 匹配信息
    3. 在 explain 返回中包含 match_reasons 数组
  - **Evidence**: src/ocmaf/retrieval/explain.py
  - **AC**: AC-XHOST-IMPL-005
  - **风险**: match_reasons 可能不完整
  - **Human-in-the-loop**: 否

- [x] T-6D-05 [P] explain() 增加 source_tool / source_host_friendly
  - **任务名称**: explain() 增加 provenance 字段
  - **目标**: explain() 返回记忆来源信息
  - **输入**: event 数据
  - **输出**: 修改后的 explain.py，增加 source_tool 和 source_host_friendly
  - **步骤**:
    1. 从 event 中提取 source_tool
    2. 调用 friendly name 映射
    3. 在返回中包含 provenance 字段
  - **Evidence**: src/ocmaf/retrieval/explain.py
  - **AC**: AC-XHOST-IMPL-006
  - **风险**: friendly name 映射重复
  - **Human-in-the-loop**: 否

- [x] T-6D-06 explain() 增加 also_written_by 字段
  - **任务名称**: explain() 增加 cross-host context
  - **目标**: 当记忆被多个 host 写入时，显示 also_written_by
  - **输入**: event 数据，EventStore
  - **输出**: 修改后的 explain.py，增加 also_written_by
  - **步骤**:
    1. 查询同一 entity_id 的其他 event
    2. 提取不同 source_tool 的记录
    3. 在返回中包含 also_written_by 数组
  - **Evidence**: src/ocmaf/retrieval/explain.py
  - **AC**: AC-XHOST-IMPL-005
  - **风险**: 查询性能影响
  - **Human-in-the-loop**: 否

### C. conflict detection 最小实现

- [x] T-6D-07 recall 时增加 conflict detection 逻辑
  - **任务名称**: 实现 conflict detection 核心逻辑
  - **目标**: 检测同一 entity 不同 source 的 content 冲突
  - **输入**: recall 候选结果
  - **输出**: 修改后的 recall.py，增加 conflict 检测
  - **步骤**:
    1. 分析候选结果的 entity_id
    2. 检查是否有同一 entity 不同 source_tool 的记录
    3. 比较 content 是否不同（使用 content hash）
    4. 若冲突存在，设置 conflict_detected=true
  - **Evidence**: src/ocmaf/retrieval/recall.py
  - **AC**: AC-XHOST-IMPL-003, AC-XHOST-IMPL-004
  - **风险**: 冲突检测逻辑复杂
  - **Human-in-the-loop**: 否

- [x] T-6D-08 recall 结果增加 candidates 字段
  - **任务名称**: 实现 conflict response
  - **目标**: 当冲突存在时，返回所有冲突的 candidates
  - **输入**: conflict detection 结果
  - **输出**: 修改后的 recall.py，candidates 字段包含所有冲突记忆
  - **步骤**:
    1. 在 conflict_detected=true 时
    2. 收集所有冲突的记忆到 candidates 数组
    3. 每个 candidate 包含 memory_id, content, source_tool, timestamp
  - **Evidence**: src/ocmaf/retrieval/recall.py
  - **AC**: AC-XHOST-IMPL-004
  - **风险**: candidates 可能为空
  - **Human-in-the-loop**: 否

### D. Friendly Name 工具函数

- [x] T-6D-09 [P] 实现 source_tool → friendly name 映射工具函数
  - **任务名称**: 实现 friendly name 映射工具
  - **目标**: 提供统一的 source_tool → friendly name 转换
  - **输入**: source_tool 字符串
  - **输出**: 新文件 src/ocmaf/retrieval/friendly.py
  - **步骤**:
    1. 创建 src/ocmaf/retrieval/friendly.py
    2. 定义 FRIENDLY_NAMES 字典
    3. 实现 get_friendly_name(source_tool) 函数
    4. 确保覆盖所有已知 source_tool 值
  - **Evidence**: src/ocmaf/retrieval/friendly.py
  - **AC**: AC-XHOST-IMPL-002, AC-XHOST-IMPL-007
  - **风险**: 映射不完整
  - **Human-in-the-loop**: 否

### E. Synthetic 测试验证

- [x] T-6D-10 synthetic recall 测试验证
  - **任务名称**: Synthetic recall 输出验证
  - **目标**: 验证 synthetic 记忆的 friendly name 显示正确
  - **输入**: synthetic 测试数据
  - **输出**: 测试通过
  - **步骤**:
    1. 使用 synthetic source_tool 写入一条测试记忆
    2. 调用 recall
    3. 验证返回的 source_host_friendly = "Synthetic (Test)"
  - **Evidence**: synthetic recall 测试结果
  - **AC**: AC-XHOST-IMPL-007
  - **风险**: 测试破坏生产数据
  - **Human-in-the-loop**: 否

### F. Evidence / Documentation

- [x] T-6D-11 更新 evidence.md
  - **任务名称**: 更新 Phase 6D evidence.md
  - **目标**: 记录 Phase 6D 实现成果
  - **输入**: Phase 6D 所有任务输出
  - **输出**: runs/025-cross-host-ux-output/evidence.md
  - **步骤**:
    1. 创建 runs/025-cross-host-ux-output/ 目录
    2. 记录 recall 输出字段增强
    3. 记录 explain 输出字段增强
    4. 记录 conflict detection 实现
    5. 包含实际运行输出
  - **Evidence**: runs/025-cross-host-ux-output/evidence.md
  - **AC**: AC-XHOST-IMPL-001~007
  - **风险**: 文档不完整
  - **Human-in-the-loop**: 否

- [x] T-6D-12 [P] 更新 known_limits.md
  - **任务名称**: 更新 Phase 6D known_limits.md
  - **目标**: 记录 Phase 6D 已知限制
  - **输入**: Phase 6D 实现经验
  - **输出**: runs/025-cross-host-ux-output/known_limits.md
  - **步骤**:
    1. 记录 implemented vs specified-only 边界
    2. 记录未实现的 FR-049/FR-052/FR-055
    3. 更新统一 known_limits.md
  - **Evidence**: runs/025-cross-host-ux-output/known_limits.md
  - **AC**: N/A
  - **风险**: 文档不一致
  - **Human-in-the-loop**: 否

---

## 并行任务说明

以下任务可并行执行:

- T-6D-01, T-6D-02, T-6D-03 (recall 输出增强)
- T-6D-04, T-6D-05, T-6D-06 (explain 输出增强)
- T-6D-07, T-6D-08 (conflict detection)

---

## 执行顺序

1. **Phase 1** (可并行): T-6B-01, T-6B-02 - OpenClaw 能力探测
2. **Phase 2**: T-6B-03, T-6B-04 - OpenClaw real host proof
3. **Phase 3**: T-6B-05 - OpenClaw same-tool 闭环
4. **Phase 4**: T-6B-06, T-6B-07 - Method boundary + production path
5. **Phase 5**: T-6B-08, T-6B-09 - OpenClaw 收口文档
6. **Phase 6**: T-6C-01, T-6C-02, T-6C-03, T-6C-04 - Cross-Host UX + spec 更新
7. **Phase 7**: T-6D-09 (friendly.py) → T-6D-01~06 (output enhancement) → T-6D-07~08 (conflict) → T-6D-10~12 (test/doc)

---

## Human-in-the-loop 场景

- T-6B-06: 确认 OpenClaw method boundary
- T-6B-07: 确认 OpenClaw production path
- T-6B-08: 确认 OpenClaw 收口文档
- T-6C-01: 确认 cross-host UX spec
- (Phase 6D 无 human-in-the-loop 任务)

---

## 验收标准映射

| AC-ID | 相关任务 |
|--------|----------|
| AC-OCL-001 | T-6B-01 |
| AC-OCL-002 | T-6B-02 |
| AC-OCL-003 | T-6B-03, T-6B-04, T-6B-05 |
| AC-OCL-004 | T-6B-06 |
| AC-OCL-005 | T-6B-06, T-6B-07 |
| AC-OCL-006 | T-6B-07, T-6B-08, T-6B-09, T-6C-04 |
| AC-XHOST-001 | T-6C-01, T-6C-03, T-6C-04 |
| AC-XHOST-002 | T-6C-02 |
| AC-XHOST-IMPL-001 | T-6D-01, T-6D-03 |
| AC-XHOST-IMPL-002 | T-6D-02, T-6D-05, T-6D-09 |
| AC-XHOST-IMPL-003 | T-6D-07 |
| AC-XHOST-IMPL-004 | T-6D-07, T-6D-08 |
| AC-XHOST-IMPL-005 | T-6D-04, T-6D-06 |
| AC-XHOST-IMPL-006 | T-6D-05 |
| AC-XHOST-IMPL-007 | T-6D-09, T-6D-10 |

---

## 成功标准

- **OpenClaw Real Host Proof**: 真实 openclaw 宿主触发 remember + recall = ✅ (blocked)
- **OpenClaw Production Path**: 明确 Method A/B/C = ✅ (blocked)
- **OpenClaw 收口**: evidence + known_limits + final_position = ✅ (blocked)
- **Cross-Host UX Spec**: provenance / conflict / explain 规则完整 = ✅
- **Cross-Host UX Output**: recall/explain 输出包含 source_tool + friendly name + conflict detection = 进行中

---

## Phase 6E: Host-Visible Output Integration

**Run ID**: 026-cross-host-visible
**日期**: 2026-03-22
**目标**: 把 Phase 6D API 字段增强推进到用户可见的 CLI 输出

### A. Codex CLI recall 输出格式化

- [x] T-6E-01 [P] Codex CLI recall 输出格式化（source_tool, friendly, timestamp）
  - **任务名称**: Codex CLI recall 输出格式化
  - **目标**: `codex recall` 输出包含 source_tool, friendly name, timestamp
  - **输入**: Phase 6D recall API 输出格式
  - **输出**: Codex CLI recall 格式化输出
  - **步骤**:
    1. 查看当前 Codex MCP recall 实现
    2. 修改返回格式化函数，增加 source_host_friendly 和 timestamp 展示
    3. 输出格式: "From Claude: 'content' (2026-03-22 10:30)"
  - **Evidence**: runs/026-cross-host-visible/codex_recall_format.md
  - **AC**: AC-VIS-001, AC-VIS-002
  - **风险**: 不破坏现有 JSON API
  - **Human-in-the-loop**: 否

### B. Codex CLI explain 输出格式化

- [x] T-6E-02 [P] Codex CLI explain 输出格式化
  - **任务名称**: Codex CLI explain 输出格式化
  - **目标**: `codex recall --explain` 输出包含 match_reasons 和 provenance
  - **输入**: Phase 6D explain API 输出格式
  - **输出**: Codex CLI explain 格式化输出
  - **步骤**:
    1. 查看当前 Codex explain 实现
    2. 修改返回格式化函数，增加 match_reasons 和 source_host_friendly 展示
    3. 输出格式: "Recall reason: keyword match 'testing' + project scope"
  - **Evidence**: runs/026-cross-host-visible/codex_explain_format.md
  - **AC**: AC-VIS-004
  - **风险**: 不破坏现有 JSON API
  - **Human-in-the-loop**: 否

### C. Conflict 输出格式化（Codex CLI）

- [x] T-6E-03 [P] Codex CLI conflict 输出格式化
  - **任务名称**: Codex CLI conflict 输出格式化
  - **目标**: conflict 场景有明确提示，展示不同 source 差异
  - **输入**: Phase 6D conflict detection 结果
  - **输出**: Codex CLI conflict 格式化输出
  - **步骤**:
    1. 查看当前 conflict candidates 返回格式
    2. 修改格式化函数，当 conflict_detected=true 时显示 ⚠️ CONFLICT DETECTED
    3. 展示不同 source 的 candidates，用 friendly name 显示
  - **Evidence**: runs/026-cross-host-visible/codex_conflict_format.md
  - **AC**: AC-VIS-003
  - **风险**: conflict candidates 可能为空
  - **Human-in-the-loop**: 否

### D. Claude system-prompt recall 注入格式化

- [x] T-6E-04 Claude system-prompt recall 注入格式化
  - **任务名称**: Claude system-prompt recall 注入格式化
  - **目标**: Claude 对话中显示的 recall 结果包含 provenance
  - **输入**: Phase 6D recall API 输出
  - **输出**: Claude system-prompt 注入文本格式
  - **步骤**:
    1. 查看当前 Claude system-prompt recall 注入逻辑
    2. 修改注入格式，增加 source_host_friendly 和 timestamp
    3. 输出格式: "From Claude: 'content' (10:30)"
  - **Evidence**: runs/026-cross-host-visible/claude_recall_format.md
  - **AC**: AC-VIS-001
  - **风险**: 不破坏 Claude 正常对话流程
  - **Human-in-the-loop**: 否

### E. Claude system-prompt explain 注入格式化

- [x] T-6E-05 Claude system-prompt explain 注入格式化
  - **任务名称**: Claude system-prompt explain 注入格式化
  - **目标**: Claude 对话中显示的 explain 结果包含 match_reasons
  - **输入**: Phase 6D explain API 输出
  - **输出**: Claude system-prompt 注入文本格式（explain）
  - **步骤**:
    1. 查看当前 Claude explain 注入逻辑
    2. 修改注入格式，增加 match_reasons 说明
    3. 输出格式: "Recalled because: keyword 'testing' + scope project=OCMF"
  - **Evidence**: runs/026-cross-host-visible/claude_explain_format.md
  - **AC**: AC-VIS-004
  - **风险**: 不破坏 Claude 正常对话流程
  - **Human-in-the-loop**: 否

### F. Claude conflict 显示格式化

- [x] T-6E-06 Claude conflict 显示格式化
  - **任务名称**: Claude conflict 显示格式化
  - **目标**: Claude 对话中 conflict 场景有明确提示
  - **输入**: Phase 6D conflict detection 结果
  - **输出**: Claude system-prompt 注入文本格式（conflict）
  - **步骤**:
    1. 查看当前 Claude conflict 显示逻辑
    2. 修改显示格式，当 conflict_detected=true 时显示警告
    3. 输出格式: "⚠️ CONFLICT: 不同宿主对同一问题有不同结论"
  - **Evidence**: runs/026-cross-host-visible/claude_conflict_format.md
  - **AC**: AC-VIS-003
  - **风险**: 不破坏 Claude 正常对话流程
  - **Human-in-the-loop**: 否

### G. Cross-Host Output 集成测试

- [x] T-6E-07 Cross-Host output 集成测试
  - **任务名称**: Cross-Host output 集成测试
  - **目标**: 验证 recall/explain/conflict 的用户可见输出正确
  - **输入**: 所有 Phase 6E 格式化输出
  - **输出**: 测试通过证据
  - **步骤**:
    1. 创建 test_host_visible_output.py 测试脚本
    2. 测试 Codex CLI recall 输出格式
    3. 测试 Codex CLI explain 输出格式
    4. 测试 conflict 输出格式
    5. 验证 Claude system-prompt 注入格式
  - **Evidence**: runs/026-cross-host-visible/test_host_visible_output.py
  - **AC**: AC-VIS-001, AC-VIS-002, AC-VIS-003, AC-VIS-004
  - **风险**: 测试环境隔离
  - **Human-in-the-loop**: 否

### H. Evidence / Documentation

- [x] T-6E-08 [P] 更新 Phase 6E evidence.md
  - **任务名称**: 更新 Phase 6E evidence.md
  - **目标**: 记录 Phase 6E 用户可见输出集成成果
  - **输入**: Phase 6E 所有任务输出
  - **输出**: runs/026-cross-host-visible/evidence.md
  - **步骤**:
    1. 创建 runs/026-cross-host-visible/ 目录
    2. 记录 Codex CLI recall 输出格式
    3. 记录 explain 输出格式
    4. 记录 conflict 输出格式
    5. 记录 Claude system-prompt 注入格式
    6. 包含实际运行输出
  - **Evidence**: runs/026-cross-host-visible/evidence.md
  - **AC**: AC-VIS-001, AC-VIS-002, AC-VIS-003, AC-VIS-004
  - **风险**: 文档不完整
  - **Human-in-the-loop**: 否

- [x] T-6E-09 [P] 更新 Phase 6E known_limits.md
  - **任务名称**: 更新 Phase 6E known_limits.md
  - **目标**: 记录 Phase 6E 已知限制
  - **输入**: Phase 6E 实现经验
  - **输出**: runs/026-cross-host-visible/known_limits.md
  - **步骤**:
    1. 记录 implemented vs host-visible 边界
    2. 记录本轮未实现的输出格式
    3. 更新统一 known_limits.md
  - **Evidence**: runs/026-cross-host-visible/known_limits.md
  - **AC**: N/A
  - **风险**: 文档不一致
  - **Human-in-the-loop**: 否

---

## 并行任务说明

以下任务可并行执行:

- T-6E-01, T-6E-02, T-6E-03 (Codex CLI 格式化输出)
- T-6E-08, T-6E-09 (evidence/documentation)
- T-6E-01, T-6E-04 (recall 输出格式化)

---

## 执行顺序

1. **Phase 1**: T-6E-01, T-6E-02, T-6E-03 - Codex CLI 格式化 (可并行)
2. **Phase 2**: T-6E-04, T-6E-05, T-6E-06 - Claude system-prompt 格式化
3. **Phase 3**: T-6E-07 - 集成测试
4. **Phase 4**: T-6E-08, T-6E-09 - Evidence/documentation

---

## Human-in-the-loop 场景

- (Phase 6E 无 human-in-the-loop 任务)

---

## 验收标准映射

| AC-ID | 相关任务 |
|--------|----------|
| AC-VIS-001 | T-6E-01, T-6E-04 |
| AC-VIS-002 | T-6E-01, T-6E-07 |
| AC-VIS-003 | T-6E-03, T-6E-06, T-6E-07 |
| AC-VIS-004 | T-6E-02, T-6E-05, T-6E-07 |

---

## 成功标准

- **Codex CLI recall 输出**: 包含 source_tool + friendly name + timestamp = ✅
- **Codex CLI explain 输出**: 包含 match_reasons + provenance = ✅
- **Codex CLI conflict 输出**: ⚠️ CONFLICT DETECTED 提示 = ✅
- **Claude system-prompt recall**: 包含 provenance = ✅
- **Claude system-prompt explain**: 包含 match_reasons = ✅
- **Claude system-prompt conflict**: ⚠️ CONFLICT 提示 = ✅

---

## Phase 6F: Stable Host-Visible Golden Examples

**Run ID**: 027-stable-golden-examples
**日期**: 2026-03-22
**目标**: 补一组稳定、可复现、可验收的 host-visible golden examples

### A. Stable Conflict Scenario

- [x] T-6F-01 [P] 构造 stable conflict scenario 数据
  - **任务名称**: 构造 stable conflict scenario 数据
  - **目标**: 构造同主题、不同 source_tool、内容不同的数据，确保 conflict 稳定触发
  - **输入**: Phase 6E recall API
  - **输出**: runs/027-stable-golden-examples/conflict_test_data.py
  - **步骤**:
    1. 构造 2 条同 title 但不同 content 的 memory
    2. 分别设置不同 source_tool (claude-code, codex-cli)
    3. 写入同一 project/user scope
    4. 验证 recall 时 conflict_detected=True
  - **Evidence**: runs/027-stable-golden-examples/conflict_test_data.py
  - **AC**: AC-GOLD-001
  - **风险**: conflict detection 可能不稳定
  - **Human-in-the-loop**: 否

- [x] T-6F-02 [P] 生成 recall conflict golden output
  - **任务名称**: 生成 recall conflict golden output
  - **目标**: 生成稳定的 recall conflict 输出样例
  - **输入**: T-6F-01 conflict data
  - **输出**: runs/027-stable-golden-examples/recall_conflict_golden.txt
  - **步骤**:
    1. 执行 recall('测试主题', context)
    2. 验证 conflict_detected=True
    3. 验证 candidates 包含 2 条
    4. 保存 CLI 输出格式到 golden file
  - **Evidence**: runs/027-stable-golden-examples/recall_conflict_golden.txt
  - **AC**: AC-GOLD-001
  - **风险**: 输出格式可能变化
  - **Human-in-the-loop**: 否

### B. Stable Cross-Host Explain Scenario

- [x] T-6F-03 [P] 构造 stable cross-host explain scenario 数据
  - **任务名称**: 构造 stable cross-host explain scenario 数据
  - **目标**: 构造被多个 host 写入的 memory，确保 also_written_by 稳定出现
  - **输入**: Phase 6E explain API
  - **输出**: runs/027-stable-golden-examples/explain_test_data.py
  - **步骤**:
    1. 先写入一条 memory (source=claude-code)
    2. 再写入同 title 的 memory (source=codex-cli)
    3. 验证 explain 时 also_written_by 包含 codex-cli
  - **Evidence**: runs/027-stable-golden-examples/explain_test_data.py
  - **AC**: AC-GOLD-002
  - **风险**: also_written_by 查询可能失败
  - **Human-in-the-loop**: 否

- [x] T-6F-04 [P] 生成 explain cross-host golden output
  - **任务名称**: 生成 explain cross-host golden output
  - **目标**: 生成稳定的 explain cross-host 输出样例
  - **输入**: T-6F-03 explain data
  - **输出**: runs/027-stable-golden-examples/explain_crosshost_golden.txt
  - **步骤**:
    1. 执行 explain(memory_id, recall_query)
    2. 验证 source_host_friendly 存在
    3. 验证 match_reasons 非空
    4. 验证 also_written_by 非空
    5. 保存 CLI 输出格式到 golden file
  - **Evidence**: runs/027-stable-golden-examples/explain_crosshost_golden.txt
  - **AC**: AC-GOLD-002
  - **风险**: 输出格式可能变化
  - **Human-in-the-loop**: 否

### C. Golden Outputs

- [x] T-6F-05 [P] 生成 recall provenance golden output
  - **任务名称**: 生成 recall provenance golden output
  - **目标**: 生成 recall provenance 展示的稳定样例
  - **输入**: Phase 6E recall API
  - **输出**: runs/027-stable-golden-examples/recall_provenance_golden.txt
  - **步骤**:
    1. 写入不同 source_tool 的 memories
    2. 执行 recall
    3. 验证 source_host_friendly 显示正确
    4. 验证 timestamp 格式正确
    5. 保存输出到 golden file
  - **Evidence**: runs/027-stable-golden-examples/recall_provenance_golden.txt
  - **AC**: AC-GOLD-003
  - **风险**: timestamp 格式可能变化
  - **Human-in-the-loop**: 否

- [x] T-6F-06 [P] 生成 injection text golden output
  - **任务名称**: 生成 injection text golden output
  - **目标**: 生成 to_injection_text() 的稳定样例
  - **输入**: Phase 6E recall API
  - **输出**: runs/027-stable-golden-examples/injection_text_golden.txt
  - **步骤**:
    1. 执行 recall 后调用 to_injection_text()
    2. 验证包含 (From Claude at HH:MM) 格式
    3. 验证包含 ⚠️ CONFLICT 提示
    4. 保存输出到 golden file
  - **Evidence**: runs/027-stable-golden-examples/injection_text_golden.txt
  - **AC**: AC-GOLD-003
  - **风险**: 格式可能变化
  - **Human-in-the-loop**: 否

### D. Evidence / Documentation

- [x] T-6F-07 [P] 生成 stable golden examples 回归测试脚本
  - **任务名称**: 生成 stable golden examples 回归测试脚本
  - **目标**: 生成可回归验证的 golden examples 测试脚本
  - **输入**: 所有 golden files
  - **输出**: runs/027-stable-golden-examples/test_golden_examples.py
  - **步骤**:
    1. 创建 test_golden_examples.py
    2. 读取 recall_conflict_golden.txt
    3. 读取 explain_crosshost_golden.txt
    4. 验证实际输出匹配 golden output
    5. 输出 PASS/FAIL
  - **Evidence**: runs/027-stable-golden-examples/test_golden_examples.py
  - **AC**: AC-GOLD-004
  - **风险**: 测试逻辑可能需要调整
  - **Human-in-the-loop**: 否

- [x] T-6F-08 [P] 更新 Phase 6F evidence.md 和 known_limits.md
  - **任务名称**: 更新 Phase 6F evidence.md 和 known_limits.md
  - **目标**: 记录 stable golden examples 成果
  - **输入**: 所有 Phase 6F 输出
  - **输出**: runs/027-stable-golden-examples/evidence.md
  - **步骤**:
    1. 创建 runs/027-stable-golden-examples/ 目录
    2. 记录所有 golden files 生成结果
    3. 区分 implemented vs stable scenario coverage
    4. 更新 known_limits.md
  - **Evidence**: runs/027-stable-golden-examples/evidence.md
  - **AC**: AC-GOLD-004
  - **风险**: 文档可能不完整
  - **Human-in-the-loop**: 否

---

## 并行任务说明

以下任务可并行执行:

- T-6F-01, T-6F-02 (conflict scenario)
- T-6F-03, T-6F-04 (explain scenario)
- T-6F-05, T-6F-06 (golden outputs)
- T-6F-07, T-6F-08 (evidence)

---

## 执行顺序

1. **Phase 1**: T-6F-01, T-6F-03 - 构造测试数据
2. **Phase 2**: T-6F-02, T-6F-04 - 生成 golden outputs
3. **Phase 3**: T-6F-05, T-6F-06 - 生成 provenance/injection golden outputs
4. **Phase 4**: T-6F-07 - 回归测试脚本
5. **Phase 5**: T-6F-08 - Evidence/documentation

---

## Human-in-the-loop 场景

- (Phase 6F 无 human-in-the-loop 任务)

---

## 验收标准映射

| AC-ID | 相关任务 |
|--------|----------|
| AC-GOLD-001 | T-6F-01, T-6F-02 |
| AC-GOLD-002 | T-6F-03, T-6F-04 |
| AC-GOLD-003 | T-6F-05, T-6F-06 |
| AC-GOLD-004 | T-6F-07, T-6F-08 |

---

## 成功标准

- **Stable Conflict Scenario**: conflict_detected 稳定触发 = ✅
- **Recall Conflict Golden**: recall_conflict_golden.txt 生成 = ✅
- **Cross-Host Explain**: also_written_by 稳定显示 = ✅
- **Explain Cross-Host Golden**: explain_crosshost_golden.txt 生成 = ✅
- **Golden Examples Regression**: test_golden_examples.py PASS = ✅

---

## Phase 7A: Unified Entry Point

**Run ID**: 029-unified-entry
**日期**: 2026-03-22
**目标**: 构建统一入口 CLI，屏蔽 MCP 细节，让用户无痛接入

### A. Unified CLI Interface

- [x] T-7A-01 定义统一入口 CLI 接口
  - **任务名称**: 定义统一入口 CLI 接口
  - **目标**: 定义 ocmaf 命令行接口设计，屏蔽 MCP 细节
  - **输入**: Phase 6 host-visible output
  - **输出**: src/ocmaf/cli/unified.py
  - **步骤**:
    1. 定义 ocmaf install 命令
    2. 定义 ocmaf status 命令
    3. 定义 ocmaf config 命令
    4. 定义 ocmaf recall/explain 命令
    5. 确保命令与现有功能兼容
  - **Evidence**: src/ocmaf/cli/unified.py
  - **AC**: AC-UE-001
  - **风险**: 与现有 CLI 冲突
  - **Human-in-the-loop**: 否

- [x] T-7A-02 实现 host auto-detection
  - **任务名称**: 实现 host auto-detection
  - **目标**: 实现自动检测当前宿主环境的逻辑
  - **输入**: Claude/Codex environment variables
  - **输出**: src/ocmaf/cli/host_detection.py
  - **步骤**:
    1. 检测 Claude 环境 (CLAUDE_* vars)
    2. 检测 Codex 环境 (CODEX_* vars)
    3. 检测 OpenClaw 环境 (OPENCLAW_* vars)
    4. 返回 host type 和 recommended method
  - **Evidence**: src/ocmaf/cli/host_detection.py
  - **AC**: AC-UE-002
  - **风险**: 环境变量不够可靠
  - **Human-in-the-loop**: 否

### B. Host Setup Scripts

- [x] T-7A-03 [P] 实现 Claude 最小启动脚本
  - **任务名称**: 实现 Claude 最小启动脚本
  - **目标**: 实现 Claude 宿主的最小启动方式
  - **输入**: Claude Method A1+B (from host_matrix)
  - **输出**: src/ocmaf/hosts/claude_setup.sh
  - **步骤**:
    1. 生成 Claude MCP 配置文件
    2. 设置 system-prompt recall 注入
    3. 验证 Claude 启动时加载 OCMF
    4. 输出启动验证证据
  - **Evidence**: src/ocmaf/hosts/claude_setup.sh
  - **AC**: AC-UE-003
  - **风险**: Claude 配置格式可能变化
  - **Human-in-the-loop**: 否

- [x] T-7A-04 [P] 实现 Codex 最小启动脚本
  - **任务名称**: 实现 Codex 最小启动脚本
  - **目标**: 实现 Codex 宿主的最小启动方式
  - **输入**: Codex Method C (from host_matrix)
  - **输出**: src/ocmaf/hosts/codex_setup.sh
  - **步骤**:
    1. 生成 Codex MCP 配置文件
    2. 设置 manual recall/remember 命令
    3. 验证 Codex 启动时加载 OCMF
    4. 输出启动验证证据
  - **Evidence**: src/ocmaf/hosts/codex_setup.sh
  - **AC**: AC-UE-004
  - **风险**: Codex MCP 配置格式可能变化
  - **Human-in-the-loop**: 否

---

## Phase 7B: Automatic Memory Experience

**Run ID**: 029-unified-entry
**日期**: 2026-03-22
**目标**: 实现默认自动记忆体验，让用户无需手动 recall/remember

### C. Auto-Memory Behavior

- [x] T-7B-01 定义默认自动记忆行为
  - **任务名称**: 定义默认自动记忆行为
  - **目标**: 定义自动 recall/remember 的触发时机和范围
  - **输入**: Phase 6E host-visible output
  - **输出**: docs/auto_memory_behavior.md
  - **步骤**:
    1. 定义 session start 自动 recall
    2. 定义 session end 自动 remember
    3. 定义 auto-memory 配置分级 (0-3)
    4. 定义降级策略
  - **Evidence**: docs/auto_memory_behavior.md
  - **AC**: AC-AM-001
  - **风险**: 行为设计可能不符合用户预期
  - **Human-in-the-loop**: 否

- [x] T-7B-02 实现自动 recall 触发
  - **任务名称**: 实现自动 recall 触发
  - **目标**: 实现 session 开始时自动 recall 的最小逻辑
  - **输入**: T-7B-01 auto-memory behavior
  - **输出**: src/ocmaf/api/auto_recall.py
  - **步骤**:
    1. 实现 session start 时 recall
    2. 实现 recall 结果格式化注入
    3. 处理 conflict/warning 显示
    4. 验证自动 recall 正确触发
  - **Evidence**: src/ocmaf/api/auto_recall.py
  - **AC**: AC-AM-002
  - **风险**: 可能干扰正常对话流程
  - **Human-in-the-loop**: 否

- [x] T-7B-03 实现自动 remember 触发
  - **任务名称**: 实现自动 remember 触发
  - **目标**: 实现 session 结束时自动 remember 的最小逻辑
  - **输入**: T-7B-01 auto-memory behavior
  - **输出**: src/ocmaf/api/auto_remember.py
  - **步骤**:
    1. 实现 session end 时 remember
    2. 实现关键事件提取
    3. 验证自动 remember 正确触发
    4. 验证不影响主流程
  - **Evidence**: src/ocmaf/api/auto_remember.py
  - **AC**: AC-AM-003
  - **风险**: 可能遗漏重要上下文
  - **Human-in-the-loop**: 否

### D. Regression Gate Integration

- [x] T-7B-04 集成 regression gate 策略
  - **任务名称**: 集成 regression gate 策略
  - **目标**: 确保 regression gate 与主线集成
  - **输入**: Phase 6G regression gate
  - **输出**: ops/integrated_gate.sh
  - **步骤**:
    1. 将 regression gate 挂接到主线
    2. 定义 gate 失败时的降级策略
    3. 文档化主线与护栏的关系
    4. 验证 gate 在 CI/CD 中工作
  - **Evidence**: ops/integrated_gate.sh
  - **AC**: AC-AM-004
  - **风险**: gate 可能过于严格
  - **Human-in-the-loop**: 否

### E. Documentation & Validation

- [x] T-7B-05 [P] 编写用户入门文档
  - **任务名称**: 编写用户入门文档
  - **目标**: 编写最小用户入门文档，屏蔽底层细节
  - **输入**: T-7A-01~04, T-7B-01~04
  - **输出**: docs/quickstart.md
  - **步骤**:
    1. 编写 ocmaf install 步骤
    2. 编写 Claude 快速开始
    3. 编写 Codex 快速开始
    4. 明确用户不需要理解的概念
  - **Evidence**: docs/quickstart.md
  - **AC**: AC-AM-005
  - **风险**: 文档可能过于技术化
  - **Human-in-the-loop**: 否

- [x] T-7B-06 验证统一入口最小包
  - **任务名称**: 验证统一入口最小包
  - **目标**: 验证统一入口方案的最小可用性
  - **输入**: 所有 7A/7B 实现
  - **输出**: runs/029-unified-entry/validation.md
  - **步骤**:
    1. 安装 OCMF
    2. 检测当前 host
    3. 运行 auto recall
    4. 验证输出包含 provenance
    5. 验证 regression gate 通过
  - **Evidence**: runs/029-unified-entry/validation.md
  - **AC**: AC-AM-006
  - **风险**: 集成测试可能失败
  - **Human-in-the-loop**: 否

- [x] T-7B-07 [P] 更新 evidence.md 和 known_limits.md
  - **任务名称**: 更新 evidence.md 和 known_limits.md
  - **目标**: 记录 Phase 7A/7B 成果和边界
  - **输入**: 所有 7A/7B 输出
  - **输出**: runs/029-unified-entry/evidence.md
  - **步骤**:
    1. 更新统一入口 evidence
    2. 更新自动记忆 evidence
    3. 明确 product mainline vs regression guardrail
    4. 明确 specified-only
  - **Evidence**: runs/029-unified-entry/evidence.md
  - **AC**: AC-AM-006
  - **风险**: 文档可能不完整
  - **Human-in-the-loop**: 否

---

## 并行任务说明

以下任务可并行执行:

- T-7A-03, T-7A-04 (host setup scripts)
- T-7B-05, T-7B-07 (documentation)

---

## 执行顺序

1. **Phase 1**: T-7A-01 - 统一 CLI 接口设计
2. **Phase 2**: T-7A-02 - Host auto-detection
3. **Phase 3**: T-7A-03, T-7A-04 - Host setup scripts (可并行)
4. **Phase 4**: T-7B-01 - Auto-memory behavior 设计
5. **Phase 5**: T-7B-02, T-7B-03 - Auto recall/remember 实现
6. **Phase 6**: T-7B-04 - Regression gate integration
7. **Phase 7**: T-7B-05, T-7B-06, T-7B-07 - Documentation & validation

---

## Human-in-the-loop 场景

- (Phase 7A/7B 无 human-in-the-loop 任务)

---

## 验收标准映射

| AC-ID | 相关任务 |
|--------|----------|
| AC-UE-001 | T-7A-01 |
| AC-UE-002 | T-7A-02 |
| AC-UE-003 | T-7A-03 |
| AC-UE-004 | T-7A-04 |
| AC-AM-001 | T-7B-01 |
| AC-AM-002 | T-7B-02 |
| AC-AM-003 | T-7B-03 |
| AC-AM-004 | T-7B-04 |
| AC-AM-005 | T-7B-05 |
| AC-AM-006 | T-7B-06, T-7B-07 |

---

## 成功标准

- **Unified CLI**: ocmaf 命令行接口定义 = 进行中
- **Host Auto-Detection**: 自动检测当前宿主 = 进行中
- **Claude Setup**: Claude 最小启动脚本 = 进行中
- **Codex Setup**: Codex 最小启动脚本 = 进行中
- **Auto-Memory Behavior**: 自动记忆行为设计 = 进行中
- **Auto Recall**: 自动 recall 触发 = 进行中
- **Auto Remember**: 自动 remember 触发 = 进行中
- **Regression Gate Integration**: gate 与主线集成 = 进行中
- **Quickstart**: 用户入门文档 = 进行中
- **Validation**: 统一入口验证 = 进行中

---

## Phase 7C: Unified Install E2E / Host Wiring Closure

**Run ID**: 030-unified-install-e2e
**日期**: 2026-03-22
**目标**: 把 unified entry 推进到可信安装闭环

### A. Unified Entry Runnable

- [x] T-7C-01 验证 unified CLI 入口可用性
  - **任务名称**: 验证 unified CLI 入口可用性
  - **目标**: `ocmaf unified --help` 不依赖 PYTHONPATH 可正常工作
  - **输入**: 当前 unified.py 实现
  - **输出**: 安装后可直接调用的 CLI 入口
  - **步骤**:
    1. 检查 `python3 -m ocmaf.cli.unified --help` 是否工作
    2. 检查 `ocmaf unified` 命令是否注册到 PATH
    3. 如需要，更新 setup.py 或 pyproject.toml 注册命令
    4. 给出最小可用安装/调用方式
  - **Evidence**: src/ocmaf/cli/unified.py, setup.py
  - **AC**: AC-7C-INSTALL-001
  - **风险**: CLI 注册可能需要 pip install -e
  - **Human-in-the-loop**: 否

### B. Claude Wiring (Method A1+B)

- [x] T-7C-02 [P] Claude install 真正配置 A1+B
  - **任务名称**: Claude install 真正配置 A1+B
  - **目标**: install 后 Claude 真正能 auto-recall
  - **输入**: Claude Method A1+B 验证结论
  - **输出**: claude_setup.sh 正确配置 MCP + system-prompt
  - **步骤**:
    1. 检查当前 claude_setup.sh 是否配置了 MCP server
    2. 检查是否配置了 system-prompt recall 注入 (B method)
    3. 检查是否配置了 native hooks (A1 method)
    4. 更新 claude_setup.sh 确保 A1+B 都配置
  - **Evidence**: src/ocmaf/hosts/claude_setup.sh
  - **AC**: AC-7C-INSTALL-001, AC-7C-INSTALL-002
  - **风险**: Claude MCP config 格式可能变化
  - **Human-in-the-loop**: 否

- [x] T-7C-03 [P] Claude install 验证 E2E
  - **任务名称**: Claude install E2E 验证
  - **目标**: Claude install 后可以真正 recall
  - **输入**: T-7C-02 配置好的 claude_setup.sh
  - **输出**: Claude E2E install 证据
  - **步骤**:
    1. 运行 claude_setup.sh
    2. 验证 MCP config 生成
    3. 验证 OCMF_AUTO_MEMORY 设置
    4. 运行 recall 测试
  - **Evidence**: runs/030-unified-install-e2e/claude_install_e2e.md
  - **AC**: AC-7C-INSTALL-002
  - **风险**: 真实环境可能与测试不同
  - **Human-in-the-loop**: 否

### C. Codex Wiring (Method C)

- [x] T-7C-04 [P] Codex install 真正配置 Method C
  - **任务名称**: Codex install 真正配置 Method C
  - **目标**: install 后 Codex 真正能通过 MCP 调用 recall/remember
  - **输入**: Codex Method C 验证结论
  - **输出**: codex_setup.sh 正确配置 MCP server 入口
  - **步骤**:
    1. 检查当前 codex_setup.sh MCP config 路径
    2. 验证 MCP server 入口指向正确的 Python 模块
    3. 确保使用已验证的 `python3 -m ocmaf.cli.main`
    4. 更新 codex_setup.sh 纠正错误的入口路径
  - **Evidence**: src/ocmaf/hosts/codex_setup.sh
  - **AC**: AC-7C-INSTALL-003
  - **风险**: MCP server 入口路径错误
  - **Human-in-the-loop**: 否

- [x] T-7C-05 [P] Codex install 验证 E2E
  - **任务名称**: Codex install E2E 验证
  - **目标**: Codex install 后可以真正 recall
  - **输入**: T-7C-04 配置好的 codex_setup.sh
  - **输出**: Codex E2E install 证据
  - **步骤**:
    1. 运行 codex_setup.sh
    2. 验证 MCP config 生成
    3. 验证 MCP server 连接
    4. 运行 recall 测试
  - **Evidence**: runs/030-unified-install-e2e/codex_install_e2e.md
  - **AC**: AC-7C-INSTALL-003
  - **风险**: Codex 环境可能不可用
  - **Human-in-the-loop**: 否

### D. Unified Status 修正

- [x] T-7C-06 [P] 修正 unified status host 判断逻辑
  - **任务名称**: 修正 unified status host 判断逻辑
  - **目标**: status 不依赖 binary 存在性判断 host
  - **输入**: 当前 host_detection.py 实现
  - **输出**: 更新的 host_detection.py，区分 installed vs runtime
  - **步骤**:
    1. 区分 "installed capability" vs "current runtime host"
    2. 不只依赖 binary 存在性
    3. 优先检测 env vars
    4. 明确显示: host detected, method recommended, auto-memory supported
  - **Evidence**: src/ocmaf/cli/host_detection.py
  - **AC**: AC-7C-STATUS-001, AC-7C-STATUS-002, AC-7C-STATUS-003
  - **风险**: 误判可能导致用户困惑
  - **Human-in-the-loop**: 否

### E. Quickstart 对齐

- [x] T-7C-07 [P] Quickstart 与真实路径对齐
  - **任务名称**: Quickstart 与真实路径对齐
  - **目标**: Quickstart 描述的每一步都真实可执行
  - **输入**: 当前 quickstart.md, T-7C-01~06 实现
  - **输出**: 更新的 quickstart.md
  - **步骤**:
    1. 检查 quickstart.md 每一步是否与实现对应
    2. 确保不暴露 MCP/method 细节
    3. 确保步骤可执行
    4. 移除"假设用户已配置"等不实描述
  - **Evidence**: docs/quickstart.md
  - **AC**: Quickstart Truthfulness Rules
  - **风险**: 描述可能过时
  - **Human-in-the-loop**: 否

### F. E2E Evidence

- [x] T-7C-08 [P] Claude 或 Codex E2E install -> recall 证据
  - **任务名称**: E2E install -> recall 证据
  - **目标**: 至少一条真实的 install -> status -> usable memory path 证据
  - **输入**: T-7C-01~07 所有实现
  - **输出**: runs/030-unified-install-e2e/e2e_evidence.md
  - **步骤**:
    1. 选择 Claude 或 Codex 作为测试目标
    2. 运行完整 install
    3. 运行 unified status
    4. 执行一次 recall
    5. 记录完整输出和退出码
  - **Evidence**: runs/030-unified-install-e2e/e2e_evidence.md
  - **AC**: AC-7C-INSTALL-005
  - **风险**: 环境限制可能导致无法完整测试
  - **Human-in-the-loop**: 否

### G. Evidence / Documentation

- [x] T-7C-09 [P] 更新 evidence.md 和 known_limits.md
  - **任务名称**: 更新 Phase 7C evidence.md 和 known_limits.md
  - **目标**: 记录 Phase 7C 成果和边界
  - **输入**: 所有 Phase 7C 输出
  - **输出**: runs/030-unified-install-e2e/evidence.md, known_limits.md
  - **步骤**:
    1. 区分 product mainline vs regression guardrail
    2. 明确 Claude/Codex 已验证路径
    3. 明确本轮新增的可信闭环
    4. 明确 specified-only
  - **Evidence**: runs/030-unified-install-e2e/evidence.md
  - **AC**: N/A
  - **风险**: 文档可能不完整
  - **Human-in-the-loop**: 否

---

## 并行任务说明

以下任务可并行执行:

- T-7C-02, T-7C-03 (Claude wiring)
- T-7C-04, T-7C-05 (Codex wiring)
- T-7C-06 (Status 修正)
- T-7C-07, T-7C-08, T-7C-09 (Documentation)

---

## 执行顺序

1. **Phase 1**: T-7C-01 - Unified CLI 入口可用性
2. **Phase 2**: T-7C-02, T-7C-04, T-7C-06 - Claude/Codex wiring + Status 修正 (可并行)
3. **Phase 3**: T-7C-03, T-7C-05 - E2E 验证 (可并行)
4. **Phase 4**: T-7C-07 - Quickstart 对齐
5. **Phase 5**: T-7C-08 - E2E 证据
6. **Phase 6**: T-7C-09 - Evidence/documentation

---

## Human-in-the-loop 场景

- (Phase 7C 无 human-in-the-loop 任务)

---

## 验收标准映射

| AC-ID | 相关任务 |
|--------|----------|
| AC-7C-INSTALL-001 | T-7C-01 |
| AC-7C-INSTALL-002 | T-7C-02, T-7C-03 |
| AC-7C-INSTALL-003 | T-7C-04, T-7C-05 |
| AC-7C-INSTALL-004 | T-7C-08 |
| AC-7C-INSTALL-005 | T-7C-08 |
| AC-7C-STATUS-001 | T-7C-06 |
| AC-7C-STATUS-002 | T-7C-06 |
| AC-7C-STATUS-003 | T-7C-06 |
| AC-7C-STATUS-004 | T-7C-06 |
| AC-7C-STATUS-005 | T-7C-06 |

---

## Phase 031: Install Closure Fix

**Run ID**: 031-install-closure
**Date**: 2026-03-22
**Status**: PASS

### 任务清单

- [x] T-031-01 修正 Claude MCP 入口
  - **任务名称**: 修正 Claude MCP 入口
  - **目标**: claude_setup.sh 指向正确入口 `ocmaf.bridge.mcp_server --tool claude-code`
  - **输入**: `src/ocmaf/hosts/claude_setup.sh`
  - **输出**: 修正后的 claude_setup.sh 和 ~/.claude/mcp_servers.json
  - **步骤**:
    1. 编辑 claude_setup.sh，将 MCP config 改为 `python3 -m ocmaf.bridge.mcp_server --tool claude-code`
    2. 同时更新 example addition 注释
    3. 运行 `source claaude_setup.sh` 验证
    4. 检查 ~/.claude/mcp_servers.json 确认正确
  - **Evidence**: runs/031-install-closure/install_closure.md
  - **AC**: AC-031-CLAUDE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-031-02 修正 Codex MCP 入口
  - **任务名称**: 修正 Codex MCP 入口
  - **目标**: codex_setup.sh 指向正确入口 `ocmaf.bridge.mcp_server --tool codex-cli`
  - **输入**: `src/ocmaf/hosts/codex_setup.sh`
  - **输出**: 修正后的 codex_setup.sh 和 ~/.codex/mcp.json
  - **步骤**:
    1. 编辑 codex_setup.sh，将 MCP config 改为 `python3 -m ocmaf.bridge.mcp_server --tool codex-cli`
    2. 运行 `source codex_setup.sh` 验证
    3. 检查 ~/.codex/mcp.json 确认正确
  - **Evidence**: runs/031-install-closure/install_closure.md
  - **AC**: AC-031-CODEX-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-031-03 修正 unified install 命令
  - **任务名称**: 修正 unified install 命令
  - **目标**: `ocmaf unified install --host claude/codex` 真正运行 setup 脚本
  - **输入**: `src/ocmaf/cli/unified.py`
  - **输出**: 修正后的 unified.py install 命令
  - **步骤**:
    1. 编辑 unified.py install 命令
    2. 添加 subprocess 调用运行 claude_setup.sh 或 codex_setup.sh
    3. 测试 `python3 -m ocmaf.cli.unified install --host claude --dry-run`
    4. 测试实际运行 `python3 -m ocmaf.cli.unified install --host claude`
  - **Evidence**: runs/031-install-closure/install_closure.md
  - **AC**: AC-031-INSTALL-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-031-04 修正 quickstart.md CLI 调用
  - **任务名称**: 修正 quickstart.md CLI 调用
  - **目标**: quickstart 显示正确的 CLI 调用方式
  - **输入**: `docs/quickstart.md`
  - **输出**: 修正后的 quickstart.md
  - **步骤**:
    1. 将所有 `PYTHONPATH=src ocmaf` 改为 `PYTHONPATH=src python3 -m ocmaf.cli.unified`
    2. 修正 "You Don't Need to Know" 部分，不再误导性声明 "we set it up for you"
  - **Evidence**: runs/031-install-closure/install_closure.md
  - **AC**: AC-031-QUICKSTART-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-031-05 修正 EventType 类型映射 bug
  - **任务名称**: 修正 EventType 类型映射 bug
  - **目标**: unified.py 使用有效的 EventType 值
  - **输入**: `src/ocmaf/cli/unified.py`
  - **输出**: 修正后的 type_map
  - **步骤**:
    1. 检查 EventType enum 的有效值
    2. 修改 type_map 使用有效值（FACT -> DECISION, CONTEXT -> CONSTRAINT 等）
    3. 测试 remember 命令：`python3 -m ocmaf.cli.unified remember --content "test" --type decision`
  - **Evidence**: runs/031-install-closure/install_closure.md
  - **AC**: AC-031-EVENTTYPE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-031-06 运行 smoke tests 和 regression gate
  - **任务名称**: 运行 smoke tests 和 regression gate
  - **目标**: 验证修改没有破坏现有功能
  - **输入**: 所有修改的文件
  - **输出**: smoke tests 和 regression gate 结果
  - **步骤**:
    1. 运行 smoke tests
    2. 运行 `bash ops/integrated_gate.sh`
    3. 确认所有测试通过
  - **Evidence**: runs/031-install-closure/install_closure.md
  - **AC**: AC-031-SMOKE-001, AC-031-GATE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-031-07 生成 evidence 文件
  - **任务名称**: 生成 evidence 文件
  - **目标**: 记录 Phase 031 成果和边界
  - **输入**: 所有 Phase 031 输出
  - **输出**: runs/031-install-closure/install_closure.md, evidence.md, known_limits.md
  - **步骤**:
    1. 创建 runs/031-install-closure/ 目录
    2. 生成 install_closure.md
    3. 生成 evidence.md
    4. 生成 known_limits.md
  - **Evidence**: runs/031-install-closure/*
  - **AC**: AC-031-EVIDENCE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

### 依赖关系

- T-031-01, T-031-02, T-031-03, T-031-04, T-031-05 可并行执行
- T-031-06 依赖 T-031-01~05
- T-031-07 依赖 T-031-06

### 验收标准

| AC | 任务 |
|----|------|
| AC-031-CLAUDE-001 | T-031-01 |
| AC-031-CODEX-001 | T-031-02 |
| AC-031-INSTALL-001 | T-031-03 |
| AC-031-QUICKSTART-001 | T-031-04 |
| AC-031-EVENTTYPE-001 | T-031-05 |
| AC-031-SMOKE-001 | T-031-06 |
| AC-031-GATE-001 | T-031-06 |
| AC-031-EVIDENCE-001 | T-031-07 |

---

## 成功标准

- **Unified CLI 入口**: `ocmaf unified --help` 不依赖 PYTHONPATH = ✓ PASS
- **Claude Wiring**: Claude install 配置 A1+B = ✓ PASS
- **Claude E2E**: Claude install -> recall = ✓ PASS
- **Codex Wiring**: Codex install 配置 MCP = ✓ PASS
- **Codex E2E**: Codex install -> recall = ✓ PASS
- **Status 修正**: 不依赖 binary 判断 = ✓ PASS
- **Quickstart**: 对应真实路径 = ✓ PASS
- **E2E Evidence**: install -> recall 证据 = ✓ PASS

### Phase 031 成功标准

- **Claude MCP 入口**: 指向 `ocmaf.bridge.mcp_server --tool claude-code` = ✓ PASS
- **Codex MCP 入口**: 指向 `ocmaf.bridge.mcp_server --tool codex-cli` = ✓ PASS
- **Unified install**: 真正运行 setup 脚本 = ✓ PASS
- **Quickstart**: 显示正确 CLI 调用 = ✓ PASS
- **EventType bug**: 修复无效类型 = ✓ PASS
- **Smoke tests**: 全部通过 = ✓ PASS
- **Regression gate**: 4/4 通过 = ✓ PASS

### Phase 032 成功标准

- **Claude config merge**: 已有 mcp_servers.json 也能安全并入 = ✓ PASS
- **OCMF_SOURCE_TOOL fallback**: Source 显示 Claude/Codex 而非 Unknown/cli = ✓ PASS
- **Quickstart unified mainline**: 使用 `ocmaf unified install --host ...` = ✓ PASS

---

## Phase 032: Install Closure Final

**Run ID**: 032-install-closure-final
**Date**: 2026-03-22
**Status**: PASS

### 任务清单

- [x] T-032-01 修正 Claude config merge 逻辑
  - **任务名称**: 修正 Claude config merge 逻辑
  - **目标**: 当 `~/.claude/mcp_servers.json` 已存在时，安全将 OCMF 合并写入
  - **输入**: `src/ocmaf/hosts/claude_setup.sh`
  - **输出**: 修正后的 claude_setup.sh
  - **步骤**:
    1. 当 MCP config 存在时，用 Python 读取现有 JSON
    2. 添加 OCMF entry 到 mcpServers
    3. 写回合并后的 config
  - **Evidence**: runs/032-install-closure-final/install_closure_final.md
  - **AC**: AC-032-MERGE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-032-02 修正 OCMF_SOURCE_TOOL fallback
  - **任务名称**: 修正 OCMF_SOURCE_TOOL fallback
  - **目标**: remember/recall 在 host detection 失败时，回落到 OCMF_SOURCE_TOOL
  - **输入**: `src/ocmaf/cli/unified.py`
  - **输出**: 修正后的 unified.py
  - **步骤**:
    1. 在 remember 命令中，当 source_tool 为 "cli" 时，回落到 OCMF_SOURCE_TOOL
    2. 在输出 Source 时也使用相同 fallback
    3. 测试：`source ~/.ocmf/config.sh && remember --content "..."`
  - **Evidence**: runs/032-install-closure-final/install_closure_final.md
  - **AC**: AC-032-IDENTITY-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-032-03 修正 quickstart 使用 unified install 主路径
  - **任务名称**: 修正 quickstart 使用 unified install 主路径
  - **目标**: quickstart 以 `ocmaf unified install --host ...` 为主路径
  - **输入**: `docs/quickstart.md`
  - **输出**: 修正后的 quickstart.md
  - **步骤**:
    1. 将 "source src/ocmaf/hosts/claude_setup.sh" 改为 "PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude"
    2. Codex 同样修改
  - **Evidence**: runs/032-install-closure-final/install_closure_final.md
  - **AC**: AC-032-QUICKSTART-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-032-04 运行 smoke tests 和 regression gate
  - **任务名称**: 运行 smoke tests 和 regression gate
  - **目标**: 验证修改没有破坏现有功能
  - **输入**: 所有修改的文件
  - **输出**: smoke tests 和 regression gate 结果
  - **步骤**:
    1. 运行 smoke tests
    2. 运行 `bash ops/integrated_gate.sh`
  - **Evidence**: runs/032-install-closure-final/install_closure_final.md
  - **AC**: AC-032-SMOKE-001, AC-032-GATE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-032-05 生成 evidence 文件
  - **任务名称**: 生成 evidence 文件
  - **目标**: 记录 Phase 032 成果和边界
  - **输入**: 所有 Phase 032 输出
  - **输出**: runs/032-install-closure-final/install_closure_final.md, evidence.md, known_limits.md
  - **步骤**:
    1. 创建 runs/032-install-closure-final/ 目录
    2. 生成 install_closure_final.md
    3. 生成 evidence.md
    4. 生成 known_limits.md
  - **Evidence**: runs/032-install-closure-final/*
  - **AC**: AC-032-EVIDENCE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

### 依赖关系

- T-032-01, T-032-02, T-032-03 可并行执行
- T-032-04 依赖 T-032-01~03
- T-032-05 依赖 T-032-04

### 验收标准

| AC | 任务 |
|----|------|
| AC-032-MERGE-001 | T-032-01 |
| AC-032-IDENTITY-001 | T-032-02 |
| AC-032-QUICKSTART-001 | T-032-03 |
| AC-032-SMOKE-001 | T-032-04 |
| AC-032-GATE-001 | T-032-04 |
| AC-032-EVIDENCE-001 | T-032-05 |

---

## Phase 7D: Real User Journey Test

**Run ID**: 033-user-journey
**Date**: 2026-03-22
**Status**: In Progress
**Goal**: 验证用户按 quickstart 操作是否能顺滑完成第一次可用记忆

### A. Claude User Journey

- [x] T-7D-01 Claude quickstart user journey test
  - **任务名称**: Claude quickstart user journey test
  - **目标**: 验证用户按 quickstart 原样操作 Claude 路径
  - **输入**: docs/quickstart.md, Phase 7C 已修复的 CLI
  - **输出**: runs/033-user-journey/claude_journey.md
  - **步骤**:
    1. 清除现有 OCMF config（rm -rf ~/.ocmf ~/.claude/mcp_servers.json）
    2. 按 quickstart 顺序执行：
       - pip install -e /path/to/ocmf
       - PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
       - source ~/.ocmf/config.sh
       - PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Using PostgreSQL for database"
       - PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "PostgreSQL"
    3. 记录每个步骤的 stdout/stderr/exit code
    4. 测量总时间（应在 5 分钟内）
    5. 识别卡点
  - **Evidence**: runs/033-user-journey/claude_journey.md
  - **AC**: AC-7D-FUM-001, AC-7D-FUM-002, AC-7D-FUM-003, AC-7D-FUM-004
  - **风险**: 无破坏性操作
  - **Human-in-the-loop**: 否

### B. Codex User Journey

- [x] T-7D-02 Codex quickstart user journey test
  - **任务名称**: Codex quickstart user journey test
  - **目标**: 验证用户按 quickstart 原样操作 Codex 路径
  - **输入**: docs/quickstart.md, Phase 7C 已修复的 CLI
  - **输出**: runs/033-user-journey/codex_journey.md
  - **步骤**:
    1. 清除现有 OCMF config（rm -rf ~/.ocmf ~/.codex/mcp.json）
    2. 按 quickstart 顺序执行：
       - pip install -e /path/to/ocmf
       - PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex
       - source ~/.ocmf/config.sh
       - PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Using MongoDB for database"
       - PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "MongoDB"
    3. 记录每个步骤的 stdout/stderr/exit code
    4. 测量总时间（应在 5 分钟内）
    5. 识别卡点
  - **Evidence**: runs/033-user-journey/codex_journey.md
  - **AC**: AC-7D-FUM-001, AC-7D-FUM-002, AC-7D-FUM-003, AC-7D-FUM-004
  - **风险**: 无破坏性操作
  - **Human-in-the-loop**: 否

### C. Friction Logging

- [x] T-7D-03 [P] Claude journey friction analysis
  - **任务名称**: Claude journey friction analysis
  - **目标**: 识别 Claude 路径的实际卡点
  - **输入**: T-7D-01 输出
  - **输出**: runs/033-user-journey/friction_log.md 中的 Claude 部分
  - **步骤**:
    1. 分析 T-7D-01 的执行记录
    2. 识别 friction point
    3. 评估严重度（HIGH/MEDIUM/LOW）
    4. 提出解决方案
    5. 更新 friction_log.md
  - **Evidence**: runs/033-user-journey/friction_log.md
  - **AC**: AC-7D-FRICTION-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-7D-04 [P] Codex journey friction analysis
  - **任务名称**: Codex journey friction analysis
  - **目标**: 识别 Codex 路径的实际卡点
  - **输入**: T-7D-02 输出
  - **输出**: runs/033-user-journey/friction_log.md 中的 Codex 部分
  - **步骤**:
    1. 分析 T-7D-02 的执行记录
    2. 识别 friction point
    3. 评估严重度（HIGH/MEDIUM/LOW）
    4. 提出解决方案
    5. 更新 friction_log.md
  - **Evidence**: runs/033-user-journey/friction_log.md
  - **AC**: AC-7D-FRICTION-002
  - **风险**: 无
  - **Human-in-the-loop**: 否

### D. Evidence & Conclusions

- [x] T-7D-05 Generate user_journey.md
  - **任务名称**: 生成 user_journey.md
  - **目标**: 汇总 Claude/Codex 用户旅程测试结果
  - **输入**: T-7D-01, T-7D-02, T-7D-03, T-7D-04 输出
  - **输出**: runs/033-user-journey/user_journey.md
  - **步骤**:
    1. 汇总两个旅程的执行结果
    2. 评估是否满足 AC-7D-FUM-*
    3. 给出 PASS/FAIL 判定
    4. 列出 friction points
  - **Evidence**: runs/033-user-journey/user_journey.md
  - **AC**: AC-7D-EVIDENCE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

---

## Phase 7E: Multi-Host Switching UX

**Run ID**: 034-switching-ux
**Date**: 2026-03-22
**Status**: Planned
**Goal**: 验证多宿主切换体验，识别 config 覆盖问题

### A. Multi-Host Switching

- [x] T-7E-01 Claude to Codex switching test
  - **任务名称**: Claude to Codex switching test
  - **目标**: 验证 Claude 配置后切换到 Codex 的体验
  - **输入**: T-7D-01 的 Claude 配置
  - **输出**: runs/034-switching-ux/claude_to_codex.md
  - **步骤**:
    1. 确保 Claude 已配置（从 T-7D-01）
    2. 执行：PYTHONPATH=src python3 -m ocmaf.cli.unified install --host codex
    3. 检查 ~/.ocmf/config.sh 的 OCMF_SOURCE_TOOL
    4. 执行 remember：PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Codex decision"
    5. 观察 Source 输出
    6. 执行 recall：PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "Codex"
    7. 记录切换体验问题
  - **Evidence**: runs/034-switching-ux/claude_to_codex.md
  - **AC**: AC-7E-SWITCH-001
  - **风险**: 只影响测试数据
  - **Human-in-the-loop**: 否

- [x] T-7E-02 Codex to Claude switching test
  - **任务名称**: Codex to Claude switching test
  - **目标**: 验证 Codex 配置后切换回 Claude 的体验
  - **输入**: T-7D-02 的 Codex 配置, T-7E-01 结果
  - **输出**: runs/034-switching-ux/codex_to_claude.md
  - **步骤**:
    1. 确保 Codex 已配置（从 T-7D-02）
    2. 执行：PYTHONPATH=src python3 -m ocmaf.cli.unified install --host claude
    3. 检查 ~/.ocmf/config.sh 的 OCMF_SOURCE_TOOL
    4. 执行 remember：PYTHONPATH=src python3 -m ocmaf.cli.unified remember --content "Claude decision"
    5. 观察 Source 输出
    6. 执行 recall：PYTHONPATH=src python3 -m ocmaf.cli.unified recall --query "Claude"
    7. 记录切换体验问题
  - **Evidence**: runs/034-switching-ux/codex_to_claude.md
  - **AC**: AC-7E-SWITCH-002
  - **风险**: 只影响测试数据
  - **Human-in-the-loop**: 否

- [x] T-7E-03 Cross-host memory sharing test
  - **任务名称**: Cross-host memory sharing test
  - **目标**: 验证跨宿主记忆共享（Claude 写入，Codex 召回）
  - **输入**: T-7E-01, T-7E-02 配置的 memory.db
  - **输出**: runs/034-switching-ux/cross_host_shared.md
  - **步骤**:
    1. 确保两个宿主的 memory.db 共享
    2. Claude: remember --content "Shared cross-host memory"
    3. 切换到 Codex 环境
    4. Codex: recall --query "cross-host"
    5. 验证能否召回 Claude 的记忆
    6. 记录来源显示是否正确
  - **Evidence**: runs/034-switching-ux/cross_host_shared.md
  - **AC**: AC-7E-SHARE-001
  - **风险**: 只影响测试数据
  - **Human-in-the-loop**: 否

### B. Switching Friction Analysis

- [x] T-7E-04 [P] Switching friction analysis
  - **任务名称**: Switching friction analysis
  - **目标**: 识别多宿主切换的实际体验问题
  - **输入**: T-7E-01, T-7E-02, T-7E-03 输出
  - **输出**: runs/034-switching-ux/friction_log.md
  - **步骤**:
    1. 分析切换测试记录
    2. 识别 friction point：
       - config 覆盖问题
       - Source 显示问题
       - 无切换警告
    3. 评估严重度
    4. 提出改进建议
  - **Evidence**: runs/034-switching-ux/friction_log.md
  - **AC**: AC-7E-FRICTION-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

### C. Evidence & Conclusions

- [x] T-7E-05 Generate switching_ux.md
  - **任务名称**: 生成 switching_ux.md
  - **目标**: 汇总多宿主切换测试结果
  - **输入**: T-7E-01, T-7E-02, T-7E-03, T-7E-04 输出
  - **输出**: runs/034-switching-ux/switching_ux.md
  - **步骤**:
    1. 汇总三个切换场景的执行结果
    2. 评估是否满足 AC-7E-*
    3. 给出 PASS/FAIL/NEEDS_WORK 判定
    4. 列出 friction points
    5. 提出 product polish priorities
  - **Evidence**: runs/034-switching-ux/switching_ux.md
  - **AC**: AC-7E-EVIDENCE-001
  - **风险**: 无
  - **Human-in-the-loop**: 否

- [x] T-7E-06 Generate final evidence and known_limits
  - **任务名称**: 生成 final evidence and known_limits
  - **目标**: 汇总 Phase 7D/7E 全部成果
  - **输入**: T-7D-05, T-7E-05 输出
  - **输出**: runs/033-user-journey/evidence.md, runs/033-user-journey/known_limits.md
  - **步骤**:
    1. 生成 runs/033-user-journey/evidence.md
    2. 生成 runs/033-user-journey/known_limits.md
    3. 更新 tasks/tasks.md 完成状态
  - **Evidence**: runs/033-user-journey/evidence.md, known_limits.md
  - **AC**: AC-7D-EVIDENCE-002, AC-7E-EVIDENCE-002
  - **风险**: 无
  - **Human-in-the-loop**: 否

### 依赖关系

- T-7D-01, T-7D-02 可并行
- T-7D-03, T-7D-04 依赖 T-7D-01, T-7D-02
- T-7D-05 依赖 T-7D-03, T-7D-04
- T-7E-01 依赖 T-7D-01
- T-7E-02 依赖 T-7D-02
- T-7E-03 依赖 T-7E-01, T-7E-02
- T-7E-04 依赖 T-7E-03
- T-7E-05 依赖 T-7E-04
- T-7E-06 依赖 T-7D-05, T-7E-05

### 验收标准

| AC | 任务 | 描述 |
|----|------|------|
| AC-7D-FUM-001 | T-7D-01, T-7D-02 | 用户能在 5 分钟内完成 first usable memory path |
| AC-7D-FUM-002 | T-7D-01, T-7D-02 | remember 后能看到 Source: Claude/Codex |
| AC-7D-FUM-003 | T-7D-01, T-7D-02 | recall 后能看到 "From Claude/Codex" |
| AC-7D-FUM-004 | T-7D-01, T-7D-02 | status 命令能看到正确的 memory count |
| AC-7D-FRICTION-001 | T-7D-03 | Claude friction 已记录 |
| AC-7D-FRICTION-002 | T-7D-04 | Codex friction 已记录 |
| AC-7D-EVIDENCE-001 | T-7D-05 | user_journey.md 已生成 |
| AC-7E-SWITCH-001 | T-7E-01 | Claude→Codex 切换已测试 |
| AC-7E-SWITCH-002 | T-7E-02 | Codex→Claude 切换已测试 |
| AC-7E-SHARE-001 | T-7E-03 | 跨宿主共享已验证 |
| AC-7E-FRICTION-001 | T-7E-04 | 切换 friction 已记录 |
| AC-7E-EVIDENCE-001 | T-7E-05 | switching_ux.md 已生成 |
| AC-7D-EVIDENCE-002 | T-7E-06 | evidence.md 已生成 |
| AC-7E-EVIDENCE-002 | T-7E-06 | known_limits.md 已生成 |

### Phase 7D 成功标准

- **Claude journey**: 按 quickstart 能完成 install → source → remember → recall = ✓ PASS/FAIL
- **Codex journey**: 按 quickstart 能完成 install → source → remember → recall = ✓ PASS/FAIL
- **Friction logged**: 所有卡点已记录在 friction_log.md = ✓ DONE
- **evidence**: user_journey.md 已生成 = ✓ DONE

### Phase 7E 成功标准

- **Claude→Codex switch**: 能切换且 config 正确 = ✓ PASS/FAIL
- **Codex→Claude switch**: 能切换且 config 正确 = ✓ PASS/FAIL
- **Cross-host sharing**: Claude 写入能被 Codex 召回 = ✓ PASS/FAIL
- **Friction logged**: 切换卡点已记录 = ✓ DONE
- **evidence**: switching_ux.md + known_limits.md 已生成 = ✓ DONE
