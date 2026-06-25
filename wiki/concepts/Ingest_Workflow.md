---
title: "Ingest Workflow"
type: concept
tags: [知识库, ingest, 工作流]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# Ingest Workflow

## 定义

Ingest Workflow（摄取流程）是把新来源从 [[Raw_Source_Layer]] 编译进 [[LLM_Wiki]] 的过程。它不是简单存档或索引，而是一次结构化整合：阅读来源、提取要点、创建摘要、更新概念与实体，并记录操作日志。

## 典型步骤

1. 用户把新资料放入 raw 集合，并要求 [[LLM_Agent]] 处理。
2. LLM 阅读来源并提炼核心主旨、实体、概念和潜在冲突。
3. LLM 创建来源摘要，例如 [[摘要-llm-wiki]]。
4. LLM 更新相关概念页和实体页，如 [[LLM_Wiki]]、[[Wiki_Schema]]、[[Obsidian]]。
5. LLM 更新 index、log 和 manifest 等全局登记文件。

## 设计原则

摄取流程的目标是让知识“编译一次，持续复用”。单个来源可能触及多个 wiki 页面，因此摄取应重视交叉引用、冲突标注和已有页面的增量合并，而不是只生成孤立摘要。

## 关联连接

- [[LLM_Wiki]] — 摄取流程维护的目标知识库。
- [[Raw_Source_Layer]] — 摄取流程读取的事实来源。
- [[Persistent_Knowledge_Base]] — 摄取流程沉淀出的长期资产。
- [[Query_Workflow]] — 复用摄取成果进行回答的流程。
- [[Wiki_Lint]] — 检查摄取后结构健康的流程。
- [[LLM_Agent]] — 执行摄取维护工作的主体。