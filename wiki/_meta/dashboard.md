# Wiki Dashboard

本页是 Obsidian 内的维护面板。它不依赖 Dataview 或其他插件；需要刷新状态时，运行本地工具命令并查看生成的元信息文件。

## 状态摘要

- wiki 内容页：0
- raw 文件：0
- translated 译文文件：0
- translation 状态：translated 0 / needs_review 0 / pending 0 / skipped 0
- manifest 条目：0
- manifest 不一致项：0
- 最近健康报告：[[health]]

## 维护入口

- [[manifest]] — raw 与 wiki 产出的来源链路。
- [[translation-manifest]] — raw 与 translated 的译文链路。
- [[taxonomy]] — 页面类型、状态、标签和命名约定。
- [[health]] — 最近一次健康检查报告。
- [[obsidian]] — Obsidian 使用约定。
- [[workflows]] — Obsidian 工作流。
- [[wiki-map.canvas|Wiki Map Canvas]]
- [[templates/source|source 模板]]
- [[templates/entity|entity 模板]]
- [[templates/concept|concept 模板]]
- [[templates/synthesis|synthesis 模板]]

## 常用命令

```powershell
python -X utf8 tools/wiki_tools.py status
python -X utf8 tools/wiki_tools.py lint --write
python -X utf8 tools/wiki_tools.py manifest --strict
python -X utf8 tools/wiki_tools.py graph --output wiki/_meta/graph.json
python -X utf8 tools/wiki_tools.py graph --format graphml --output wiki/_meta/graph.graphml
```

## Agent 工作流

- `/status` — 查看当前状态。
- `/translate <路径>` — 将外文 raw 资料翻译到 translated。
- `/ingest <路径>` — 摄取 raw 资料或 translated 译文到 wiki。
- `/lint` — 更新健康报告。
- `/query <问题>` — 查询已编译的 wiki 内容。

## 下一步

当前库为空。建议在功能优化完成后，放入 1-2 个 raw 测试资料，完整验证 translate、ingest、lint、query 和 graph export 流程。
