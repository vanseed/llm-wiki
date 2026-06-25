---
title: "OpenAI Codex"
type: entity
tags: [工具, agent, openai]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# OpenAI Codex

## 定义

OpenAI Codex 是 [[摘要-llm-wiki]] 中列举的 LLM agent 环境之一，可作为接收想法文件、遵循 [[Wiki_Schema]] 并维护 [[LLM_Wiki]] 的执行工具。

## 在 LLM Wiki 中的角色

在该模式下，OpenAI Codex 不是单纯回答问题的聊天界面，而是可以在本地 vault 中读取、创建和更新 markdown 文件的 [[LLM_Agent]]。它需要遵守 raw 只读、wiki 可写、manifest 登记和日志追加等维护约束。

## 关联连接

- [[LLM_Agent]] — OpenAI Codex 可承担的角色。
- [[LLM_Wiki]] — OpenAI Codex 可维护的知识库模式。
- [[Wiki_Schema]] — OpenAI Codex 需要遵循的行为规范。
- [[Ingest_Workflow]] — OpenAI Codex 可执行的摄取流程。
- [[Claude_Code]] — 另一个被文中列举的 agent 环境。
- [[摘要-llm-wiki]] — OpenAI Codex 被提及的来源摘要。