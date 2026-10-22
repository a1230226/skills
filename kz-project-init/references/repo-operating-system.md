# 把仓库当作协作操作系统来初始化

## 目的

这份参考文档说明：`kz-project-init` 不应只产出一份静态 `AGENTS.md`，而应帮助项目把协作入口梳理清楚并直接沉淀到 `AGENTS.md`。

## 四类关键入口

初始化时应优先识别并记录这四类入口：

- 规则入口：`AGENTS.md`、`README*`、`docs/contributing.md`
- 命令入口：`justfile`、`Makefile`、`Taskfile`、项目脚本入口
- 门禁入口：`.github/workflows/*.yml`、lint / test / release workflow
- 证据入口：`snapshots/`、`fixtures/`、schema 生成物、可比较输出

## Discovery-first 原则

不要先写规范，再去找证据；应该先发现仓库已经如何运作，再把这些事实整理成初始化文档。

优先回答这些问题：

1. 团队今天用什么命令作为本地标准入口？
2. 哪些 CI workflow 在阻止坏改动进入主分支？
3. 哪些改动会联动 schema、fixture、snapshot 或文档？
4. 哪些用户可见变化需要留下可 review 的证据？

## 初始化输出应承载什么

### `AGENTS.md`

应告诉后续 agent：

- 先看哪里拿规则
- 优先跑哪个本地入口
- 什么时候必须补文档、schema、fixture、snapshot

## 迁移建议

如果项目目前还没有统一入口，不要在初始化文档里假装它已经存在。应明确写出：

- 当前缺失哪些入口
- 建议优先补什么
- 哪些风险暂时仍需要人工 review 兜底
