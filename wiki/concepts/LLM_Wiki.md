---
title: "LLM Wiki"
type: concept
tags: [知识库, llm, wiki, 方法论]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# LLM Wiki

## 定义

LLM Wiki 是一种由 [[LLM_Agent]] 增量构建和维护的个人或团队知识库模式。它不是在每次提问时临时检索原始文档，而是把来源编译为持久的 markdown 页面、实体页、概念页、摘要页与综合分析页。

## 核心机制

LLM Wiki 的核心机制是把知识处理从“查询时临时拼接”提前到“摄取时结构化编译”。当新资料进入 [[Raw_Source_Layer]] 后，[[Ingest_Workflow]] 会提取要点、创建来源摘要、更新相关概念和实体，并维护交叉引用。之后的 [[Query_Workflow]] 直接在已编译的知识网络上综合回答。

这种模式让知识库成为 [[Persistent_Knowledge_Base]]：交叉引用、矛盾标注、主题综合和历史日志都会保留下来，并随着来源和问题的增加持续增厚。

## 适用场景

- 个人目标、健康、心理和自我提升记录。
- 长期研究项目、论文阅读和主题深挖。
- 阅读书籍时构建角色、主题、情节和世界观页面。
- 团队内部 wiki、会议记录、客户访谈和项目文档维护。
- 竞品分析、尽职调查、旅行规划、课程笔记和兴趣研究。

## 与 RAG 的差异

[[Retrieval_Augmented_Generation]] 主要在查询时从原始资料中检索片段并生成答案；LLM Wiki 则在资料进入时就把知识编译成可持续维护的结构。前者强调即时检索，后者强调长期积累。

## 关联连接

- [[摘要-llm-wiki]] — Karpathy 关于该模式的原始想法摘要。
- [[Persistent_Knowledge_Base]] — LLM Wiki 的目标形态。
- [[Raw_Source_Layer]] — LLM Wiki 的事实来源层。
- [[Wiki_Schema]] — 约束 LLM Wiki 维护方式的规范层。
- [[Ingest_Workflow]] — LLM Wiki 的核心写入流程。
- [[Query_Workflow]] — LLM Wiki 的核心使用流程。
- [[Wiki_Lint]] — LLM Wiki 的健康维护流程。
- [[Obsidian]] — 可作为 LLM Wiki 的浏览与图谱环境。