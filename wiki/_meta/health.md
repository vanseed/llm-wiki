# Wiki Health

最近检查日期：2026-06-25

## 摘要

- wiki 内容页：14 个（不含 `wiki/index.md`、`wiki/log.md` 和 `wiki/_meta/`）
- raw 文件：1 个
- translated 译文文件：1 个
- manifest 状态：`ingested` 1 个，`path_mismatch` 0 个，`pending` 0 个，`conflict_paused` 0 个
- translation 状态：`translated` 1 个, `needs_review` 0 个, `pending` 0 个, `skipped` 0 个
- 已注册但未创建页面：0 个
- 知识页死链引用：0 处（0 个唯一目标；不含 `wiki/index.md`、`wiki/log.md` 和 `wiki/_meta/`）
- 孤儿页面：0 个
- Manifest 不一致项：0 个

## 已注册但未创建页面

- 无

## 知识页死链目标

- 无

## Manifest 注意事项

- 未发现 manifest/raw/source 不一致项。

## Lint 口径

- 死链扫描默认排除 `wiki/log.md`。
- `wiki/index.md` 中预注册但未创建的页面归类为“已注册但未创建”，不与普通知识页死链混在一起。
- `wiki/_meta/templates/` 不作为正式知识页参与索引、死链、孤儿页面或知识冲突统计。
- 修复动作必须经过用户确认。

## 下一步建议

1. 当前未发现结构性问题，继续翻译、增量摄取或查询即可。
