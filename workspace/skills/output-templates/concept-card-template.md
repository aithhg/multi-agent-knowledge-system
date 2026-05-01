# 概念卡模板

> 适用：单个概念的清晰定义和关联

---

## 模板

```yaml
---
id: concept-name-slug
title: 概念名称
type: concept
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
aliases:
  - 别名1
  - 别名2
related:
  - [[相关概念卡1]]
  - [[相关概念卡2]]
sources:
  - [[raw文件id1]]
  - [[raw文件id2]]
---

## Definition

<!-- 在当前系统语境下的精确定义 -->
<!-- 回答：这个概念在这里是什么意思？ -->

## Why It Matters

<!-- 为什么这个概念重要 -->
<!-- 回答：理解它有什么价值？ -->

## Where It Appears

<!-- 在哪些材料/场景里反复出现 -->
<!-- 帮助建立知识关联 -->

## Notes

<!-- 相关补充、例子、边界条件 -->
<!-- 适合放非结构化的补充信息 -->

## Examples

<!-- 具体例子，帮助理解概念的适用场景 -->
```

---

## 长度规范

| 部分 | 长度 | 说明 |
|------|------|------|
| Definition | 50-200 字 | 精确定义，避免循环定义 |
| Why It Matters | 30-100 字 | 简洁有力 |
| Where It Appears | 30-100 字 | 列出具体来源 |
| Notes | 0-300 字 | 可选 |
| Examples | 0-200 字 | 可选 |
| **总计** | 100-600 字 | |

---

## 写作规则

- [ ] Definition 是原创的，不是复制粘贴
- [ ] Why It Matters 回答「这个概念对我有什么用」
- [ ] Where It Appears 列出具体的、真实的来源
- [ ] 概念名称稳定，不要随意改名

## 禁止出现

- ❌ 循环定义（「X 是指 X」）
- ❌ 空泛的价值描述（「很重要」「很有意义」）
- ❌ 无法验证的「 appears everywhere」
