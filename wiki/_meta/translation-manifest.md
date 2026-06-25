# Translation Manifest

本文件记录 `raw/` 原始资料与 `translated/` 中文译文之间的派生链路。`translated/` 是可重建的译文层，不是事实源，也不是正式知识页。

## 状态枚举

- `pending`：raw 文件存在，但尚未生成中文译文。
- `translated`：已生成完整简体中文译文。
- `needs_review`：译文已生成，但需要人工复核术语、结构或关键段落。
- `skipped`：该资料不需要翻译，或用户决定跳过。

## Manifest

| raw_path | translated_path | status | translated_at | notes |
|---|---|---|---|---|
| raw/01-articles/LLM-Wiki.md | translated/01-articles/LLM-Wiki.zh.md | translated | 2026-06-24 | 完整翻译 Karpathy LLM Wiki 想法文件。 |
