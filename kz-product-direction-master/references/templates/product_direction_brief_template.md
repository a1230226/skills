---
name: product-direction-brief-template
description: 产品方向 brief 模板。当你需要把方向讨论收敛成可交给 PRD、实验执行或专利技能继续消费的标准中间件时使用。
version: 1.3.0
---

# direction_brief 模板

> **版本**: v1.3.0
> 用法：每次完成方向讨论后，都尽量收敛成一份 `direction_brief`，供后续 PRD、实验执行或专利技能继续消费。

---

## 标准模板

```markdown
# direction_brief

- `request_summary`: `用户当前想解决的问题`
- `scene_name`: `当前场景名称`
- `scene_group`: `所属业务域`
- `maturity_level`: `L0_idea | L1_defined | L2_validated | L3_proven`
- `business_scenario`: `场景发生在什么业务链路中，服务谁，何时触发`
- `target_description`: `本次最重要的目标是什么`
- `core_tension`: `为什么这个方向值得做，同时为什么它现在仍危险`
- `core_pain_points`:
  - `痛点1`: `...`
  - `痛点2`: `...`
- `business_chain_steps`:
  - `步骤1`: `完整业务主链中的关键步骤`
  - `当前卡点`: `当前问题位于哪一步`
- `business_chain_table`: `如适用，引用或内嵌核心主链拆解表`
- `key_decision_points`:
  - `决策点1`: `最值得优先关注的链路节点或判断点`
- `key_inputs_outputs`:
  - `inputs`: `关键输入数据 / 触发事件 / 角色动作`
  - `processing`: `核心处理中间态 / 判定机制 / 流程编排`
  - `outputs`: `结果输出 / 系统动作 / 用户感知`
  - `feedback_loop`: `如何根据结果继续调整`
- `direction_candidates`:
  - `方向A`: `一句话定位 + 优先级理由 + 风险`
  - `方向B`: `一句话定位 + 优先级理由 + 风险`
- `recommended_priority_direction`: `当前建议优先推进的方向`
- `why_priority_now`:
  - `理由1`
  - `理由2`
- `mvp_scope`:
  - `must_have`: `当前阶段必须实现的闭环`
  - `should_defer`: `可以延后一阶段的模块`
  - `not_now`: `本阶段明确不纳入的内容`
  - `mvp_cut`: `兼容旧版写法；如需回填方向库，可映射为同义字段`
- `human_in_loop`:
  - `人工环节1`: `当前可先由人工或半自动流程承担的步骤`
- `technical_levers`:
  - `技术抓手1`: `可被产品、研发和专利同时理解的关键机制`
  - `技术抓手2`: `...`
- `capability_layers`:
  - `能力层1`: `如数据接入 / 内容理解 / 策略判断 / 执行辅助 / 反馈学习`
- `priority_capabilities`:
  - `能力A`: `当前最值得先建设的能力 + 支撑价值`
- `evidence_status`:
  - `verified_evidence`: `已经具备的独立证据 / 结果证据 / 外部行为信号`
  - `internal_observations`: `来自内部讨论、访谈摘要、团队判断的内容`
  - `key_assumptions`: `仍需验证的关键假设`
  - `evidence_gaps`: `当前最关键的证据空白`
- `validation_plan`:
  - `key_hypothesis`: `当前最关键的待验证假设`
  - `validation_action`: `如何验证`
  - `adoption_signal`: `什么结果意味着用户愿意采用`
  - `success_signal`: `什么结果意味着方向继续推进`
  - `failure_signal`: `什么结果意味着收缩或转向`
  - `disconfirming_signal`: `什么结果会快速削弱当前推荐方向`
  - `judgment_update_rule`: `什么新证据会升档、降档或更换主方向`
  - `next_gate`: `通过这一轮后下一阶段验证什么`
  - `validation_signals`: `兼容旧版写法；如需回填方向库，可映射为同义字段`
- `decision_gates`:
  - `Gate 1`: `先看什么信号再进入下一阶段`
- `disconfirming_signals`:
  - `反证1`: `最危险的反证或不成立信号`
- `feedback_signals`:
  - `信号1`: `后续如何回收结果并用于校准`
- `patent_handoff_candidates`:
  - `是否存在适合继续做专利的技术/机制方向`
- `related_assets`:
  - `可复用的历史产品 / 文档 / 专利 / 研究素材`
- `next_action`: `继续补资料 / 做实验 / 写 PRD / 进入专利 skill`
- `last_updated`: `2026-05-01`
```

---

## 最小可用版

如果这份 `direction_brief` 预计要继续交给 `kz-patent-master`，不要使用比下面更少的字段。

```markdown
# direction_brief

- `scene_name`: `...`
- `maturity_level`: `...`
- `target_description`: `...`
- `core_tension`: `...`
- `core_pain_points`: `...`
- `business_chain_steps`: `...`
- `business_chain_table`: `...`
- `key_inputs_outputs`: `...`
- `direction_candidates`: `...`
- `recommended_priority_direction`: `...`
- `mvp_scope`: `...`
- `human_in_loop`: `...`
- `technical_levers`: `...`
- `priority_capabilities`: `...`
- `evidence_status`: `...`
- `validation_plan`: `...`
- `disconfirming_signals`: `...`
- `patent_handoff_candidates`: `...`
- `next_action`: `...`
```

---

## 版本历史

- **v1.3.0** (2026-05-19) - 补充 `mvp_cut` 与 `validation_signals` 兼容别名，降低与方向库模板的字段分叉
- **v1.2.0** (2026-05-19) - 新增 `core_tension`、`evidence_status`、`disconfirming_signals` 与 `judgment_update_rule` 字段，增强 brief 的证据状态与改判表达
- **v1.1.0** (2026-05-06) - 新增 `business_chain_table` 字段，支持把核心主链拆解表挂接进标准 brief
