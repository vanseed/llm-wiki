# Verification

本文件记录下载或修改本项目后建议运行的本地验证命令。

## Python 版本

建议使用 Python 3.10 或更高版本。工具层只使用 Python 标准库。

```powershell
python --version
```

## 单元测试

```powershell
python -B -X utf8 -m unittest tools.test_wiki_tools
```

期望结果：

```text
OK
```

## Wiki 状态

```powershell
python -X utf8 tools/wiki_tools.py status
```

干净模板的期望口径：

```text
wiki 内容页：0
raw 文件：0
translated 译文文件：0
translation 状态：translated 0 / needs_review 0 / pending 0 / skipped 0
manifest 不一致项：0
```

## Manifest 一致性

```powershell
python -X utf8 tools/wiki_tools.py manifest --strict
```

干净模板的期望结果：

```text
问题：无
```

## 图谱文件

```powershell
python -m json.tool wiki/_meta/graph.json
python -c "import xml.etree.ElementTree as ET; ET.parse('wiki/_meta/graph.graphml')"
```

两个命令都应以退出码 `0` 结束。

## Codex 技能校验

如果本机存在 Codex skill creator 的 `quick_validate.py`，可以运行：

```powershell
python -X utf8 C:\Users\leonl\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\ingest
python -X utf8 C:\Users\leonl\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\translate
python -X utf8 C:\Users\leonl\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\query
python -X utf8 C:\Users\leonl\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\lint
python -X utf8 C:\Users\leonl\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\status
```

期望结果均为：

```text
Skill is valid!
```
