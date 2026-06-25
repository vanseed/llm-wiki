---
title: "Wiki Schema"
type: concept
tags: [知识库, schema, agent规范]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# Wiki Schema

## 定义

Wiki Schema 是约束 [[LLM_Agent]] 如何维护 [[LLM_Wiki]] 的规则文档。它定义目录结构、命名约定、页面格式、工作流、权限边界和日志要求，使 LLM 从通用聊天机器人转变为有纪律的 wiki 维护者。

## 典型内容

一个有效的 Wiki Schema 通常包括：

- [[Raw_Source_Layer]] 的只读边界。
- wiki 页面类型、frontmatter 和命名规则。
- [[Ingest_Workflow]]、[[Query_Workflow]] 和 [[Wiki_Lint]] 的操作步骤。
- index 与 log 的维护约定。
- 冲突处理、双向链接和健康检查策略。

## 共同演化

Karpathy 的想法文件强调，schema 不是一次性固定的配置，而是用户与 LLM 在实践中共同演化的协议。随着领域、资料类型和输出需求变化，schema 也应被修订，以保持知识库维护的一致性。

## 关联连接

- [[LLM_Wiki]] — Wiki Schema 服务的知识库模式。
- [[LLM_Agent]] — 需要被 schema 约束的执行主体。
- [[Raw_Source_Layer]] — schema 必须保护的事实层。
- [[Ingest_Workflow]] — schema 中最重要的写入工作流。
- [[Query_Workflow]] — schema 中的问答和综合流程。
- [[Wiki_Lint]] — schema 中的健康检查流程。
- [[摘要-llm-wiki]] — Wiki Schema 概念的来源摘要。