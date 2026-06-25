---
name: translate
description: 将 raw/ 中的非中文原始资料完整翻译为简体中文译文，写入 translated/ 对应分类目录。使用场景：用户执行 /translate、要求翻译 Web Clipper 英文文章、或希望先得到中文全文再执行 /ingest。必须保持 raw/ 不变，并更新 wiki/_meta/translation-manifest.md。
---

# translate 技能

## 核心目标

将 `raw/` 中的外文原始资料完整翻译为简体中文，输出到 `translated/` 对应分类目录。执行前先阅读并遵循根目录 `AGENT_GUIDE.md`。

`translate` 只负责翻译，不负责知识萃取：

- 不创建 `wiki/concepts/`、`wiki/entities/`、`wiki/sources/` 或 `wiki/syntheses/` 页面。
- 不更新 `wiki/index.md`。
- 不移动、删除、重命名或改写 `raw/` 文件。
- 翻译完成后更新 `wiki/_meta/translation-manifest.md`，必要时在 `wiki/_meta/manifest.md` 中为原始 raw 文件登记 `pending` 行，并追加 `wiki/log.md`。

## 触发逻辑

1. 用户执行 `/translate <path>`：翻译指定 raw 文件。
2. 用户执行 `/translate`：扫描 `raw/` 路径与 `wiki/_meta/translation-manifest.md`，报告可翻译候选项并询问要处理哪一个。
3. 用户自然语言要求“翻译这篇 Web Clipper 文章”“把英文文章转成中文再入库”：按本流程执行。

## 输出路径

按 raw 分类镜像到 `translated/`：

- `raw/01-articles/example.md` -> `translated/01-articles/example.zh.md`
- `raw/02-papers/example.md` -> `translated/02-papers/example.zh.md`
- `raw/03-transcripts/example.md` -> `translated/03-transcripts/example.zh.md`
- `raw/04-notes/example.md` -> `translated/04-notes/example.zh.md`

如果输出文件已存在，先报告现有路径并询问用户是否覆盖或跳过。

## 翻译格式

译文文件使用以下结构：

```markdown
---
title: "中文标题"
type: translation
raw_path: raw/01-articles/example.md
source_language: en
target_language: zh-CN
translated_at: YYYY-MM-DD
status: translated
---

# 中文标题

## 来源导航

- 原始剪藏：[[raw/01-articles/example|example.md]]
- 原始网页：<如果原文 frontmatter 或正文中存在 URL，则保留；否则写“无”>
- 机器路径：`raw/01-articles/example.md`

## 原始元数据

- 标题：<原始标题>
- 作者：<如有>
- 发布日期：<如有>
- 抓取日期：<如有>
- URL：<如有>

## 完整译文

<完整简体中文译文>

## 译注

- <只记录必要的术语、歧义或无法确认的上下文；没有则写“无”。>
```

## 质量要求

- 使用简体中文完整翻译，不摘要、不改写观点、不主动删减段落。
- 保留原文标题层级、列表、代码块、表格和链接。
- 专有名词首次出现时可保留英文括注，例如“检索增强生成（Retrieval-Augmented Generation, RAG）”。
- 对明显的广告、导航、Cookie 提示等网页噪声，可在 `## 译注` 中说明并省略。
- 无法确定的术语不要硬译，在译注中标注。
- `## 来源导航` 必须同时包含 Obsidian 可点击的原始剪藏 wikilink、原始网页 URL 和机器路径。Markdown 原始文件的 wikilink 目标去掉 `.md` 后缀，例如 `[[raw/01-articles/example|example.md]]`；PDF 等非 Markdown 文件可保留扩展名，例如 `[[raw/02-papers/paper.pdf|paper.pdf]]`。
- `raw_path` frontmatter 和 manifest 中的路径必须保持纯文本路径，不要改成 wikilink。

## UTF-8 写入要求

- 译文、`wiki/_meta/translation-manifest.md` 和 `wiki/log.md` 必须以 UTF-8 写入。
- 在 Windows/PowerShell 环境中，禁止用未指定编码的 `Set-Content`、`Out-File`、`>` 或 `>>` 写入中文内容；这些路径可能把中文替换成 `?`。
- 优先使用编辑工具直接写入 Markdown。若必须通过脚本写入，必须使用 `Path.write_text(text, encoding="utf-8", newline="\n")`。
- 写入后必须抽查译文：正文应包含大量中文字符，不应出现整段 `????`。如果出现，立即停止并重写译文，不要继续更新摄取流程。

## Manifest 更新

翻译成功后，在 `wiki/_meta/translation-manifest.md` 中新增或更新一行：

```markdown
| raw_path | translated_path | status | translated_at | notes |
```

- 成功翻译：`status` 设为 `translated`。
- 需要人工复核：`status` 设为 `needs_review`。
- 用户决定不翻译：`status` 设为 `skipped`。

同时检查 `wiki/_meta/manifest.md`：

- 如果该 `raw_path` 尚未登记，新增 `pending` 行。
- `notes` 可写：`已翻译至 translated/...，尚未摄取`。
- 不要创建 source 页面，不要把状态设为 `ingested`，除非随后完成 `/ingest`。

## 写入后校验

翻译完成后运行等价检查：

```powershell
python -B -X utf8 -c "from pathlib import Path; t=Path('translated/01-articles/example.zh.md').read_text(encoding='utf-8'); print(sum('\u4e00' <= c <= '\u9fff' for c in t), t.count('?'))"
```

中文译文的中文字符数应明显大于 0；如果问号数量异常高，检查是否发生编码替换。

## 后续摄取

如果用户希望把译文编译进正式知识库，提示下一步执行：

```text
/ingest translated/01-articles/example.zh.md
```
