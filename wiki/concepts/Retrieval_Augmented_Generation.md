---
title: "Retrieval Augmented Generation"
type: concept
tags: [llm, rag, 检索]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# Retrieval Augmented Generation

## 定义

Retrieval Augmented Generation（检索增强生成，RAG）是一种让 LLM 在回答问题时先检索相关资料片段，再基于这些片段生成答案的范式。Karpathy 的 LLM Wiki 想法文件把它作为对比对象，用来说明传统文件问答缺少长期知识积累。

## 在本文中的问题定位

RAG 可以解决“从大量文档中找相关内容”的问题，但在普通用法中，它常常让模型每次提问都重新发现、筛选和综合知识。对于需要跨多份文档形成长期理解的问题，这种方式容易重复劳动，也难以保留前一次综合出的结构。

## 与 LLM Wiki 的关系

[[LLM_Wiki]] 并不否定检索，而是把关键差异放在“是否形成持久中间层”上。RAG 更像查询时的即时检索；LLM Wiki 则通过 [[Ingest_Workflow]] 将来源编译为 [[Persistent_Knowledge_Base]]，再由 [[Query_Workflow]] 复用这个结构。

## 关联连接

- [[LLM_Wiki]] — 与 RAG 形成对比的持久 wiki 模式。
- [[Persistent_Knowledge_Base]] — LLM Wiki 相比普通 RAG 增加的长期资产层。
- [[Ingest_Workflow]] — 把知识提前编译，而不是查询时才临时拼接。
- [[Query_Workflow]] — 在已编译 wiki 上进行综合回答。
- [[摘要-llm-wiki]] — 本概念在当前知识库中的来源摘要。