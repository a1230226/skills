# Skills

> 一组面向 AI 编码助手（如 Claude Code、Codex 等）的开源 Skills，用于增强 AI 在项目初始化、流程编排、深度分析、产品规划、文档共创与视觉设计方面的能力。

[English](README.en.md) | **中文**

---

## 📋 Skills 汇总

| Skill | 描述 | 版本 |
|-------|------|------|
| [kz-project-init](#kz-project-init) | 项目初始化与 AI 协作基线建立 | v1.11.1 |
| [kz-bmad-run](#kz-bmad-run) | BMAD 流程编排与 Story 驱动器 | v1.13.0 |
| [kz-article-deep-analysis](#kz-article-deep-analysis) | 文章深度解读与认知增量分析 | v1.0.3 |
| [kz-skill-creator](#kz-skill-creator) | Skill 创建、重构与评测指南 | v1.40.6 |
| [kz-product-direction-master](#kz-product-direction-master) | 产品方向定位与立项规划助手 | v1.5.0 |
| [kz-doc-coauthoring](#kz-doc-coauthoring) | 文档共创工作流 | v1.2.0 |
| [kz-design](#kz-design) | 高保真视觉设计、原型与交接工作流 | v1.0.9 |

---

## 📦 包含的 Skills

### kz-project-init

> 项目初始化与 AI 协作基线建立

为新项目或存量仓库建立 AI 协作初始化基线：自动扫描仓库结构、识别 Git/BMAD/代码目录拓扑、生成规范化的 `AGENTS.md`，并按需沉淀项目画像与 `project-context.md`。

**适用场景**：新项目接手、旧仓库补齐 AGENTS.md、BMAD 启动前的项目画像整理。

**版本**：v1.11.1

---

### kz-bmad-run

> BMAD 流程编排与 Story 驱动器

在 BMAD 设计阶段基本完成后，作为"story 实现阶段的流程驱动器"协调各 BMAD skill。自动读取项目上下文、识别当前 story 状态、选择合适的 BMAD workflow（如 `bmad-help`、`bmad-create-story`、`bmad-dev-story`、`bmad-code-review` 等），并将 Git 收尾和状态同步纳入同一执行链。

**适用场景**：任意采用 BMAD 或兼容工件的项目中的 story 持续开发、新 session 接手、review 后修复与 Git 收尾。

**版本**：v1.13.0

---

### kz-article-deep-analysis

> 文章深度解读与认知增量分析

深度解读非学术类文章（博客、随笔、评论），穿透表面信息，抽取核心议题与核心主张，梳理论证逻辑，并评估对读者的认知增量与张力，输出结构化分析报告（含推理拓扑图与认知卡片）。

**适用场景**：博客、公众号文章、随笔、评论的深度阅读与知识提炼（不适用于学术论文或书籍）。

**版本**：v1.0.3

---

### kz-skill-creator

> Skill 创建、重构与评测指南

指导创建、重构与评测高质量、可验证、可发布的 AI Skill 及相关可复用指令资产。提供完整的 Skill 创建方法论，包括渐进式披露设计、语义化标记系统规范、工作流边界梳理、参考文档组织、验证机制设计与结构质量评测。

**适用场景**：创建新 Skill、重构现有 Skill、评测 Skill 或结构化指令资产的质量、编写参考文档与验证脚本。

**版本**：v1.40.6

---

### kz-product-direction-master

> 产品方向定位与立项规划助手

适用于业务场景梳理、方向收敛、优先级排序、MVP 切分、验证路径设计与方向库沉淀。帮助把分散想法收敛成可执行的方向、MVP 和验证路径，解决"想法很多但不清楚先做什么、做到什么程度、怎么验证"的问题。

**适用场景**：产品方向探索、立项判断、优先级收敛、MVP 规划、验证设计、方向库维护。

**版本**：v1.5.0

---

### kz-doc-coauthoring

> 文档共创工作流

以"收集上下文 → 搭骨架 → 逐段写作 → 读者测试"的结构化流程协助用户高质量完成文档写作。适用于技术规格、设计文档、决策记录、RFC、提案、README、操作手册等结构化内容，也适用于把零散讨论与上下文整理成可被他人阅读、复用、再提问的文档。

**适用场景**：撰写技术方案/设计文档/RFC/PRD/决策记录/提案，整理聊天记录或会议纪要为团队文档，从读者视角审校文档。

**版本**：v1.2.0

---

### kz-design

> 高保真视觉设计、原型与交接工作流

面向高保真 HTML 原型、设计 Demo、幻灯片、信息图/数据可视化、动画视频、设计方向探索、设计评审和实现交接。通过事实/资产核验、风格方向选择、媒介适配、反 AI slop 质量规则、截图/浏览器验证与交接文档，把一句设计需求推进到可打开、可验证、可交接的视觉产物。

**适用场景**：制作原型/HTML 演示/App mockup、PPT/Slides/信息图/数据可视化、动画 Demo，探索配色/布局/视觉风格，评审并修复设计，生成 UI 规范或实现交接包。

**版本**：v1.0.9

---

## 🚀 安装

### 方式一：直接复制（推荐）

将需要的 Skill 目录复制到你的 AI 编码助手的 Skills 目录中：

```bash
# 克隆仓库
git clone https://github.com/kingzeus/skills.git

# 复制指定 Skill 到你的项目
cp -r skills/kz-project-init /path/to/your/project/.skills/
```

### 方式二：作为 Git Submodule

```bash
git submodule add https://github.com/kingzeus/skills.git .skills
```

## 📖 使用说明

每个 Skill 目录下都包含一个 `SKILL.md` 文件，这是 Skill 的核心定义文件。AI 编码助手在加载 Skill 时会读取该文件来理解 Skill 的功能、工作流和约束。

### 目录结构

```
skill-name/
├── SKILL.md          # Skill 定义文件（核心）
├── assets/           # 模板与静态资源
├── references/       # 参考文档与详细规则
└── scripts/          # 校验与辅助脚本
```

### 使用示例

1. **项目初始化**：在项目根目录触发 `kz-project-init`，自动生成 `AGENTS.md` 和项目画像
2. **BMAD 流程驱动**：在 BMAD 项目中使用 `kz-bmad-run` 自动判断下一步 workflow 并推进
3. **文章深度解读**：提供文章 URL 或文本，使用 `kz-article-deep-analysis` 生成结构化分析报告
4. **创建新 Skill**：使用 `kz-skill-creator` 按规范创建、重构或评测 Skill
5. **产品方向规划**：使用 `kz-product-direction-master` 梳理业务场景、收敛方向、规划 MVP 与验证路径
6. **文档共创**：使用 `kz-doc-coauthoring` 以结构化流程撰写技术文档、RFC、提案或整理零散讨论
7. **视觉设计**：使用 `kz-design` 生成高保真原型、幻灯片、信息图、动画 Demo、设计评审或实现交接包

## 🤝 参与贡献

欢迎贡献新的 Skill 或改进现有 Skill！

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feat/your-skill-name`
3. 按 Skill 目录规范创建你的 Skill（包含 `SKILL.md`）
4. 提交代码：`git commit -m 'feat: add your-skill-name'`
5. 推送分支：`git push origin feat/your-skill-name`
6. 提交 **Pull Request**

### Skill 规范

- 每个 Skill 独立一个目录，目录名以 `kz-` 为前缀
- 必须包含 `SKILL.md` 文件，定义 Skill 的名称、描述、版本和工作流
- 建议包含 `scripts/validate_skill.py` 用于结构校验
- 参考文档放在 `references/` 目录，模板资源放在 `assets/` 目录

## 📄 许可证

[MIT License](LICENSE) © 2026 kingzeus
