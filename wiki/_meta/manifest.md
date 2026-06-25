# Source Manifest

本文件记录 `raw/` 原始资料与 `wiki/` 编译页面之间的来源链路。`raw/` 文件不通过移动、删除或改写来表示状态；摄取状态只在本 manifest 中维护。

## 状态枚举

- `pending`：raw 文件存在，但尚未形成 source 页面。
- `ingested`：raw 文件已有对应 source 页面和知识页产出。
- `path_mismatch`：source frontmatter 中记录的 raw 路径与当前真实路径不一致。
- `conflict_paused`：摄取过程中发现知识冲突，等待用户决策。

## Manifest

| raw_path | status | source_page | output_pages | last_ingested | notes |
|---|---|---|---|---|---|
| raw/01-articles/LLM-Wiki.md | ingested | [[摘要-llm-wiki]] | [[LLM_Wiki]]; [[Persistent_Knowledge_Base]]; [[Raw_Source_Layer]]; [[Wiki_Schema]]; [[Ingest_Workflow]]; [[Query_Workflow]]; [[Wiki_Lint]]; [[Retrieval_Augmented_Generation]]; [[Obsidian]]; [[LLM_Agent]]; [[OpenAI_Codex]]; [[Claude_Code]]; [[Andrej_Karpathy]] | 2026-06-24 | 从 `translated/01-articles/LLM-Wiki.zh.md` 摄取；原始来源保持不变。 |