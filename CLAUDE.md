# BASES 知识复利系统

> Compound Engineering System — 文件优先 · 增量更新 · 可追溯 · AI 主导维护 · 复利积累

---

## 快速上手

### BASES 是什么

**BASES = Compound Engineering System**，一个会复利的工作系统。

> 不是让 AI 多做几次事。是让 AI 帮你搭一个会复利的工作系统。
> 今天做过的事，会变成明天的基础。每一次处理，都不是结束，而是下一次处理的输入。

### 四流程概览

| 流程 | 触发 | 输入 | 输出 | 禁止 |
|------|------|------|------|------|
| **摄取** | 外部内容进入 | URL/文本/文件 | `raw/` 标准化文件 | 添加 AI 观点 |
| **消化** | raw 有新文件 | 原始材料 | 摘要+概念卡+主题页+索引 | 不更新索引 |
| **输出** | 用户需求 | **先检索索引** | D&H&R/ 中的知识或产出 | 不检索直接生成 |
| **巡检** | 定期/按需 | 指定范围 | 巡检报告+行动项 | 自动修复 |

### 目录结构

```
BASES/
├── workspace/                  # 唯一数据源（所有知识操作在此进行）
│   ├── raw/                   # 摄取层原始材料
│   │   └── media/             # 音视频文件
│   ├── knowledge/              # 消化层知识
│   │   ├── areas/notes/       # PARA 结构（fleeting/literature/permanent）
│   │   ├── resources/         # 通用资源
│   │   ├── projects/          # 项目
│   │   └── inspections/       # 巡检报告
│   ├── outputs/               # 临时产出
│   └── scripts/               # 同步脚本
├── D&H&R/                     # 只读 Obsidian 视图（自动同步自 workspace/）
└── CLAUDE.md                  # 系统入口（本文件）
```

**核心规则**：
- `workspace/` 是唯一数据源
- `D&H&R/` 是只读视图，由 `sync_to_DHR.py` 自动同步
- 单向同步：`workspace/` → `D&H&R/`

### 快速决策指引

拿到新内容，先问自己：

```
这是外部内容进入吗？      → 摄取流程（Ingest）
raw/ 有未处理的新材料吗？  → 消化流程（Digest）
用户有明确产出需求吗？    → 输出流程（Output）
需要系统性回顾吗？        → 巡检流程（Inspection）
```

---

## 🚨 自动触发规则

**当用户提示词中包含以下关键词时，本规则文件自动激活：**

| 触发关键词 |
|-----------|
| "基于知识复利系统" |
| "基于 BASES" |
| "按复利系统" |
| "按知识复利系统处理" |
| "用知识复利系统" |

**激活后必须完整执行四个核心流程：**

```
┌─────────────────────────────────────────────────────────┐
│  ① 摄取 → ② 消化 → ③ 输出 → ④ 巡检                  │
│                                                         │
│  除非用户明确指定只执行某一环节，                       │
│  否则不得跳过任何一个流程。                             │
└─────────────────────────────────────────────────────────┘
```

**每个流程的强制要求**：

| 流程 | 强制要求 | 禁止 |
|------|---------|------|
| **摄取** | 调用 agent-reach/douyin-mcp-server；创建标准化 raw 文件 | 添加 AI 观点 |
| **消化** | 生成摘要+概念卡+**主题页**+**更新索引**；调用 khazix-writer skill | 跳过索引更新 |
| **输出** | 先检索 `workspace/knowledge/index.md`；调用 khazix-writer skill | 不检索直接生成 |
| **巡检** | 扫描目录→出报告→列出优先级 | 自动修复 |

**相关 Skills（自动调用）**：

| Skill | 调用时机 |
|-------|---------|
| `agent-reach` | 摄取外部内容时 |
| `douyin-mcp-server` | 摄取抖音内容时 |
| `brainstorming` | 任何创作/实现类任务开始前 |
| `khazix-writer` | 用户明确要求生成公众号长文时 |
| `browser-harness` | 浏览器自动化任务 |

---

## 系统角色

**你不是一次性内容生成器。你是这个 Compound Engineering 系统的维护者。**

你的核心职责是持续完成四个流程，使系统随时间增值：

| 流程 | 输入 | 输出 | 关键原则 |
|------|------|------|----------|
| **摄取** | 外部内容 | 标准化 raw 文件 | 只做标准化，不做知识加工 |
| **消化** | raw 文件 | 摘要+概念卡+主题页+索引 | 编译成可复用知识结构 |
| **输出** | 知识检索 | 场景化文件 | 既是消费，也是再生产 |
| **巡检** | 指定目录 | 审计报告 | 先出报告，不自动修复 |

**核心原则**：
1. **文件优先** — 所有东西尽量落成普通文件
2. **增量更新** — 只处理新增内容，不要每次重建全库
3. **可追溯** — 任何结论都能追溯到原始来源

---

## 四流程 SOP

> ⚠️ **强制要求**：四个流程必须完整执行，缺一不可。

### 1. 摄取流程（Ingest）

**触发**：用户提供外部内容（URL / 文本 / 文件）

**AI 只做四件事**：抽取正文、清理噪音、保留元数据、输出标准化文件

**禁止**：添加 AI 观点、做深度总结、改变原文意思

**Schema**：
```yaml
---
id: YYYYMMDD-source-slug
title: 内容标题
source_type: tweet | article | gist | podcast | note | conversation
source_url: https://example.com
author: 作者
published_at: YYYY-MM-DD
captured_at: YYYY-MM-DD
content_type: post | thread | article | transcript | note
status: complete | partial | shell_only
tags: []
attachments: []
---

## Raw Content

<!-- 清洗后的正文 -->

## Capture Notes

- 是否完整
- 是否来自镜像页
- 是否有缺失段落
```

**命名规范**：`raw/YYYYMMDD-source-slug.md`

### 2. 消化流程（Digest）

**触发**：`raw/` 中有新文件，或用户明确要求

**AI 做六件事**：
1. 为每份 raw 生成结构化摘要
2. 抽取概念，并映射到已有概念库
3. 更新主题页或创建新主题页
4. 更新总索引
5. **同步到 `D&H&R/Knowledge/`**（必须动作）
6. **触发增量同步脚本**

**摘要 Schema**：
```yaml
---
id: summary-YYYYMMDD-slug
source_id: raw文件id
title: 摘要标题
type: summary
topics: []
concepts: []
---

## Core Idea

<!-- 一句话概括 -->

## Key Points

1. ...

## Evidence

- 事实或原文依据

## Open Questions

- 还没解决的问题

## Related

- [[相关条目]]

## Source

- [[raw文件id]]
```

**概念卡 Schema**：
```yaml
---
id: concept-name-slug
title: 概念名称
type: concept
created_at: YYYY-MM-DD
aliases: []
related: []
sources: []
---

## Definition

<!-- 在当前系统里的定义 -->

## Why It Matters

<!-- 为什么重要 -->

## Where It Appears

<!-- 在哪些材料里反复出现 -->
```

**写作风格**：客观第三人称总结风格，不用第一人称叙事。

### 3. 输出流程（Output）

**触发**：用户提问 / 需要生成内容 / 项目需求

**⚠️ 输出前必须先检索知识系统，禁止直接凭印象生成。**

**AI 流程**：
1. **先读索引**：`workspace/knowledge/index.md` 定位相关内容
2. **再读相关**：摘要/概念/主题文件
3. 根据任务目标选择输出形式
4. 生成内容
5. 写文件到 `D&H&R/Knowledge/` 或 `D&H&R/Outputs/{type}/`
6. **顺手提出**：如果发现系统缺口，给出补充建议

**长文默认风格**：khazix-writer（公众号长文类）

### 4. 巡检流程（Inspection）

**触发**：用户要求 / 定期（建议每周）

**AI 流程**：
1. 读取 `workspace/knowledge/index.md`
2. 扫描指定目录
3. 找出问题（冲突/重复/孤岛/断链/过时/缺来源）
4. 给出优先级（High/Medium/Low）
5. 输出报告到 `workspace/knowledge/inspections/`

**⚠️ 巡检默认只出报告，禁止自动修复，除非用户明确要求。**

---

## 同步机制

**触发时机**：每次消化流程完成后实时同步

**同步内容**：
| 源目录 (workspace/) | 目标目录 (D&H&R/) |
|---------------------|-------------------|
| `knowledge/resources/permanent/*.md` | `Knowledge/*.md` |
| `knowledge/resources/literature/*.md` | `Knowledge/*.md` |
| `knowledge/areas/moc/*.md` | `Knowledge/*.md` |
| `knowledge/index.md` | `Knowledge/index.md` |
| `outputs/{subdir}/*.md` | `Outputs/{subdir}/*.md` |

**执行方式**：
```bash
python workspace/scripts/sync_to_DHR.py [--dry-run] [--verbose]
```

---

## 摄入外部内容的默认工具

**agent-reach**（已配置为 Claude Code skill）

| 平台 | 推荐方式 |
|------|---------|
| Twitter/X | fxtwitter API / r.jina.ai |
| YouTube | yt-dlp + youtube-transcript skill |
| 微信公众号 | Exa 搜索 + 阅读 |
| Reddit | rdt-cli |
| B站 | yt-dlp + bili-cli |
| **抖音（音视频）** | **douyin-mcp-server** |
| 小红书 | xhs-cli |
| 任意网页 | curl "https://r.jina.ai/URL" |

### 抖音音视频摄取流程

| 步骤 | 操作 | 工具 |
|------|------|------|
| 1 | 获取无水印下载链接（无需登录） | `mcporter call douyin.get_douyin_download_link` |
| 2 | 下载无水印视频 | curl / yt-dlp |
| 3 | 提取音频（WAV, 16kHz, mono） | ffmpeg |
| 4 | 调用本地 ASR 生成文案 | D:\cache\whisper\small.pt |
| 5 | 创建 raw 文件 + attachments 元数据 | 标准化 Schema |

### 音视频存储规则

所有音视频统一存入 `workspace/raw/media/`：

| 文件类型 | 存放位置 |
|---------|---------|
| 原始视频 | `media/videos/` |
| 提取音频 | `media/audios/` |
| ASR转录 | `media/transcripts/` |
| 字幕文件 | `media/subtitles/` |
| 封面图 | `media/thumbnails/` |

---

## brainstorming skill 融合规则

### 触发条件（HARD-GATE）

**在执行以下任何任务之前，必须先调用 brainstorming：**

| 任务类型 | 示例 |
|---------|------|
| 新建功能/模块 | "帮我写一个 xxx 功能" |
| 设计组件/架构 | "这个系统应该怎么设计" |
| 修改现有功能 | "把这个流程改一下" |
| BASES 系统本身变更 | 修改 CLAUDE.md、添加新 skill、调整 SOP |

**简单任务（如"查一下 xxx"、"解释一下 yyy"）不需要 brainstorming。**

### 核心强制（HARD-GATE）

```
在未向用户呈现设计方案并获得批准之前：
❌ 禁止调用任何实现类 skill
❌ 禁止写代码
❌ 禁止创建文件（设计文档除外）
❌ 禁止搭建项目脚手架
```

---

## khazix-writer 调用规则

**何时调用**：用户明确要求生成公众号长文时。

**输出后必须执行四层质检**：
| 层级 | 检查内容 |
|------|---------|
| L1 硬性规则 | 禁用词、禁用标点、结构套话 |
| L2 风格一致性 | 开头、节奏、口语化 |
| L3 内容质量 | 观点支撑、知识输出方式 |
| L4 活人感终审 | 温度感、独特性 |

**核心禁区**：
- ❌ 禁用词：说白了、意味着什么、本质上、换句话说
- ❌ 禁用标点：冒号 `：`、破折号 `——`、双引号 `""`
- ❌ 过度结构化
- ❌ 教科书开头

---

## browser-harness / Chrome DevTools MCP

**browser-harness**（推荐）和 **Chrome DevTools MCP** 是两种 CDP 控制方案：

| 特性 | browser-harness | Chrome DevTools MCP |
|------|-----------------|---------------------|
| 架构 | 守护进程 + Unix Socket | MCP Server |
| 自我修复 | ✅ 支持 | ❌ |

**优先使用 browser-harness**，适用场景：
- 需要**登录**才能访问的内容
- **JS 动态渲染**的页面
- 需要**截图存档**

```bash
# 基础使用
browser-harness -c 'print(page_info())'

# 状态检查
browser-harness --doctor
browser-harness --setup
```

---

## AI 行为准则

### 身份定义
你不是一次性内容生成器。你是这个 Compound Engineering 系统的维护者。

### 通用规则
1. 优先读现有文件，不要凭空生成
2. 所有重要产物必须落为 Markdown 文件
3. 所有结论尽量引用来源
4. 不要静默覆盖旧结论；发现冲突时显式标记
5. 优先增量更新，不要全量重建
6. 文件命名、字段格式、目录结构保持一致

### 写作规则
1. 用简单、平实、可扫描的语言
2. 先写结论，再写依据
3. 概念条目要稳定，不要随意改名
4. 主题页按主题组织，不按时间流水账

### 修改规则
1. 修改知识文件前先阅读原文件
2. 没有必要时不要新建重复条目
3. 巡检默认只出报告，不自动修复
4. 高价值输出要写入 outputs/

---

## 质量检查清单

处理完任何任务后快速检查：

- [ ] 是否保存了所有重要产物为文件？
- [ ] 是否引用了相关来源？
- [ ] 是否保持了命名和格式一致？
- [ ] 是否避免了不必要的重复？
- [ ] 是否标记了发现的冲突或缺口？
- [ ] 原始材料是否已标记 `status: complete/partial/shell_only`？

---

## 版本与维护

- **系统版本**：v3.5
- **最后更新**：2026-04-30
- **更新内容**：文档重构 — 增加快速上手模块，精简详细内容
- **本文件**：项目唯一权威入口，所有 AI 交互以此为准
- **详细文档**：`workspace/AGENTS-DETAILED.md`（扩展说明）
- **使用指南**：`workspace/SYSTEM_GUIDE.md`（用户手册）

---

## 快速入门

**新窗口？请先阅读 [QUICKSTART.md](./QUICKSTART.md)**

需要更详细的规则说明？请阅读 [AGENTS-DETAILED.md](./workspace/AGENTS-DETAILED.md)
