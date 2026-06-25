---
title: "Raw Source Layer"
type: concept
tags: [知识库, 来源, 架构]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# Raw Source Layer

## 定义

Raw Source Layer（原始来源层）是 [[LLM_Wiki]] 架构中的不可变事实层，保存文章、论文、图片、数据文件、剪藏和转录稿等原始资料。LLM 可以读取这些资料，但不应移动、删除、重命名或改写它们。

## 作用

原始来源层确保知识库拥有可追溯的事实基础。wiki 页面可以被修订、合并和重构，但它们的来源必须能回到原始文件。这样，当后续发现解释错误、摘要过度简化或观点冲突时，[[LLM_Agent]] 和用户都能回到事实源重新判断。

## 与 wiki 输出层的关系

[[Ingest_Workflow]] 会从原始来源层读取资料，并把其中的核心价值编译进 wiki 输出层。输出层可以包含来源摘要、实体页、概念页和综合分析，但这些页面不是原始事实本身，而是基于 raw 文件生成的结构化知识。

## 关联连接

- [[LLM_Wiki]] — 使用原始来源层作为事实根基。
- [[Ingest_Workflow]] — 从原始来源层读取并编译知识。
- [[Wiki_Schema]] — 规定 raw 文件的只读边界和目录约定。
- [[Persistent_Knowledge_Base]] — 在原始来源层之上形成的知识资产。
- [[摘要-llm-wiki]] — 描述三层架构的来源摘要。