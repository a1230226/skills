---
name: product-direction-reference-template
description: 产品方向参考库模板。当你需要把单个业务场景沉淀为可长期复用的方向条目时使用。
version: 1.2.0
---

# 产品方向参考库模板

> **版本**: v1.2.0
> 用法：每个业务场景维护 1 个条目；同一业务域下维护多个条目；不要按成熟度拆出多套模板。

---

## 单条条目模板

```markdown
### [场景名称]

- `scene_id`: `SCENE-YYYY-NNN`
- `scene_group`: `education_ai | fintech | healthcare | ...`
- `maturity_level`: `L0_idea | L1_defined | L2_validated | L3_proven`
- `business_scenario`: `场景发生在什么业务链路中，服务谁，何时触发`
- `target_description`: `当前最重要的目标`
- `core_tension`: `为什么这个方向值得做，同时为什么它现在仍危险`
- `core_pain_points`:
  - `痛点1`: `为什么是问题，现有做法哪里不够`
  - `痛点2`: `...`
- `business_chain_steps`:
  - `步骤1`: `完整业务主链中的关键步骤`
  - `当前卡点`: `当前问题位于哪一步`
- `core_chain_breakdown_table`: `如适用，引用或内嵌核心主链拆解表`
- `key_decision_points`:
  - `决策点1`: `当前最值得优先关注的节点或判断点`
- `key_inputs_outputs`:
  - `inputs`: `关键输入`
  - `processing`: `处理中间态 / 判定 / 编排`
  - `outputs`: `输出`
  - `feedback_loop`: `反馈如何反哺`
- `direction_candidates`:
  - `方向A`: `一句话定位 + 优先级理由 + 主要风险`
  - `方向B`: `一句话定位 + 优先级理由 + 主要风险`
- `recommended_priority_direction`: `当前建议优先推进的方向`
- `mvp_scope`:
  - `must_have`: `...`
  - `should_defer`: `...`
  - `not_now`: `...`
- `mvp_cut`: `兼容旧版写法；与 mvp_scope 同义`
- `human_in_loop`:
  - `人工环节1`: `当前可先由人工或半自动流程承担的步骤`
- `capability_layers`:
  - `能力层1`: `如数据接入 / 内容理解 / 策略判断 / 执行辅助 / 反馈学习`
- `priority_capabilities`:
  - `能力A`: `当前最值得先建设的能力 + 支撑价值`
- `evidence_status`:
  - `verified_evidence`: `...`
  - `internal_observations`: `...`
  - `key_assumptions`: `...`
  - `evidence_gaps`: `...`
- `validation_plan`:
  - `key_hypothesis`: `...`
  - `validation_action`: `...`
  - `adoption_signal`: `...`
  - `success_signal`: `...`
  - `failure_signal`: `...`
  - `disconfirming_signal`: `...`
  - `judgment_update_rule`: `...`
  - `next_gate`: `...`
- `validation_signals`: `兼容旧版写法；与 validation_plan 同义`
- `disconfirming_signals`:
  - `反证1`: `...`
- `feedback_signals`:
  - `信号1`: `后续如何回收结果并用于校准`
- `patent_handoff_candidates`:
  - `哪些机制或流程适合继续转译成专利`
- `related_assets`:
  - `相关产品 / 文档 / 专利 / 研究资产`
- `known_unknowns`:
  - `目前还不知道或尚未验证的关键问题`
- `next_action`: `继续补资料 / 做验证 / 进入 PRD / 进入专利 skill`
- `last_updated`: `2026-05-01`
- `update_note`: `首次建档 / 根据验证结果调整 / 与专利条目关联`
```

---

## 回填提醒

- `L0_idea` 重点写：场景、痛点、候选方向、待验证问题。
- `L1_defined` 重点写：输入输出链路、推荐方向、MVP 初切、优先能力。
- `L2_validated` 重点写：验证证据、方向调整理由、下一阶段门槛、哪些能力已被证明有效。
- `L3_proven` 重点写：稳定闭环、复制条件、可转译到专利或平台化资产的部分。

## 版本历史

- **v1.2.0** (2026-05-19) - 补齐与 brief 模板一致的证据与改判字段，并保留旧字段别名兼容回填
- **v1.1.0** (2026-05-06) - 新增 `core_chain_breakdown_table` 字段，支持把核心主链拆解表沉淀进方向库条目
