---
title: "Query Workflow"
type: concept
tags: [知识库, query, 工作流]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# Query Workflow

## 定义

Query Workflow（查询流程）是在 [[LLM_Wiki]] 中定位相关页面、深度阅读并综合回答的过程。它与一次性聊天不同：回答可以引用已有页面，也可以在有价值时回写为新的 wiki 页面。

## 核心思想

在 LLM Wiki 模式下，查询不是只从原始资料临时拼接答案。[[LLM_Agent]] 应先利用 index 或搜索工具定位相关页面，再阅读来源摘要、概念页和实体页，最后生成带引用的综合回答。这样，回答建立在 [[Persistent_Knowledge_Base]] 的已有结构上。

## 回写价值

Karpathy 特别强调：好的答案不应消失在聊天历史中。比较表、分析、发现的新联系或阶段性结论，都可以通过后续操作归档为综合页面，让探索过程本身继续复利增长。

## 关联连接

- [[LLM_Wiki]] — 查询流程运行的知识网络。
- [[Persistent_Knowledge_Base]] — 查询流程复用的已有结构。
- [[Ingest_Workflow]] — 查询流程依赖的前置编译过程。
- [[Wiki_Lint]] — 查询中发现的问题可反馈给健康检查。
- [[Retrieval_Augmented_Generation]] — 与查询时临时检索形成对比的范式。
- [[摘要-llm-wiki]] — 查询流程思想的来源摘要。