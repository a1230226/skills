# Dev Story 前人工确认

<!-- @类型: 参考文档 -->
<!-- @目的: 为 `kz-bmad-run` 提供进入 `bmad-dev-story` 前的人工确认套路 -->
<!-- @场景: story 已 `ready-for-dev` 或 `in-progress`，准备正式进入实现 -->
<!-- @加载时机: 当下一步候选 workflow 为 `bmad-dev-story` 时按需读取 -->

## 目的

这份文档不是独立 workflow，而是 `kz-bmad-run` 在调用 `bmad-dev-story` 前必须执行的一次人工确认暂停。

它的目标不是重新做完整需求分析，而是用低成本方式先把“这条 story 这次到底要开发什么”说清楚，给用户一个补充或微调的窗口，减少实现后返工。

## 触发时机

以下情况默认触发：

- 当前 story 状态为 `ready-for-dev`，准备第一次进入 `bmad-dev-story`
- 当前 story 状态为 `in-progress`，但这是一次新的 `kz-bmad-run` 编排，会再次进入 `bmad-dev-story`
- 用户明确要求“开始开发这条 story”“继续实现这条 story”“按 BMAD 流程推进这条 story”

以下情况通常不触发：

- 只是查看 sprint 状态、判断下一步 workflow、做 code review、做 Git 收尾
- 已明确转向 `bmad-correct-course`、`bmad-create-story`、`bmad-edit-prd` 等非开发 workflow

## 开发前确认摘要

进入 `bmad-dev-story` 前，主 agent 至少输出以下内容：

- 本 story 要开发什么：本轮计划落地的功能、页面、逻辑、接口、模型或交互
- 本轮明确不做什么：不在本次 story 范围内的功能、已知后置工作、暂不处理的扩展项
- 关键验收点：本轮是否完成的判断口径，优先写用户可感知结果
- 当前假设 / 边界 / 风险：依赖哪些前置工件、哪些口径仍可能调整、哪些部分实现时容易返工
- 是否需要先补充或修正 story：给用户一个明确入口，允许在真正开始开发前补充小需求

建议把摘要建立在以下证据之上：

- 当前 story 文件
- `sprint-status.yaml`
- 用户这轮消息中的最新补充
- 当前项目的 `AGENTS.md`、相关实现约束文档与仓库事实

## 用户反馈后的分流规则

### 可直接吸收的小修订

以下情况通常可以先补进 story 文件或当前执行口径，然后继续 `bmad-dev-story`：

- 文案补充
- 某个步骤或页面多一个小交互
- 某个按钮、字段、提示、显示顺序需要细化
- 验收口径需要补充一两条可执行描述
- 原 story 已涵盖该方向，只是表述不够完整

处理要求：

- 先把修订同步到 story 文件或本轮执行说明
- 再重新给出简化后的开发前确认摘要
- 得到用户确认后再进入 `bmad-dev-story`

### 不应直接硬进开发的漂移

以下情况默认不应直接继续 `bmad-dev-story`：

- 用户补充后，story 的目标、边界或优先级已明显变化
- 发现当前 story 缺少关键信息，已经不足以安全开发
- 问题实际落在 PRD、epics/story 拆解或 architecture 层
- 用户希望把一个 story 拆成多个 story，或把多个 story 合并

建议分流：

- story 内容不足但仍属于同一条 story 的补强：`bmad-create-story`
- 执行中的范围/优先级/验收变化：`bmad-correct-course`
- PRD 层变化：`bmad-edit-prd`
- epics / stories 拆解变化：`bmad-create-epics-and-stories`
- 技术方案或架构约束变化：`bmad-create-architecture`

## 输出口径建议

推荐把确认输出写成短结构，而不是长篇解释：

```text
## 当前状态
- 当前 story：
- 当前 BMAD 阶段：
- 下一步候选 workflow：`bmad-dev-story`

## 开发前确认
- 本 story 要开发：
- 本轮明确不做：
- 关键验收点：
- 当前假设/边界/风险：
- 是否需要先补充或修正 story：

## 待确认
- 是否按以上范围进入开发
```

## 使用边界

- 这一步是为了降低返工，不是把 `kz-bmad-run` 变成新的需求讨论器
- 如果用户已明确补充修正并确认，可以尽快进入 `bmad-dev-story`
- 如果问题已经明显偏到上游 BMAD 工件层，就应切换 workflow，而不是在确认摘要里无限追加细节
