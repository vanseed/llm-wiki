---
title: "Persistent Knowledge Base"
type: concept
tags: [知识库, 复利, 知识管理]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# Persistent Knowledge Base

## 定义

Persistent Knowledge Base（持久知识库）指一种会长期保留并持续演化的知识资产。它不是把每次问答当成一次性对话，而是把来源摘要、概念关系、实体信息、矛盾记录和综合分析沉淀为可再次使用的 wiki 页面。

## 为什么重要

在普通文件上传或 [[Retrieval_Augmented_Generation]] 流程中，模型常常需要在每次提问时重新检索、重组和综合资料。持久知识库则把这些劳动沉淀下来，使后续问题可以建立在已有结构之上，而不是从零开始。

在 [[LLM_Wiki]] 中，持久性主要体现在：

- 来源被编译为 [[摘要-llm-wiki]] 这样的来源摘要。
- 概念和实体页会在后续摄取时持续更新。
- 矛盾、缺口和新问题会被 [[Wiki_Lint]] 或查询过程显式标出。
- 好的 [[Query_Workflow]] 输出可以回写成新页面。

## 复利效应

“复利”意味着每次摄取和查询都会增加知识库未来可用的结构。交叉引用越多，后续检索和综合越容易；矛盾越早标注，后续判断越可靠；概念页越成熟，新的来源越容易被整合。

## 关联连接

- [[LLM_Wiki]] — 持久知识库的一种 LLM 维护实现。
- [[Ingest_Workflow]] — 负责把新资料变成持久结构。
- [[Query_Workflow]] — 负责复用并扩展已有知识结构。
- [[Wiki_Lint]] — 负责维护持久知识库的健康度。
- [[Raw_Source_Layer]] — 持久知识库背后的事实来源层。