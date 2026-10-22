# 项目初始化中的仓库发现规则

## 目的

这份参考文档用于帮助 `kz-project-init` 在项目初始化时稳定识别：

- 项目容器目录
- Git 仓库根目录
- BMAD 工件目录
- 主代码目录
- 文档目录与测试入口

## 基本原则

1. 不要默认当前工作目录就是实际代码仓库。
2. 不要默认只有一个 Git 仓库。
3. BMAD 工件目录与代码仓库目录可以分离。
4. “主代码仓库”与“项目容器目录”是两个不同概念。
5. 目录扫描要主动忽略缓存、依赖和构建产物，避免把噪声识别成项目事实。

## 发现顺序

### 1. Git 仓库

- 在目标目录下递归发现 `.git` 目录
- 允许根目录、子目录、嵌套模块同时拥有独立仓库
- 如果出现多仓库，后续所有 Git 规则都必须按仓库分别描述
- 如果只发现一个子仓库而根目录本身不是 Git 仓库，应归类为 `single-subrepo`

### 2. BMAD 工件

优先寻找：

- `_bmad-output/`
- `_bmad/`
- `project-context.md`
- `sprint-status.yaml`

如果 BMAD 工件位于根目录而代码位于子仓库，必须明确写入初始化结果。

若发现 `_bmad-output/` 存在，不要只记录“有 BMAD”；还应优先读取其中能解释项目目标、路线图、story、方案设计、阶段状态的文档，把这些内容作为强化项目认知的辅助事实来源。BMAD 文档的优先级低于代码与 Git 结构事实，但高于纯猜测。

### 3. 代码主目录

优先从这些线索判断：

- `pyproject.toml`、`package.json`、`Cargo.toml`、`go.mod` 等 manifest
- `justfile`、`Makefile`、`Taskfile.yml` 等统一命令入口
- `src/`、`server/`、`app/`、`backend/`、`frontend/`
- 实际存在的测试目录与运行脚本

### 4. 文档目录

优先识别：

- `docs/`
- `README*`
- `docs/contributing.md`
- 架构 / PRD / 设计文档目录

### 5. 门禁与证据入口

初始化时还应主动发现：

- `.github/workflows/*.yml` / `.yaml`
- `snapshots/`、`__snapshots__/`
- `fixtures/`、`fixture/`
- `*.schema.json` 或其他明确的 schema 产物
- `.github/ISSUE_TEMPLATE/`、`.github/PULL_REQUEST_TEMPLATE*`

## 扫描忽略规则

初始化扫描默认应忽略这些目录，除非用户明确要求深入：

- `.git`
- `__pycache__`
- `.pytest_cache`
- `.mypy_cache`
- `node_modules`
- `dist`
- `build`
- `.venv`
- `venv`

## 分类结果

初始化时应至少输出以下分类：

- `project_container`
- `git_repositories`
- `primary_code_repo`
- `nested_code_repos`
- `bmad_roots`
- `docs_roots`
- `test_entry_hints`
- `repo_type`
- `command_entry_files`
- `workflow_files`
- `snapshot_dirs`
- `fixture_dirs`
- `schema_files`

## 当前项目启发

像当前项目这种结构：

- `/.git`
- `/server/.git`
- `/server/kz_dash/.git`

说明初始化 skill 不能把“根目录就是唯一 Git 根”写死到 `AGENTS.md` 里。应明确说明：

- 哪个目录是项目容器
- 哪个目录是当前主要代码仓库
- 哪些子目录是独立仓库
- Git 操作应该默认在哪个目录执行
