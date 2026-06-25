# Codex 入口

请始终使用简体中文与用户对话、思考并编写知识库内容。

本知识库采用“一个主规范 + 多入口兼容”的结构。Codex 必须先阅读并遵循根目录的 [`AGENT_GUIDE.md`](AGENT_GUIDE.md)。该文件是本 Obsidian LLM Wiki 的唯一主规范，定义语言、目录权限、Wiki Schema、工作流和页面格式。

Codex 仓库级技能目录位于 `.agents/skills/`：

- `.agents/skills/ingest/` — 将 `raw/` 原始资料编译到 `wiki/`
- `.agents/skills/translate/` — 将 `raw/` 外文资料完整翻译到 `translated/`
- `.agents/skills/query/` — 检索并综合回答本地 Wiki 内容
- `.agents/skills/lint/` — 检查知识库健康状态
- `.agents/skills/status/` — 快速报告页面数、raw 摄取状态、缺失页面和下一步建议

Claude Code 兼容入口仍保留在 `CLAUDE.md`，Claude Code 专用技能仍保留在 `.claude/skills/`。两个入口都指向同一份主规范，避免规则漂移。
