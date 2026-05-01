# 摄取技能和工具指南

## 概述

本目录包含用于**摄取阶段**的各种技能、工具和方法。摄取阶段的目标是将外部输入（网页、推文、视频、播客等）标准化为统一的Markdown格式。

## 核心原则

1. **技能化**：将常见的摄取任务封装为可复用的技能
2. **文档化**：每个技能都有详细的使用说明和示例
3. **可扩展**：遇到新的内容类型时，研究并添加新技能
4. **开源协作**：参考和贡献到开源技能库

## 已确认的技能和工具

### 1. 通用网页抓取

#### r.jina.ai
- **用途**：快速抓取网页文本内容
- **方法**：`https://r.jina.ai/{URL}`
- **示例**：`https://r.jina.ai/https://twitter.com/username/status/123456`
- **特点**：绕过部分登录墙，返回清洁文本
- **限制**：可能遇到反爬虫机制

#### 浏览器自动化
- **工具**：Playwright、Puppeteer
- **用途**：处理JavaScript渲染的页面
- **时机**：当静态抓取失败时使用

### 2. X (Twitter) 抓取

#### 方法一：r.jina.ai
```bash
curl "https://r.jina.ai/https://twitter.com/username/status/123456"
```

#### 方法二：官方JSON API
```bash
curl "https://cdn.syndication.twimg.com/tweet-result?id=123456"
```
- **返回**：JSON格式，包含完整推文数据
- **优势**：官方API，稳定性高
- **注意**：需要推文ID，不是完整的URL

#### 方法三：Twitter API
- **正式方法**：使用Twitter开发者API
- **要求**：API密钥，速率限制
- **适用**：大量抓取需求

### 3. YouTube 视频转录

#### youtube-transcript 技能
- **来源**：https://github.com/badlogic/pi-skills
- **安装**：下载并配置到Claude Code技能系统
- **功能**：获取YouTube视频的完整字幕
- **输出**：纯文本，无需时间戳

#### 替代方案
1. **YouTube Data API**：官方API，需要密钥
2. **第三方服务**：如YouTube Transcript API
3. **手动转录**：AI辅助听写

### 4. 播客音频转录

#### 获取转录稿的方法
1. **查找现有转录**：播客网站、第三方转录网站
2. **自动语音识别**：使用Whisper、Deepgram等ASR服务
3. **视频版本**：有些播客有YouTube视频版本，可获取字幕
4. **人工转录**：外包或自行听写

#### 推荐工具
- **Whisper**：开源的语音识别模型
- **Deepgram**：商业API，准确率高
- **Rev.com**：人工转录服务

### 5. 学术论文和PDF

#### PDF提取工具
1. **pdfplumber**：Python库，提取文本和表格
2. **PyPDF2**：基础PDF操作
3. **Adobe Acrobat**：商业软件，OCR功能强
4. **在线转换器**：Smallpdf、iLovePDF等

#### 学术数据库
- **arXiv**：开放获取，提供PDF和LaTeX源
- **Google Scholar**：元数据搜索
- **PubMed**：生物医学文献
- **IEEE Xplore**：工程和计算机科学

### 6. 社交媒体平台

#### Reddit
- **官方API**：需要应用注册
- **Pushshift**：历史数据存档
- **r.jina.ai**：简单抓取

#### LinkedIn
- **难度**：高，严格的反爬虫
- **建议**：使用官方API或手动保存

#### 微信公众号
- **难度**：非常高，需要微信客户端
- **建议**：手动保存或使用授权工具

## 技能开发流程

### 遇到新内容类型的处理流程

```
发现新内容类型 → 研究获取方法 → 测试验证 → 文档化 → 集成到系统
```

#### 1. 研究阶段
- 分析内容结构和访问方式
- 查找现有工具和API
- 测试不同的抓取方法
- 评估稳定性和合法性

#### 2. 开发阶段
```bash
# 创建新技能目录
mkdir -p skills/ingestion/new-platform/

# 编写技能文档
cat > skills/ingestion/new-platform/README.md << 'EOF'
# 新平台抓取技能

## 平台特点
- 内容类型：
- 访问方式：
- 反爬虫措施：

## 获取方法
### 方法一：XXX
步骤：
1. 
2. 
3. 

### 方法二：YYY
...

## 代码示例
```python
# 示例代码
```

## 注意事项
- 限制：
- 错误处理：
- 合规性：
EOF
```

#### 3. 测试阶段
- 使用真实内容测试
- 验证数据完整性
- 检查错误处理
- 评估性能

#### 4. 集成阶段
- 更新AGENTS.md中的处理指南
- 添加模板示例
- 培训AI使用新技能
- 监控使用效果

### 技能贡献规范

#### 技能文档结构
```
技能名称/
├── README.md          # 技能说明
├── examples/          # 示例文件
│   ├── example1.md    # 成功示例
│   └── example2.md    # 边界情况示例
├── scripts/           # 脚本文件
│   ├── extract.py     # 提取脚本
│   └── config.json    # 配置文件
└── tests/             # 测试用例
    └── test_basic.md  # 测试文件
```

#### README.md 模板
```markdown
# [平台名称] 抓取技能

## 概述
简要说明技能用途和适用场景。

## 获取方法
### 推荐方法
步骤和说明。

### 备选方法
其他可行方案。

## 代码示例
```python
# 实际代码
```

## 配置要求
- 依赖库：
- API密钥：
- 环境变量：

## 使用示例
```bash
# 命令行使用示例
```

## 常见问题
### Q: 遇到登录墙怎么办？
A: 解决方法...

### Q: 内容不完整怎么办？
A: 解决方法...

## 性能指标
- 成功率：X%
- 平均耗时：Y秒
- 数据完整度：Z%

## 更新日志
- 2026-04-14: 初始版本
```

## 工具集配置

### Claude Code 集成

#### 环境变量配置
```bash
# 设置技能路径
export CLAUDE_SKILLS_PATH="$WORKSPACE/skills"

# 设置临时目录
export CLAUDE_TEMP_PATH="$WORKSPACE/.claude-context/temp"
```

#### 技能自动加载
```json
// Claude Code 配置
{
  "skills": {
    "autoLoad": true,
    "paths": [
      "f:/Obsidian-writing everything down/BASES/workspace/skills",
      "~/.claude/skills"
    ]
  }
}
```

### 常用命令别名

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias ingest-web="claude --skill ingestion/web"
alias ingest-x="claude --skill ingestion/x"
alias ingest-youtube="claude --skill ingestion/youtube"
alias ingest-podcast="claude --skill ingestion/podcast"
```

## 故障排除

### 常见问题

#### 1. 抓取内容不完整
**可能原因**：
- 页面需要JavaScript渲染
- 内容分页加载
- 反爬虫机制触发

**解决方案**：
1. 使用浏览器自动化工具
2. 检查是否有分页参数
3. 添加请求头模拟浏览器
4. 降低请求频率

#### 2. 遇到登录墙
**解决方法**：
1. 查找公开的镜像站
2. 使用r.jina.ai等绕过工具
3. 手动登录后保存
4. 考虑是否值得绕过

#### 3. 内容格式混乱
**处理方法**：
1. 使用HTML解析器（BeautifulSoup）
2. 应用正则表达式清理
3. 手动标注混乱部分
4. 在Capture Notes中说明

### 错误处理策略

#### 分级处理
1. **轻度错误**：内容部分缺失，记录在Capture Notes中
2. **中度错误**：主要内容缺失，尝试备选方法
3. **严重错误**：完全无法获取，记录原因并跳过

#### 重试机制
```python
# 示例重试逻辑
max_retries = 3
for attempt in range(max_retries):
    try:
        content = fetch_content(url)
        if validate_content(content):
            return content
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)  # 指数退避
```

## 合规性和伦理

### 法律合规
1. **遵守robots.txt**：尊重网站的爬虫协议
2. **尊重版权**：仅用于个人学习，不用于商业分发
3. **限制频率**：避免对服务器造成负担
4. **数据最小化**：只获取必要内容

### 伦理准则
1. **透明度**：在Capture Notes中说明获取方法
2. **尊重隐私**：不抓取个人信息
3. **注明来源**：始终保留原始出处
4. **合理使用**：符合合理使用原则

### 风险规避
1. **使用公开API**：优先使用官方接口
2. **获取授权**：必要时联系内容所有者
3. **本地缓存**：避免重复请求
4. **监控变化**：定期检查技能有效性

## 技能更新和维护

### 定期检查
- **每月**：检查所有技能的有效性
- **每季度**：更新文档和示例
- **每年**：全面评估技能架构

### 社区贡献
1. **发现问题**：在技能目录中创建issue
2. **提交改进**：通过Pull Request贡献代码
3. **分享经验**：在示例目录中添加新案例
4. **文档协作**：共同完善使用指南

### 技能生命周期管理
```
新技能 → 测试验证 → 正式发布 → 维护更新 → 归档淘汰
    ↓          ↓          ↓          ↓          ↓
  研发期    验证期    稳定期    维护期    归档期
```

## 快速开始

### 第一步：安装基础工具
```bash
# 安装Python依赖
pip install beautifulsoup4 requests playwright

# 安装Playwright浏览器
playwright install chromium
```

### 第二步：测试第一个技能
```bash
# 测试网页抓取
curl "https://r.jina.ai/https://example.com/article" > test.md

# 检查输出格式
cat test.md | head -20
```

### 第三步：创建你的第一个技能
```bash
# 创建新技能目录
mkdir -p skills/ingestion/my-platform/

# 编写技能文档
vim skills/ingestion/my-platform/README.md
```

### 第四步：集成到工作流
1. 更新`AGENTS.md`中的处理指南
2. 添加模板示例到`raw/_template.md`
3. 测试完整摄取流程
4. 记录使用经验

---

**记住**：技能是系统的延伸，好的技能能让摄取工作事半功倍。遇到困难时，研究、实验、文档化，然后分享给社区。