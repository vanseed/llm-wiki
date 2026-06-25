---
name: lint
description: 知识库全局健康度检查。扫描 wiki/ 目录，检测死链、孤儿页面、未同步索引、manifest 不一致和知识冲突。当用户输入 /lint、/scan、/health 或要求“检查知识库状态”、“检查健康”时调用。报告前禁止修改任何文件；输出或更新 wiki/_meta/health.md。
user-invocable: true
---

# lint 技能：知识图谱健康巡检

## 核心目标

将软件工程中的“静态代码分析”引入知识管理。定期运行此 skill，找出知识库长期演进中产生的：死链、孤岛、未同步索引、manifest 不一致、认知冲突。

## 工具优先

如果 `tools/wiki_tools.py` 存在，优先运行：

```bash
python -X utf8 tools/wiki_tools.py lint --write
```

该工具会重新生成 `wiki/_meta/health.md`，并且只列出 `raw/` 与 `translated/` 文件路径，不读取两者文件内容。工具不可用时，再按下面的巡检流程手动扫描。

## 触发条件

- 用户输入 `/lint`
- 用户输入 `/scan`
- 用户输入 `/health`
- 用户询问“我的知识库健康状况如何”
- 用户要求“检查知识库状态”或“检查健康”

## 知识库路径

- 使用 Glob 工具动态定位当前工作区下的 wiki/ 目录
- 扫描知识页面、`wiki/index.md` 和 `wiki/_meta/manifest.md`
- 默认排除 `wiki/log.md` 的历史双链，避免历史记录制造假阳性
- `wiki/_meta/templates/` 和 `translated/` 不作为正式知识页参与索引、死链、孤儿页面或知识冲突统计；只检查模板文件是否存在、frontmatter 是否包含 `template: true` 与 `status: template`
- 仅在 manifest 一致性检查中读取 `raw/` 文件列表，不读取 raw 文件内容

## 巡检流水线

### 第 1 步：索引一致性检查

1. 读取 `wiki/index.md` 全部内容
2. 扫描知识页面，排除 `index.md`、`log.md`、`wiki/_meta/`、`wiki/_meta/templates/` 和 `translated/`
3. 提取 index.md 中注册的所有双链链接 `[[页面名称]]`
4. 比对：找出已注册但文件不存在的条目，或文件存在但未注册的页面

### 第 2 步：双向链接健康检查

1. 扫描知识页面，排除 `index.md`、`log.md`、`wiki/_meta/`、`wiki/_meta/templates/` 和 `translated/`，提取所有 `[[双链]]` 格式的链接
2. 如果链接指向的页面不存在 → 标记为 **知识页面死链**
3. 统计被引用的页面，排除 self-reference
4. 找出从未被任何其他页面引用的页面 → **孤儿页面**

### 第 3 步：认知冲突审查

1. 全局搜索知识页面，排除 `index.md`、`log.md`、`wiki/_meta/` 和 `wiki/_meta/templates/`，查找包含 `## 知识冲突` 的页面
2. 提取每个冲突的简要描述（冲突双方是什么）
3. 统计带未解决冲突的页面（认知技术债）

### 第 4 步：Manifest 一致性检查

1. 读取 `wiki/_meta/manifest.md`
2. 扫描 `raw/` 下文件路径，只列路径，不读取文件内容
3. 标记 raw 文件存在但 manifest 未登记的条目
4. 标记 manifest 中 source 页面不存在的条目，且不要把 `_meta/templates` 当知识页面
5. 标记 source frontmatter `sources` 路径与 manifest `raw_path` 不一致的条目

## 报告输出规范

扫描完成后，输出结构化报告，并将同样内容写入或更新 `wiki/_meta/health.md`。保持 Claude 风格的清晰分区：

```markdown
## 知识库健康体检报告 — YYYY-MM-DD

### 绿灯项
- [运行良好的项目]

### 黄灯项
- **发现 N 个孤儿页面**：[列表] - 建议添加关联或分类
- **发现 N 个未同步索引**：[列表] - 文件存在但未在 index.md 注册
- **发现 N 个已注册但未创建页面**：[列表] - index.md 已注册但文件不存在
- **发现 N 个 manifest 不一致项**：[列表] - raw/source/manifest 之间不一致

### 红灯项
- **发现 N 个知识页面死链**：[来源页面] → [[不存在的目标页面]]
- **存在 N 个未解决的知识冲突**：[页面名称]

### 下一步行动
1. 是否需要自动修复未同步索引？
2. 是否需要针对知识冲突进行重新推演？
3. 是否需要补齐已注册但未创建页面？
```

## 硬约束

- **仅读扫描**：生成报告前，禁止修改、删除、重命名任何文件；唯一允许的写入是扫描完成后输出或更新 `wiki/_meta/health.md`
- **不读 raw/translated 内容**：manifest 一致性检查只列出 `raw/` 文件路径，状态统计只列出 `translated/` 文件路径，不读取两者文件内容
- **手动确认**：报告后等待用户确认再执行修复
- **静默日志**：修复完成后，在 `wiki/log.md` 追加 `## [YYYY-MM-DD] lint | 修复了 N 个问题`
