---
name: browser-harness
description: 极简自我修复浏览器控制工具，通过CDP给LLM完全自由完成任何浏览器任务
---

# Browser Harness Skill

> 通过 CDP（Chrome DevTools Protocol）直接控制浏览器，Agent 可以在任务中途写入缺失的辅助代码实现自我修复。

## 核心定位

**给 LLM 完全的自由通过 CDP 完成任何浏览器任务。**

- 无框架、无配方、无护栏
- 一个 WebSocket 直连 Chrome
- Agent 可在任务中途扩展能力（写入 `agent-workspace/agent_helpers.py`）

## 架构

```
Chrome → CDP WS → browser_harness.daemon → /tmp/bu-<NAME>.sock → browser_harness.run
```

## 常用命令

```bash
# 基础使用
browser-harness -c 'print(page_info())'

# 新标签页
browser-harness -c '
new_tab("https://example.com")
wait_for_load()
'

# 截图驱动探索
browser-harness -c '
capture_screenshot()
'

# DOM 操作
browser-harness -c '
js("document.querySelector(\"#title\").textContent")
'

# 坐标点击（通过 iframe/shadow DOM/cross-origin）
browser-harness -c '
click_at_xy(x, y)
'

# 滚动
browser-harness -c '
scroll_to(0, 500)
'
```

## 核心原则

1. **坐标点击优先** — compositor 级别通过 iframe/shadow DOM/cross-origin
2. **截图驱动探索** — 比 DOM 查找更快，避免 selector 脆弱性
3. **截图验证** — 每次有意义的操作后重新截图确认
4. **复用用户 Chrome** — 继承登录态，避免账号风险

## 交互技能（interaction-skills/）

| 技能 | 用途 |
|------|------|
| `tabs.md` | 标签页管理 |
| `cookies.md` | Cookie 操作 |
| `uploads.md` | 文件上传 |
| `dialogs.md` | 对话框处理 |
| `dropdowns.md` | 下拉框 |
| `iframes.md` | 跨域 iframe |
| `shadow-dom.md` | Shadow DOM |
| `screenshots.md` | 截图 |
| `scrolling.md` | 滚动 |

## 领域技能（domain-skills/）

任务中发现非显而易见的模式时，贡献到 `agent-workspace/domain-skills/<site>/`：

- URL 模式和查询参数
- 私有 API 及 payload 结构
- 稳定选择器（data-*, aria-*, role）
- 框架怪癖
- 等待条件及原因
- 陷阱和失效选择器

## 自我修复回路

```
Agent 执行任务 → 发现缺失 helper →
在 agent_helpers.py 写入新 helper → 任务继续
```

## 部署要求

- Python 3.11+
- Chrome 开启 remote debugging
- 或 Browser Use Cloud 远程浏览器

## 状态检查

```bash
browser-harness --doctor
browser-harness --setup
```
