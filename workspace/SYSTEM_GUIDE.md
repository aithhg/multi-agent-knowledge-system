# Compound Engineering 系统 - 使用指南

> 本系统基于 **Compound Engineering**（复合工程）方法论构建。
> 核心理念：不是让 AI 多做几次事，而是让 AI 帮你搭一个会复利的工作系统。

## 欢迎使用

欢迎使用 Compound Engineering 系统！这是一个基于**文件优先**、**增量更新**和**可追溯**原则设计的复利工作系统。本指南将帮助您快速上手并有效使用系统。

## 系统核心理念

### 1. 复利效应
知识应该像复利一样随时间增值。今天做过的事，会变成明天的基础。每一次处理，都不是结束，而是下一次处理的输入。

### 2. Compound Engineering 是什么
一套让 AI帮你构建复利系统的方法论。适用于：知识库、内容生产、研究、产品分析、销售、招聘、个人生活管理。

核心只有一句话：**不要只让 AI 生成一次性的结果。要让 AI 帮你生成一套能持续使用的系统。**

### 3. 三大原则
- **文件优先**：所有知识保存为普通文本文件，避免被工具锁定
- **增量更新**：只处理新增内容，不重复劳动
- **可追溯**：每个结论都能找到原始来源

### 4. AI 协作
系统设计为与 AI（特别是 Claude）协同工作，AI 作为知识助理帮助持续完成摄取→消化→输出→巡检四个流程。

## 快速开始

### 第一步：熟悉目录结构
```
workspace/
├── raw/                 # 原始材料 - 放这里开始
├── knowledge/           # 消化后的知识（按PARA+MOC+Zettelkasten组织）
│   ├── projects/       # 有明确目标和截止时间的事项
│   ├── areas/          # 长期持续负责的领域  
│   ├── resources/      # 参考资料和主题知识
│   ├── archives/       # 归档内容
│   └── inspections/    # 巡检报告
├── outputs/            # 产出内容
└── .claude-context/    # AI 上下文缓存
```

### 第二步：您的第一次知识保存
1. 找到一个有价值的内容（文章、视频、想法）
2. 保存到 `raw/sources/`：`20260414-web-article-topic-abc123.md`
3. 让 AI 帮助提取要点到 `raw/captures/`
4. 关键概念保存到 `knowledge/areas/notes/permanent/` 或 `knowledge/resources/permanent/` 对应分类中

### 第三步：提出第一个问题
1. 在 Claude Code 或 Obsidian 中打开本系统
2. 提问时说明：“请基于复利知识系统回答”
3. AI 将自动检索相关知识和历史上下文

## 详细工作流程

### 1. 知识输入流程

#### 1.1 保存原始材料
```bash
# 手动保存示例
echo "# 文章标题" > "raw/sources/$(date +%Y%m%d)-web-article-title-hash123.md"
```

#### 1.2 使用 AI 处理
```
用户：我发现一篇关于 Claude API 的文章
AI：已保存到 raw/sources/20260414-web-article-claude-api-xyz789.md
      正在提取关键要点...
      已创建摘要：raw/captures/20260414-claude-api-summary.md
      识别到新概念：knowledge/areas/notes/permanent/claude-api_v1.md
```

#### 1.3 手动处理模板
创建 `raw/sources/template.md` 文件：
```markdown
---
source: https://example.com
title: 文章标题
type: article/video/podcast/book
author: 作者
date: YYYY-MM-DD
tags: [topic, subtopic]
confidence: high/medium/low
---

# [标题]

## 核心观点

## 关键细节

## 我的思考

## 行动项
```

### 2. 知识消化流程（Digestion）

#### 2.1 原理
消化是这套系统的核心。它做的不是“再写一遍摘要”，而是把原始材料编译成可以复用的知识结构。原始材料是输入，摘要、概念、主题页、索引是编译产物。如果说摄取是在建原料仓，消化就是在建知识层。

#### 2.2 原则
1. 以增量方式处理新增内容。
2. 每条结论尽量带来源。
3. 先抽象出概念，再组织主题。
4. 人负责判断，AI 负责整理和联结。
5. 不追求一次性完美分类，持续迭代就够。

#### 2.3 AI 在消化阶段应该做什么
AI 在消化阶段做四件事：
1. 为每份 raw 生成结构化摘要。
2. 抽取概念，并映射到已有概念库。
3. 更新主题页或创建新主题页。
4. 更新总索引。

#### 2.4 提示词写法
重点是告诉 AI：不是总结一篇文章，而是更新一个系统。

完整提示词如下：
```
你正在执行“消化”步骤。

目标：
把新增的 raw 原始材料编译为知识层内容，包括摘要、概念条目、主题页和索引更新。

工作要求：
1. 只处理新增或指定的 raw 文件。
2. 先阅读原始材料，再判断它应该更新哪些知识文件。
3. 先复用已有概念和主题页，必要时再新建。
4. 所有结论都尽量保留来源引用。
5. 不要把知识层写成流水账。
6. 不要只按时间组织内容，优先按主题、观点、关系组织。
7. 如果发现内容与现有知识冲突，标记冲突，不要偷偷覆盖。
8. 处理原则遵循 Atomic Notes：每条笔记只表达一个明确主题或一个独立知识单元，不要把多个概念、多个论点、多个案例混写在同一条笔记里。每条笔记必须能够脱离原始上下文单独理解，标题应当清晰、具体、可检索，最好本身就是一句完整判断或一个明确名词短语。

你的任务顺序：
1. 阅读 raw 文件。
2. 输出结构化摘要。
3. 抽取关键概念。
4. 判断应更新的主题页。
5. 给出索引更新建议。
6. 严格按照 schema 输出。
```

#### 2.5 摘要 schema
```markdown
---
id: summary-2026-04-09-karpathy-llm-kb-001
source_id: 2026-04-09-karpathy-llm-kb-001
title: LLM 知识库工作流摘要
created_at: 2026-04-09
type: summary
topics:
  - knowledge-system
  - llm-workflow
concepts:
  - incremental-processing
  - file-over-app
---

## Core Idea

一句话概括这份材料最重要的观点。

## Key Points

1. ...
2. ...
3. ...

## Evidence

- 事实或原文依据

## Open Questions

- 还没解决的问题

## 相关条目
  - [[相关条目 1]]
  - [[相关条目 2]]

## Source

- [[2026-04-09-karpathy-llm-kb-001]]
```
*保存位置：`knowledge/resources/literature/`*

#### 2.6 概念卡 schema
```markdown
---
id: concept-incremental-processing
title: 增量处理
type: concept
created_at: 2026-04-09
updated_at: 2026-04-09
aliases:
  - incremental compilation
related:
  - file-over-app
  - traceability
sources:
  - 2026-04-09-karpathy-llm-kb-001
---

## Definition

这个概念在当前系统里的定义。

## Why It Matters

它为什么重要。

## Where It Appears

它在哪些材料里反复出现。

## Notes

相关补充。
```
*保存位置：`knowledge/areas/notes/permanent/` 或 `knowledge/resources/permanent/`*

#### 2.7 主题页 schema
```markdown
---
id: topic-llm-knowledge-system
title: LLM 知识系统
type: topic
updated_at: 2026-04-09
related:
  - concept-incremental-processing
  - concept-file-over-app
sources:
  - 2026-04-09-karpathy-llm-kb-001
  - 2026-04-09-fankaishuoai-001
---

## Thesis

这个主题页要表达的核心判断。

## Main Structure

### 1. 系统目标

...

### 2. 核心机制

...

### 3. 典型流程

...

## Tensions

- 这里记录冲突、差异和未决问题。
```
*保存位置：`knowledge/topics/`*

#### 2.8 索引文件建议
`knowledge/index.md`
```markdown
# Knowledge Index

## Topics

- [[LLM 知识系统]]
- [[个人知识库工作流]]

## Concepts

- [[增量处理]]
- [[文件优先]]
- [[可追溯性]]
```

#### 2.9 事实验证
- 可验证的事实 → `knowledge/facts/`
- 带有来源引用和时间戳
- 定期审查更新状态

#### 2.10 流程总结
- 操作方法 → `knowledge/processes/`
- 分步骤说明
- 包含成功案例和常见问题

#### 2.11 示例消化会话
假设您有一个新的 raw 文件 `raw/20260414-test-article.md`，您可以这样启动消化流程：

```
用户：请执行消化步骤，处理 raw/20260414-test-article.md

AI：正在执行消化步骤...
1. 阅读 raw 文件：20260414-test-article.md
2. 生成结构化摘要：knowledge/resources/literature/summary-20260414-test-article.md
3. 抽取关键概念：knowledge/areas/notes/permanent/concept-automated-knowledge-extraction.md, knowledge/areas/notes/permanent/concept-knowledge-graphs.md
4. 更新主题页（MOC）：knowledge/areas/moc/moc-ai-knowledge-management.md
5. 更新索引：knowledge/index.md

消化完成。系统已更新。
```

通过这个流程，原始材料被编译成了可重用的知识组件，并整合到了知识网络中。

### 3. 知识输出流程（Output）

#### 3.1 原理
输出不是系统的终点，而是系统继续变强的一部分。你不是拿知识库去“查一下”，然后什么都不留下。你应该让每一次高质量问答、每一次内容生成、每一个研究结论、每一份交付物都落成文件，重新变成系统资产。也就是说，输出既是消费，也是再生产。

#### 3.2 原则
1. 先检索，再综合，再生成。
2. 输出结果尽量引用来源。
3. 高价值输出必须落文件。
4. 输出格式应该服务于场景，而不是被固定模板限制。
5. 不把聊天记录当资产，文件才是资产。
6. **默认输出目录为 `D&H&R/`**：专题内容保存到对应主题目录（LLM/Occupation/国产模型等），通用知识保存到 `D&H&R/Knowledge/`，格式化输出保存到 `D&H&R/Outputs/`。

#### 3.3 这一阶段 AI 应该做什么
1. 先读索引定位相关内容。
2. 再读相关 summary、concept、topic。
3. 根据任务目标选择输出形式。
4. 生成最终文件。
5. 根据内容主题选择保存目录：专题→主题目录，通用→Knowledge/，格式化→Outputs/。
6. 如果发现系统缺口，顺手提出补充建议。

#### 3.4 提示词写法
输出阶段最重要的一点是：不要把“输出”理解成一种固定格式。你完全可以围绕不同场景，定义不同类型的输出 skills。

完整提示词如下：
```
你正在执行“输出”步骤。

目标：
基于现有知识系统回答问题或生成内容，并根据任务目标输出为合适的文件格式。

要求：
1. 先读取 index，再定位相关主题、概念、摘要。
2. 不要直接凭印象作答。
3. 输出中明确区分：
   - 已知结论
   - 推断
   - 待确认问题
4. 尽量引用具体来源文件。
5. 根据任务目标选择最合适的输出形式，例如 Markdown、图片脚本、PDF、PPT、长文、海报文案等。
6. 如果输出过程中发现知识库缺少关键概念或链接，单独列出。
7. 最终要产出实际文件，而不是只给一段聊天回复。

任务流程：
1. 检索相关内容。
2. 阅读必要文件。
3. 判断最合适的输出 skill 或输出格式。
4. 形成内容。
5. 写入对应文件。
6. 列出系统改进建议。
```

#### 3.5 输出层的组织方式
可以按“技能类型”来组织输出目录，每一类输出 skill 都可以有自己的产物格式：

```
D&H&R/Outputs/
  article/           # Markdown 长文
  infographic/       # 图片说明稿、设计文案、生成脚本或最终 PNG
  pdf/               # 导出的正式文档
  ppt/               # 演讲提纲、逐页内容、最终演示文件
  memo/              # 内部备忘录、研究笔记
  social/            # 社交媒体文案、thread、短帖、海报文案
  artifacts/         # 项目代码、临时产物（保留现有）
  drafts/            # 草稿文件（保留现有）
  published/         # 已发布的正式内容（保留现有）
  feedback/          # 使用反馈和改进建议（保留现有）

D&H&R/Knowledge/     # 通用知识输出（概念、主题页等）
D&H&R/LLM/           # AI/大模型相关输出
D&H&R/Occupation/    # 职业发展相关输出
D&H&R/国产模型/       # 国产AI模型相关输出
```

这里不建议强行规定一个统一 schema。输出天然是场景化的，最合理的做法是为不同输出类型创造不同 skill，让 skill 自己决定最合适的文件格式。

#### 3.6 常见输出技能类型
例如：
1. **文章输出 skill**：生成图文并茂的长文 → `D&H&R/Outputs/article/`
2. **信息图输出 skill**：生成信息图片或视觉卡片 → `D&H&R/Outputs/infographic/`
3. **PDF 输出 skill**：生成适合归档或分享的 PDF 文档 → `D&H&R/Outputs/pdf/`
4. **PPT 输出 skill**：生成演示文稿结构和页面内容 → `D&H&R/Outputs/ppt/`
5. **研究备忘录输出 skill**：生成内部 memo → `D&H&R/Outputs/memo/`
6. **社交媒体输出 skill**：生成 thread、短帖、海报文案 → `D&H&R/Outputs/social/`

#### 3.7 示例输出会话

**示例1：生成备忘录简报**
```
用户：请基于知识系统，生成一份关于AI知识管理最新趋势的简短报告。

AI：正在执行输出步骤...
1. 检索索引：找到相关主题 [[AI知识管理]]、概念 [[自动化知识提取]]、[[知识图谱]]
2. 阅读文件：knowledge/areas/moc/moc-ai-knowledge-management.md, knowledge/areas/notes/permanent/concept-automated-knowledge-extraction.md, knowledge/areas/notes/permanent/concept-knowledge-graphs.md
3. 选择输出格式：简报适合使用 memo 格式
4. 生成内容：D&H&R/Outputs/memo/memo-ai-km-brief_20260414.md
5. 系统改进建议：缺少概念”自然语言交互”的详细定义文件

输出完成。备忘录已保存，系统缺口已记录。
```

**示例2：生成社交媒体内容**
```
用户：请基于AI知识管理主题，生成一个Twitter thread文案。

AI：正在执行输出步骤...
1. 检索索引：找到相关主题 [[AI知识管理]]
2. 阅读文件：knowledge/topics/topic-ai-knowledge-management.md
3. 选择输出格式：社交媒体适合 thread 格式
4. 生成内容：D&H&R/Outputs/social/social-ai-km-thread_20260414.md
5. 系统改进建议：可添加具体产品案例增强说服力

输出完成。Twitter thread文案已保存。
```

**示例3：生成正式报告**
```
用户：请生成一份正式的AI知识管理趋势分析报告，用于内部参考。

AI：正在执行输出步骤...
1. 检索索引：全面检索AI知识管理相关主题和概念
2. 阅读文件：knowledge/areas/moc/moc-ai-knowledge-management.md, knowledge/areas/notes/permanent/concept-automated-knowledge-extraction.md, knowledge/areas/notes/permanent/concept-knowledge-graphs.md, knowledge/resources/literature/summary-20260414-test-article.md
3. 选择输出格式：正式报告适合PDF格式的详细文档
4. 生成内容：D&H&R/Outputs/pdf/pdf-ai-km-report_20260414.md
5. 系统改进建议：建议补充”多模态知识管理”概念卡

输出完成。正式报告已保存，可进一步转换为PDF。
```

**关键输出原则体现**：
- **先检索再生成**：先读索引和文件，不凭印象作答
- **格式匹配场景**：根据不同需求选择最合适的输出格式
- **文件化资产**：所有输出都保存为文件，成为系统资产
- **缺口识别**：输出过程中自动识别知识系统不足

#### 3.8 反馈与改进循环
每次输出使用后：
1. **记录效果** → `D&H&R/Outputs/feedback/`：记录输出物的使用效果、用户反馈、改进建议
2. **识别知识缺口**：标记系统缺失的关键概念或链接
3. **触发新知识输入**：基于缺口收集新资料，重新进入摄取→消化→输出循环

### 4. 知识巡检流程（Inspection）

#### 4.1 原理
任何系统只要持续运行，就一定会积累结构问题。知识系统也一样。会出现重复概念、冲突定义、断链、孤岛页面、过时结论、空文件、命名混乱。巡检的作用就是定期审计，而不是等系统烂掉之后重建。

#### 4.2 原则
1. 巡检先出报告，不要默认自动改。
2. 巡检最好按目录或主题分批进行。
3. 巡检关注结构问题，不只看内容对不对。
4. 巡检结果也要落文件。

#### 4.3 巡检应检查什么
1. **定义冲突**：相同概念在不同文件中的定义不一致
2. **重复概念**：相同或高度相似的概念有多个文件
3. **孤岛文件**：未被任何其他文件引用的文件
4. **缺少来源支持**：结论未标注原始材料来源
5. **过时内容**：长期未更新但仍被高频引用的内容
6. **断链问题**：指向不存在文件的链接
7. **结构问题**：文件过大、分类混乱、命名不规范等

#### 4.4 这一阶段 AI 应该做什么
1. 读取索引和指定目录的文件
2. 分析结构问题，找出冲突、重复、孤岛等
3. 生成详细的巡检报告，包含证据和建议
4. 不自动修复，除非被明确要求

#### 4.5 提示词写法
完整提示词如下：
```
你正在执行“巡检”步骤。

目标：
对现有知识系统进行结构性审计，找出问题并生成修复建议报告。

要求：
1. 你现在的职责是审计，不是直接重写整个知识库。
2. 优先发现结构问题：冲突、重复、孤岛、断链、过时、缺来源。
3. 每个问题都要给出证据。
4. 每个问题都要给出建议动作。
5. 不要自动修复，除非被明确要求。
6. 输出必须符合巡检报告 schema。

巡检顺序：
1. 读取 index。
2. 扫描指定目录。
3. 找出问题。
4. 给出优先级。
5. 输出报告。
```

#### 4.6 巡检报告 schema
```markdown
---
id: inspection-2026-04-09-weekly
title: 知识系统巡检报告
type: inspection
created_at: 2026-04-09
scope:
  - knowledge/areas/notes/permanent
  - knowledge/areas/moc
---

## Findings

### High Priority

1. ...

### Medium Priority

1. ...

### Low Priority

1. ...

## Evidence

- 文件 A 与文件 B 在定义上冲突

## Suggested Fixes

1. 合并两个概念条目
2. 为主题页补来源
3. 给孤岛文件补链接
```
*保存位置：`knowledge/inspections/`*

#### 4.7 巡检模板
系统提供了详细的巡检报告模板：`knowledge/inspections/_template.md`，包含：
- 执行摘要
- 按优先级分类的问题列表
- 详细证据
- 修复计划
- 系统健康度指标
- 预防措施建议

#### 4.8 示例巡检报告
系统提供了示例巡检报告供参考：`knowledge/inspections/inspection-2026-04-14-concepts-sample.md`。该报告展示了如何对概念目录进行结构审计，包含：

- 实际发现的问题（命名不一致、缺少版本管理、链接不足等）
- 详细的证据和影响分析
- 具体的修复计划和时间估算
- 系统健康度指标计算

通过阅读示例报告，您可以了解巡检的深度和广度，以及如何编写高质量的巡检报告。

#### 4.9 示例巡检会话
假设您想对概念目录进行巡检，可以这样启动：

```
用户：请执行巡检步骤，检查 knowledge/areas/notes/permanent/ 目录

AI：正在执行巡检步骤...
1. 读取索引文件：knowledge/index.md
2. 扫描目录：knowledge/areas/notes/permanent/
3. 分析结构问题...
4. 生成巡检报告：knowledge/inspections/inspection-2026-04-14-concepts-weekly.md

巡检完成。发现3个高优先级问题，2个中优先级问题，1个低优先级问题。
```

#### 4.10 巡检频率建议
- **快速巡检**：每周一次，检查高优先级问题
- **全面巡检**：每月一次，覆盖所有知识目录
- **专项巡检**：在重大结构调整前进行

## 文件管理规范

### 命名约定速查表

| 类型 | 格式 | 示例 |
|------|------|------|
| 原始材料 | `YYYYMMDD-source-type-content-hash.md` | `20260414-web-article-claude-api-abc123.md` |
| 知识概念 | `concept-name_version.md` | `knowledge-management_v1.md` |
| 输出文件 | `type-title_timestamp.md` | `article-ai-knowledge-trends_202604141530.md` (article)<br>`memo-weekly-report_202604141530.md` (memo)<br>`social-tweet-thread_202604141530.md` (social) |
| 会话缓存 | `session-id_topic.md` | `claude-session-001_knowledge-mgmt.md` |

### 标签系统

#### 常用标签
- `#status/new` - 新内容，待处理
- `#status/verified` - 已验证
- `#status/outdated` - 已过时
- `#priority/high` - 高优先级
- `#type/concept` - 概念类型
- `#type/fact` - 事实类型
- `#type/process` - 流程类型

#### 领域标签
- `#area/technology` - 技术领域
- `#area/career` - 职业发展
- `#area/learning` - 学习方法
- `#area/productivity` - 生产力工具

### 链接系统

#### 内部链接
```markdown
[[concept-name]]           # 链接到概念文件
@raw/sources/filename      # 链接到原始材料
@knowledge/areas/notes/permanent/file   # 链接到知识文件（永久笔记）
```

#### 外部链接
```markdown
[链接文本](https://example.com)
```

## AI 协作指南

### 如何有效与 AI 协作

#### 1. 提供充分上下文
```
不好：告诉我关于知识管理的信息
好：基于复利知识系统中的 [[knowledge-management_v1]] 和最近的 raw/sources/ 材料，总结知识管理的最新趋势
```

#### 2. 明确任务类型
- **知识保存**："请将这段内容保存到系统中"
- **知识提取**："从这些材料中提取关键概念"
- **知识连接**："建立这些概念之间的关联"
- **知识应用**："基于系统知识回答这个问题"

#### 3. 使用系统命令
```
# 检查系统状态
系统状态如何？有哪些新内容需要处理？

# 处理积压
处理 raw/sources/ 中所有 #status/new 的文件

# 生成报告
生成本周知识增长报告
```

### AI 能力范围

#### 自动化处理
- 自动分类和标签
- 概念提取和总结
- 关联发现和链接建立
- 重复内容检测

#### 智能检索
- 语义搜索知识库
- 上下文关联推荐
- 缺口分析和建议
- 时效性评估

#### 创作辅助
- 基于知识的写作
- 结构优化建议
- 引用自动添加
- 多版本管理

## 维护和优化

### 日常维护清单

#### 每天（5分钟）
1. 检查 `raw/sources/` 新文件
2. 快速处理 1-2 个 `#status/new` 项目
3. 清理 `.claude-context/sessions/` 旧会话

#### 每周（30分钟）
1. 生成知识增长报告
2. 审查重要概念的状态
3. 建立新的知识关联
4. 备份重要数据

#### 每月（2小时）
1. 全面系统审查
2. 优化目录结构
3. 清理低价值内容
4. 更新本指南

### 性能优化技巧

#### 存储优化
- 大文件拆分：超过 1000 行的文件考虑拆分
- 附件管理：大附件使用外部存储，只保存链接
- 定期归档：旧项目移动到 `archive/` 目录

#### 检索优化
- 索引文件：为每个领域创建 `_index.md`
- 标签整理：定期合并相似标签
- 链接检查：修复死链和重复链接

### 故障排除

#### 常见问题

**问题1：系统响应慢**
```
解决方案：
1. 清理 .claude-context/ 缓存
2. 拆分大知识文件
3. 优化标签系统
```

**问题2：找不到相关内容**
```
解决方案：
1. 检查标签是否正确
2. 建立更多概念关联
3. 创建更好的索引文件
```

**问题3：知识碎片化**
```
解决方案：
1. 定期进行知识整合
2. 创建综合概念文件
3. 使用连接图可视化
```

#### 应急措施
1. **数据丢失**：从 `raw/sources/` 重新处理
2. **系统混乱**：基于原始材料重建知识层
3. **AI 异常**：重新阅读 AGENTS.md 协议

## 高级用法

### 1. 自定义工作流

#### 研究项目工作流
```
1. 创建项目目录：outputs/projects/project-name/
2. 收集资料：raw/sources/project-name-*.md
3. 知识构建：knowledge/projects/notes/permanent/project-*.md
4. 产出结果：outputs/published/project-report.md
5. 经验总结：knowledge/processes/project-retrospective.md
```

#### 学习课程工作流
```
1. 课程材料：raw/sources/course-*.md
2. 学习笔记：knowledge/areas/notes/permanent/course-concept-*.md
3. 练习作业：outputs/artifacts/course-exercise-*.md
4. 总结反思：knowledge/processes/course-learnings.md
```

### 2. 集成其他工具

#### 与 Obsidian 集成
1. 将 `workspace/` 作为 Obsidian 库打开
2. 利用图谱视图查看知识连接
3. 使用 Obsidian 插件增强功能

#### 与 Claude Code 集成
1. 设置工作目录为 `workspace/`
2. 创建常用命令别名
3. 配置环境变量

#### 与 MCP 服务器集成
1. 使用 `exa` 搜索新资料
2. 使用 `weibo` 获取社交媒体信息
3. 考虑添加其他数据源

### 3. 团队协作

#### 共享知识库
1. 使用 Git 进行版本控制
2. 建立协作规范
3. 定期同步和合并

#### 分工协作
- 材料收集员：负责 `raw/sources/`
- 知识工程师：负责 `knowledge/`
- 产出创作者：负责 `outputs/`
- 系统维护员：负责整体协调

## 成功指标

### 量化指标
1. **知识密度**：每周新增概念文件 > 5个
2. **连接度**：平均每文件链接数 > 3个
3. **产出率**：每月产出有价值内容 > 3项
4. **复用率**：知识被引用比例 > 60%

### 质化指标
1. **思考深度**：问题回答更加深入和全面
2. **创造效率**：产出同样质量内容时间减少
3. **系统智能**：AI 更能理解上下文和需求
4. **个人成长**：明显感觉到知识积累和认知提升

## 开始行动

### 今日任务清单
- [ ] 阅读本指南并理解核心概念
- [ ] 创建第一个原始材料文件
- [ ] 尝试与 AI 进行一次知识对话
- [ ] 探索目录结构，熟悉文件位置

### 本周目标
- [ ] 建立个人工作流习惯
- [ ] 积累 10 个以上知识概念
- [ ] 完成第一个知识产出
- [ ] 进行一次系统维护

### 本月里程碑
- [ ] 系统稳定运行，形成习惯
- [ ] 知识库初具规模（50+ 概念）
- [ ] 产出 3 个有价值的内容
- [ ] 感受到复利效应开始显现

## 获取帮助

### 系统内帮助
1. 阅读 `AGENTS.md` 了解 AI 交互规则
2. 检查 `.claude-context/help/` 获取最新指南
3. 使用命令："系统帮助" 或 "如何使用 [功能]"

### 外部资源
- Obsidian 官方文档
- Claude Code 使用指南
- 知识管理相关社区

### 反馈和改进
发现问题或有改进建议？
1. 记录到 `D&H&R/Outputs/feedback/system-feedback.md`
2. 与 AI 讨论改进方案
3. 更新系统文档

---

**最后提醒**：系统的价值在于持续使用。每天花 15 分钟，坚持 30 天，您将看到明显的复利效应。

开始您的知识复利之旅吧！