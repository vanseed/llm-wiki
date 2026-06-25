# Wiki Tools

`wiki_tools.py` 是本地 LLM Wiki 的零依赖工具层。它负责机械化检查和导出，让 Agent 少做手工统计。

工具只读取 `wiki/` 内容，并列出 `raw/` 与 `translated/` 文件路径；不会读取或改写这两个目录中的文件内容。子目录中的 `.gitkeep` 会被忽略。

## 命令

### status

```powershell
python -X utf8 tools/wiki_tools.py status
```

输出 wiki 内容页、raw 文件、translated 译文文件、translation 状态、manifest 状态、死链数量和最近操作。

### lint

```powershell
python -X utf8 tools/wiki_tools.py lint --write
```

重新生成 `wiki/_meta/health.md`。

### manifest

```powershell
python -X utf8 tools/wiki_tools.py manifest
python -X utf8 tools/wiki_tools.py manifest --strict
python -X utf8 tools/wiki_tools.py manifest --format markdown
```

检查 `raw/`、`wiki/_meta/manifest.md` 和 source 页面之间的一致性。`--strict` 会在发现问题时返回非零退出码。

### search

```powershell
python -X utf8 tools/wiki_tools.py search "prompt engineering"
python -X utf8 tools/wiki_tools.py search "prompt engineering" --format json
```

搜索正式 wiki 知识页，不搜索 `raw/` 或 `translated/` 内容。结果只用于辅助定位页面，最终回答仍应读取 wiki 页面本身。

### graph

```powershell
python -X utf8 tools/wiki_tools.py graph --output wiki/_meta/graph.json
python -X utf8 tools/wiki_tools.py graph --format graphml --output wiki/_meta/graph.graphml
```

导出知识图谱 JSON 或 GraphML。

### stats

```powershell
python -X utf8 tools/wiki_tools.py stats
```

输出机器可读统计数据，包含 `content_pages`、`raw_files`、`translated_files` 和 `translation_statuses`，适合后续接 dashboard 或 CI。

## 测试

```powershell
python -B -X utf8 -m unittest tools.test_wiki_tools
```
