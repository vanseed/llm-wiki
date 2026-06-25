---
name: ingest
description: 将 raw/ 原始资料或 translated/ 中文译文编译到 wiki/ 中。支持 `/ingest` 和 `/ingest <path>`。当用户提到"摄取"、"导入"、"收入"资料，或要求将文件加入知识库时，也应该触发此技能。禁止移动、删除或改写 raw 文件；处理完成后更新 wiki/index.md、wiki/log.md 与 wiki/_meta/manifest.md。
user-invocable: true
---

# ingest 技能

## 核心工作流：Inbox & Manifest

你正在维护一个 **LLM Wiki**（Obsidian 知识库）。`raw/` 是只读事实层，`translated/` 是完整中文译文层，`wiki/` 是知识编译输出层，`wiki/_meta/manifest.md` 是来源状态登记表。

**目录结构约定：**
- `raw/01-articles/` — 网页剪藏的 Markdown 文章
- `raw/02-papers/` — 论文和 PDF 文献
- `raw/03-transcripts/` — 视频、播客、课程和访谈转录
- `raw/04-notes/` — 个人笔记、会议记录和头脑风暴
- `translated/` — raw 的完整简体中文译文派生层
- `wiki/sources/` — 资料摘要
- `wiki/entities/` — 实体（人物、公司、工具、产品）
- `wiki/concepts/` — 概念（框架、方法论、理论）

## 触发逻辑

1. **用户执行 `/ingest`**：扫描 `raw/` 所有子目录，找出待处理文件。
2. **用户执行 `/ingest <path>`**：仅处理指定 `raw/` 文件或 `translated/` 译文。
3. **隐式触发**：用户说"把这个资料摄入知识库"、"导入这篇文章"时，自动执行 ingest。

## 编译流水线

对每个待处理源文件，严格按以下步骤执行：

### 步骤 -1：判定输入层

- 输入为 `raw/...`：直接读取该原始资料，manifest 的 `raw_path` 使用该路径。
- 输入为 `translated/...`：先读取译文 frontmatter 的 `raw_path` 字段，并用它作为 `wiki/_meta/manifest.md` 的 `raw_path`；正文内容从译文文件读取。
- 如果译文缺少 `raw_path`，暂停并要求用户确认对应原始资料，不要猜测。
- source 页面 frontmatter 的 `sources` 仍记录原始 `raw_path`，可在正文中补充“中文译文：`translated/...`”。

### 步骤 0：读取 manifest

- 先读取 `wiki/_meta/manifest.md`。
- 如果目标 raw 文件已是 `ingested`，先报告已存在的 source 页面和产出页面，询问用户是否执行增量更新。
- 如果目标 raw 文件是 `path_mismatch`，报告真实路径与 source frontmatter 路径差异，不要移动 raw 文件。
- 如果目标 raw 文件未登记，继续摄取，并在完成后新增 manifest 行。

### 步骤 1：读取源文件

- **如果是 `.md` 文件**：使用读取工具完整读取内容。
- **如果是 `.pdf` 文件**：使用读取工具尝试提取文本。如果无法提取或内容为空，改为记录文件元信息（文件名、页数）在 sources 页面中。
- **如果是 `translated/` 译文**：读取完整译文，并通过 `raw_path` 保持原始来源追溯。

### 步骤 2：提炼核心并翻译

从源文件中提取：
- **核心主旨**：这段资料讲什么（1-2句话）
- **实体**：人物、公司、工具、产品等具体名词
- **概念**：框架、方法论、理论等抽象名词

如果是非中文内容，则翻译成中文。

如果输入已经是 `translated/` 中文译文，不要重复生成全文翻译，只做知识萃取和结构化。

### 步骤 3：创建来源摘要

在 `wiki/sources/` 创建 Markdown 文件：

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

文件名使用 kebab-case：`摘要-{文件slug}.md`

### 步骤 4：知识网络化（实体/概念页面）

对于步骤 2 提取的每个实体和概念：

**目标目录：**
- 实体 → `wiki/entities/`
- 概念 → `wiki/concepts/`

**处理逻辑：**
1. 页面不存在 → 按照 AGENT_GUIDE.md 的 Frontmatter 规范创建新页面
2. 页面已存在 → 读取现有内容，**增量合并**新信息
3. **发现冲突** → **立即暂停**，向用户报告冲突内容，询问处理方式后再继续

**页面模板：**

```markdown
---
title: "页面名称"
type: entity | concept
tags: [标签]
sources: [关联的源文件]
last_updated: YYYY-MM-DD
---

## 定义
[对该实体/概念的定义]

## 关键信息
[从源文件中提取的详细信息]

## 关联连接
- [[摘要-source-slug]] — 来源
- [[RelatedEntity]] — 相关实体
```

### 步骤 5：更新全局注册表

**更新 `wiki/index.md`：**
按照 AGENT_GUIDE.md 规定的格式，将新增页面添加到对应分类下：
- Sources: `[[摘要-source-slug]] — 该资料的核心主旨`
- Entities: `[[EntityName]] — 该实体的身份定义`
- Concepts: `[[ConceptName]] — 该概念的核心定义`

**更新 `wiki/log.md`：**
追加操作日志（Append-only）：
```markdown
## [YYYY-MM-DD] ingest | 操作简述
- **变更**: 新增 [[PageName]]; 更新 [[index.md]]
- **冲突**: 无 (或: 冲突 [[ConflictingPage]], 已暂停等待决策)
```

### 步骤 6：更新 manifest

在确认以下全部完成后，更新 `wiki/_meta/manifest.md`：

- sources 页面已创建或更新
- 实体/概念页面已创建或更新
- index.md 已更新
- log.md 已更新

manifest 行必须记录：

```markdown
| raw_path | status | source_page | output_pages | last_ingested | notes |
```

摄取成功时将 `status` 设为 `ingested`；发现路径不一致时设为 `path_mismatch`；冲突暂停时设为 `conflict_paused`。

**绝对禁止移动、删除、重命名或改写 `raw/` 文件。**

## 冲突处理流程

当发现新旧知识冲突时：

1. **暂停**：停止当前 ingest 流程
2. **报告**：向用户说明冲突内容（哪个页面、冲突点是什么）
3. **询问**：请用户选择处理方式：
   - A) 保留新旧两者，标注为"知识冲突"
   - B) 在保留来源记录/冲突记录的前提下更新主叙述
   - C) 放弃本次 ingest
4. **继续**：根据用户选择继续或终止

## 注意事项

- 所有 wiki 页面必须包含 `## 关联连接` 区域，不能产生孤岛页面
- 使用简体中文编写所有内容
- Source 页面使用 `摘要-{kebab-case-slug}.md`
- Synthesis 页面使用 `{kebab-case-slug}.md`
- Entity 页面使用 `TitleCase.md`
- Concept 页面使用 `TitleCase_With_Underscores.md`
