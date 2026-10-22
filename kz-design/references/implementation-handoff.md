---
name: implementation-handoff
description: "kz-design 的设计实现交接协议：先产出通用设计交接包，再按目标实现系统生成轻量适配层。"
version: 1.0.3
---

# 设计实现交接协议

> **版本**: v1.0.3
> **用途**: 当设计结果需要交给前端、Dash、移动端、小程序或其他实现系统落地时，定义稳定的交接格式和适配边界

## @工作流: 通用交接包加系统适配层

<!-- @类型: 参考流程 -->
<!-- @目的: 让设计决策能被不同实现系统接住，同时避免为每个系统维护一套完整设计格式 -->
<!-- @场景: 用户要求 UI 规范、设计交接、给开发落地、适配组件库或接入某个工程 Skill -->
<!-- @后置验证: 输出中包含通用设计交接包、目标系统适配层和验证建议 -->
<!-- @ID: wf-design-implementation-handoff -->

### @步骤1: 先区分产物类型

<!-- @类型: 决策步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 已明确本次交付是探索、原型、交接还是实现修复建议 -->
<!-- @验证方式: 输出文件结构或交付说明能区分视觉产物、设计规范和实现适配 -->
<!-- @ID: step-classify-handoff-output -->

- @动作: `探索型` 交付用于选方向：输出 2-3 个方向、风险和最小 demo 计划。
- @动作: `原型型` 交付用于看效果和交互：输出 HTML、截图、交互路径和验证记录。
- @动作: `交接型` 交付用于工程落地：输出 `design-brief.md`、`ui-spec.md`、`implementation-handoff.md`，必要时附 HTML 或截图作为视觉参考。
- @动作: `评审型` 交付用于修复已有设计：输出问题优先级、修复动作和必要的改稿路径。
- @动作: HTML 是视觉验证和交互说明媒介，不默认等于生产源码；除非用户明确要求，否则不要把 HTML 当作唯一实现依据。

### @步骤2: 生成通用设计交接包

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 交接包不绑定某个前端框架，也足够让实现系统理解设计意图 -->
<!-- @验证方式: `design-brief.md` 与 `ui-spec.md` 能独立说明目标、结构、状态、tokens 和组件意图 -->
<!-- @ID: step-generate-general-design-package -->

通用设计交接包默认包含两份文档：

| 文件 | 内容 |
|---|---|
| `design-brief.md` | 目标受众、使用场景、成功标准、内容范围、事实与素材状态、关键假设 |
| `ui-spec.md` | 信息架构、页面/区块列表、阅读顺序、关键状态、交互路径、响应式规则、Theme Package、Visualization Spec、组件意图、内容/数据契约 |

- @动作: 先写设计目标和信息架构，再写视觉细节；不要只交付配色和截图。
- @动作: 组件意图用语义表达，例如主操作、次操作、危险操作、状态标签、筛选、数据表、抽屉、弹窗、消息反馈、空状态、加载状态。
- @动作: tokens 使用可映射名称，例如 `primary`、`success`、`warning`、`danger`、`info`、`text-primary`、`surface`、`border`、`radius-md`、`space-lg`，不要只写散落 hex。
- @动作: `Theme Package` 至少包含 theme name、visual intent、best used for、colors、typography、contrast notes 和 do-not-use。
- @动作: 若设计包含图表、信息图或数据看板，补充 `Visualization Spec`，用问题、字段、编码、聚合、单位、数据来源和状态说明图表语义；不要只交付截图或视觉样式。
- @动作: 外部数据必须记录数据来源、提供方、引用链接和新鲜度；缺来源的数据只能作为示例数据或 placeholder 标注。
- @动作: 状态必须覆盖默认、加载、空态、错误、禁用、成功、权限不足和数据过期等与任务相关的状态。
- @动作: 交互说明要写触发、反馈、结果和失败处理，不只写“点击按钮”。

### @步骤3: 读取目标实现系统约束

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 已识别目标系统的组件库、token 机制、布局系统、禁用做法和验证命令 -->
<!-- @验证方式: `implementation-handoff.md` 中有来源明确的系统约束清单；不确定项被标为待确认 -->
<!-- @ID: step-read-implementation-system -->

- @动作: 若用户提供目标实现 Skill、项目规则、组件规范或代码库，先读取最小必要入口，再生成适配层。
- @动作: 重点提取 5 类约束：可用组件库、token/theme 机制、布局系统、禁止使用的实现方式、验证命令。
- @动作: 如果目标系统没有提供规范，只输出系统无关交接包，并列出实现系统需要补充的信息。
- @动作: 不臆测组件 API、props、路由、状态管理或构建方式；适配层只写已确认或可由实现系统自行映射的内容。
- @动作: 不为每个系统复制一套完整设计格式；只在通用交接包后追加一段轻量映射。

### @步骤4: 生成实现系统适配层

<!-- @类型: 操作步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 适配层能把设计语义翻译成目标系统可执行的组件、tokens、布局和验证任务 -->
<!-- @验证方式: `implementation-handoff.md` 包含映射表、禁用项、开放问题和验收清单 -->
<!-- @ID: step-generate-adapter-layer -->

`implementation-handoff.md` 默认结构：

```markdown
# Implementation Handoff

## Target System
- Name:
- Source rules read:
- Component library:
- Token/theme mechanism:
- Layout system:
- Verification commands:

## Design To System Mapping
| Design intent | Target component/pattern | Token/style mapping | Notes |
|---|---|---|---|

## Theme Package
- Theme name:
- Visual intent:
- Best used for:
- Colors:
  - primary:
  - accent:
  - background:
  - surface:
  - text:
  - border:
  - success/warning/danger/info:
- Typography:
  - display:
  - body:
  - mono/code:
- Contrast notes:
- Do not use:

## Visualization Spec
- Question:
- Chart type:
- Data fields:
- Encoding:
- Aggregation:
- Unit:
- Time grain:
- Labels/legend:
- Source:
- Data provenance:
  - Provider:
  - Reference link:
  - Freshness:
- Interaction:
- Empty/error state:

## States And Data Contract
- Loading:
- Empty:
- Error:
- Disabled:
- Permission:
- Data freshness:

## Do Not Implement As
- ...

## Open Questions
- ...

## Acceptance Checks
- ...
```

- @动作: 映射表只做“设计意图 -> 目标组件/模式 -> token/style 映射 -> 注意事项”，不要直接写大段生产代码。
- @动作: 如果目标系统有封装组件，优先映射到封装组件；没有时再映射到底层组件。
- @动作: 如果目标系统要求语义 token，交接时不要要求实现方硬编码 hex；把品牌色、状态色和中性色映射到 token。
- @动作: 如果设计中有自由视觉效果，需要标注能否降级为目标系统已有组件、theme 或 CSS；无法稳定落地的效果列入风险。
- @动作: 如果设计中有图表，优先映射到目标系统已有图表组件或可视化库；若目标系统没有图表能力，只交付 Visualization Spec 和视觉参考，不要求实现方照搬静态图片。
- @动作: 验收清单必须包含视觉一致性、关键交互、响应式、空/错/加载状态，以及目标系统自己的校验命令。

### @步骤5: 和实现 Skill 协作

<!-- @类型: 协作步骤 -->
<!-- @优先级: 必须 -->
<!-- @验证点: 设计 Skill 与实现 Skill 的职责边界清晰，不互相覆盖 -->
<!-- @验证方式: 交付中能看到设计决策与实现任务分离，且实现任务可被目标 Skill 接续执行 -->
<!-- @ID: step-collaborate-with-implementation-skill -->

- @动作: `kz-design` 负责目标、结构、视觉方向、tokens、组件意图、状态、交互和验证参考。
- @动作: 实现 Skill 负责代码落点、组件 API、props、路由、数据契约、状态管理、测试和生产约束。
- @动作: 交给实现 Skill 时，把 HTML 或截图称为视觉参考，把 `ui-spec.md` 和 `implementation-handoff.md` 称为落地依据。
- @动作: 若实现过程中发现组件库不支持某个设计要求，应回到交接包更新降级方案，而不是让实现方临时硬写不可维护样式。

## 版本历史

- **v1.0.3** (2026-05-31) - 强化 Visualization Spec 的数据来源、提供方、引用链接和新鲜度字段。
- **v1.0.2** (2026-05-31) - 新增 Visualization Spec 交接字段，用于把图表语义交给不同实现系统。
- **v1.0.1** (2026-05-31) - 新增 Theme Package 交接字段，用于把配色策略和布局语法翻译成可复用 tokens。
- **v1.0.0** (2026-05-31) - 初始版本：定义通用设计交接包、目标系统适配层和实现 Skill 协作边界。
