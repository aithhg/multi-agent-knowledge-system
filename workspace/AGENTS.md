# Compound Engineering AI 规则手册（精要版）

> 本文件是 `../CLAUDE.md` 的精要速查版。实际执行以 `CLAUDE.md` 为准。

---

## 🚨 自动触发规则

**当用户提示词中包含以下关键词时，本规则自动激活，执行完整 SOP 四流程：**

| 触发关键词 |
|-----------|
| "基于知识复利系统" |
| "基于 BASES" |
| "按复利系统" |
| "按知识复利系统处理" |
| "用知识复利系统" |

**激活后强制执行**：

| 流程 | 必须执行的操作 |
|------|--------------|
| **摄取** | agent-reach/douyin-mcp-server + 标准化 raw 文件 |
| **消化** | 摘要+概念卡+**主题页**+**索引**（客观总结风格） |
| **输出** | 先检索 index.md；**brainstorming**（实现类任务）；khazix-writer（仅用户要求公众号长文时） |
| **巡检** | 扫描→出报告→不自动修复 |

**禁止**：跳过任何流程 / 不检索直接生成 / 自动修复

## 系统愿景

**不是让 AI 多做几次事。是让 AI 帮你搭一个会复利的工作系统。**

今天做过的事，会变成明天的基础。每一次处理，都不是结束，而是下一次处理的输入。

---

## 四个核心流程（必须完整执行）

> **⚠️ 强制要求**：四个流程必须完整执行，缺一不可。

| 流程 | 触发 | 输入 | 输出 | 禁止 |
|------|------|------|------|------|
| **摄取** | 用户提供外部内容 | URL/文本/文件 | `raw/YYYYMMDD-source-slug.md` | 添加AI观点 |
| **消化** | raw 有新文件 | 原始材料 | 摘要+概念卡+**主题页**+**索引** | 不更新索引 |
| **输出** | 用户提问/需求 | **先检索索引** | `D&H&R/Knowledge/` 或 `Outputs/{type}/` | 不检索直接作答 |
| **巡检** | 用户要求/每周 | 指定目录 | `knowledge/inspections/inspection-*.md` | 自动修复 |

---

## 目录结构（已验证）

```
BASES/
├── D&H&R/                     # 默认输出仓库
│   ├── Outputs/{article,memo,social,ppt,infographic,pdf,artifacts,drafts,published,feedback}/
│   ├── Knowledge/             # 精选知识卡
│   └── {LLM,Occupation,国产模型}/  # 专题输出
└── workspace/
    ├── raw/YYYYMMDD-source-slug.md
    ├── knowledge/
    │   ├── areas/notes/{fleeting,literature,permanent}/
    │   ├── resources/{literature,permanent,references}/
    │   ├── projects/{moc,notes/}
    │   ├── inspections/
    │   └── index.md
    └── outputs/              # 已迁移导向 D&H&R/Outputs/
```

---

## 摄取规范（摄取触发时必读）

### 命名：`raw/YYYYMMDD-source-slug.md`
- ✅ `20260414-twitter-karpathy-llm-kb.md`
- ❌ `20260414-example-001.md`（无意义 slug）

### Schema
```yaml
---
id: YYYYMMDD-source-slug
title: 内容标题
source_type: x | article | gist | podcast | note | conversation
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

### 摄取禁止行为
- ❌ 添加 AI 观点
- ❌ 深度总结或概念抽取（那是消化阶段的事）
- ❌ 改写原文意思

### 摄取阶段 AI 只做四件事
1. 抽取正文
2. 清理噪音
3. 保留元数据
4. 输出标准化文件

### 抖音音视频摄取特殊规则

**核心流程**：douyin-mcp-server → 获取无水印链接 → 下载 → 提取音频 → 本地 ASR 转写

| 步骤 | 操作 | 工具 |
|------|------|------|
| 1 | 获取无水印下载链接 | `mcporter call douyin.get_douyin_download_link` |
| 2 | 下载视频 | curl |
| 3 | 提取音频 | ffmpeg |
| 4 | ASR 转写 | Python + D:\cache\whisper\small.pt |
| 5 | 创建 raw + attachments | 标准化 Schema |

**音视频存储**：`workspace/raw/media/{videos,audios,transcripts,subtitles,thumbnails}/`

### 摄入外部内容默认工具（agent-reach）

| 平台 | 方式 | 补充工具 |
|------|------|---------|
| Twitter/X | fxtwitter API / r.jina.ai | — |
| YouTube | yt-dlp + youtube-transcript skill | — |
| 微信公众号 | Exa 搜索 + 阅读 | — |
| Reddit | rdt-cli | — |
| B站 | yt-dlp + bili-cli | — |
| 抖音 | douyin-mcp-server（需 DASHSCOPE_API_KEY） | — |
| 小红书 | xhs-cli | Chrome DevTools MCP（登录页/需交互） |
| 任意网页 | curl "https://r.jina.ai/URL" | Chrome DevTools MCP（JS渲染/登录页） |

#### Chrome DevTools MCP 补充渠道

**适用场景**：需要登录才能访问的内容、JS 动态渲染页面、截图存档

**启动方式**：
```bash
# 直接启动
chrome-devtools-mcp --headless

# 守护进程模式（推荐）
chrome-devtools --daemon
```

**Token 消耗**：高于专用工具，优先使用专用渠道

---

## 消化规范（消化触发时必读）

### AI 在消化阶段做六件事（全部必须执行）
1. 为每份 raw 生成结构化摘要
2. 抽取概念，并映射到已有概念库
3. **更新主题页或创建新主题页**（MOC）
4. **更新总索引**（index.md）
5. **同步到 `D&H&R/Knowledge/`**（必须动作，不可跳过）
6. **触发增量同步脚本**（自动同步所有变更到 D&H&R/）

### 操作顺序
1. 阅读原始材料
2. 输出结构化摘要 → `knowledge/resources/literature/summary-*.md`
3. 抽取关键概念 → `knowledge/areas/notes/permanent/concept-*.md`
4. 判断应更新的主题页（MOC）
5. 给出索引更新建议
6. 更新 `workspace/knowledge/index.md`
7. **写入 `D&H&R/Knowledge/`**（Obsidian 可直接访问）
8. **执行 `python scripts/sync_to_DHR.py`** 同步所有变更
9. 原始材料标记 `status: complete` → `digested`

### 消化原则
- **原子化**：一个文件一个核心概念（Atomic Notes）
- **可链接**：`[[文件名]]` 建立关联
- **可追溯**：标注来源 `@raw/YYYYMMDD-file`
- **不覆盖**：创建新版而非修改旧版
- **Tensions**：主题页记录冲突、差异和未决问题
- **风格**：消化产出的所有文本使用**客观第三人称总结风格**，不使用 khazix-writer 人称叙事

---

## 同步机制

### 数据源原则
- **`workspace/` 是唯一数据源**，所有知识操作在此进行
- **`D&H&R/` 为只读 Obsidian 视图**，由同步脚本自动生成

### 同步触发
- 每次消化流程完成后自动触发
- 可手动执行：`python workspace/scripts/sync_to_DHR.py`

### 同步内容
| 源 (workspace/) | 目标 (D&H&R/) |
|-----------------|---------------|
| `knowledge/resources/permanent/*.md` | `Knowledge/*.md` |
| `knowledge/resources/literature/*.md` | `Knowledge/*.md` |
| `knowledge/areas/moc/*.md` | `Knowledge/*.md` |
| `knowledge/index.md` | `Knowledge/index.md` |
| `outputs/{subdir}/*.md` | `Outputs/{subdir}/*.md` |

### 同步策略
- **增量同步**：基于文件 modification time，仅同步有变化的文件
- **冲突处理**：workspace/ 版本优先
- **不删除**：D&H&R/ 中 workspace/ 没有的文件不删除

### 索引健康度检查
- 执行：`python workspace/scripts/check_index_health.py`
- 检查 index.md 中引用的文件是否存在
- 检查是否存在未被 index 收录的文件
- 生成健康度报告

---

## 输出规范（输出触发时必读）

### 操作顺序
1. 读 `knowledge/index.md` 定位相关内容
2. 读相关摘要/概念/主题
3. 根据任务目标选择输出形式（skill）
4. 生成答案或内容
5. 写入对应目录
6. 顺手列出系统改进建议

### 输出禁止
- ❌ 不检索就直接凭印象作答

### 默认输出目录
- 专题知识 → `D&H&R/{LLM,Occupation,国产模型}/标题.md`
- 通用知识 → `D&H&R/Knowledge/标题.md`
- 格式化输出 → `D&H&R/Outputs/{type}/`

### 输出 skill 类型
- `article/` — 长文（**必须使用 khazix-writer skill**，调用方式见下方）
- `infographic/` — 信息图/视觉卡片
- `pdf/` — PDF 文档
- `ppt/` — 演示文稿
- `memo/` — 备忘录
- `social/` — 社交媒体文案

### khazix-writer skill 调用规则

**调用方式**：
```
Skill: khazix-writer
Args: [素材内容或任务描述]
```

**输出后必须执行四层质检**：
| 层级 | 检查内容 |
|------|---------|
| L1 | 禁用词/禁用标点/结构套话/空泛工具名 |
| L2 | 开头/节奏/口语化/标点禁令 |
| L3 | 观点支撑/知识输出方式/文化升维/对立面 |
| L4 | 温度感/独特性/姿态/心流 |

**核心禁区**：
- ❌ 禁用词：说白了、意味着什么、本质上、换句话说
- ❌ 禁用标点：冒号`：`、破折号`——`、双引号`""`
- ❌ 小标题（方法论分条目除外）
- ❌ 教科书开头

---

## 巡检规范（巡检触发时必读）

### 操作顺序
1. 读取 index
2. 扫描指定目录
3. 找出问题（冲突/重复/孤岛/断链/过时/缺来源）
4. 给出优先级
5. 输出报告 → `knowledge/inspections/inspection-YYYYMMDD-scope.md`

### 报告结构
```markdown
## Findings
### High Priority
### Medium Priority
### Low Priority
## Evidence
## Suggested Fixes
```

### 巡检禁止
- ❌ 不自动修复，除非被明确要求

---

## AI 行为准则

### 身份定义
你不是一次性内容生成器。你是这个 Compound Engineering 系统的维护者。

### 通用规则
1. **优先读现有文件**，不要凭空生成
2. **所有重要产物必须落为 Markdown 文件**
3. **所有结论尽量引用来源**
4. **不要静默覆盖旧结论**；发现冲突时显式标记
5. **优先增量更新**，不要全量重建
6. **保持一致**：文件命名、字段格式、目录结构

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

- [ ] 是否保存了所有重要产物为文件？
- [ ] 是否引用了相关来源？
- [ ] 是否保持了命名和格式一致？
- [ ] 是否避免了不必要的重复？
- [ ] 是否标记了发现的冲突或缺口？
- [ ] 原始材料是否已标记消化状态？

---

## 通用原则

| 原则 | 说明 |
|------|------|
| **文件优先** | 所有东西落为 .md 文件，聊天记录不是资产 |
| **增量更新** | 只处理新增，不重建全库 |
| **可追溯** | 结论引用 `@raw/文件` 或 `[[知识文件]]` |
| **冲突显式标记** | 新旧冲突同时呈现，不偷偷覆盖 |

---

**版本**：v3.4（2026-04-23 更新：增量同步机制、索引自动维护）
**权威入口**：`../CLAUDE.md`
**方法论来源**：Compound Engineering
**详细文档**：`AGENTS-DETAILED.md`（扩展说明）、`SYSTEM_GUIDE.md`（用户手册）

---

## brainstorming skill（HARD-GATE）

> 来源：`skills/brainstorming/SKILL.md`

**触发**：任何创作/实现类任务开始前（新建功能、设计组件、修改行为、BASES 本身变更）。

**HARD-GATE**：未向用户呈现设计方案并获得批准之前，禁止写代码/创建文件/调用实现类 skill。

**流程**：探索上下文 → 评估范围 → 一次一问 → 提出2-3方案 → 分段呈现设计 → 用户批准 → 写设计文档 → 自检 → 用户审阅 → **调用 writing-plans**。
