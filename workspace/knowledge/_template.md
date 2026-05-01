# 知识文件标准模板

> **重要**：本模板已与 `CLAUDE.md` 保持一致。实际使用时可直接复制使用。
> **方法论来源**：Compound Engineering v3.4

---

## 摘要文件 Schema

保存到：`knowledge/resources/literature/summary-YYYYMMDD-slug.md`

```yaml
---
id: summary-YYYYMMDD-slug
source_id: raw文件id
title: 摘要标题
created_at: YYYY-MM-DD
type: summary
topics: []
concepts: []
---

## Core Idea

<!-- 一句话概括这份材料最重要的观点 -->

## Key Points

1. ...
2. ...
3. ...

## Evidence

- 事实或原文依据

## Open Questions

- 还没解决的问题

## Related

- [[相关条目 1]]
- [[相关条目 2]]

## Source

- [[raw文件id]]
```

---

## 概念卡 Schema

保存到：`knowledge/areas/notes/permanent/concept-name-slug.md`
或：`knowledge/resources/permanent/concept-name-slug.md`

```yaml
---
id: concept-name-slug
title: 概念名称
type: concept
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
synced_to_DHR: true
aliases: []
related: []
sources: []
---

## Definition

<!-- 这个概念在当前系统里的定义 -->

## Why It Matters

<!-- 它为什么重要 -->

## Where It Appears

<!-- 它在哪些材料里反复出现 -->

## Notes

<!-- 相关补充 -->
```

---

## 主题页 Schema

保存到：`knowledge/areas/moc/moc-topic-name.md`

```yaml
---
id: topic-slug
title: 主题名称
type: topic
updated_at: YYYY-MM-DD
related: []
sources: []
---

## Thesis

<!-- 这个主题要表达的核心判断 -->

## Main Structure

### 1. 系统目标

...

### 2. 核心机制

...

### 3. 典型流程

...

## Tensions

<!-- 冲突、差异和未决问题 -->
```

---

## Atomic Notes 原则

每条笔记只表达一个明确主题或一个独立知识单元：
- 不要把多个概念混写在同一条笔记里
- 不要把多个论点混写在同一条笔记里
- 不要把多个案例混写在同一条笔记里
- 每条笔记必须能够脱离原始上下文单独理解
- 标题应当清晰、具体、可检索
- 最好本身就是一句完整判断或一个明确名词短语

---

## 索引文件 Schema

`knowledge/index.md`：

```markdown
# Knowledge Index

> 最后更新：YYYY-MM-DD
> 系统版本：v3.4
> 同步状态：✅ 已与 D&H&R/Knowledge/ 同步
> 方法论：Compound Engineering

## Topics

- [[主题名称]]（YYYY-MM-DD）
  - 来源：workspace/knowledge/areas/moc/moc-xxx.md
  - 状态：✅ 正常 | ⚠️ missing

## Concepts

### 分类名称

- [[概念名称]]（YYYY-MM-DD）
  - 来源：workspace/knowledge/resources/permanent/concept-xxx.md
  - 状态：✅ 正常 | ⚠️ missing
  - synced：true

## Inspections

- [[巡检报告：YYYYMMDD-名称]]

---

## 系统状态

| 指标 | 数值 |
|------|------|
| 总条目数 | — |
| 正常条目 | — |
| 缺失条目 | — |
| 健康度 | —% |

