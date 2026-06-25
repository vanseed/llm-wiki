# Claude Code 入口

本知识库采用“一个主规范 + 多入口兼容”的结构。

Claude Code 必须先阅读并遵循根目录的 [`AGENT_GUIDE.md`](AGENT_GUIDE.md)。该文件是本 Obsidian LLM Wiki 的唯一主规范，定义语言、目录权限、Wiki Schema、工作流和页面格式。

Claude Code 专用技能目录位于 `.claude/skills/`：

- `.claude/skills/ingest/` — 将 `raw/` 原始资料编译到 `wiki/`
- `.claude/skills/translate/` — 将 `raw/` 外文资料完整翻译到 `translated/`
- `.claude/skills/query/` — 检索并综合回答本地 Wiki 内容
- `.claude/skills/lint/` — 检查知识库健康状态
- `.claude/skills/status/` — 快速报告页面数、raw 摄取状态、缺失页面和下一步建议

除非用户明确要求，否则不要在本文件中维护重复规则；长期规则应写入 `AGENT_GUIDE.md`。
