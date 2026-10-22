---
name: kz-bmad-run
description: 该 skill 适用于由 Codex 在 BMAD 设计阶段基本完成后，继续驱动 story 实现过程：读取当前项目状态、判断下一步 workflow、轻量编排 bmad-help、story 开发/审查与 Git 收尾，并在高风险节点暂停确认。
version: 1.13.0
---

# Kz Bmad Run

<!-- @类型: Skill 概览 -->
<!-- @目的: 让 Codex 在当前项目中稳定地驱动 BMAD + Git 开发流程 -->

> **一句话**: 我是当前项目的 BMAD 流程编排器，帮助 Codex 根据当前状态自动判断下一步并按顺序推进。
> **版本**: v1.13.0
> **用途**: 在 BMAD 设计阶段基本完成、PRD 或 epics 已存在后，读取项目上下文、识别当前 story 状态、选择合适的 BMAD skill，并把 Git 收尾和状态同步纳入同一条执行链。
> **适用范围**: 任意采用 BMAD 或兼容工件的项目中的 story 持续开发、新 session 接手、review 后修复与 Git 收尾；若当前仓库存在额外项目规则或扩展 skill，则在通用主流程之上叠加使用。

## Overview

本 Skill 不是替代现有 BMAD skills，而是作为“story 实现阶段的流程驱动器”协调它们。它优先读取**当前项目**中的 `AGENTS.md`、`project-context.md`、`sprint-status.yaml` 和当前 story 文件；其中 `AGENTS.md` 是项目规则、Git 根路由、默认工作目录、分支与收尾约定的单一事实来源，再根据状态机选择 `bmad-help`、`bmad-create-story`、`bmad-dev-story`、`bmad-code-review` 等具体 skill。进入 Git 收尾时，默认按 **story scope 是否已收口** 与 **是否存在 merge blockers** 判断是否可继续，不再把“整个仓库必须完全干净”当作默认前提；当用户已明确授权继续 Git 收尾，且当前 story 已 `done`、`${MERGE_BLOCKERS}` 为空时，默认收尾链不只停在 commit，而是继续完成 `commit -> 切回 ${GIT_MAIN_BRANCH} -> merge 当前 story branch -> 确认 merge 成功 -> 删除本地 story branch`。

详细路由表与暂停点见 [workflow-map.md](references/workflow-map.md)。
进入 `bmad-dev-story` 前的人工确认套路见 [pre-dev-story-confirmation.md](references/pre-dev-story-confirmation.md)。
涉及多目录 / 嵌套仓库 / BMAD 工件与代码不在同一 Git 仓库时，额外读取 [git-root-routing.md](references/git-root-routing.md)。

通用变量约定：

- `${PROJECT_ROOT}`：当前仓库根目录
- `${PROJECT_RULES_ENTRY}`：项目级协作规则入口；优先为 `${PROJECT_ROOT}/AGENTS.md`，承载 Git / BMAD / 多仓库路由与任务收尾规则
- `${BMAD_ROOT}`：BMAD 工件根目录；优先候选为 `${PROJECT_ROOT}/_bmad-output`，若项目另有约定则以仓库事实为准
- `${SPRINT_STATUS_PATH}`：优先候选为 `${BMAD_ROOT}/implementation-artifacts/sprint-status.yaml`
- `${GIT_REPO_CANDIDATES}`：`${PROJECT_ROOT}` 下发现的 Git 仓库根目录集合，允许出现嵌套仓库
- `${REPO_FILE_MAP}`：当前 story / BMAD 工件 / 目标改动文件到所属 Git 仓库根目录的映射；归属规则采用“最近祖先仓库优先”
- `${ACTIVE_GIT_ROOT}`：当前 workflow 应执行 Git 操作的仓库根目录；从 `${REPO_FILE_MAP}` 推断，禁止默认等同于 `${PROJECT_ROOT}`
- `${GIT_MAIN_BRANCH}`：`${ACTIVE_GIT_ROOT}` 对应仓库的主集成分支；优先从项目文档、仓库约定或 Git 事实推断，常见值为 `master` 或 `main`
- `${STORY_SCOPE}`：当前 story 在 `${ACTIVE_GIT_ROOT}` 下应纳入提交与收尾判断的目标文件集合；来源优先级为 story `File List`、本轮实际改动文件、用户显式点名文件
- `${MERGE_BLOCKERS}`：会阻止切换主分支、合并或删除分支的工作区问题；例如 scope 内未收口改动、未跟踪文件覆盖风险、无法判定归属的脏文件

执行兼容策略：

- 如当前 AI 工具支持 subagent / 子代理，优先把单个 BMAD workflow 放到 fresh subagent 中执行，主 agent 负责编排、确认、Git 和收口。
- 如当前 AI 工具不支持 subagent，则继续由主 agent 执行，但在每个 workflow 开始前主动重载最小必要上下文，避免把上一阶段的长历史直接带入下一阶段。

subagent 授权约定：

- 当用户明确说“用 `kz-bmad-run` 开始开发”“按 BMAD 流程推进”“由 Codex 直接驱动整个 BMAD 流程”时，在当前项目语义中视为**已明确授权使用 workflow 级 fresh subagent**。
- 这项授权的范围仅限单个 BMAD workflow 的执行，例如 `bmad-help` / `bmad-create-story` / `bmad-dev-story` / `bmad-code-review` / validation / QA。
- 高风险动作仍不下放给 subagent：包括 story 标记 `done`、合并回 `${GIT_MAIN_BRANCH}`、删除分支、开始下一条 story、最终 Git 收尾决策。
- 如果平台或上层工具策略仍禁止 subagent，则退化为主 agent 执行，但必须明确说明“本应由 fresh subagent 承载，本次因工具策略退化为主 agent + 最小上下文重载”。

## 触发示例

用户说以下话时会触发此 Skill：

- "继续按 BMAD 流程推进这个项目"
- "帮我判断现在下一步该跑哪个 BMAD workflow"
- "从当前 sprint 状态继续往下执行"
- "按仓库规则驱动 story 开发直到收口"

## 工程化脚本（推荐）

- `scripts/validate_skill.py`: 校验 `SKILL.md` 是否满足结构要求，并检查关键编排约束是否存在

在修改或打包前先运行：

```bash
python scripts/validate_skill.py --skill .
```

## @工作流: 启动并驱动当前 BMAD 会话

<!-- @类型: 标准操作流程(SOP) -->
<!-- @目的: 在当前项目中由 Codex 稳定驱动 BMAD 流程，而不是依赖人工逐步提醒 -->
<!-- @场景: 新 session 接手、继续某条 story、判断下一步 workflow、准备 Git 收尾 -->
<!-- @前置条件: 当前工作目录位于采用 BMAD 或兼容工件的仓库；至少存在部分可读取的项目规则、BMAD 工件或 story 线索 -->
<!-- @后置验证: 已明确当前状态、选择正确 workflow、同步 BMAD 与 Git，并在高风险动作前暂停确认 -->
<!-- @ID: wf-main -->

### @步骤1: 装载仓库事实与最小上下文

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 已读取当前 session 所需的稳定规则与动态状态 -->
<!-- @验证方式: 能明确说出当前 story / sprint / Git 所处状态 -->
<!-- @ID: step-load-context -->

- @动作: 优先读取 `${PROJECT_RULES_ENTRY}`；如项目没有 `AGENTS.md`，则读取仓库中的等价规则文件
- @动作: 读取 `${BMAD_ROOT}/project-context.md`；如项目未生成该文件，且这会影响当前阶段判断，则优先回到 `bmad-help` 做保守导航
- @动作: 从 `${PROJECT_RULES_ENTRY}` 提取 Git 根路由、默认工作目录、主分支、分支策略、多仓库暂停点与任务收尾口径；不要默认寻找或依赖历史侧车 Git 文档
- @动作: 只有当 `${PROJECT_RULES_ENTRY}` 显式引用额外规则文档时，才按引用读取；不要把缺少侧车 Git 文档视为流程阻塞
- @动作: 读取 `${SPRINT_STATUS_PATH}`；如项目 BMAD 工件路径不同，则按仓库事实发现对应状态文件
- @动作: 如果用户指定了某条 story，或最近 story 与下一步强相关，则补充读取对应 story 文件
- @动作: 发现 `${GIT_REPO_CANDIDATES}`：在 `${PROJECT_ROOT}` 下收集所有 Git 仓库根目录（允许嵌套仓库），并按“最近祖先仓库优先”规则为当前 story 文件、File List、BMAD 工件与明确提到的目标文件建立 `${REPO_FILE_MAP}`
- @动作: 基于 `${REPO_FILE_MAP}` 识别 `${ACTIVE_GIT_ROOT}`；若当前执行目标涉及多个 Git 仓库，先按仓库分组并暂停说明“哪些文件属于哪个仓库、建议如何拆分”
- @动作: 在 `${ACTIVE_GIT_ROOT}` 内构造 `${STORY_SCOPE}`；不要用“整个仓库所有脏文件”替代当前 story 作用域
- @动作: 只在 `${ACTIVE_GIT_ROOT}` 已确定时，检查该仓库的当前 Git 分支、工作区状态和主集成分支；禁止因为 cwd 在 `${PROJECT_ROOT}` 就直接在根目录盲跑 Git
- @动作: 如果发现当前项目还提供额外的技术/业务约束文档或扩展 skill，只记录“何时补充使用”，不要在此步一次性全部展开

@提示: 如果用户已明确给出“继续 1.2”或“把 1.1 收口”，用户请求优先于自动推断。
@提示: 如果部分工件缺失，不要把“缺文件”直接等价于“可以跳流程”；先明确缺了什么，再做保守路由或补上下文。
@提示: 一旦进入任何 Git / review / 收尾动作，优先按需读取 [git-root-routing.md](references/git-root-routing.md)，不要假设 BMAD 工件目录与代码仓库目录相同。

### @步骤2: 识别目标并判断下一步 workflow

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-load-context -->
<!-- @验证点: 已给出清晰的当前状态判断和下一步 workflow 选择 -->
<!-- @验证方式: 能说明为什么选该 workflow，而不是别的 workflow -->
<!-- @ID: step-route-workflow -->

- @动作: 如果用户明确要求执行某一步，直接按用户目标推进
- @动作: 如果用户只说“继续”“下一步”，则先用 `${REPO_FILE_MAP}` 缩小 Git 作用域，再根据 `sprint-status.yaml`、story 文件状态、Git 状态自动路由
- @动作: 当状态判断不够清晰时，优先使用 `bmad-help` 做保守路由，而不是直接开始实现
- @动作: 参考 [workflow-map.md](references/workflow-map.md) 中的状态映射表做判断
- @动作: 先判断当前问题属于哪一层：状态导航、story 执行、story 纠偏、实现前工件就绪性、PRD 修正、epics/story 重拆、架构修正
- @动作: 如果问题本质上是 BMAD 工件不一致或规格漂移，优先路由到对应 BMAD workflow，不要由 `kz-bmad-run` 手工散改多个工件
- @动作: 如果 `sprint-status.yaml`、story 文件或其他核心 BMAD 工件缺失，且无法可靠判断当前应走哪条上游 workflow，优先回到 `bmad-help`
- @动作: 只要下一步候选 workflow 是 `bmad-dev-story`，不要立刻开始开发；先按 [pre-dev-story-confirmation.md](references/pre-dev-story-confirmation.md) 输出一份“开发前确认摘要”，并等待用户确认或补充

默认路由规则：

- `backlog` -> 先确认目标 story，并从最新 `${GIT_MAIN_BRANCH}` 创建对应 story 分支，再执行 `bmad-create-story`
- `ready-for-dev` -> 先输出“开发前确认摘要”，经用户确认后执行 `bmad-dev-story`
- `in-progress` -> 通常也先补一次“开发前确认摘要”再继续 `bmad-dev-story`；若边界、优先级或验收口径已偏移，则改走 `bmad-correct-course`
- `review` -> `bmad-code-review`，或根据用户反馈回到 `bmad-dev-story`
- `done` 且尚未完成 Git 收尾 -> 按 `${PROJECT_RULES_ENTRY}` 中的当前项目 Git 规则，在 `${ACTIVE_GIT_ROOT}` 上执行完整收尾链；默认目标是完成 commit、合并回 `${GIT_MAIN_BRANCH}` 并清理本地 story 分支
- 当前 story 已收口且准备进入下一条 story -> 先暂停并请求人工确认，默认建议使用 fresh context / 新 session 再继续
- Epic 已收口或用户要求复盘 -> 先判断是否建议追加可选 `bmad-retrospective`

场景补充路由规则：

- “当前下一步不清楚 / 想知道该用哪个 BMAD workflow” -> `bmad-help`
- “需要查看当前 sprint 全局状态、风险或推荐动作” -> `bmad-sprint-status`
- “当前没有 `sprint-status.yaml`、story 文件或其他核心 BMAD 工件，导致无法稳定判断下一步” -> `bmad-help`
- “准备开始实现，但怀疑 PRD / UX / Architecture / Epics / Story 不完整或彼此不一致” -> `bmad-check-implementation-readiness`
- “当前 story 还没创建成可开发工件，backlog story 需要生成 story 文件，或已有 story 但上下文不足需要补强” -> `bmad-create-story`
- “story 已 ready-for-dev，且问题主要是落地实现” -> 先做开发前人工确认，再执行 `bmad-dev-story`
- “执行中发现边界、优先级、验收口径、需求方向发生明显变化” -> `bmad-correct-course`
- “问题在 PRD 层，属于需求定义或产品范围要修正” -> `bmad-edit-prd`
- “问题在 epic / story 拆解层，属于 stories 列表、切分方式或验收拆解不合理” -> `bmad-create-epics-and-stories`
- “问题在技术方案、架构边界、实现一致性约束” -> `bmad-create-architecture`

@提示: 不要因为“看起来可以继续写代码”就跳过 `create-story`、`review` 或 Git 收尾。
@提示: `kz-bmad-run` 的职责是识别当前处于哪个 BMAD 层级并路由到合适 workflow；一旦确认属于 PRD / 架构 / epics / story 工件问题，优先让对应 BMAD skill 处理，而不是在本 skill 中手工维护全部工件。

Epic retrospective 判定规则：

- 默认不因为“某个 epic 刚结束”就自动追加 retrospective；它仍然是可选步骤
- 当用户明确要求复盘、epic 刚经历过 correct-course / 大幅优先级调整 / 多次返工 / review finding 集中爆发 / 跨 story 协作明显失真时，建议追加 `bmad-retrospective`
- 当 epic 基本按既定 story 顺序平稳完成、没有明显返工或流程偏移时，可跳过 retrospective，直接在人工确认后进入下一条 story 或 Git 收尾
- 若 `sprint-status.yaml` 中对应 `epic-X-retrospective` 仍为 `optional`，且当前只是在正常 story 切换，不要把 retrospective 当成阻塞步骤
- 做出 retrospective 建议时，应明确说明触发依据，而不是只因为“流程上通常会复盘”

### @步骤3: 调用具体 BMAD skill 并推进执行

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-route-workflow -->
<!-- @验证点: 已选择合适的 BMAD skill，并说明使用原因 -->
<!-- @验证方式: 在输出中明确说明“当前调用哪个 skill，解决什么问题” -->
<!-- @ID: step-run-workflow -->

- @动作: 路由判断阶段优先使用 `bmad-help`
- @动作: 如工具支持 subagent，优先把单个 BMAD workflow 放到 fresh subagent 中执行；如不支持，则由主 agent 按“最小上下文重载”方式兼容执行
- @动作: story 准备阶段先确保已进入对应 story 分支，再使用 `bmad-create-story`
- @动作: 开发阶段使用 `bmad-dev-story`，但每次真正调用前都要先由主 agent 输出“开发前确认摘要”并暂停等待用户确认
- @动作: 审查阶段使用 `bmad-code-review`
- @动作: 需要看当前实现阶段全局状态时使用 `bmad-sprint-status`
- @动作: 如果核心 BMAD 文件缺失、前置不清或无法稳定判断应走哪条上游 workflow，优先使用 `bmad-help`
- @动作: 进入实现前若怀疑规划工件缺漏、冲突或未就绪，优先使用 `bmad-check-implementation-readiness`
- @动作: 发生阶段偏移或 story 边界变化时使用 `bmad-correct-course`
- @动作: 如果问题明确落在 PRD / epics / architecture 层，分别使用 `bmad-edit-prd`、`bmad-create-epics-and-stories`、`bmad-create-architecture`
- @动作: 若当前项目提供额外的框架/业务扩展 skill（如 Dash、Django、Rails、数据平台、Infra 等），在对应阶段补充调用，但不要让扩展 skill 取代 BMAD 主流程编排
- @动作: `bmad-create-story`、validation、`bmad-code-review`、QA 优先使用 fresh subagent；`bmad-dev-story` 可用 subagent 执行，但主 agent 负责最终整合与验证
- @动作: 将 story 标记为 `done`、合并回 `${GIT_MAIN_BRANCH}`、删除分支、开始下一条 story 等跨阶段高风险动作，应始终由主 agent 持有最终决策权
- @动作: “开发前确认摘要”至少说明：本 story 要开发什么、本轮明确不做什么、关键验收点、当前假设/边界/风险、是否需要先调整 story
- @动作: 如果用户在确认阶段只提出小修订，可先补更新 story 文件或当前执行口径，再进入 `bmad-dev-story`
- @动作: 如果用户在确认阶段暴露出 PRD / epics / architecture / story 边界层面的明显漂移，不要直接硬进开发；优先改走 `bmad-correct-course`、`bmad-create-story` 或对应上游 workflow

subagent 执行模板：

| 当前 workflow | 默认执行者 | 主 agent 职责 | subagent 职责 |
| --- | --- | --- | --- |
| `bmad-help` | fresh subagent（推荐） | 读取仓库事实、给出最终路由决定 | 只做状态判断与 workflow 建议 |
| `bmad-sprint-status` | fresh subagent（推荐） | 决定是否继续、暂停或切换 workflow | 汇总 sprint 状态、风险和推荐动作 |
| `bmad-check-implementation-readiness` | fresh subagent（推荐） | 根据 readiness 结果决定是否进入实现，或转交后续 BMAD workflow | 校验 PRD / UX / Architecture / Epics / Stories 是否完整对齐，并指出缺口 |
| `bmad-create-story` | fresh subagent（默认） | 先建 story 分支、审阅工件、提交 story 工件 | 生成或补强 story 文件，并返回 create-story 结论 |
| `bmad-edit-prd` | fresh subagent（推荐） | 决定 PRD 修正完成后是否还需回到其他规划 workflow | 按原 workflow 执行 PRD 编辑，并在交互/审批点暂停等待结果 |
| `bmad-create-epics-and-stories` | fresh subagent（推荐） | 决定重拆完成后如何回到 create-story / dev-story | 按原 workflow 执行 epics / stories 重拆，并在交互/审批点暂停等待结果 |
| `bmad-create-architecture` | fresh subagent（推荐） | 决定架构修正完成后是否影响当前 sprint 和实现边界 | 按原 workflow 执行架构修正，并在交互/审批点暂停等待结果 |
| validation / QA | fresh subagent（默认） | 决定是否继续开发或回退修复 | 专注校验、列出问题、不做高风险 Git |
| `bmad-dev-story` | fresh subagent（推荐） | 把控边界、整合结果、运行最终验证、同步 BMAD/Git | 按 story 实现代码与局部验证 |
| `bmad-code-review` | fresh subagent（默认） | 接收 finding、决定修复与收口节奏 | 只做 review，输出 findings / 风险 / 测试缺口 |

@提示: 只要用户触发了 `kz-bmad-run`，默认就不是“要不要用 subagent”的讨论题，而是“哪个 workflow 该由哪个 fresh subagent 承载”的编排题。

@提示: 这里的“调用”是指在 Codex 中显式启用相应 skill，而不是只在口头上提到名称。

### @步骤4: 同步 BMAD 工件与 Git 动作

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-run-workflow -->
<!-- @验证点: BMAD 状态、story 工件、Git 分支与提交节奏保持一致 -->
<!-- @验证方式: story 状态、`sprint-status.yaml` 和 Git 历史互相能解释得通 -->
<!-- @失败信号: 代码已完成但状态文件未更新；story 已 done 但 Git 未收尾；直接在项目主集成分支上开发 -->
<!-- @排查: 重新读取 `${PROJECT_RULES_ENTRY}` 与当前 story 文件，核对分支、状态和提交记录 -->
<!-- @ID: step-sync-bmad-git -->

- @动作: 对 `backlog` story，先按 SOP 从最新 `${GIT_MAIN_BRANCH}` 创建对应 story 分支，再执行 `create-story`
- @动作: `create-story` 生成或更新 story 文件、`sprint-status.yaml` 或等价状态工件后，先提交 story 工件，再继续 validation 或开发
- @动作: 所有 Git 动作都必须从 `${ACTIVE_GIT_ROOT}` 执行，且只操作该仓库拥有的路径；不要跨仓库构造一个“假装统一”的 commit / branch / merge
- @动作: 如果当前 story 的实现文件、BMAD 工件或验证材料分布在多个 Git 仓库，先输出 repo 分组结果和建议拆分方案；未经确认不要自动在多个仓库同时收尾
- @动作: 开发或 review 修复时，按功能块提交，不把所有改动堆成一个巨型 commit
- @动作: 进行 review、验证或准备 commit 时，显式纳入 untracked 文件；不要只依赖 `git diff`，还要结合 `git status --short` 或按文件清单补充全文件检查
- @动作: 进入 Git 收尾前，把 `${ACTIVE_GIT_ROOT}` 的脏区分类为：`in_scope_dirty`、`out_of_scope_tracked`、`out_of_scope_untracked`、`${MERGE_BLOCKERS}`
- @动作: 默认只让 `in_scope_dirty` 未收口项与 `${MERGE_BLOCKERS}` 阻塞收尾；`out_of_scope_tracked` 与 `out_of_scope_untracked` 只要不影响 checkout / merge / delete branch，就记录为挂起项，不默认阻塞
- @动作: 在请求人工验证前，整理当前 story 的验证交接摘要，至少包含：本 story 涉及的功能、建议的人工测试步骤、需要特别注意的点
- @动作: 用户验证通过后，将 story markdown 与 `sprint-status.yaml` 或等价状态工件同步改为 `done`
- @动作: story 已 `done` 后，按 `${PROJECT_RULES_ENTRY}` 中的当前项目 Git 规则执行 Git 收尾；默认顺序是：整理并提交本 story 改动 -> 切回 `${GIT_MAIN_BRANCH}` -> 合并当前 story branch（默认优先非快进合并，以项目规则为准）-> 验证 merge 成功 -> 删除本地 story branch
- @动作: 若用户已明确要求“继续收尾”“直接进行合并”“提交并收尾”“合并回主分支”或等价表达，且 `${MERGE_BLOCKERS}` 为空，则把上述完整收尾链视为同一组默认动作执行，而不是只在 commit 后停止
- @动作: 如果当前 worktree 因 scope 外噪音、未跟踪文件冲突或 checkout 风险无法安全切到 `${GIT_MAIN_BRANCH}`，优先改走“临时 worktree 收尾模式”，在干净 worktree 中完成 merge / cleanup
- @动作: 如果 merge 已成功且仓库没有远端，或用户未要求推送远端，则本轮 Git 收尾仍视为已完成；此时至少要把“已提交、已合并、已删除本地分支”分别交代清楚
- @动作: 若当前 story 的完成同时意味着整个 epic 收口，先按“Epic retrospective 判定规则”判断是否建议追加可选 retrospective，再决定是进入复盘还是直接收尾/转入下一条 story
- @动作: 当前 story 收尾完成后，如要进入下一条 story，先暂停并请求用户确认；默认建议重新开始一个 fresh context，避免 token 上下文过长或跨 story 污染
- @动作: 如果仓库没有远端，则跳过 `pull` / `push`，只完成本地收尾

@提示: Git 由 shell 命令执行，流程判断由本 Skill 编排；两者职责不同，不要混淆。
@提示: BMAD 工件同步与代码仓库提交是两套时钟。只要路径归属不同，就要分别报告“哪个仓库已完成什么、哪个仓库还没收尾”。

### @步骤5: 在高风险节点暂停确认

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-sync-bmad-git -->
<!-- @验证点: 高后果动作发生前，已让用户明确确认或已得到显式授权 -->
<!-- @验证方式: 输出中清楚列出“待确认动作”和后果 -->
<!-- @ID: step-pause-on-risk -->

- @动作: 在为 `backlog` story 创建新 story 分支前，如用户尚未明确要进入该 story，先确认
- @动作: 在发现当前 workflow 需要跨多个 Git 仓库执行时，先确认是“拆成多仓库分步执行”还是“本轮仅处理其中一个仓库”
- @动作: 在首次准备调用 `bmad-dev-story` 前，必须先输出“开发前确认摘要”，让用户确认本 story 的开发范围、边界与待补充项
- @动作: 在请求人工验证前，先输出结构化验证摘要，避免用户自己反推“这次到底改了什么、该怎么测”
- @动作: 在将 story 标记为 `done` 前，如仍缺人工验证，先暂停
- @动作: 在 Git 收尾前，若 `${MERGE_BLOCKERS}` 非空，或某些脏文件无法判定是否属于 `${STORY_SCOPE}`，先暂停说明阻塞项与建议处理方式
- @动作: 在合并回 `${GIT_MAIN_BRANCH}` 前，如用户尚未明确授权继续 Git 收尾，先确认本次 story 是否真的完成收口
- @动作: 在删除本地 story 分支前，确认合并已经成功；若 merge 失败、目标分支不对或 branch 仍承载未落地改动，则暂停，不做删除
- @动作: 在结束当前 story 并准备开始下一条 story 前，必须人工确认是否继续；默认建议新开 session / fresh context 后再启动下一条

@提示: 如果用户已经明确要求“继续执行”“提交 git”“收口为 done”“继续收尾”“直接进行合并”“提交并收尾”，且当前语义仍在同一条 story 的 Git 收尾链内，可视为已授权继续执行 merge back + local cleanup；但跨 story 自动续跑不默认授权，除非用户明确要求在当前会话继续下一条。

## @工作流: 遇到阻塞或流程不一致时的处理

<!-- @类型: 纠偏流程 -->
<!-- @目的: 在状态冲突、实现偏差或并行冲突出现时，提供稳定回退路径 -->
<!-- @场景: story 状态不清、Git 与 BMAD 不一致、并行开发撞热点文件、运行时错误 -->
<!-- @前置条件: 主工作流已发现冲突或阻塞 -->
<!-- @后置验证: 已找到新的安全下一步，而不是盲目继续推进 -->
<!-- @ID: wf-exceptions -->

### @步骤1: 识别阻塞类型

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 能明确当前属于状态不清、需求变更、并行冲突还是技术问题 -->
<!-- @验证方式: 给出一句分类判断，并指出证据来源 -->
<!-- @ID: step-classify-blocker -->

- @动作: 如果是“当前下一步不清楚”，优先回到 `bmad-help`
- @动作: 如果是“状态是清楚的，但想快速看 sprint 风险和推荐动作”，转到 `bmad-sprint-status`
- @动作: 如果是“核心 BMAD 文件缺失、前置不清或无法稳定判断该走哪条上游 workflow”，转到 `bmad-help`
- @动作: 如果是“尚未开始实现，但感觉规划工件不完整或互相打架”，转到 `bmad-check-implementation-readiness`
- @动作: 如果是“已有 story，但内容不够完整、上下文不足或不足以安全开发”，优先转到 `bmad-create-story` 做补强
- @动作: 如果是 story 边界或优先级变化，转到 `bmad-correct-course`
- @动作: 如果是 PRD 层定义错误或需求范围变化，转到 `bmad-edit-prd`
- @动作: 如果是 epics / stories 拆解不合理、story 列表与验收拆分有误，转到 `bmad-create-epics-and-stories`
- @动作: 如果是架构边界、方案一致性或实现约束定义有误，转到 `bmad-create-architecture`
- @动作: 如果是项目特定技术问题，转到对应的项目扩展 skill 或技术规范
- @动作: 如果是 Git 状态与文件路径归属不一致，先重建 `${REPO_FILE_MAP}` 并读取 [git-root-routing.md](references/git-root-routing.md)
- @动作: 如果是并行 story 冲突，检查 `Dependencies`、`Write Set`、`Shared Hotspots`、`Interface Contract`

### @步骤2: 给出保守下一步，而不是强推实现

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @依赖: step-classify-blocker -->
<!-- @验证点: 已给出最安全、最小范围的继续动作 -->
<!-- @验证方式: 输出中包含“先做什么，再做什么”而不是直接跳到编码 -->
<!-- @ID: step-safe-next-action -->

- @动作: 先恢复状态一致性，再继续实现
- @动作: 如果冲突来自高热点文件，优先串行，不要硬并行
- @动作: 如果工件不足以继续，但又无法明确判断应补哪类上游工件，优先回到 `bmad-help`，而不是在 `kz-bmad-run` 中手工散改工件或自己层层向上推导

## 输出模式

本 Skill 使用严格模板输出，默认结构如下：

```text
## 当前状态
- 当前 story：
- 当前 BMAD 阶段：
- 当前 Git 状态：

## 建议动作
- 下一步 workflow：
- 原因：

## 本次执行
- 已读取：
- 已决定：
- 已执行：

## Git 收尾
- 已提交：
- 已合并回主分支：
- 已删除本地分支：
- 未执行原因：

## 待确认
- [仅在高风险动作前列出]

## 开发前确认
- 本 story 要开发：
- 本轮明确不做：
- 关键验收点：
- 当前假设/边界/风险：
- 是否需要先补充或修正 story：

## 人工验证
- 本 story 涉及功能：
- 建议测试步骤：
- 特别注意：

## 风险与阻塞
- [如无则明确写“无”]

## 挂起项
- [仅在存在 scope 外改动、环境噪音或本轮刻意未处理文件时列出]
```

---

## Resources

### scripts/

确定性校验脚本。

```bash
python scripts/validate_skill.py --skill .
```

### references/

按需读取的详细路由说明、Git 仓库归属规则、状态机映射，以及 `bmad-dev-story` 前的人工确认套路。

### assets/

当前无需额外资产，可保持为空。

---

## 版本历史

- **v1.13.0** (2026-05-10) - 强化 Git 收尾闭环：明确 story `done` 后默认执行完整收尾链（commit -> merge 回主分支 -> 删除本地分支），并补充“继续收尾 / 直接进行合并 / 提交并收尾”等显式授权口径
- **v1.12.0** (2026-05-10) - 强化 Git 收尾鲁棒性：引入 `${STORY_SCOPE}` 与 `${MERGE_BLOCKERS}`，将收尾阻塞从“全仓干净”改为“story scope 已收口 + 无 merge blockers”，并新增临时 worktree 收尾模式与挂起项输出
- **v1.11.0** (2026-05-10) - 对齐新版 `kz-project-init`：明确 `AGENTS.md` 是项目规则、Git 根路由与收尾约定的单一事实来源，移除对历史侧车 Git SOP 的默认依赖
- **v1.10.0** (2026-05-07) - 在进入 `bmad-dev-story` 前新增强制人工确认：要求先输出“开发前确认摘要”说明本 story 要开发/不开发的内容、验收点与假设边界，并在用户确认或补充后再进入实现；新增对应参考文档与路由说明
- **v1.9.1** (2026-05-03) - 收紧 skill 边界：明确 `kz-bmad-run` 默认在 BMAD 设计阶段完成后、围绕 story 实现过程工作；核心工件缺失或前置不清时统一回到 `bmad-help`，不在本 skill 中层层向上游推导
