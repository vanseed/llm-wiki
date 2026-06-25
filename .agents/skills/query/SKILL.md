---
name: query
description: 在本地 Wiki 知识库中回答用户提问。使用场景：用户执行 /query，或询问“我的笔记/历史决定/过往笔记/知识库”中的内容。必须先读取 wiki/index.md 定位相关页面，再深度阅读并用 [[wikilink]] 标注来源；禁止凭模型记忆回答本地知识库问题。
---

# query 技能

## 核心目标

把用户问题转化为对本地 Wiki 的深度检索，综合出带有明确 `[[wikilink]]` 来源的回答。执行本技能前先遵循根目录 `AGENT_GUIDE.md`。

## 触发场景

- 用户输入 `/query <问题>`。
- 用户询问“我的笔记里关于 X 是怎么说的”“过去我对 Y 的决策是什么”“查询 Z 相关知识”。
- 用户提及本地 wiki、知识库、笔记、记录等关键词。

## 降级策略

如果问题属于纯通用知识，且 `wiki/index.md` 中无相关内容，必须声明：

> 本地知识库中未找到相关内容，以下为通用知识回答：

然后再给出通用回答。

## 检索与综合流水线

### 1. 查阅全局索引

永远先读取 `wiki/index.md`，定位与问题相关的：

- Sources
- Entities
- Concepts
- Syntheses

如果 `tools/wiki_tools.py` 存在，可先运行：

```powershell
python -X utf8 tools\wiki_tools.py search "<问题>"
```

该工具只搜索正式 wiki 知识页，不读取 raw 或 translated 文件内容。工具结果只用于辅助定位候选页面，最终回答仍必须深度阅读命中的 wiki 页面，并以 `[[wikilink]]` 标注来源。

### 2. 深度阅读目标文件

选取最相关页面，完整读取内容。必要时继续读取被双链引用的关键页面。

### 2.5 来源追溯

当回答需要说明资料出处、source 页面对应 raw 文件、translated 译文文件、或 synthesis 的来源链路时，读取 `wiki/_meta/manifest.md` 和 `wiki/_meta/translation-manifest.md`。不要读取 raw 或 translated 文件内容，除非用户明确要求重新摄取、核对原文或查看译文。

### 3. 综合与回答

综合信息后回答用户问题。

双链引用规范：

- 每当引用某个 Wiki 页面的信息，使用 `[[页面名称]]` 标注。
- 整段引用同一页面时，段落首尾各引用一次即可。
- 引用特定原文时，使用 Markdown 块引用。

### 4. 高价值内容固化

如果回答超过 2 个段落，或具有分析对比/总结价值，主动询问用户是否保存为 synthesis：

> 这是一个有价值的总结，是否需要我将其保存到 `wiki/syntheses/` 目录？

用户同意后，按照 `AGENT_GUIDE.md` 规范创建 synthesis 页面，并在 `wiki/index.md` 的 Syntheses 分类下注册。

### 5. 记录操作日志

无论是否生成 synthesis 页面，查询结束后必须在 `wiki/log.md` 末尾追加：

如果本次回答保存为 synthesis，并且引用了多个 source 页面，在 `wiki/_meta/manifest.md` 的相关 source 行 notes 中记录该 synthesis 页面，或在 synthesis 页面 frontmatter 的 `sources` 中列出引用来源。

```markdown
## [YYYY-MM-DD] query | <操作简述>
- **输出**: <引用页面列表或"即时回答未保存">
```

## 强制约束

- 禁止凭记忆回答本地知识库问题。
- 禁止过度引用，同一页面的信息在段落首尾引用一次即可。
- 知识库无相关内容时必须明确声明。

## 关联连接

- [[wiki/index.md]] — 全局索引入口
- [[wiki/log.md]] — 操作日志
- [[AGENT_GUIDE.md]] — Wiki 架构主规范
