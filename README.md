# LLM Wiki Vault

这是一个基于 [Karpathy 的 LLM Wiki 理念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构建的 Obsidian 知识库模板。它用于把原始资料编译成结构化、可链接、可由 Agent 检索和维护的本地知识网络。

本项目按干净模板思路设计：可从空库开始，也可以放入 1-2 个测试资料，验证完整剪藏、翻译、摄取、检索和健康检查流程。运行演示后，`raw/`、`translated/` 和 `wiki/` 中的内容数量会相应增加。

## 快速开始

1. 安装并打开 Obsidian。
2. 选择 `Open folder as vault`，并选择本项目根目录。
3. 在 Obsidian 中从 `Home.md` 开始浏览。
4. 将原始资料放入 `raw/` 对应子目录。
5. 如果资料是外文且希望先阅读中文全文，执行 `/translate <raw路径>`。
6. 通过 Agent 执行 `/status`、`/ingest <路径>`、`/lint` 和 `/query <问题>`。
7. 阅读 [VERIFY.md](VERIFY.md) 运行本地验证命令。

`raw/` 是不可变事实层。资料放入后，不要通过移动、删除或改写文件表达摄取状态；摄取状态记录在 `wiki/_meta/manifest.md`。
`translated/` 是译文派生层，只保存按需生成的完整简体中文译文；它不是原始事实来源，也不是正式知识页。

## 完整实操演示

本节演示一条完整链路：用 Obsidian Web Clipper 剪藏英文文章，生成中文译文，再编译进正式 wiki，最后查询知识。

### 1. 打开 vault

在 Obsidian 中选择 `Open folder as vault`，打开本项目根目录。打开后建议从 `Home.md` 开始浏览。

### 2. 配置 Web Clipper 模板

在浏览器的 Obsidian Web Clipper 扩展中打开设置，创建一个模板，例如 `LLM Wiki Raw Article`。

模板的目标 vault 选择当前 vault。`Note location` 填：

```text
raw/01-articles
```

不要填写绝对路径，也不要以 `/` 开头。

`Note name` 推荐填：

```text
{{title|safe_name:windows}}
```

正文模板推荐：

```markdown
---
title: "{{title}}"
source: "{{url}}"
author: "{{author}}"
published: "{{published}}"
clipped_at: "{{date}}"
source_language: en
status: raw
---

{{content}}
```

### 3. 剪藏英文文章

打开一篇英文网页文章，使用 Web Clipper 保存到当前 vault。保存后应在 Obsidian 中看到类似文件：

```text
raw/01-articles/example.md
```

`raw/` 是不可变事实层。剪藏完成后，不要通过移动、删除或改写 raw 文件来表达处理状态。

### 4. 查看当前状态

在 Claude Code、Codex 或 Claudian 中，让 Agent 先读取主规范：

```text
请先读取 AGENT_GUIDE.md，然后执行 /status
```

或手动运行：

```powershell
python -X utf8 tools/wiki_tools.py status
```

剪藏后通常会看到 `raw 文件` 数量增加。如果 raw 文件尚未摄取，manifest 状态会显示 `pending`。

### 5. 翻译英文原文

让 Agent 执行：

```text
/translate raw/01-articles/example.md
```

预期产物：

```text
translated/01-articles/example.zh.md
wiki/_meta/translation-manifest.md
wiki/log.md
```

译文页应包含 `## 来源导航`，可以从 Obsidian 中一键跳回原始剪藏：

```markdown
- 原始剪藏：[[raw/01-articles/example|example.md]]
- 原始网页：https://example.com/article
- 机器路径：`raw/01-articles/example.md`
```

如果译文出现 `????` 乱码，说明写入时没有使用 UTF-8。应立即停止后续流程，让 Agent 按 `AGENT_GUIDE.md` 的 UTF-8 规则重写译文。

### 6. 从译文摄取进 wiki

确认译文正常后执行：

```text
/ingest translated/01-articles/example.zh.md
```

预期产物：

```text
wiki/sources/摘要-example.md
wiki/concepts/...
wiki/entities/...
wiki/index.md
wiki/_meta/manifest.md
wiki/log.md
```

即使从 `translated/` 摄取，正式 source 页和 manifest 仍必须追溯到原始 `raw_path`。

### 7. 检查健康状态

执行：

```text
/lint
/status
```

或手动运行：

```powershell
python -X utf8 tools/wiki_tools.py lint --write
python -X utf8 tools/wiki_tools.py status
python -X utf8 tools/wiki_tools.py manifest --strict
```

理想情况下，`manifest 不一致项` 为 0，`translation 状态` 中 `translated` 数量增加，`manifest 状态` 中对应资料变为 `ingested`。

### 8. 查询已编译知识

执行：

```text
/query 这篇文章的核心观点是什么？
```

Agent 应优先检索正式 wiki 页面，并在回答中使用 `[[wikilink]]` 标注来源。高价值回答可以按需保存为 `wiki/syntheses/` 中的 synthesis 页面。

## Agent 兼容策略

本知识库采用“一个主规范 + 多入口兼容”的结构：

- `AGENT_GUIDE.md` — 唯一主规范，定义语言、目录权限、Wiki Schema、工作流和页面格式。
- `CLAUDE.md` — Claude Code 兼容入口，指向 `AGENT_GUIDE.md`。
- `AGENTS.md` — Codex 兼容入口，指向 `AGENT_GUIDE.md`。
- `wiki/_meta/` — Agent 维护的元信息层，记录 manifest、taxonomy、templates、health report 和图谱导出。
- `translated/` — 按需保存外文资料的完整简体中文译文。
- `Home.md` — Obsidian vault 首页。
- `tools/wiki_tools.py` — 本地工具层，自动执行链接扫描、manifest 校验、health 生成和图谱导出。
- `.claude/skills/` — Claude Code 可用的项目技能。
- `.agents/skills/` — Codex 可发现的项目技能。

长期规则应写入 `AGENT_GUIDE.md`，避免在 `CLAUDE.md` 和 `AGENTS.md` 中维护两套重复规范。

## 目录结构

```text
LLM-Wiki-Vault/
├── assets/                   # 统一媒体资源层：图片、PDF、附件
├── raw/                      # 原始资料只读事实层
│   ├── 01-articles/          # 网页、博客、官方文档、教程
│   ├── 02-papers/            # 论文、白皮书、PDF、研究报告
│   ├── 03-transcripts/       # 视频、播客、课程、访谈转录
│   └── 04-notes/             # 个人笔记、会议记录、头脑风暴
├── translated/               # raw 的完整中文译文派生层
│   ├── 01-articles/          # 网页文章译文
│   ├── 02-papers/            # 论文/报告译文
│   ├── 03-transcripts/       # 转录稿译文
│   └── 04-notes/             # 笔记译文
├── wiki/                     # 知识编译输出层
│   ├── _meta/                # Agent 维护元信息：manifest、taxonomy、templates、health
│   │   ├── manifest.md       # raw 到 wiki 页面产出的来源链路
│   │   ├── translation-manifest.md # raw 到 translated 的译文链路
│   │   ├── taxonomy.md       # 类型、状态、标签和命名约定
│   │   ├── health.md         # 最近一次健康检查结果
│   │   ├── graph.json        # 工具导出的知识图谱 JSON
│   │   ├── graph.graphml     # 工具导出的 GraphML 图谱
│   │   ├── dashboard.md      # Obsidian 维护面板
│   │   ├── obsidian.md       # Obsidian 使用约定
│   │   ├── workflows.md      # Obsidian 工作流
│   │   ├── wiki-map.canvas   # Obsidian Canvas 结构地图
│   │   └── templates/        # source/entity/concept/synthesis 页面模板
│   ├── index.md              # 全局内容字典
│   ├── log.md                # 操作日志
│   ├── concepts/             # 概念、框架、方法论
│   ├── entities/             # 人物、公司、工具、产品
│   ├── sources/              # raw 文件的一对一摘要
│   └── syntheses/            # 复杂问题的综合分析
├── tools/
│   ├── wiki_tools.py         # 本地扫描、统计和图谱导出工具
│   ├── test_wiki_tools.py    # 工具层单元测试
│   └── README.md             # 工具命令说明
├── VERIFY.md                 # 本地验证命令
├── Home.md                   # Obsidian vault 首页
├── requirements.txt          # Python 依赖说明
├── AGENT_GUIDE.md            # Claude Code 与 Codex 共用主规范
├── CLAUDE.md                 # Claude Code 入口
├── AGENTS.md                 # Codex 入口
├── .claude/                  # Claude Code 项目技能
└── .agents/                  # Codex 项目技能
```

## 常用 Agent 命令

- `/status` — 快速查看页面数、raw 摄取状态、缺失页面、死链数量、最近操作和下一步建议。
- `/translate <路径>` — 将外文 raw 资料完整翻译成简体中文，写入 `translated/`。
- `/lint` — 检查知识库健康度，并更新 `wiki/_meta/health.md`。
- `/ingest <路径>` — 将新的原始资料或中文译文编译到 `wiki/`。
- `/query <问题>` — 在已编译的 wiki 页面中搜索相关内容，并用 `[[wikilink]]` 标注来源。

## 本地工具命令

工具层使用 Python 标准库，无第三方依赖：

```powershell
python -X utf8 tools/wiki_tools.py status
python -X utf8 tools/wiki_tools.py search "prompt engineering"
python -X utf8 tools/wiki_tools.py lint --write
python -X utf8 tools/wiki_tools.py manifest --strict
python -X utf8 tools/wiki_tools.py graph --output wiki/_meta/graph.json
python -X utf8 tools/wiki_tools.py graph --format graphml --output wiki/_meta/graph.graphml
python -X utf8 tools/wiki_tools.py stats
```

这些工具只列出 `raw/` 与 `translated/` 文件路径，不读取或改写两者的文件内容。子目录中的 `.gitkeep` 仅用于保留空目录，工具不会将其统计为资料。

## 干净模板状态

如果尚未运行上述演示，干净模板的期望状态是：

- wiki 内容页：0
- raw 文件：0
- translated 译文文件：0
- translation 状态：translated 0 / needs_review 0 / pending 0 / skipped 0
- manifest 条目：0
- manifest 不一致项：0

运行以下命令可以检查：

```powershell
python -B -X utf8 -m unittest tools.test_wiki_tools
python -X utf8 tools/wiki_tools.py status
python -X utf8 tools/wiki_tools.py manifest --strict
```

运行完整演示后，这些数字会随剪藏、翻译和摄取而增加。只要 `manifest 不一致项` 为 0，且 `/lint` 没有报告需要处理的结构问题，就说明流程处于健康状态。
