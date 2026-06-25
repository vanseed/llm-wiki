# Obsidian 工作流

本页说明在 Obsidian 中维护这个 LLM Wiki 的推荐节奏。

## 1. 收集资料

将资料放入 `raw/` 的对应子目录：

- `raw/01-articles/` — 网页、博客、官方文档和教程。
- `raw/02-papers/` — 论文、白皮书、PDF 和研究报告。
- `raw/03-transcripts/` — 视频、播客、课程和访谈转录。
- `raw/04-notes/` — 个人笔记、会议记录和头脑风暴。

`raw/` 是不可变事实层。放入后不要通过移动、删除或改写文件表达处理状态。

## 2. 可选：翻译外文资料

如果资料来自 Obsidian Web Clipper，且正文主要是英文或其他外文，可以先生成完整中文译文：

```text
/translate raw/01-articles/example.md
```

译文会写入：

```text
translated/01-articles/example.zh.md
```

翻译完成后应更新：

- `translated/`
- `wiki/_meta/translation-manifest.md`
- `wiki/log.md`

`translated/` 是派生译文层，不是原始事实来源，也不是正式知识页。

## 3. 查看状态

在 Agent 中执行：

```text
/status
```

或手动运行：

```powershell
python -X utf8 tools/wiki_tools.py status
```

## 4. 摄取资料

选择一个 raw 文件或 translated 译文，让 Agent 执行：

```text
/ingest raw/01-articles/example.md
```

或：

```text
/ingest translated/01-articles/example.zh.md
```

如果从 `translated/` 摄取，source 页面仍必须追溯到译文 frontmatter 中记录的原始 `raw_path`。

摄取完成后应更新：

- `wiki/sources/`
- `wiki/entities/`
- `wiki/concepts/`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/_meta/manifest.md`

## 5. 检查健康

执行：

```text
/lint
```

或手动运行：

```powershell
python -X utf8 tools/wiki_tools.py lint --write
```

结果写入 [[health]]。

## 6. 查询知识

当资料已经编译到 `wiki/` 后，执行：

```text
/query <问题>
```

Agent 会优先使用本地搜索定位候选页面，再阅读正式 wiki 页面并回答。

## 7. 导出图谱

```powershell
python -X utf8 tools/wiki_tools.py graph --output wiki/_meta/graph.json
python -X utf8 tools/wiki_tools.py graph --format graphml --output wiki/_meta/graph.graphml
```

`graph.graphml` 可用于 Gephi、yEd 等图谱工具。
