---
title: "摘要-llm-wiki"
type: source
tags: [来源, llm-wiki, 知识库]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# 摘要-llm-wiki

## 核心摘要

Karpathy 的 LLM Wiki 模式主张：不要只在查询时对原始文档做 RAG 检索，而应让 [[LLM_Agent]] 增量构建并维护一个持久的 [[LLM_Wiki]]。这个 wiki 位于原始资料和用户提问之间，把来源一次性编译成结构化、相互链接、可持续更新的知识网络。

该模式的核心价值在于让知识产生复利：交叉引用、矛盾标注、主题综合和实体页面不会在每次查询时从零重建，而是沉淀在 [[Persistent_Knowledge_Base]] 中持续演化。[[Obsidian]] 被定位为阅读、浏览和图谱化这个知识库的 IDE，而 LLM agent 则承担摘要、归档、链接维护和一致性管理等繁重工作。

原文还给出三层架构：不可变的 [[Raw_Source_Layer]]、由 LLM 维护的 wiki 输出层，以及约束 agent 行为的 [[Wiki_Schema]]。操作层面则包含 [[Ingest_Workflow]]、[[Query_Workflow]] 与 [[Wiki_Lint]]，共同支撑一个可长期维护的个人或团队知识库。

原始资料：`raw/01-articles/LLM-Wiki.md`
中文译文：`translated/01-articles/LLM-Wiki.zh.md`
原始链接：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## 关键摘录式要点

- [[Retrieval_Augmented_Generation]] 在查询时临时拼接知识，但缺少持续积累；LLM Wiki 则把知识编译成持久资产。
- [[LLM_Wiki]] 的维护成本由 LLM 承担，人类主要负责筛选来源、提出问题和判断重点。
- [[Wiki_Schema]] 是关键配置层，它把通用聊天机器人约束成有纪律的知识库维护者。
- 好的查询结果不应消失在聊天历史中，而应回写为新的 wiki 页面，让探索本身也复利增长。
- 定期 [[Wiki_Lint]] 可以发现矛盾、孤岛页面、缺失概念和可继续探索的数据空白。

## 关联连接

- [[LLM_Wiki]] — 本文提出的核心模式。
- [[Persistent_Knowledge_Base]] — 该模式追求的复利式知识资产。
- [[Raw_Source_Layer]] — LLM Wiki 的不可变事实层。
- [[Wiki_Schema]] — 约束 LLM 维护 wiki 的配置规范。
- [[Ingest_Workflow]] — 将来源编译进 wiki 的操作流程。
- [[Query_Workflow]] — 基于 wiki 综合回答并回写成果的流程。
- [[Wiki_Lint]] — 保持 wiki 健康的检查流程。
- [[Retrieval_Augmented_Generation]] — 被本文对比的传统检索式范式。
- [[Obsidian]] — 作为 wiki 浏览、编辑和图谱视图的环境。
- [[LLM_Agent]] — 执行摘要、交叉引用和维护工作的主体。
- [[OpenAI_Codex]] — 文中举例的 LLM agent 环境之一。
- [[Claude_Code]] — 文中举例的 LLM agent 环境之一。
- [[Andrej_Karpathy]] — 原始想法文件作者。
