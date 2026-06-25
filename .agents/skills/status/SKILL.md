---
name: status
description: 快速报告本地 LLM Wiki 状态。使用场景：用户执行 /status、/stats，或询问“知识库现在怎么样”“还有哪些待处理”“当前健康状态”。读取 wiki/index.md、wiki/_meta/manifest.md、wiki/_meta/translation-manifest.md、wiki/_meta/health.md 和 wiki/log.md，输出页面数、raw 摄取状态、translated 译文数量、缺失页面、死链数量、最近操作和下一步建议；默认不修改任何文件。
---

# status 技能

## 核心目标

提供本地 LLM Wiki 的快速状态摘要。执行本技能前先遵循根目录 `AGENT_GUIDE.md`。

## 工具优先

如果 `tools/wiki_tools.py` 存在，优先运行：

```powershell
python -X utf8 tools\wiki_tools.py status
```

该工具只读取 `wiki/` 元信息并列出 `raw/` 与 `translated/` 文件路径，不读取两者文件内容，不修改任何文件。工具不可用时，再按下面的读取范围手动汇总。

## 读取范围

- `wiki/index.md` — 统计注册页面和已注册但未创建页面。
- `wiki/_meta/manifest.md` — 统计 raw 文件摄取状态。
- `wiki/_meta/translation-manifest.md` — 统计译文状态。
- `wiki/_meta/health.md` — 读取最近一次健康检查结果。
- `wiki/log.md` — 提取最近一次操作。

默认不读取 raw 或 translated 文件内容，不修改任何文件。

## 输出格式

```markdown
## Wiki Status — YYYY-MM-DD

### 摘要
- wiki 内容页：N 个
- raw 文件：N 个
- translated 译文文件：N 个
- translation 状态：translated N / needs_review N / pending N / skipped N
- manifest 状态：ingested N / pending N / path_mismatch N / conflict_paused N
- 已注册但未创建页面：N 个
- 最近一次操作：YYYY-MM-DD action | 摘要

### 需要关注
- [从 health.md 或 manifest 中提取的关键问题]

### 建议下一步
1. [最高优先级动作]
2. [次优先级动作]
```

## 约束

- 只读报告，不自动修复。
- 如果 `wiki/_meta/manifest.md` 或 `wiki/_meta/health.md` 不存在，报告缺失文件并建议先运行 `/lint` 或执行结构化增强初始化。
- 不把 `wiki/log.md` 的历史双链计入死链统计。
- `wiki/_meta/templates/` 不作为正式知识页参与页面数、缺失页或死链统计。
