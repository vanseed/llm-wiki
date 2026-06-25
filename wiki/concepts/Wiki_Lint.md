---
title: "Wiki Lint"
type: concept
tags: [知识库, lint, 健康检查]
sources: [raw/01-articles/LLM-Wiki.md]
last_updated: 2026-06-24
---

# Wiki Lint

## 定义

Wiki Lint 是对 [[LLM_Wiki]] 做周期性健康检查的流程。它用于发现结构问题、知识冲突、过时主张、孤岛页面、缺失链接和需要继续研究的数据空白。

## 检查对象

典型检查包括：

- 页面之间是否存在矛盾或过时说法。
- 是否有没有入链或出链的孤岛页面。
- 是否有重要概念被反复提到却没有独立页面。
- 是否缺少关键交叉引用。
- 是否存在需要补充来源或网络搜索的数据缺口。

## 在 LLM Wiki 中的作用

随着 [[Ingest_Workflow]] 和 [[Query_Workflow]] 不断增加页面，知识库可能变得复杂。Wiki Lint 负责把维护成本继续交给 [[LLM_Agent]]，让 [[Persistent_Knowledge_Base]] 保持可导航、可追溯和一致。

## 关联连接

- [[LLM_Wiki]] — Wiki Lint 检查的目标系统。
- [[Persistent_Knowledge_Base]] — Wiki Lint 保持其长期健康。
- [[Ingest_Workflow]] — 摄取后可能触发健康检查。
- [[Query_Workflow]] — 查询中发现的问题可转化为 lint 线索。
- [[Wiki_Schema]] — 定义健康标准和检查口径。
- [[摘要-llm-wiki]] — Wiki Lint 思想的来源摘要。