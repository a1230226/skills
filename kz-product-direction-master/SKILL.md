---
name: kz-product-direction-master
description: 产品方向定位与立项规划助手。适用于业务场景梳理、方向收敛、优先级排序、MVP 切分、验证路径设计与方向库沉淀。当用户还在“想法很多但不清楚先做什么、做到什么程度、怎么验证”阶段时触发。
version: 1.5.0
---

# 产品方向大师 (Product Direction Master)

<!-- @类型: 领域专家助手 -->
<!-- @目的: 提供从业务场景到方向、MVP 与验证路径的统一工作流 -->
<!-- @场景: 产品方向探索、立项判断、优先级收敛、MVP 规划、验证设计 -->
<!-- @触发条件: 用户提出产品方向梳理、MVP 规划、优先级排序、验证路径设计或方向库维护需求 -->

> **一句话**: 我是产品方向定位助手，帮助把分散想法收敛成可执行的方向、MVP 和验证路径
> **版本**: v1.5.0
> **用途**: 辅助完成产品方向定位、MVP 切分与验证规划，并把结论沉淀为可复用方向资产
> **适用范围**: 产品经理、业务负责人、创新探索团队、需要将产品方向转译为专利机会的团队

## 触发示例

用户说以下话时会触发此 Skill：

- "这个产品想法很多，帮我梳理下先做什么"
- "这个业务场景的 MVP 应该怎么切"
- "帮我判断几个方向的优先级和验证路径"
- "我们有几个相关场景，想先收敛成 1 个主方向"
- "把这个场景沉淀成方向库条目"
- "帮我更新这个方向库条目的成熟度和验证结论"
- "把这个产品方向整理成一版可以给专利继续用的 brief"

---

## 目录

- [1. 核心能力](#1-核心能力)
- [2. 标准工作流](#2-标准工作流)
- [3. 方向库维护工作流](#3-方向库维护工作流)
- [4. 关键参考](#4-关键参考)

---

## 1. 核心能力 {#1-核心能力}

本 Skill 聚焦七类能力：

1. **方向定位能力**：从业务场景、目标、痛点与成熟度出发，生成并排序 2-5 个候选方向。
2. **MVP 规划能力**：把推荐方向切分为当前必须做、应该延后和暂不纳入的范围，避免“想法很多但边界失控”。
3. **验证设计能力**：为每个主方向定义关键假设、验证动作、判断信号与下一阶段决策门槛，并沉淀成标准 `direction_brief`。
4. **能力建设能力**：把业务链路翻译成可复用能力模块，识别底层共用能力、当前优先建设能力，以及哪些环节应先采用人机协同验证。
5. **主链结构化能力**：把业务流程压缩成统一的 `核心主链拆解表`，让方向判断、能力建设、人机协同、专利映射和成熟度评估围绕同一张表展开。
6. **证据纪律能力**：区分 `已验证证据`、`内部判断 / 团队陈述` 与 `待验证假设`，补齐最危险反证和改判条件，避免因为故事更顺就误判方向已经成立。
7. **交付路由能力**：在 `direction_brief`、完整产品方向文档、方向库条目和专利附加层之间做明确切换，避免把所有产品相关内容都混成同一种输出。

@提示: 本 Skill 解决的是“先做什么、做到什么程度、怎么验证”的问题，不直接替代 PRD、详细方案文档或专利交底书。
@提示: 当方向已经收敛、并且需要继续判断专利价值或撰写交底书时，再衔接 [kz-patent-master](../kz-patent-master/SKILL.md)。
@提示: 当用户讨论容易直接跳到页面、功能或大而全方案时，优先先拉平业务主链，再决定从哪个链路节点切入。
@提示: 当用户核心在问“这个有没有市场、值不值得做、投资人怎么看”时，先用 [investor-perspective](../investor-perspective/SKILL.md) 做外部压力测试，再回到本 Skill 做方向收敛与 MVP 切分；若边界不清，优先读取 [direction_evidence_and_handoff.md](references/workflows/direction_evidence_and_handoff.md)。

### @步骤0: 运行期决策矩阵

<!-- @类型: 决策步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 已根据用户原话命中方向收敛、方向库维护或外部压力测试路径 -->
<!-- @验证方式: 能根据命中信号说明当前应走哪条处理路径 -->

运行期优先级：

| 场景 | 命中信号 | 跳转到 |
|---|---|---|
| 方向收敛 / 优先级排序 / MVP 切分 / 验证路径设计 | 想法很多、先做什么、怎么切、怎么验证 | 本工作流 |
| 方向库维护 | 需要沉淀场景条目、更新成熟度、回填条目 | 方向库维护工作流 |
| 市场 / 商业 / 投资压力测试 | 有市场吗、值不值得做、投资人怎么看 | `investor-perspective` |

### @步骤1: 强规则摘要

<!-- @类型: 规则步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 已应用本 Skill 的证据纪律、反证意识和视角切换边界 -->
<!-- @验证方式: 能说明哪些规则是本 Skill 常驻约束，哪些情况应切到 investor-perspective -->

- 先区分 `已验证证据`、`内部判断 / 团队陈述`、`待验证假设`，再做方向排序。
- 不因表达更完整、故事更顺或汇报材料更漂亮，就自动提高 `maturity_level` 或推荐优先级。
- 每个推荐主方向至少补 1 个 `最危险反证`，避免只做正向论证。
- 默认输出方向判断，不默认输出 `MEET / WATCH / PASS` 一类投资标签；若用户明确要市场 / 投资视角，再衔接 `investor-perspective`。

### 默认输出合同

如果用户没有额外指定，本 Skill 的**默认输出**固定为以下 `6` 件套：

1. `场景定义`
2. `核心主链拆解表`
3. `候选方向与优先级`
4. `MVP 边界`
5. `验证路径`
6. `direction_brief`

默认情况下：

- 不直接展开成完整产品方向文档
- 不默认回填方向库条目
- 不默认做专利映射

这些都属于扩展输出，而不是本 Skill 的基础交付。

其中 `验证路径` 默认至少要回答 4 个问题：

- 当前方向依赖哪些关键假设
- 这些假设分别有哪些 `已验证证据`，哪些只是 `内部判断`
- 最危险的反证是什么
- 出现什么新证据时需要改判、升档或降档

### 默认判断纪律

沿用上方 `强规则摘要` 作为运行期常驻规则；只有当用户明确要求更强市场/商业压力测试时，才切换到 `investor-perspective`。

### 扩展输出类型

当用户明确提出或上下文强触发时，再进入以下扩展输出：

- `full_direction_doc`: 完整产品方向文档，适合申报、汇报、立项或对外对内评审材料
- `direction_library_entry`: 方向库沉淀条目，适合归档到长期方向资产库
- `patent_handoff_addon`: 专利映射附加层，只在明确存在专利资产、专利台账、交底书或要衔接专利时追加

@提示: 专利是高价值内容，但不是每个产品方向都适合默认做专利映射，因此它应作为附加增强层，而不是主工作流默认产物。

---

## 2. 标准工作流 {#2-标准工作流}

## @工作流: 产品方向定位、MVP 切分与验证路径设计

<!-- @类型: 主工作流 -->
<!-- @目的: 标准化处理产品方向探索、优先级排序、MVP 规划与验证路径设计 -->
<!-- @场景: 用户仍处于产品方向探索阶段，尚未收敛到稳定的实施路线 -->
<!-- @前置条件: 至少提供一个业务场景、目标、痛点或产品想法 -->
<!-- @后置验证: 形成 direction_brief，并明确推荐方向、MVP 边界、验证路径与下一步动作 -->
<!-- @触发条件: 用户提出方向太多、优先级不清、MVP 边界不明、验证路径模糊或需要沉淀方向库 -->
<!-- @ID: wf-product-direction-main -->

### @步骤1: 需求确认与现状归档

<!-- @类型: 交互步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 已明确当前要解决的是方向、MVP、验证还是方向库维护问题 -->
<!-- @验证方式: 输出任务目标、输入材料范围和本次交付目标 -->
<!-- @ID: step-direction-requirement-confirmation -->

- @动作: **识别任务意图**：判断当前重点是“方向收敛”“优先级排序”“MVP 切分”“验证路径设计”还是“维护方向库”。
- @动作: **收集最小输入**：确认是否已有场景描述、业务目标、痛点、数据或产品现状、历史验证证据、约束条件。
- @动作: **补主链视角**：若问题仍停留在功能或页面层，先补充当前业务主链、关键步骤、当前卡点和上下游依赖。
- @动作: **建立任务边界**：明确本次输出是讨论稿、立项判断、`direction_brief`、方向库条目，还是给下游专利/产品文档使用的中间件。
- @动作: **确定交付类型**：在 `default_brief`、`full_direction_doc`、`direction_library_entry`、`patent_handoff_addon` 中明确当前要产出的交付形态；若用户未指定，默认使用 `default_brief`。
- @动作: **识别分析视角**：判断本次更应该从“方向排序”“能力优先级”还是“页面/功能落地”角度推进；若用户尚未明确，默认先做方向与能力视角。
- @动作: **识别已有资产**：优先定位已有的方向库条目、历史方案、PRD、评估记录、用户反馈和实验数据。
- @动作: **拆分证据层级**：把当前输入拆成 `已验证证据`、`内部判断 / 团队陈述`、`待验证假设` 三层；若缺少独立证据，显式标记为待核验，不要直接写成“方向已成立”。
- @动作: **必要时读取边界参考**：若“继续做方向判断”与“先做市场 / 投资压力测试”的边界不清，先读取 [direction_evidence_and_handoff.md](references/workflows/direction_evidence_and_handoff.md) 再决定是否切换视角。
- @动作: **判断是否需要外部压力测试**：若用户的真实问题更接近“市场有没有、商业是否成立、投资人怎么看”，则先串联 [investor-perspective](../investor-perspective/SKILL.md) 做压力测试，再回到本 Skill 完成方向收敛与 MVP 规划。
- @动作: **判断是否需要主链表**：若场景存在 3 步以上业务链路、明显上下游依赖，或后续要衔接 PRD / 立项 / 专利 / 汇报，则默认输出 `核心主链拆解表`；若链路过短，则降级为简版主链清单。
- @动作: **判断是否追加专利层**：只有当用户明确提到“专利、交底书、专利台账、技术资产、布局”等上下文时，才追加 `patent_handoff_addon`；否则不默认输出专利映射。

### @步骤2: 检索方向库并建立场景视图

<!-- @类型: 分析步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-direction-requirement-confirmation -->
<!-- @验证点: 已识别与当前问题最接近的历史场景条目和可复用结论 -->
<!-- @验证方式: 输出 1-5 个候选历史条目及其借鉴用途 -->
<!-- @ID: step-direction-library-retrieval -->

- @动作: **优先查方向库**：如项目内已有方向参考库，先读取对应业务域文件，例如 [education_ai.md](references/directions/education_ai.md)，再决定本次是否新增或更新条目。
- @动作: **无方向库时临时建索引**：若尚无正式方向库，则从现有材料中提炼“场景-目标-痛点-候选方向-验证状态”摘要，作为临时索引。
- @动作: **识别成熟度**：把当前场景标记为 `L0_idea`、`L1_defined`、`L2_validated` 或 `L3_proven`。
- @动作: **建立场景视图**：明确当前分析对象属于哪个业务域、服务谁、在何种流程节点发生、与哪些相邻场景关联。
- @动作: **定位链路节点**：标记当前问题位于业务主链的哪个节点，识别其上游输入、下游结果，以及它更偏“前置决策层”“执行层”还是“反馈层”问题。
- @动作: **必要时先拉平主链**：若用户给出的信息仍然是碎片化想法，先输出一版业务主链，再进行候选方向排序和 MVP 切分。
- @动作: **按需输出主链表**：需要主链表时，优先按 [core_chain_breakdown_table.md](references/templates/core_chain_breakdown_table.md) 输出基础版；若已有能力建设、人机协同或专利上下文，则升级为增强版。

@提示: 若当前工作流已经确定，但用户提供的信息不足以直接执行，读取 [input-template-product-direction-workflow.md](references/examples/input-template-product-direction-workflow.md) 获取一次性输入模板。

### @步骤3: 执行核心产品任务

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-direction-library-retrieval -->
<!-- @验证点: 已完成方向排序、MVP 切分与验证路径设计 -->
<!-- @验证方式: 输出的 `direction_brief` 符合模板，并可支撑下一步产品或专利动作 -->
<!-- @ID: step-direction-execute-task -->

根据任务重点，执行以下动作：

#### A. 产品方向定位与优先级排序
引用规则：[product_direction_mapping.md](references/workflows/product_direction_mapping.md)

- @动作: **拆解问题链路**：从业务目标、关键痛点、输入输出链路和约束条件中提炼真正值得做的技术或产品抓手。
- @动作: **生成候选方向**：输出 2-5 个候选方向，并区分“推荐主方向”“可并行方向”“暂不建议方向”。
- @动作: **提炼核心矛盾**：用一句话说明“为什么这个方向值得做，同时为什么它现在仍危险”，避免只写正向机会不写主要阻力。
- @动作: **排序与解释**：基于用户价值、差异化空间、落地复杂度、证据密度、证据可信度、资产衔接度、反馈飞轮潜力、底座复用度和反证风险进行排序。
- @动作: **区分层级**：显式判断每个候选方向更偏前置决策、执行提效还是反馈复盘，避免默认把执行层工具排在前面。
- @动作: **保持排序克制**：若只有更顺的故事、没有更强的新证据，不要把原本需要观察的方向直接升级为主方向。

#### B. MVP 切分与范围控制
引用规则：[product_direction_mapping.md](references/workflows/product_direction_mapping.md)

- @动作: **定义最小验证闭环**：明确当前必须跑通的最小链路，而不是一次性塞入所有设想。
- @动作: **切分范围层级**：把方案拆成 `must_have`、`should_defer`、`not_now` 三层。
- @动作: **补人机协同**：显式标记哪些环节可以先由人工或半自动流程替代，哪些环节必须在第一阶段就产品化。
- @动作: **识别失控风险**：指出哪些模块是当前不做也不影响验证结论的，避免“伪 MVP”。

#### C. 验证路径设计
引用规则：[product_direction_mapping.md](references/workflows/product_direction_mapping.md)

- @动作: **明确关键假设**：列出当前方向成立所依赖的关键判断，不默认所有设想都正确。
- @动作: **设计验证动作**：为每条关键假设匹配验证方式，如访谈、灰度、人工服务替代、原型测试、局部实验。
- @动作: **区分证据级别**：将证据至少分为 `内部判断 / 团队陈述`、`外部行为信号`、`结果性证据` 三层；没有外部行为或结果证据时，不要轻易写成 `validated`。
- @动作: **定义判断信号**：明确 adoption、结果改善、复用意愿或付费意愿等不同层次的信号，哪些结果意味着继续推进，哪些结果意味着要收缩或转向。
- @动作: **写出最危险反证**：明确什么现象一旦出现，会快速削弱当前推荐方向，例如采用率过低、结果改善不成立、关键角色不愿切换流程或无法形成可复用底座。
- @动作: **定义改判条件**：写清楚“看到什么新证据会升档、看到什么新证据会降档或改向”，避免验证结束后仍停留在模糊判断。
- @动作: **设计阶段门**：用 `Gate 1 / Gate 2 / Gate 3` 明确先验证什么，再进入下一阶段。
- @动作: **避免伪验证**：不要把“用户说不错”“演示顺利”“内部团队有共识”直接当成方向成立；这些最多只能算弱信号。

#### D. 能力建设优先级梳理
引用规则：[product_direction_mapping.md](references/workflows/product_direction_mapping.md)

- @动作: **抽象能力层**：把业务步骤翻译成若干能力层，例如数据接入、内容理解、策略判断、执行辅助、反馈学习。
- @动作: **识别共用底座**：指出哪些能力属于跨方向复用的底层能力，例如对象标准化、标签体系、评分体系、知识沉淀。
- @动作: **收敛优先能力**：明确当前最值得先建设的 3-5 个能力，以及它们分别支撑哪些候选方向。

#### E. 核心主链拆解表
引用规则：[core_chain_breakdown_table.md](references/templates/core_chain_breakdown_table.md)

- @动作: **默认输出基础版**：当场景存在稳定业务链路时，至少输出 `步骤 | 核心目标 | 关键输入 | 关键输出 | 常见痛点 | 可产品化机会` 六列。
- @动作: **按上下文升级为增强版**：若当前讨论涉及能力建设、MVP、人机协同、成熟度或专利，则补齐 `关键决策点`、`人机协同`、`对应能力层`、`当前成熟度`、`对应专利项`。
- @动作: **表格优先服务主链而非页面**：表格行应对应关键业务步骤或决策节点，不要退化成页面列表或功能菜单。
- @动作: **控制粒度**：默认保持 `5-12` 行；若链路过长，优先合并弱相关子步骤，而不是无限细分。
- @动作: **向下游复用**：若后续要进入专利 skill 或完整产品方向文档，优先复用这张表作为统一中间层，而不是重新口头描述主链。

#### F. 交付组装与边界控制

- @动作: **默认只交付 6 件套**：若交付类型为 `default_brief`，则仅输出场景定义、主链表、候选方向、MVP、验证路径和 `direction_brief`。
- @动作: **完整文档单独展开**：若交付类型为 `full_direction_doc`，按 [product_direction_full_doc_template.md](references/templates/product_direction_full_doc_template.md) 组织完整文档。
- @动作: **方向库单独沉淀**：若交付类型为 `direction_library_entry`，使用 [product_direction_reference_template.md](references/templates/product_direction_reference_template.md) 回填条目，不要混写成完整文档。
- @动作: **专利映射只做附加层**：若交付类型包含 `patent_handoff_addon`，则在默认输出或完整文档之后，再追加“主链步骤 -> 专利映射 -> 空白点”分析；不要把专利映射并入每次默认产物。
- @动作: **明确下游边界**：PRD、详细方案设计、交互设计、技术架构设计、专利价值评估和交底书撰写，不属于本 Skill 默认交付，应作为后续衔接动作指出。

### @步骤4: 输出 direction_brief 并回填方向资产

<!-- @类型: 验证步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-direction-execute-task -->
<!-- @验证点: 已生成标准中间产物，并明确是否写回方向库或交给下游技能 -->
<!-- @验证方式: 输出符合模板的 `direction_brief`，并给出下一步动作 -->
<!-- @ID: step-direction-brief-writeback -->

- @动作: **输出标准 brief**：按 [product_direction_brief_template.md](references/templates/product_direction_brief_template.md) 生成 `direction_brief`。
- @动作: **保证下游可消费**：若下一步明确要进入 [kz-patent-master](../kz-patent-master/SKILL.md)，则 `direction_brief` 中不得省略 `target_description`、`key_inputs_outputs`、`technical_levers` 与 `patent_handoff_candidates`。
- @动作: **保证能力视角可复用**：若本次问题明显依赖能力建设分析，则在 `direction_brief` 中补齐 `business_chain_steps`、`key_decision_points`、`priority_capabilities`、`human_in_loop` 与 `feedback_signals`。
- @动作: **保证判断纪律可复用**：在 `direction_brief` 中补齐 `core_tension`、`evidence_status`、`disconfirming_signals` 与 `judgment_update_rule`，让下游知道当前哪些已被验证、哪些仍只是判断、什么证据会改变结论。
- @动作: **禁止过度宣称**：若当前没有独立外部行为或结果证据，不要把结论写成“已验证 / 已跑通 / 方向成立”，应使用“待验证 / 初步观察 / 低置信度成立”等更准确口径。
- @动作: **按需挂接主链表**：若本次已输出 `核心主链拆解表`，则在 `direction_brief` 或完整文档中同步保留 `business_chain_table` 或 `core_chain_breakdown_table` 字段，供后续 PRD、汇报或专利继续消费。
- @动作: **按交付类型裁剪输出**：`default_brief` 保留中间件风格；`full_direction_doc` 扩展成完整文档；`direction_library_entry` 聚焦条目化沉淀；`patent_handoff_addon` 仅作为附加章节追加。
- @动作: **沉淀长期资产**：若本次方向具有复用价值，按 [product_direction_reference_template.md](references/templates/product_direction_reference_template.md) 写回方向库条目。
- @动作: **明确下游衔接**：若方向已足够清晰，指出后续进入 PRD、需求拆解、验证执行，还是交给 [kz-patent-master](../kz-patent-master/SKILL.md) 继续做专利价值评估或交底书。
- @动作: **给出下一步建议**：例如补场景素材、补验证证据、先做人工流程、先写评估文档、先立外围方向。

---

## 3. 方向库维护工作流 {#3-方向库维护工作流}

## @工作流: 产品方向参考库维护

<!-- @类型: 子工作流 -->
<!-- @目的: 把一次性的方向讨论沉淀为可复用的方向资产 -->
<!-- @场景: 某个业务场景已经完成方向收敛或阶段性验证，希望纳入长期参考库 -->
<!-- @前置条件: 至少形成了一版明确的方向判断或 direction_brief -->
<!-- @后置验证: 对应业务域文件中新增或更新了场景条目 -->
<!-- @触发条件: 用户要求维护方向库，或当前任务已经形成稳定结论，适合沉淀 -->
<!-- @ID: wf-product-direction-library-maintenance -->

### @步骤1: 收集场景与验证信息

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 已定位当前场景条目的核心输入与来源 -->
<!-- @验证方式: 能列出场景描述、目标、痛点、候选方向和验证状态 -->
<!-- @ID: step-library-source-collection -->

- @动作: **定位场景来源**：收集当前场景描述、方向讨论记录、历史实验、用户反馈或产品方案。
- @动作: **标记成熟度**：根据当前证据选择 `L0_idea`、`L1_defined`、`L2_validated`、`L3_proven`。
- @动作: **补能力变化**：若本次讨论涉及能力建设优先级调整，记录新识别的底层能力、优先能力和对应验证状态。
- @动作: **判断维护方式**：若方向库中尚无此场景则新增；已有相近条目则在原条目基础上补充成熟度变化与验证结论。
- @动作: **补结构化主链资产**：若当前场景已形成稳定主链，则把 `核心主链拆解表` 也视为可复用资产的一部分，一并写回条目。

### @步骤2: 回填条目并检查复用性

<!-- @类型: 验证步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-library-source-collection -->
<!-- @验证点: 条目能支持后续快速判断“这个场景先做什么、MVP 到哪、如何验证” -->
<!-- @验证方式: 条目按模板落盘，并能回答方向、MVP、验证、下一步四个问题 -->
<!-- @ID: step-library-writeback -->

- @动作: **使用统一模板**：按 [product_direction_reference_template.md](references/templates/product_direction_reference_template.md) 写入条目。
- @动作: **按业务域归档**：把条目放入对应业务域文件中，例如 [education_ai.md](references/directions/education_ai.md)。
- @动作: **检查可复用性**：确认条目能回答“推荐方向是什么、为什么优先、MVP 到哪里、先补什么能力、要看什么信号”。
- @动作: **检查主链表是否可复用**：若条目包含 `core_chain_breakdown_table`，确认它能支持后续快速判断“业务主链是什么、卡点在哪、哪些步骤已具备能力或专利支撑”。

@提示: 方向库的维护单元是“场景条目”，不是“一个想法一个模板”，也不是“一个成熟度一套模板”。

---

## 4. 关键参考 {#4-关键参考}

优先根据任务读取以下参考：

- **方向定位与 MVP 规则**: [product_direction_mapping.md](references/workflows/product_direction_mapping.md)
- **证据纪律与视角切换**: [direction_evidence_and_handoff.md](references/workflows/direction_evidence_and_handoff.md)
- **核心主链拆解表模板**: [core_chain_breakdown_table.md](references/templates/core_chain_breakdown_table.md)
- **direction_brief 模板**: [product_direction_brief_template.md](references/templates/product_direction_brief_template.md)
- **完整产品方向文档模板**: [product_direction_full_doc_template.md](references/templates/product_direction_full_doc_template.md)
- **方向参考库模板**: [product_direction_reference_template.md](references/templates/product_direction_reference_template.md)
- **工作流输入示例**: [input-template-product-direction-workflow.md](references/examples/input-template-product-direction-workflow.md)
- **主链表教育场景示例**: [input-template-core-chain-breakdown-education-ai.md](references/examples/input-template-core-chain-breakdown-education-ai.md)
- **方向库示例**: [education_ai.md](references/directions/education_ai.md)
- **内容创作方向库示例**: [content_creation_ai.md](references/directions/content_creation_ai.md)
- **投资压力测试视角**: [investor-perspective](../investor-perspective/SKILL.md)
- **专利下游衔接**: [kz-patent-master](../kz-patent-master/SKILL.md)

@提示: `references/examples/*.md` 只在工作流已经确定、但用户输入不足时读取；它们不参与主流程路由。

---

## 版本历史

- **v1.5.0** (2026-05-19) - 下沉证据纪律与 investor 分流边界到独立参考，并补强新版字段示例，降低主文档密度与后续扩写冲突
- **v1.4.1** (2026-05-19) - 补充运行期决策矩阵与强规则摘要，强化多意图路由与外部压力测试边界
- **v1.4.0** (2026-05-19) - 吸收投资视角中的证据纪律：新增证据分层、最危险反证、改判条件与核心矛盾要求；明确市场/投资问题与 `investor-perspective` 的边界
- **v1.3.0** (2026-05-06) - 增加默认输出合同与交付类型路由；明确专利映射为附加增强层；新增完整产品方向文档模板
- **v1.2.0** (2026-05-06) - 将“核心主链拆解表”升级为标准输出件；补充主链表模板、教育场景示例，以及 `direction_brief` / 方向库模板中的主链表字段
