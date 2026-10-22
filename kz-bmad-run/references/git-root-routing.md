# kz-bmad-run Git Root Routing

## 目的

这份参考文档用于约束 `kz-bmad-run` 在多目录、嵌套仓库、BMAD 工件与代码分离时如何发现 Git 仓库、判定文件归属，并把 review / branch / commit / merge 等动作路由到正确仓库。

## 变量约定

- `${PROJECT_ROOT}`：当前项目根目录，承载 BMAD 工件与项目级文档
- `${GIT_REPO_CANDIDATES}`：`${PROJECT_ROOT}` 下发现的全部 Git 仓库根目录
- `${REPO_FILE_MAP}`：目标文件到所属 Git 仓库根目录的映射
- `${ACTIVE_GIT_ROOT}`：当前 workflow 的 Git 操作目标仓库
- `${GIT_MAIN_BRANCH}`：`${ACTIVE_GIT_ROOT}` 的主集成分支
- `${STORY_SCOPE}`：当前 story 在 `${ACTIVE_GIT_ROOT}` 下的目标文件集合
- `${MERGE_BLOCKERS}`：会阻止 checkout / merge / cleanup 的工作区问题集合

## 仓库发现规则

1. 在 `${PROJECT_ROOT}` 下收集所有 Git 仓库根目录，允许出现嵌套仓库。
2. 识别目标文件集合，最少包含：
   - 当前 story 文件
   - story `File List` 中列出的实现文件
   - 当前轮用户显式点名的文件
   - BMAD 工件（如 `sprint-status.yaml`、story markdown）
3. 为每个目标文件分配所属仓库时，使用“最近祖先仓库优先”：
   - 文件同时被 `${PROJECT_ROOT}` 仓库和子目录仓库覆盖时，归属更深层的那个仓库
   - 不能因为 cwd 在根目录，就把所有文件都算到根仓库
4. 形成 `${REPO_FILE_MAP}` 后，再决定 `${ACTIVE_GIT_ROOT}`；禁止反过来先拍脑袋选仓库。

## ACTIVE_GIT_ROOT 选择规则

- 如果所有实现文件都归属于同一个仓库，该仓库就是 `${ACTIVE_GIT_ROOT}`
- 如果只有 BMAD 工件在根仓库、代码在子仓库，默认把**代码仓库**作为 `${ACTIVE_GIT_ROOT}`，并把 BMAD 工件同步单独记录
- 如果多个代码仓库同时参与当前 story，本轮不得自动合并为一个 Git 单元；应暂停并给出 repo 分组摘要，等待用户确认“拆分执行”或“只处理其中一个仓库”
- 如果当前只有 BMAD 工件变更、没有任何实现文件，则允许把拥有 BMAD 工件的仓库作为 `${ACTIVE_GIT_ROOT}`

## Git 动作路由规则

以下命令都必须在 `${ACTIVE_GIT_ROOT}` 执行：

- `git status`
- `git diff`
- `git log`
- `git checkout` / `git switch`
- `git branch`
- `git add`
- `git commit`
- `git merge`
- `git pull` / `git push`

并且：

- 只操作属于 `${ACTIVE_GIT_ROOT}` 的文件路径
- 不得在 `${PROJECT_ROOT}` 盲跑这些命令，除非 `${PROJECT_ROOT}` 本身就是 `${ACTIVE_GIT_ROOT}`
- 不得把两个仓库的文件塞进同一个 commit 计划里

## Review / Diff 规则

`git diff` 不能作为唯一事实来源，因为它会漏掉未跟踪文件。review 前至少同时做三件事：

1. 在 `${ACTIVE_GIT_ROOT}` 查看 `git status --short`
2. 获取 repo-scoped diff
3. 将 `??` untracked 文件作为“全文件 review 目标”纳入检查

如果当前 review 涉及多个仓库：

- 先输出每个仓库下的目标文件列表
- 再按仓库分别生成 review 输入
- 没有用户确认时，不自动做“跨仓库汇总 diff”

## Story Scope 与阻塞判定

Git 收尾不要默认要求“整个仓库完全干净”，而要先构造 `${STORY_SCOPE}`。

`${STORY_SCOPE}` 的优先来源：

1. 当前 story `File List`
2. 本轮已确认属于当前 story 的实际改动文件
3. 用户显式点名要求纳入本次提交/收尾的文件

工作区分类：

- `in_scope_dirty`：scope 内未收口改动，默认阻塞
- `out_of_scope_tracked`：scope 外已跟踪改动，默认不阻塞
- `out_of_scope_untracked`：scope 外未跟踪文件，默认不阻塞
- `${MERGE_BLOCKERS}`：真正会阻止收尾的项，例如未跟踪覆盖风险、scope 归属不清、无法安全 checkout

结论规则：

- `in_scope_dirty` 未收口 -> 阻塞
- `${MERGE_BLOCKERS}` 非空 -> 阻塞
- 仅有 `out_of_scope_tracked` / `out_of_scope_untracked` 且不影响 merge -> 允许继续，并在最终汇报中作为挂起项列出

## BMAD 工件与代码仓库分离时的处理

当 story markdown、`sprint-status.yaml` 等 BMAD 工件与实现代码不在同一个仓库时：

- BMAD 状态同步与 Git 提交视为两套节奏
- 代码仓库的 review / branch / commit / merge 不应因为 BMAD 工件在另一个仓库而被误判失败
- 汇报时必须明确区分：
  - 哪个仓库的代码状态已完成
  - 哪个仓库的 BMAD 工件已同步
  - 哪个仓库还没收尾

## 收尾规则

story 进入 `done` 后，Git 收尾必须基于 `${ACTIVE_GIT_ROOT}` 执行：

1. 确认该仓库下的目标文件状态已准备好
2. 推断并确认该仓库的 `${GIT_MAIN_BRANCH}`
3. 先构造 `${STORY_SCOPE}` 并判定 `${MERGE_BLOCKERS}`
4. 若当前 worktree 不适合直接切 `${GIT_MAIN_BRANCH}`，优先使用临时 `worktree` 在干净目录完成 merge / cleanup
5. 在该仓库执行 merge / cleanup
6. 若还有其他仓库参与本 story，单独列为“待确认的后续仓库收尾项”

## 临时 Worktree 收尾模式

推荐在以下场景使用临时 `worktree`：

- 当前目录存在大量 scope 外未跟踪文件
- 这些文件不适合提交，也不适合直接写入 `.gitignore`
- 它们会阻止 `checkout`、`switch`、`merge` 或 branch cleanup

使用原则：

- 临时 `worktree` 只用于 Git 收尾，不替代主工作目录继续开发
- 原工作目录中的 scope 外噪音保留原状，不因本次收尾被强行清理
- 最终汇报时要明确说明：story 已收尾，但原目录仍存在哪些挂起项

## 当前项目启发

像当前项目这种结构：

- `${PROJECT_ROOT}/.git`
- `${PROJECT_ROOT}/server/.git`
- `${PROJECT_ROOT}/server/kz_dash/.git`

说明同一个项目目录下可能同时存在项目级仓库、模块级仓库、子模块仓库。`kz-bmad-run` 必须先做归属判断，再做任何 Git 动作。
