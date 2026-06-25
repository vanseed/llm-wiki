# Wiki Taxonomy

本文件定义本 LLM Wiki 的页面类型、状态、命名规则和常用标签。生成或更新 wiki 页面时，优先遵循 `AGENT_GUIDE.md`，再参考本文件。

## 页面类型

| type | 目录 | 用途 |
|---|---|---|
| `source` | `wiki/sources/` | 从单个 raw 文件提炼的一对一来源摘要 |
| `entity` | `wiki/entities/` | 人物、公司、工具、产品、模型等具体实体 |
| `concept` | `wiki/concepts/` | 框架、方法论、理论、技术模式等抽象概念 |
| `synthesis` | `wiki/syntheses/` | 面向复杂问题的综合分析和答案 |

`translated/` 中的 `type: translation` 只表示译文派生产物，不属于正式 wiki 页面类型，也不参与 `wiki/index.md`。

## Manifest 状态

| status | 含义 | 处理方式 |
|---|---|---|
| `pending` | raw 文件尚未摄取 | `/ingest` 优先处理 |
| `ingested` | raw 文件已形成 wiki 输出 | 后续只做增量维护 |
| `path_mismatch` | source 记录路径与真实路径不一致 | 由 `/lint` 报告，人工确认后修正 |
| `conflict_paused` | 摄取时发现知识冲突 | 等待用户决策 |

## Translation Manifest 状态

| status | 含义 | 处理方式 |
|---|---|---|
| `pending` | raw 文件尚未生成译文 | 按需执行 `/translate` |
| `translated` | 已生成完整简体中文译文 | 可执行 `/ingest translated/...` |
| `needs_review` | 译文需要人工复核 | 复核后更新 manifest |
| `skipped` | 不需要翻译或决定跳过 | 保留记录即可 |

## 命名规则

- source 页面：`摘要-{kebab-case-slug}.md`
- synthesis 页面：`{kebab-case-slug}.md`
- entity 页面：`TitleCase.md`
- concept 页面：`TitleCase_With_Underscores.md`
- translation 文件：沿用 raw 文件名并追加 `.zh.md`

## 常用标签

- `提示工程`
- `上下文工程`
- `提示框架`
- `提示技术`
- `模型`
- `组织`
- `来源`
- `综合分析`
- `知识冲突`
