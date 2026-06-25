# Obsidian 使用约定

本 vault 以 Obsidian wikilink 为核心，同时保持纯 Markdown 可读。

## 推荐入口

- 打开 vault 后，从根目录的 [[Home]] 开始。
- 正式知识目录从 [[../index|Wiki Index]] 开始。
- 维护状态从 [[dashboard|Dashboard]] 开始。
- 可视化结构从 [[wiki-map.canvas|Wiki Map Canvas]] 开始。

## 链接约定

- 正式知识页之间使用 `[[页面名称]]` 双链。
- 引用 source、entity、concept、synthesis 时，优先链接对应 wiki 页面，而不是直接链接 raw 文件。
- `wiki/_meta/` 中的页面服务维护流程，不作为正式知识页参与统计。
- `translated/` 中的译文可作为阅读材料链接，但不要把它当作正式知识页维护双链网络。
- `translated/` 译文页应包含 `## 来源导航`，用 `[[raw/...|文件名]]` 快速跳回原始剪藏。

## 附件约定

- 图片、PDF 和媒体附件放入 `assets/`。
- 在 wiki 页面中引用附件时，使用 Obsidian 语法：`![[文件名.png]]`。
- 原始资料放入 `raw/`，不要把 `raw/` 当作正式知识页目录。
- 外文资料的完整中文译文放入 `translated/`，不要把 `translated/` 当作正式知识页目录。

## 模板约定

页面模板位于 `wiki/_meta/templates/`：

- [[templates/source|source 模板]]
- [[templates/entity|entity 模板]]
- [[templates/concept|concept 模板]]
- [[templates/synthesis|synthesis 模板]]

模板文件带有 `template: true` 和 `status: template`，不会被工具当作正式知识页统计。

## 插件约定

本模板不要求任何 Obsidian 插件。后续可以按个人习惯添加 Dataview、Templater 或其他插件，但不要把个人化 `.obsidian/` 配置作为主规范的一部分。

## Canvas 约定

- `wiki/_meta/wiki-map.canvas` 是 vault 结构地图。
- Canvas 只作为导航和理解结构的辅助，不作为正式知识页统计。
- 如果后续加入更多工作流或模块，可以在 Canvas 中添加 file node 指向相关 Markdown 页面。

## 空库状态

当前模板是干净空库：

- `raw/` 只有 `.gitkeep` 占位文件。
- `translated/` 只有 `.gitkeep` 占位文件。
- `wiki/concepts/`、`wiki/entities/`、`wiki/sources/`、`wiki/syntheses/` 只有 `.gitkeep` 占位文件。
- `wiki/_meta/manifest.md` 是空 manifest 表。
- `wiki/_meta/translation-manifest.md` 是空 translation manifest 表。
