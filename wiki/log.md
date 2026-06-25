# Wiki 操作日志

---

## [2026-04-12] ingest | 批量摄入提示工程核心资料

### 处理文件清单

**Articles（5 篇）：**
- `raw/01-articles/提示设计策略  _  Gemini API.md` — Google Gemini 中文指南
- `raw/01-articles/Prompt Engineering in 2025_ Complete Guide for ChatGPT, Claude, and Gemini.md` — PromptBuilder 指南
- `raw/01-articles/The Complete Guide to AI Prompt Engineering in 2025-2026.md` — Espo.ai 指南
- `raw/01-articles/The Complete Prompt Engineering Guide (2025).md` — BrilliantPrompts 指南
- `raw/01-articles/Prompting best practices-Anthropic.md` — Anthropic 官方最佳实践

**Papers（2 篇）：**
- `raw/02-papers/Goolge-Prompt-Engineering-whitepaper.pdf` — Google 官方白皮书（65 页）
- `raw/02-papers/5C Prompt Contracts .pdf` — 5C 提示契约研究论文

### 创建的来源摘要（7 个）

| 文件 | 描述 |
|------|------|
| [[摘要-gemini-api-prompting-strategies]] | Gemini API 提示设计策略 |
| [[摘要-prompt-engineering-2025-guide-promptbuilder]] | Prompt Engineering 2025 完整指南 |
| [[摘要-ai-prompt-engineering-2025-2026-espo]] | AI 提示工程 2025-2026 指南 |
| [[摘要-complete-prompt-engineering-guide-2025]] | 完整提示工程指南 2025 |
| [[摘要-anthropic-prompting-best-practices]] | Anthropic 提示最佳实践 |
| [[摘要-google-prompt-engineering-whitepaper]] | Google 提示工程白皮书 |
| [[摘要-5c-prompt-contracts-paper]] | 5C Prompt Contracts 论文 |

### 创建的概念页面（5 个）

| 页面 | 类型 | 核心内容 |
|------|------|----------|
| [[Prompt_Engineering]] | 核心概念 | 提示工程总览、七大要素、技术分类 |
| [[5C_Framework]] | 框架 | 5C 提示契约框架详解 |
| [[Chain_of_Thought]] | 技术 | 思维链技术、Zero-shot/Few-shot CoT |
| [[Few_Shot_Prompting]] | 技术 | 少样本提示最佳实践 |
| [[Context_Engineering]] | 范式 | 从提示工程到上下文工程的转变 |

### 创建的实体页面（4 个）

| 页面 | 描述 |
|------|------|
| [[Google]] | Google 公司及其 AI 产品 |
| [[Anthropic]] | Anthropic 公司及其安全研究 |
| [[Gemini]] | Google Gemini 模型家族特性 |
| [[Claude]] | Anthropic Claude 模型家族特性 |

### 冲突与发现

**知识冲突（已标注）：**
- 在 [[5C_Framework]] 页面中记录了「5C vs 复杂 DSL 之争」的知识冲突

**重要发现：**
1. **提示长度悖论**：研究表明 150-300 词是最佳长度，超过 3,000 tokens 性能显著下降
2. **CoT 悖论**：现代推理模型（GPT-5, Claude 4, Gemini 3）内部自动推理，显式 CoT 反而可能有害
3. **5C 效率优势**：平均仅需 54 tokens 输入，比 DSL 节省 6 倍以上
4. **Gemini 简化趋势**：Gemini 3 不再需要复杂提示工程，建议使用简化提示
5. **Context Engineering 范式**：行业正在从单个提示优化转向系统上下文管理

### 更新文件
- [[index.md]] — 重新组织了总目录结构
- [[log.md]] — 记录本次操作（本条目）

### 归档操作
所有 7 个源文件已移动至 `raw/09-archive/` 目录。

---

## [2026-04-12] query | 基于 5C Framework 设计 Markdown 笔记提示词

- **查询**: 根据 5C Framework 设计撰写 Markdown 格式知识笔记的提示词
- **引用**: [[5C_Framework]]
- **输出**: 已创建 synthesis 文件 [[5c-prompt-markdown-note-taking]]
- **更新**: [[index.md]] 已注册新 synthesis

### 提示词特色
- 遵循 5C 框架：Character/Cause/Constraint/Contingency/Calibration
- Token 高效（约 150 tokens）
- 包含完整的使用示例和变体建议
- 内置质量自检机制（Calibration）

---

## [2026-04-12] lint | 知识库健康检查

### ✅ 绿灯项
- 所有来源页面均有双向链接引用
- 所有概念页面均有双向链接引用
- 所有实体页面均有双向链接引用
- 新知识冲突已正确标注

### ⚠️ 黄灯项
- **8 个未同步索引（文件不存在但 index.md 已注册）**：
  - [[Zero_Shot_Prompting]] — 计划中，待创建
  - [[APE_Framework]] — 计划中，待创建
  - [[CO-STAR_Framework]] — 计划中，待创建
  - [[RISEN_Framework]] — 计划中，待创建
  - [[CRAFT_Framework]] — 计划中，待创建
  - [[POWER_Framework]] — 计划中，待创建
  - [[ReAct]] — 计划中，待创建
  - [[Tree_of_Thoughts]] — 计划中，待创建
  - [[RAG]] — 计划中，待创建

- **10 个死链（页面引用不存在的文件）**：
  - [[Constitutional_AI]]（被 Anthropic.md 引用）
  - [[Adaptive_Thinking]]（被 Anthropic.md、Claude.md 引用）
  - [[Agentic_Systems]]（被 Anthropic.md、Context_Engineering.md 引用）
  - [[Token_Efficiency]]（被 5C_Framework.md、摘要-5c-prompt-contracts-paper.md 引用）
  - [[Prompt_Design]]（被 5C_Framework.md、摘要-5c-prompt-contracts-paper.md 引用）
  - [[DSL_Prompting]]（被 5C_Framework.md 引用）
  - [[ChatGPT]]（被 摘要-complete-prompt-engineering-guide-2025.md 引用）
  - [[DeepMind]]（被 Google.md 引用）

### ❌ 红灯项
- **1 个待解决的知识冲突**：
  - [[5C_Framework]] 页面中记录的「5C vs 复杂 DSL 之争」（概念性标注，待补充具体冲突内容）

### 🛠️ 下一步行动
1. **高优先级**：创建核心概念页面（Zero_Shot_Prompting、ReAct、RAG）
2. **中优先级**：创建框架页面（APE、CO-STAR、RISEN、CRAFT、POWER）
3. **低优先级**：补充辅助概念（Constitutional_AI、DeepMind、Token_Efficiency 等）
4. **可选**：完善 5C_Framework 的知识冲突区块，补充具体争议点

### 统计
- 总文件数：19 个（不含 index/log）
- 存在页面：19 个
- 孤儿页面：0 个
- 未同步索引：8 个（计划中的框架/技术）
- 死链：10 个（辅助/补充概念）
- 知识冲突：1 个（概念性标注）

---

## [2026-06-22] sync | 增加 Codex 兼容入口与技能目录
- **变更**: 新增 [[AGENT_GUIDE.md]]、[[AGENTS.md]] 与 `.agents/skills/`; 将 [[CLAUDE.md]] 调整为 Claude Code 兼容入口; 更新 [[README.md]]
- **影响**: Claude Code 与 Codex 共用同一套主规范; 未修改 `raw/` 原始资料

---

## [2026-06-23] sync | 增加结构化元信息层与状态技能
- **变更**: 新增 `wiki/_meta/manifest.md`、`wiki/_meta/taxonomy.md`、`wiki/_meta/templates/`、`wiki/_meta/health.md`; 新增 Claude Code 与 Codex 的 `status` 技能; 更新 [[AGENT_GUIDE.md]]、[[README.md]] 和 ingest/query/lint 技能
- **影响**: `raw/` 保持不可变，摄取状态改由 manifest 管理; `/lint` 输出 health report; `/status` 可快速报告知识库状态

---

## [2026-06-23] sync | 启动 C 阶段工具化脚本
- **变更**: 新增 `tools/wiki_tools.py` 与 `wiki/_meta/graph.json`; 工具支持 `status`、`lint`、`manifest`、`graph`、`stats`; 更新 [[AGENT_GUIDE.md]]、[[README.md]]、lint/status 技能和 `.gitignore`
- **影响**: `/lint` 与 `/status` 可优先调用本地脚本生成结构化结果; health report 和图谱 JSON 可重复生成; `raw/` 仍保持不可变

---

## [2026-06-23] sync | 增加本地搜索与 GraphML 导出
- **变更**: `tools/wiki_tools.py` 新增 `search` 命令和 `graph --format graphml`; 新增 `tools/test_wiki_tools.py` 覆盖搜索、GraphML、manifest 路径解析和 raw 只读约束; 生成 `wiki/_meta/graph.graphml`
- **影响**: `/query` 可优先用本地搜索定位候选页面; 图谱可导出给 Gephi/yEd 等工具; 工具层仍不读取 `raw/` 文件内容

---

## [2026-06-23] lint | 修正 source 路径与 manifest 不一致
- **变更**: 更新 [[摘要-complete-prompt-engineering-guide-2025]] 的 `sources` 路径，并将 `wiki/_meta/manifest.md` 中对应条目恢复为 `ingested`
- **结果**: `python -X utf8 tools/wiki_tools.py manifest --strict` 通过，manifest 不一致项为 0；未修改 `raw/`

---

## [2026-06-23] sync | 重置为干净 Wiki 骨架
- **变更**: 删除现有正式知识页，重置 [[index.md]]、`wiki/_meta/manifest.md`、`wiki/_meta/health.md`、`wiki/_meta/graph.json` 和 `wiki/_meta/graph.graphml`
- **结果**: `wiki/concepts/`、`wiki/entities/`、`wiki/sources/`、`wiki/syntheses/` 保留为空目录骨架；8 个 `raw/` 文件全部登记为 `pending`；未修改 `raw/`

---

## [2026-06-23] sync | 移除 raw 历史归档目录
- **变更**: 经用户确认，将 `raw/09-archive/The Complete Prompt Engineering Guide (2025).md` 移回 `raw/01-articles/`，删除空的 `raw/09-archive/`，并更新 `wiki/_meta/manifest.md`、[[README.md]] 和 ingest 技能
- **结果**: `raw/` 不再包含历史归档目录；8 个原始资料仍全部保留并登记为 `pending`

---

## [2026-06-23] sync | 清空 raw 原始资料
- **变更**: 经用户确认，删除 `raw/` 子目录中的 8 个原始资料文件，并清空 `wiki/_meta/manifest.md` 的资料条目
- **结果**: `raw/` 保留空目录结构（仅含 `.gitkeep` 占位文件）；wiki 正式内容页为 0；manifest、health 和图谱输出均重置为空库状态

---

## [2026-06-23] sync | 优化 raw 分类目录
- **变更**: 新增 `raw/04-notes/` 用于个人笔记、会议记录和头脑风暴；更新 [[AGENT_GUIDE.md]]、[[README.md]] 和 ingest 技能中的 raw 分类说明
- **结果**: `raw/` 保持空库状态，仅包含目录占位文件；工具仍将 raw 原始资料数统计为 0

---

## [2026-06-24] sync | 增加本地分发友好文档
- **变更**: 新增 [[QUICKSTART.md]]、[[VERIFY.md]]、`tools/README.md` 和 `requirements.txt`; 重写 [[README.md]] 为项目首页; 更新 `.gitignore`
- **结果**: 下载后可直接按 quickstart 打开 Obsidian vault，并用 VERIFY 中的命令验证工具、manifest 和空库状态

---

## [2026-06-24] sync | 增加 Obsidian 入口与维护面板
- **变更**: 新增 [[Home.md]]、`wiki/_meta/dashboard.md` 和 `wiki/_meta/obsidian.md`; 更新 [[README.md]]、[[QUICKSTART.md]] 和 [[index.md]]
- **结果**: Obsidian 打开后可从 Home 进入 dashboard、主规范、验证说明和 wiki 索引；未引入个人化 `.obsidian/` 配置

---

## [2026-06-24] sync | 合并 Quickstart 到 README
- **变更**: 将 `QUICKSTART.md` 的快速开始内容合并进 [[README.md]]，删除独立 `QUICKSTART.md`，并更新 [[Home.md]] 入口链接
- **结果**: 根目录保留 README、Home、VERIFY 三个面向不同场景的入口，减少重复文档

---

## [2026-06-24] sync | 增强 Obsidian Canvas 与工作流入口
- **变更**: 新增 `wiki/_meta/wiki-map.canvas` 和 `wiki/_meta/workflows.md`; 更新 [[Home.md]]、`wiki/_meta/dashboard.md`、`wiki/_meta/obsidian.md` 和 [[README.md]]
- **结果**: Obsidian 内可通过 Home 进入结构地图、维护面板和完整工作流说明；仍不引入个人化 `.obsidian/` 配置

## [2026-06-24] sync | 增加译文派生层与 translate 技能
- **变更**: 新增 `translated/` 四类目录、`wiki/_meta/translation-manifest.md`、Claude Code/Codex 的 `translate` 技能；更新 [[AGENT_GUIDE.md]]、[[README.md]]、[[Home.md]]、`wiki/_meta/workflows.md` 和工具说明
- **结果**: 外文 Web Clipper 资料可先完整翻译为中文译文，再通过 `/ingest translated/...` 编译进正式 wiki；`raw/` 仍保持不可变事实层

## [2026-06-24] sync | 增加 Obsidian 本地配置忽略规则
- **变更**: 更新 `.gitignore`，忽略 `.obsidian/` 与 `.trash/`
- **结果**: 打开 Obsidian vault 或演示 Web Clipper 后，不会默认把个人插件、布局和回收站状态纳入发布内容

## [2026-06-24] translate | 翻译 LLM Wiki 原始资料
- **变更**: 新增 [[translated/01-articles/LLM-Wiki.zh.md]]；更新 [[wiki/_meta/translation-manifest.md]]
- **来源**: `raw/01-articles/LLM-Wiki.md`
- **结果**: 已生成完整简体中文译文；未修改 `raw/`

## [2026-06-24] sync | 修复 translate 写入编码约束
- **变更**: 修复 [[translated/01-articles/LLM-Wiki.zh.md]]、`wiki/_meta/translation-manifest.md` 和 [[log.md]] 中的编码替换问题；更新 `translate` 技能与 [[AGENT_GUIDE.md]] 的 UTF-8 写入要求
- **结果**: 译文在 Obsidian 中应以正常中文显示；`/translate` 后会将 raw 文件登记为 `pending`，等待后续 `/ingest`

## [2026-06-24] sync | 增强译文来源导航
- **变更**: 在 [[translated/01-articles/LLM-Wiki.zh.md]] 中新增 `## 来源导航`；更新 `translate` 技能、[[AGENT_GUIDE.md]] 和 `wiki/_meta/obsidian.md`
- **结果**: 译文页可在 Obsidian 中一键跳回原始剪藏，同时保留纯文本 `raw_path` 供工具和 agent 解析

## [2026-06-24] ingest | 摄取 LLM Wiki 方法论
- **变更**: 新增 [[摘要-llm-wiki]]、[[LLM_Wiki]]、[[Persistent_Knowledge_Base]]、[[Raw_Source_Layer]]、[[Wiki_Schema]]、[[Ingest_Workflow]]、[[Query_Workflow]]、[[Wiki_Lint]]、[[Retrieval_Augmented_Generation]]、[[Obsidian]]、[[LLM_Agent]]、[[OpenAI_Codex]]、[[Claude_Code]]、[[Andrej_Karpathy]]；更新 [[index.md]] 与 `wiki/_meta/manifest.md`
- **来源**: `raw/01-articles/LLM-Wiki.md`；译文 `translated/01-articles/LLM-Wiki.zh.md`
- **冲突**: 无

## [2026-06-24] query | 查询 LLM Wiki 文章核心观点
- **输出**: 即时回答未保存；引用 [[摘要-llm-wiki]]、[[LLM_Wiki]]、[[Persistent_Knowledge_Base]]、[[Retrieval_Augmented_Generation]]、[[Ingest_Workflow]]、[[Query_Workflow]]、[[Wiki_Schema]]、[[LLM_Agent]]、[[Obsidian]]

## [2026-06-24] sync | README 增加完整实操演示
- **变更**: 更新 [[README.md]]，新增 Web Clipper 剪藏、`/translate`、`/ingest`、`/lint` 和 `/query` 的端到端演示步骤
- **结果**: 下载或打开项目后，可以直接按 README 复现英文文章进入本地 LLM Wiki 的完整流程
