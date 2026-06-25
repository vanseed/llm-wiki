---
name: ingest
description: 将 raw/ 原始资料或 translated/ 中文译文编译到 wiki/ 中。使用场景：用户执行 /ingest、要求摄取/导入/收入资料、或要求将指定文件加入本地 LLM Wiki。禁止移动、删除或改写 raw 文件；处理完成后更新 wiki/index.md、wiki/log.md 与 wiki/_meta/manifest.md。
---

# ingest 技能

## 核心目标

维护本 Obsidian **LLM Wiki**。`raw/` 是只读事实层，`translated/` 是完整中文译文层，`wiki/` 是知识编译输出层，`wiki/_meta/manifest.md` 是来源状态登记表。执行本技能前先遵循根目录 `AGENT_GUIDE.md`。

## 触发逻辑

1. 用户执行 `/ingest`：扫描 `raw/` 所有子目录，找出待处理文件。
2. 用户执行 `/ingest <path>`：仅处理指定 `raw/` 文件或 `translated/` 译文。
3. 用户自然语言要求“摄取”“导入”“收入资料”“加入知识库”：按 ingest 流程执行。

## raw 分类约定

- `raw/01-articles/` — 网页、博客、官方文档和教程。
- `raw/02-papers/` — 论文、白皮书、PDF 和研究报告。
- `raw/03-transcripts/` — 视频、播客、课程和访谈转录。
- `raw/04-notes/` — 个人笔记、会议记录和头脑风暴。

## 编译流水线

### -1. 判定输入层

- 输入为 `raw/...`：直接读取该原始资料，manifest 的 `raw_path` 使用该路径。
- 输入为 `translated/...`：先读取译文 frontmatter 的 `raw_path` 字段，并用它作为 `wiki/_meta/manifest.md` 的 `raw_path`；正文内容从译文文件读取。
- 如果译文缺少 `raw_path`，暂停并要求用户确认对应原始资料，不要猜测。
- source 页面 frontmatter 的 `sources` 仍记录原始 `raw_path`，可在正文中补充“中文译文：`translated/...`”。

### 0. 读取 manifest

- 先读取 `wiki/_meta/manifest.md`。
- 如果目标 raw 文件已是 `ingested`，先报告已存在的 source 页面和产出页面，询问用户是否执行增量更新。
- 如果目标 raw 文件是 `path_mismatch`，报告真实路径与 source frontmatter 路径差异，不要移动 raw 文件。
- 如果目标 raw 文件未登记，继续摄取，并在完成后新增 manifest 行。

### 1. 读取源文件

- `.md` 文件：完整读取内容。
- `.pdf` 文件：尝试提取文本；无法提取时，在来源摘要中记录文件元信息。
- `translated/` 译文：读取完整译文，并通过 `raw_path` 保持原始来源追溯。

### 2. 提炼核心并翻译

从源文件中提取：

- 核心主旨：1-2 句话说明资料讲什么。
- 实体：人物、公司、工具、产品等具体名词。
- 概念：框架、方法论、理论等抽象名词。

非中文内容必须翻译成简体中文。

如果输入已经是 `translated/` 中文译文，不要重复生成全文翻译，只做知识萃取和结构化。

### 3. 创建来源摘要

在 `wiki/sources/` 创建 Markdown 文件，文件名使用 `摘要-{文件slug}.md`：

```markdown
---
title: "摘要-文件slug"
type: source
tags: [来源, 原始文件]
sources: [raw/01-articles/xxx.md]
last_updated: YYYY-MM-DD
---

## 核心摘要
[3-5句话的核心总结]

原始资料：`raw/01-articles/xxx.md`
中文译文：`translated/01-articles/xxx.zh.md`（如适用）

## 关联连接
- [[EntityName]] — 关联实体
- [[ConceptName]] — 关联概念
```

### 4. 知识网络化

对提取出的实体和概念：

- 实体写入 `wiki/entities/`。
- 概念写入 `wiki/concepts/`。
- 页面不存在时创建新页。
- 页面存在时增量合并新信息。
- 发现冲突时立即暂停，向用户报告冲突内容并询问处理方式。

页面必须包含 `## 关联连接`，并遵循 `AGENT_GUIDE.md` 的 frontmatter 规范。

### 5. 更新全局注册表

更新 `wiki/index.md`：

- Sources: `[[摘要-source-slug]] — 该资料的核心主旨`
- Entities: `[[EntityName]] — 该实体的身份定义`
- Concepts: `[[ConceptName]] — 该概念的核心定义`

追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] ingest | 操作简述
- **变更**: 新增 [[PageName]]; 更新 [[index.md]]
- **冲突**: 无 (或: 冲突 [[ConflictingPage]], 已暂停等待决策)
```

### 6. 更新 manifest

在确认以下全部完成后，更新 `wiki/_meta/manifest.md`：

- source 页面已创建或更新
- 实体/概念页面已创建或更新
- `wiki/index.md` 已更新
- `wiki/log.md` 已追加记录

manifest 行必须记录：

```markdown
| raw_path | status | source_page | output_pages | last_ingested | notes |
```

摄取成功时将 `status` 设为 `ingested`；发现路径不一致时设为 `path_mismatch`；冲突暂停时设为 `conflict_paused`。

**绝对禁止移动、删除、重命名或改写 `raw/` 文件。**

## 命名规则

- Source 页面使用 `摘要-{kebab-case-slug}.md`。
- Synthesis 页面使用 `{kebab-case-slug}.md`。
- Entity 页面使用 `TitleCase.md`。
- Concept 页面使用 `TitleCase_With_Underscores.md`。

## 冲突处理

发现新旧知识冲突时：

1. 停止当前 ingest。
2. 报告冲突页面和冲突点。
3. 询问用户选择：
   - A) 保留新旧两者，标注为 `## 知识冲突`
   - B) 在保留来源记录/冲突记录的前提下更新主叙述
   - C) 放弃本次 ingest
4. 根据用户选择继续或终止。
