# kz-bmad-run Workflow Map

## 目的

这份参考文档用于给 `kz-bmad-run` 提供按需加载的详细路由表，避免把全部状态机细节塞进 `SKILL.md` 正文。

变量约定：

- `${PROJECT_ROOT}`：当前仓库根目录
- `${PROJECT_RULES_ENTRY}`：项目级协作规则入口；优先为 `${PROJECT_ROOT}/AGENTS.md`
- `${BMAD_ROOT}`：BMAD 工件根目录；优先候选为 `${PROJECT_ROOT}/_bmad-output`
- `${SPRINT_STATUS_PATH}`：优先候选为 `${BMAD_ROOT}/implementation-artifacts/sprint-status.yaml`
- `${GIT_REPO_CANDIDATES}`：`${PROJECT_ROOT}` 下发现的全部 Git 仓库根目录
- `${REPO_FILE_MAP}`：目标文件到所属 Git 仓库根目录的映射，采用“最近祖先仓库优先”
- `${ACTIVE_GIT_ROOT}`：当前 workflow 应执行 Git 动作的仓库根目录
- `${GIT_MAIN_BRANCH}`：`${ACTIVE_GIT_ROOT}` 对应仓库的主集成分支；优先由项目规则与 Git 事实推断，常见值为 `master` 或 `main`
- `${STORY_SCOPE}`：当前 story 在 `${ACTIVE_GIT_ROOT}` 下的目标文件集合；优先来自 story `File List`、本轮实际改动文件与用户显式点名文件
- `${MERGE_BLOCKERS}`：会阻止切换主分支、合并或删除分支的问题集合

## 必读文件

每次进入流程编排时，优先读取：

- `${PROJECT_RULES_ENTRY}` 或仓库中的等价规则文件
- `${BMAD_ROOT}/project-context.md` 或项目中的等价上下文文档
- `${SPRINT_STATUS_PATH}` 或项目中的等价 story / sprint 状态文件
- [git-root-routing.md](git-root-routing.md)（仅在需要做 Git / review / 收尾动作，或项目存在多目录/嵌套仓库时）
- [pre-dev-story-confirmation.md](pre-dev-story-confirmation.md)（仅在下一步候选 workflow 为 `bmad-dev-story` 时）

Git / BMAD / 多仓库路由口径：

- 默认直接从 `${PROJECT_RULES_ENTRY}` 提取 Git 根路由、默认工作目录、分支策略、多仓库暂停点与任务收尾说明
- 只有当 `${PROJECT_RULES_ENTRY}` 明确引用额外规则文档时，才按引用继续读取
- 不要把缺少历史侧车 Git 文档，误判为流程阻塞

按需补充：

- 当前 story 文件
- `${BMAD_ROOT}/planning-artifacts/epics.md`
- `${BMAD_ROOT}/planning-artifacts/architecture.md`
- 项目提供的技术 / 业务扩展 skill 或专项规范文档

## Git 仓库发现与归属规则

在任何 Git 动作之前，先做两件事：

1. 发现 `${GIT_REPO_CANDIDATES}`
2. 基于当前 story 文件、story `File List`、用户明确点名的文件、BMAD 工件建立 `${REPO_FILE_MAP}`

归属判定使用“最近祖先仓库优先”：

- 文件同时落在项目根仓库和子目录仓库时，优先归属更深层的那个仓库
- 不得因为当前 cwd 在 `${PROJECT_ROOT}`，就默认所有 Git 动作都在根目录执行

`${ACTIVE_GIT_ROOT}` 选择规则：

- 所有实现文件都在同一仓库：该仓库即 `${ACTIVE_GIT_ROOT}`
- BMAD 工件在一个仓库、代码在另一个仓库：默认以代码仓库作为 `${ACTIVE_GIT_ROOT}`，BMAD 工件同步单独记录
- 多个代码仓库同时参与：先暂停并给出 repo 分组，不自动合并为一个 Git 单元

## Story 状态路由表

| 状态 | 默认下一步 | 优先 skill | 备注 |
| --- | --- | --- | --- |
| `backlog` | 先建分支并准备 story | `kz-bmad-run` + `bmad-create-story` | 先在 `${ACTIVE_GIT_ROOT}` 从最新 `${GIT_MAIN_BRANCH}` 创建对应 story 分支，再生成 story 工件；若用户未指定 story，可先走 `bmad-help` |
| `ready-for-dev` | 先确认再进入开发 | `bmad-dev-story` | 先输出“开发前确认摘要”，确认本次要开发/不开发的范围后再实现 |
| `in-progress` | 先确认再继续开发 | `bmad-dev-story` | 新一轮编排进入开发前仍补一次“开发前确认摘要”；若偏离原边界、优先级或验收口径，改走 `bmad-correct-course` |
| `review` | 审查或修复 | `bmad-code-review` / `bmad-dev-story` | 用户若已给出报错，可先修复再复审 |
| `done` | 先判断是否建议 retrospective，再做 Git 收尾或进入下一条 | `kz-bmad-run` 编排 Git + `bmad-help` | `done` 不等于已合并；Git 收尾必须基于 `${ACTIVE_GIT_ROOT}`；跨 story 默认建议 fresh context / 新 session |

## 场景到 BMAD workflow 的补充映射

当问题不是单纯的 story 状态推进，而是“这件事到底属于哪个 BMAD 层级”时，按下面规则路由：

| 场景 | 推荐 workflow / skill | 路由理由 |
| --- | --- | --- |
| 不知道当前在哪个阶段、下一步该跑什么 | `bmad-help` | 先做状态导航，再决定是否进入 create-story / dev-story / review |
| 想看当前 sprint 全局状态、风险和推荐动作 | `bmad-sprint-status` | 先读 `sprint-status.yaml`，不要直接猜下一步 |
| 核心 BMAD 文件缺失（如 `sprint-status.yaml`、story 文件、关键上游工件），导致无法稳定判断下一步 | `bmad-help` | 编排器优先回到 BMAD 正式导航，不在本 skill 中自己层层向上游推导 |
| story 准备开发前，怀疑 PRD / UX / Architecture / Epics / Stories 不完整或互相冲突 | `bmad-check-implementation-readiness` | 先确认工件是否足以支撑实现，再进入开发 |
| 当前 story 仍在 `backlog`，或已有 story 文件但上下文不足、需要补强 | `bmad-create-story` | 先补齐或补强 story 工件，再进入实现 |
| 当前 story 已 `ready-for-dev`，问题主要是编码实现 | `bmad-dev-story` | 已具备开发条件，但先做开发前人工确认，再正式执行 story |
| sprint 执行中边界、优先级、验收口径发生明显变化 | `bmad-correct-course` | 属于执行期变更管理，而不是单纯继续编码 |
| 需求定义、范围边界、产品口径写错，需要修 PRD | `bmad-edit-prd` | 问题在 PRD 层，优先修 PRD |
| epics / stories 切分不合理、Story 列表与验收拆分需要重构 | `bmad-create-epics-and-stories` | 问题在拆解层，优先重建 epics / stories |
| 技术方案、系统边界、实现一致性约束有误 | `bmad-create-architecture` | 问题在架构层，优先修正架构决策 |

路由原则：

- 如果问题已经明确落在 PRD / epics / architecture / story 工件层，优先调用对应 BMAD workflow
- 不要让 `kz-bmad-run` 自己手工维护全部 BMAD 工件；它负责识别问题层级、选择 workflow、编排执行顺序
- 如果还不确定问题到底落在哪一层，先回到 `bmad-help` 做保守导航
- 如果核心 BMAD 文件缺失、前置依赖不清，优先回到 `bmad-help`；不要在本 skill 中继续向上游阶段层层推导
- `bmad-check-implementation-readiness` 负责发现 readiness 缺口，不直接替代后续 PRD / epics / architecture 回修 workflow

## Epic Retrospective 判定规则

- retrospective 在通用 BMAD 流程里始终是“可选步骤”，不是每个 epic 收口后的默认必经步骤
- 当出现以下任一信号时，建议在 epic 收口时追加 `bmad-retrospective`：
  - 用户明确要求复盘
  - 刚发生过 `bmad-correct-course`
  - 同一 epic 内出现多次 review 修复、明显返工或 story 顺序重排
  - 并行/交接/热点文件冲突导致了显著流程偏移
- 当 epic 基本平稳完成，没有明显返工、优先级漂移或流程异常时，可跳过 retrospective
- 如果 `sprint-status.yaml` 中对应 `epic-X-retrospective` 仍为 `optional`，且没有上述触发信号，不要把 retrospective 当成阻塞下一步的前置条件
- 建议 retrospective 时，输出中必须附带触发依据，避免“因为流程看起来像收尾了”就机械建议复盘

## Subagent 兼容策略

- 如当前 AI 工具支持 subagent / 子代理，优先将单个 BMAD workflow 放到 fresh subagent 中执行。
- 当用户显式请求“用 `kz-bmad-run` 开始开发”“按 BMAD 流程推进”“由 Codex 直接驱动整个 BMAD 流程”时，在当前项目内默认视为已授权 workflow 级 subagent。
- 推荐优先 subagent 化的 workflow：`bmad-create-story`、validation、`bmad-code-review`、QA。
- `bmad-dev-story` 可以由 subagent 执行，但主 agent 仍负责最终整合、验证和 Git 收口。
- 如当前 AI 工具不支持 subagent，则由主 agent 执行相同 workflow，但每次进入新 workflow 前重新读取最小必要文件，模拟 fresh context。
- 将 story 标记为 `done`、合并回 `${GIT_MAIN_BRANCH}`、删除分支、开始下一条 story 等高风险动作，不因 subagent 支持而下放，默认仍由主 agent 决策。

## Dev Story 前人工确认规则

- 只要下一步候选 workflow 是 `bmad-dev-story`，主 agent 都应先读取 [pre-dev-story-confirmation.md](pre-dev-story-confirmation.md)
- 在真正调用 `bmad-dev-story` 前，必须先输出“开发前确认摘要”
- 摘要至少包含：本 story 要开发什么、本轮明确不做什么、关键验收点、当前假设/边界/风险、是否需要先补充或修正 story
- 用户若只做小修订，可先更新 story 文件或本轮执行口径，再进入 `bmad-dev-story`
- 用户若暴露出 story 边界、优先级、PRD、epics 或 architecture 层的明显漂移，应切换到对应上游 workflow，而不是直接继续开发

## Workflow 到 Subagent 的默认映射

| Workflow | 默认执行形态 | 备注 |
| --- | --- | --- |
| `bmad-help` | fresh subagent | 负责状态路由，不直接做 Git 收尾 |
| `bmad-sprint-status` | fresh subagent | 负责 sprint 风险与推荐动作，不直接改工件 |
| `bmad-check-implementation-readiness` | fresh subagent | 负责判断工件是否足以进入实现，并指出后续应转交的 workflow |
| `bmad-create-story` | fresh subagent | 主 agent 先建分支，subagent 生成或补强 story 工件 |
| `bmad-edit-prd` | fresh subagent | 聚焦 PRD 修正，按原 workflow 交互执行 |
| `bmad-create-epics-and-stories` | fresh subagent | 聚焦 epics/story 重拆与验收重组，按原 workflow 交互执行 |
| `bmad-create-architecture` | fresh subagent | 聚焦架构修正与实现一致性约束，按原 workflow 交互执行 |
| `bmad-dev-story` | fresh subagent | 主 agent 保留整合、最终验证与状态同步 |
| `bmad-code-review` | fresh subagent | 推荐和开发 subagent 分离，保持 fresh context |
| validation / QA | fresh subagent | 输出问题清单，不下放高风险决策 |

如果因为平台策略、工具约束或当前环境不允许使用 subagent：

- 必须显式说明这是一次“从默认 subagent 路径退化到主 agent 执行”的兼容运行。
- 退化执行时，仍要保留“一次 workflow 一次最小上下文重载”的纪律，避免跨 workflow 污染。

## Git 收尾路由

适用于 story 已 `done`，且用户要求“提交 git”“按 SOP 收尾”“合并回主分支”时。

顺序：

1. 确认 story 文件与 `sprint-status.yaml` 已同步到 `done`
2. 在 `${ACTIVE_GIT_ROOT}` 下构造 `${STORY_SCOPE}`，并将脏区分类为：
   - `in_scope_dirty`
   - `out_of_scope_tracked`
   - `out_of_scope_untracked`
   - `${MERGE_BLOCKERS}`
3. 只要 `in_scope_dirty` 已收口，且 `${MERGE_BLOCKERS}` 为空，就允许继续收尾；scope 外噪音默认记为挂起项，不再要求“整个仓库完全干净”
4. 优先尝试在当前 worktree 切到 `${GIT_MAIN_BRANCH}`
5. 若 checkout / merge 可能被 scope 外噪音、未跟踪文件覆盖风险或环境残留阻塞，改走“临时 worktree 收尾模式”
6. 如有远端则同步主分支；无远端则跳过
7. `--no-ff` 合并该仓库中的 story 分支
8. 删除该仓库中的本地 story 分支
9. 若当前 story 还涉及其他仓库，把它们列为单独待确认项，不自动假设“所有仓库都已收尾”

## Review 与未跟踪文件规则

plain `git diff` 会漏掉 untracked 文件，因此在 review 或提交前至少同时检查：

1. `${ACTIVE_GIT_ROOT}` 下的 `git status --short`
2. repo-scoped diff
3. `??` 文件对应的全文件内容

如果一个 story 同时涉及多个仓库：

- 先输出每个仓库下的目标文件列表
- 再按仓库分别构造 review 输入
- 未经用户确认，不自动生成“跨仓库混合 diff”

## 收尾脏区分类规则

收尾时不要再用“仓库是否完全干净”做唯一判断，而是按 `${STORY_SCOPE}` 分类：

- `in_scope_dirty`：属于当前 story scope、且仍未提交/未收口的改动；默认阻塞收尾
- `out_of_scope_tracked`：scope 外的已跟踪改动；默认不阻塞，但要在输出中列为挂起项
- `out_of_scope_untracked`：scope 外的未跟踪文件；默认不阻塞，但要检查是否会影响 checkout / merge
- `${MERGE_BLOCKERS}`：真正阻塞 Git 收尾的项，例如：
  - scope 内仍有未提交改动
  - 未跟踪文件会覆盖目标分支已有文件
  - 目标文件归属无法判断，无法确定是否属于当前 story
  - 当前 worktree 无法安全切换 `${GIT_MAIN_BRANCH}`

暂停规则：

- 只有 `in_scope_dirty` 未收口或 `${MERGE_BLOCKERS}` 非空时，才默认暂停
- 仅存在 `out_of_scope_tracked` / `out_of_scope_untracked` 且不影响 merge 时，允许继续并在最终输出中记录挂起项

## 临时 worktree 收尾模式

当当前 worktree 因环境噪音不适合直接 checkout / merge 时，默认优先使用临时 worktree 收尾：

1. 在 `${ACTIVE_GIT_ROOT}` 外围创建指向 `${GIT_MAIN_BRANCH}` 的临时干净 worktree
2. 在临时 worktree 中执行主分支同步、merge 与 branch cleanup
3. 完成后删除临时 worktree，并回到原工作目录继续汇报

适用场景：

- scope 外未跟踪文件很多，且不适合纳入 Git、也不适合忽略
- 当前目录存在会阻止 `checkout` 的噪音文件
- 用户明确要求“先把 story 合回主分支”，但不希望先清理整个工作区

## 高风险暂停点

默认需要暂停或明确确认的动作：

- 新建 story 分支
- 首次准备进入 `bmad-dev-story`
- 请求人工验证
- 将 story 改为 `done`
- 合并回 `${GIT_MAIN_BRANCH}`
- 删除本地 story 分支
- 结束当前 story 后开始下一条 story

若用户已明确发出这些动作指令，可视为已授权继续。

## 并行开发保护规则

如果用户要求多个 story 并行推进，至少检查：

- `Dependencies`
- `Write Set`
- `Shared Hotspots`
- `Interface Contract`

项目级热点识别规则：

- 优先读取 `AGENTS.md`、项目架构文档或并行开发模板里显式声明的热点文件
- 如果项目没有显式热点清单，则把“路由入口、权限配置、数据库配置、共享页面文件、共享模型文件、共享服务主入口、构建/部署配置”视为默认高冲突区域
- 若两个 story 会同时写同一热点文件，默认改为串行，或先冻结接口契约再并行

## 典型调用策略

### 继续项目但不知道下一步

- 先由 `kz-bmad-run` 读取状态
- 状态不清晰时调用 `bmad-help`
- 再进入后续 skill

### 准备开发，但怀疑工件还没对齐

- 先确认是不是单纯缺 story，还是上游规划工件彼此冲突
- 仅缺 story 上下文，或已有 story 但质量不足以安全开发时，走 `bmad-create-story`
- 如果怀疑 PRD / UX / Architecture / Epics / Story 整体未对齐，先走 `bmad-check-implementation-readiness`
- readiness 暴露出具体层级问题后，再转 `bmad-edit-prd`、`bmad-create-epics-and-stories`、`bmad-create-architecture` 或 `bmad-correct-course`
- 如果 readiness 结果仍不足以稳定判断应走哪条上游 workflow，回到 `bmad-help`

### 准备开始 story 开发，但想先确认这次具体要做什么

- 即使当前 story 已 `ready-for-dev` 或 `in-progress`，也不要直接开始 `bmad-dev-story`
- 先读取 [pre-dev-story-confirmation.md](pre-dev-story-confirmation.md)，输出“开发前确认摘要”
- 让用户先确认“本 story 要开发什么 / 本轮明确不做什么 / 关键验收点 / 当前假设边界”
- 如果用户只补小需求，先同步到 story 或执行口径，再进入 `bmad-dev-story`
- 如果用户的补充已经改变 story 边界或上游工件，应改走 `bmad-create-story`、`bmad-correct-course` 或其他对应 workflow

### 缺少核心 BMAD 文件

- 如果 `sprint-status.yaml`、story 文件或其他关键 BMAD 文件缺失，不要由 `kz-bmad-run` 自己继续向上游阶段递推
- 先回到 `bmad-help`，让 BMAD 正式导航决定应该进入 `bmad-sprint-planning`、`bmad-create-story` 或其他上游 workflow
- `kz-bmad-run` 默认更关注 story 实现过程，前提是 BMAD 设计阶段已经基本完成、PRD 或 epics 已存在

### 执行中发现规格漂移

- 如果是 sprint 执行期的边界、优先级、验收口径变化，优先走 `bmad-correct-course`
- 如果确认问题落在 PRD 层，转 `bmad-edit-prd`
- 如果确认问题落在 epics/story 拆解层，转 `bmad-create-epics-and-stories`
- 如果确认问题落在技术方案层，转 `bmad-create-architecture`
- 不要一边继续 `bmad-dev-story`，一边让 `kz-bmad-run` 手工散改多个 BMAD 工件

### 指定继续下一条 story

- 先读取 `sprint-status.yaml`
- 如该 story 仍是 `backlog`，先识别 `${ACTIVE_GIT_ROOT}`，创建对应 story 分支，再调用 `bmad-create-story`
- `create-story` 生成 story 文件与 `sprint-status.yaml` 后，先提交 story 工件
- 如已是 `ready-for-dev`，先做开发前人工确认，再调用 `bmad-dev-story`

### 已完成 story，准备收尾

- 先校验 story / sprint 状态一致性
- 先确认 Git 收尾应该落在哪个 `${ACTIVE_GIT_ROOT}`，并检查是否存在多仓库拆分
- 再构造 `${STORY_SCOPE}`，判断 `in_scope_dirty`、`out_of_scope_tracked`、`out_of_scope_untracked` 与 `${MERGE_BLOCKERS}`
- 若该 story 的完成同时意味着 epic 收口，先按“Epic Retrospective 判定规则”判断是否建议追加可选 retrospective
- 如仍需人工验证，先输出验证交接摘要：本 story 涉及功能、建议测试步骤、特别注意事项
- 如果当前 worktree 不适合直接切主分支，优先改走临时 worktree 收尾模式
- 再按 `${PROJECT_RULES_ENTRY}` 中的项目 Git 规则做合并收尾
- 对 scope 外但未阻塞的改动，作为“挂起项”报告，不要求为了本次收尾强行清仓
- 收尾完成后不要自动开始下一条 story；先请求人工确认，默认建议新开 session 再继续
