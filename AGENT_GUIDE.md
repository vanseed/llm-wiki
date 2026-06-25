# LLM Wiki Agent 主规范

本文件是本 Obsidian 知识库的唯一主规范。Claude Code、Codex 以及其他 AI agent 都必须遵循本文件；工具专属入口文件只负责指向本规范。

# 语言设定与核心角色 (Global Rules)

- **语言指令**：无论输入何种语言，你必须始终使用**简体中文**进行思考、回复和知识库的编写。
- **编码指令**：所有 Markdown、manifest、日志和译文文件必须以 UTF-8 写入。Windows 环境中禁止使用未显式指定 UTF-8 的 `Set-Content`、`Out-File`、`>` 或 `>>` 写入中文内容；优先使用编辑工具、补丁工具，或明确指定 `encoding="utf-8"` 的写入方式。
- **角色定义**：你正在维护一个 **LLM Wiki**（根据 [Karpathy 的规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)），你的任务是将碎片化的信息编译成结构化、高度相互链接的 Obsidian 知识库。

# 核心目录与权限边界 (Immutability & Architecture)

你必须严格遵守以下文件操作权限，这是不可逾越的底线：

- `/raw/` (不可变层 - Immutable)：
  - **绝对只读**。这里存放我的原始素材、网页剪藏和自媒体文案。
  - **禁止修改、删除、重命名或移动此目录下的任何文件**。它是事实的唯一真相来源。
  - 摄取状态不得通过移动文件表达，必须通过 `wiki/_meta/manifest.md` 的 `status` 字段维护。
  - 子目录分类：`01-articles/` 存放网页、博客、官方文档和教程；`02-papers/` 存放论文、白皮书、PDF 和研究报告；`03-transcripts/` 存放视频、播客、课程和访谈转录；`04-notes/` 存放个人笔记、会议记录和头脑风暴。
- `/translated/` (译文派生层 - Derived Translation Layer)：
  - 存放从 `raw/` 派生出的完整简体中文译文，主要服务外文 Web Clipper 文章、论文、转录稿和笔记。
  - 该目录可由 agent 写入和更新，但不得被当作原始事实来源；来源真相仍以 `raw/` 为准。
  - 子目录分类镜像 `raw/`：`01-articles/`、`02-papers/`、`03-transcripts/`、`04-notes/`。
  - 翻译状态记录在 `wiki/_meta/translation-manifest.md`。译文进入正式 wiki 前，必须继续通过 `/ingest` 编译。
- `/assets/` (媒体资产层)：
  - 存放图片、PDF 和媒体。引用时使用 Obsidian 标准语法 `![[文件名称.png]]`。
- `/wiki/` (编译输出层 - You Own This)：
  - 这是你的专属工作区。你需要在此处创建、更新、提炼知识并解决矛盾。
- `/tools/` (工具自动化层)：
  - 存放可重复运行的本地脚本，用于链接扫描、manifest 校验、health 生成和图谱导出。
  - 工具可以读取 `wiki/`，并列出 `raw/` 与 `translated/` 文件路径，但不得读取或改写这两个目录中的文件内容。

# Wiki 核心文件契约 (The Wiki Schema)

当你在 `/wiki/` 中工作时（尤其是执行写入操作后），必须维护以下基石：

1. **`wiki/index.md` (总目录)**：
   每次向 wiki 新增知识页后，必须同步更新此文件，将其按分类加入目录中。
   格式要求：`[[页面名称]] — 一句话描述`。
   - Entity 页面：使用 `TitleCase.md` 命名。
   - Concept 页面：使用 `TitleCase_With_Underscores.md` 命名。
   - Source 页面：使用 `摘要-{kebab-case-slug}.md` 命名。
   - Synthesis 页面：使用 `{kebab-case-slug}.md` 命名。

   范例：

   ```markdown
   # Wiki Index

   ## Sources
   - [[摘要-source-slug]] — 该资料的核心主旨摘要。

   ## Entities
   - [[EntityName]] — 该实体的身份定义或核心功能。

   ## Concepts
   - [[ConceptName]] — 该概念或框架的核心定义。

   ## Syntheses
   - [[synthesis-slug]] — 该页面回答的复杂问题。
   ```

2. **`wiki/log.md` (操作日志)**：
   只能追加写入（Append-only）。每次操作后记录：`## [YYYY-MM-DD] <动作> | <操作简述>`。
   操作类型：`translate`、`ingest`、`query`、`lint`、`sync`。

   范例：

   ```markdown
   ## [2026-04-11] ingest | 引入项目 Claude Code 核心概念
   - **变更**: 新增 [[ClaudeCode]], [[摘要-claude-code-docs]]; 更新 [[index.md]]
   - **冲突**: 无 (或: 冲突 [[RAG架构]], 已标注)

   ## [2026-04-11] query | 解析 Karpathy LLM-Wiki 理念
   - **输出**: 已保存至 [[分析-karpathy-wiki-philosophy]]

   ## [2026-04-11] lint | 周度健康检查
   - **结果**: 修复 2 处死链，发现 1 个孤儿页面 [[UnlinkedPage]]
   ```

3. **内容分类**：
   - `/wiki/concepts/`：存放概念、框架、方法论（如 `Agent_Skill.md`）。
   - `/wiki/entities/`：存放人物、公司、工具、产品（如 `Claude_Code.md`）。
   - `/wiki/sources/`：存放从 `raw/` 提炼出的原始素材摘要。
   - `/wiki/syntheses/`：存放针对复杂问题生成的综合分析。
   - `/wiki/_meta/`：存放维护元信息，包括 manifest、taxonomy、templates 和 health report；它服务 agent 工作流，不作为正式知识页面索引。

4. **强制双向链接**：
   每一个 wiki 页面必须包含 `## 关联连接` 区域，使用 Obsidian 双链 `[[页面名称]]` 链接到其他相关概念。绝不能产生孤岛页面。

5. **矛盾处理原则**：
   如果新摄入的知识与旧知识冲突，不要静默覆盖。在页面中新建 `## 知识冲突` 区块，将两种说法都保留并做对比。

# 工作流指令说明 (Workflows / Skills)

当被要求执行以下操作时，请遵循核心逻辑。Claude Code 的技能位于 `.claude/skills/`，Codex 的技能位于 `.agents/skills/`；两者都必须服从本主规范。涉及来源状态、模板和健康检查时，优先读取 `wiki/_meta/`。

- `/translate <路径>`：读取指定的 `raw/` 文件，将外文内容完整翻译为简体中文，并写入 `translated/` 对应分类目录。必须更新 `wiki/_meta/translation-manifest.md` 和 `wiki/log.md`。禁止移动、删除、重命名或改写 `raw/` 文件。翻译只生成译文，不创建正式知识页。
- `/ingest <路径>`：读取指定的 `raw/` 文件或 `translated/` 译文，将其核心价值提炼并整合到 `wiki/` 目录的相关概念/实体中。若输入是 `translated/`，必须读取译文 frontmatter 的 `raw_path` 并用该 raw 路径维护 `wiki/_meta/manifest.md`；source 页面 frontmatter 的 `sources` 仍记录原始 raw 路径。必须更新 `wiki/index.md`、`wiki/log.md` 和 `wiki/_meta/manifest.md`。禁止移动、删除、重命名或改写 `raw/` 文件。

译文页面必须包含 `## 来源导航`，提供可点击的 Obsidian wikilink 指向原始剪藏，同时保留原始网页 URL 和机器路径。例如：`[[raw/01-articles/example|example.md]]`。frontmatter 的 `raw_path` 和 manifest 表格中的路径仍必须保持纯文本路径，不得改成 wikilink。
- `/query <问题>`：通过读取 `wiki/index.md` 寻找相关文件，进行深度阅读后综合回答，并在回答中必须使用 `[[wikilink]]` 标注引用来源。若 `tools/wiki_tools.py` 存在，可先运行 `python -X utf8 tools/wiki_tools.py search "<问题>"` 辅助定位候选页面；最终回答仍必须深度阅读命中的 wiki 页面。
- `/lint`：全局扫描 `wiki/` 目录，找出孤岛页面（没有双链）、死链（链接不存在的页面）、manifest 不一致以及存在逻辑冲突的地方，并向用户报告。若 `tools/wiki_tools.py` 存在，优先运行 `python -X utf8 tools/wiki_tools.py lint --write` 生成 `wiki/_meta/health.md`。
- `/status`：读取 `wiki/index.md`、`wiki/_meta/manifest.md`、`wiki/_meta/health.md` 和 `wiki/log.md`，快速报告页面数、raw 摄取状态、缺失页面、死链数量和建议下一步动作。若 `tools/wiki_tools.py` 存在，优先运行 `python -X utf8 tools/wiki_tools.py status` 获取结构化摘要。

# 页面 Frontmatter (YAML) 规范

所有生成的 wiki 页面必须包含以下 YAML 头部：

```yaml
---
title: "页面标题"
type: concept | entity | source | synthesis
tags: [知识标签]
sources: [关联的raw文件相对路径]
last_updated: YYYY-MM-DD
---
```

如果页面是从 `translated/` 译文摄取生成，`sources` 仍必须记录译文 frontmatter 中的原始 `raw_path`；译文路径可以写在正文或 manifest notes 中，但不得替代 raw 来源。
