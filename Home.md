# LLM Wiki Home

欢迎使用这个 Obsidian LLM Wiki 模板。这里是 vault 的人工入口页。

## 快速入口

- [[wiki/index|Wiki Index]] — 正式知识页总目录。
- [[wiki/_meta/dashboard|Dashboard]] — 当前状态、常用命令和维护入口。
- [[wiki/_meta/obsidian|Obsidian 使用约定]] — 本 vault 的 Obsidian 约定。
- [[wiki/_meta/workflows|Obsidian 工作流]] — 从收集资料到查询知识的操作路径。
- [[wiki/_meta/wiki-map.canvas|Wiki Map]] — Obsidian Canvas 结构地图。
- [[AGENT_GUIDE|Agent 主规范]] — Claude Code、Codex 和其他 Agent 共用规则。
- [[README|README]] — 项目说明和快速开始。
- [[VERIFY|Verification]] — 本地验证命令。

## 当前状态

- wiki 正式内容页：0
- raw 原始资料：0
- translated 中文译文：0
- manifest 条目：0
- 模板状态：干净初始库
- Obsidian 增强：Home、Dashboard、Workflow、Canvas

## 推荐流程

1. 将 1-2 个测试资料放入 `raw/` 的对应子目录。
2. 让 Agent 执行 `/status` 确认资料已出现。
3. 如果是外文资料且需要中文全文，执行 `/translate <raw路径>`。
4. 让 Agent 执行 `/ingest <路径>` 编译资料或译文。
5. 执行 `/lint` 检查健康状态。
6. 使用 `/query <问题>` 查询已经进入 wiki 的内容。

## 目录提醒

- `raw/` 是不可变事实层。
- `translated/` 是完整中文译文派生层。
- `wiki/` 是知识编译输出层。
- `wiki/_meta/` 是维护元信息层，不作为正式知识页。
- `assets/` 用于图片、PDF 和附件。
