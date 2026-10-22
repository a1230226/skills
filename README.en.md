# Skills

> A collection of open-source Skills for AI coding assistants (e.g., Claude Code, Codex) that enhance AI capabilities in project initialization, workflow orchestration, deep analysis, product planning, document coauthoring, and visual design.

**English** | [中文](README.md)

---

## 📋 Skills Overview

| Skill | Description | Version |
|-------|-------------|---------|
| [kz-project-init](#kz-project-init) | Project Initialization & AI Collaboration Baseline | v1.11.1 |
| [kz-bmad-run](#kz-bmad-run) | BMAD Workflow Orchestrator & Story Driver | v1.13.0 |
| [kz-article-deep-analysis](#kz-article-deep-analysis) | In-Depth Article Analysis & Cognitive Insight Extraction | v1.0.3 |
| [kz-skill-creator](#kz-skill-creator) | Skill Creation, Refactoring & Evaluation Guide | v1.40.6 |
| [kz-product-direction-master](#kz-product-direction-master) | Product Direction & Project Planning Assistant | v1.5.0 |
| [kz-doc-coauthoring](#kz-doc-coauthoring) | Document Coauthoring Workflow | v1.2.0 |
| [kz-design](#kz-design) | High-Fidelity Visual Design, Prototyping & Handoff Workflow | v1.0.9 |

---

## 📦 Included Skills

### kz-project-init

> Project Initialization & AI Collaboration Baseline

Establishes an AI collaboration baseline for new or existing repositories: automatically scans repository structure, identifies Git/BMAD/code directory topology, generates a standardized `AGENTS.md`, and optionally produces a project profile and `project-context.md`.

**Use cases**: Onboarding new projects, adding `AGENTS.md` to existing repos, preparing project profiles before BMAD adoption.

**Version**: v1.11.1

---

### kz-bmad-run

> BMAD Workflow Orchestrator & Story Driver

Acts as a "story implementation stage workflow driver" that coordinates BMAD skills after the design phase is largely complete. Automatically reads project context, identifies current story status, selects the appropriate BMAD workflow (e.g., `bmad-help`, `bmad-create-story`, `bmad-dev-story`, `bmad-code-review`), and integrates Git finalization and status synchronization into a single execution chain.

**Use cases**: Continuous story development, new session handoff, post-review fixes, and Git finalization in any project using BMAD or compatible artifacts.

**Version**: v1.13.0

---

### kz-article-deep-analysis

> In-Depth Article Analysis & Cognitive Insight Extraction

Performs deep analysis of non-academic articles (blogs, essays, reviews), extracting core issues and central claims, mapping argumentation logic, and evaluating cognitive value for readers — outputting a structured analysis report with reasoning topology diagrams and insight cards.

**Use cases**: Deep reading and knowledge extraction from blogs, essays, reviews, and opinion pieces (not suitable for academic papers or books).

**Version**: v1.0.3

---

### kz-skill-creator

> Skill Creation, Refactoring & Evaluation Guide

Guides the creation, refactoring, and evaluation of high-quality, verifiable, and publishable AI Skills and related reusable instruction assets. Provides a complete Skill creation methodology including progressive disclosure design, semantic markup system specifications, workflow boundary definition, reference documentation organization, validation mechanism design, and structural quality assessment.

**Use cases**: Creating new Skills, refactoring existing Skills, evaluating Skill or structured instruction asset quality, writing reference docs and validation scripts.

**Version**: v1.40.6

---

### kz-product-direction-master

> Product Direction & Project Planning Assistant

For business scenario analysis, direction convergence, priority sorting, MVP scoping, validation path design, and direction library maintenance. Helps consolidate scattered ideas into executable directions, MVPs, and validation paths — solving the problem of "having many ideas but not knowing what to do first, to what extent, and how to validate".

**Use cases**: Product direction exploration, project initiation decisions, priority convergence, MVP planning, validation design, direction library maintenance.

**Version**: v1.5.0

---

### kz-doc-coauthoring

> Document Coauthoring Workflow

A structured workflow — "gather context → build outline → write section by section → reader test" — for high-quality document creation. Suitable for technical specs, design docs, decision records, RFCs, proposals, READMEs, and runbooks. Also works for organizing scattered discussions and context into readable, reusable, and queryable documents.

**Use cases**: Writing tech specs, design docs, RFCs, PRDs, decision records, or proposals; organizing chat logs or meeting notes into team documents; reviewing documents from a reader's perspective.

**Version**: v1.2.0

---

### kz-design

> High-Fidelity Visual Design, Prototyping & Handoff Workflow

Supports high-fidelity HTML prototypes, design demos, slide decks, infographics/data visualizations, animation videos, design direction exploration, design review, and implementation handoff. It uses fact and asset verification, visual direction selection, medium-specific rules, anti-AI-slop quality checks, browser/screenshot verification, and handoff documents to turn a design request into a visual artifact that can be opened, verified, and handed off.

**Use cases**: Creating prototypes, HTML demos, app mockups, PPT/Slides, infographics, data visualizations, and animation demos; exploring color, layout, and visual style; reviewing and fixing designs; generating UI specs or implementation handoff packages.

**Version**: v1.0.9

---

## 🚀 Installation

### Option 1: Direct Copy (Recommended)

Copy the desired Skill directory to your AI coding assistant's Skills directory:

```bash
# Clone the repository
git clone https://github.com/kingzeus/skills.git

# Copy a specific Skill to your project
cp -r skills/kz-project-init /path/to/your/project/.skills/
```

### Option 2: Git Submodule

```bash
git submodule add https://github.com/kingzeus/skills.git .skills
```

## 📖 Usage

Each Skill directory contains a `SKILL.md` file — the core definition file. AI coding assistants read this file to understand the Skill's functionality, workflows, and constraints.

### Directory Structure

```
skill-name/
├── SKILL.md          # Skill definition file (core)
├── assets/           # Templates and static resources
├── references/       # Reference docs and detailed rules
└── scripts/          # Validation and utility scripts
```

### Examples

1. **Project Initialization**: Trigger `kz-project-init` in your project root to auto-generate `AGENTS.md` and a project profile
2. **BMAD Workflow**: Use `kz-bmad-run` in a BMAD project to automatically determine the next workflow and drive execution
3. **Article Analysis**: Provide an article URL or text to `kz-article-deep-analysis` for a structured analysis report
4. **Create New Skill**: Use `kz-skill-creator` to create, refactor, or evaluate Skills following best practices
5. **Product Direction Planning**: Use `kz-product-direction-master` to analyze business scenarios, converge directions, plan MVPs and validation paths
6. **Document Coauthoring**: Use `kz-doc-coauthoring` to write tech docs, RFCs, or proposals through a structured workflow, or organize scattered discussions
7. **Visual Design**: Use `kz-design` to create high-fidelity prototypes, slide decks, infographics, animation demos, design reviews, or implementation handoff packages

## 🤝 Contributing

Contributions of new Skills or improvements to existing ones are welcome!

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feat/your-skill-name`
3. Create your Skill following the directory conventions (must include `SKILL.md`)
4. Commit your changes: `git commit -m 'feat: add your-skill-name'`
5. Push the branch: `git push origin feat/your-skill-name`
6. Submit a **Pull Request**

### Skill Conventions

- Each Skill lives in its own directory, prefixed with `kz-`
- Must include a `SKILL.md` file defining the Skill's name, description, version, and workflows
- Recommended to include `scripts/validate_skill.py` for structural validation
- Reference docs go in `references/`, templates and static assets in `assets/`

## 📄 License

[MIT License](LICENSE) © 2026 kingzeus
