---
title: "LLM Agent"
type: entity
tags: [agent, llm, 知识库]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# LLM Agent

## 定义

LLM Agent 是在 [[LLM_Wiki]] 模式中实际维护知识库的执行主体。它读取来源、编写页面、维护交叉引用、更新日志和索引，并根据 [[Wiki_Schema]] 遵守目录、格式与权限规则。

## 职责边界

在 Karpathy 的设想中，人类负责筛选来源、提出问题、判断重点和引导探索；LLM Agent 负责其余繁重维护工作，包括摘要、归档、链接、合并、冲突提示和一致性管理。

## 示例环境

原文提到的 LLM agent 环境包括 [[OpenAI_Codex]]、[[Claude_Code]]、OpenCode / Pi 等。不同工具可以采用不同入口文件，但核心是都需要被 [[Wiki_Schema]] 约束成稳定的 wiki 维护者。

## 关联连接

- [[LLM_Wiki]] — LLM Agent 维护的目标知识库。
- [[Wiki_Schema]] — 约束 LLM Agent 行为的规范层。
- [[Ingest_Workflow]] — LLM Agent 的核心写入职责。
- [[Query_Workflow]] — LLM Agent 的核心回答职责。
- [[Wiki_Lint]] — LLM Agent 的健康检查职责。
- [[Obsidian]] — 用户查看 LLM Agent 输出的常用环境。
- [[摘要-llm-wiki]] — LLM Agent 角色的来源摘要。