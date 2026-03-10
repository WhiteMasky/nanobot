# 🛠️ 技能清单 (Skills Manifest)

**最后更新**: 2026-03-10 01:30  
**总数**: 20+ 技能

---

## 📊 分类统计

| 分类 | 数量 | 状态 |
|------|------|------|
| 阿里云百炼 | 6 | ✅ 完成 |
| 飞书集成 | 3 | ✅ 完成 |
| GitHub | 2 | ✅ 完成 |
| 数据处理 | 3 | ✅ 完成 |
| 内容创作 | 5 | ✅ 完成 |
| 工具实用 | 4 | ✅ 完成 |

---

## 🤖 阿里云百炼 Skills

| 技能 | 文件 | 功能 | 状态 |
|------|------|------|------|
| 图像生成 | `bailian_image.py` | 文生图 (wanx-v1) | ✅ |
| 语音合成 | `bailian_tts.py` | 文字转语音 (cosyvoice-v1) | ✅ |
| 语音识别 | `bailian_stt.py` | 语音转文字 (paraformer-v2) | ✅ |
| 视频生成 | `bailian_video.py` | 文生视频 (wanx-v2-video) | ✅ |
| 多模态 | `bailian_multimodal.py` | 图像理解 | ✅ |
| PPT 生成 | `ppt_generator.py` | 演示文稿生成 | ✅ |

**API Key**: `sk-24486854cd0447b3973602d22fe43004`  
**API Base**: `https://dashscope.aliyuncs.com/api/v1`

---

## 💬 飞书集成 Skills

| 技能 | 文件 | 功能 | 状态 |
|------|------|------|------|
| 消息推送 | `feishu_messenger.py` | 文本/卡片/文件/图片 | ✅ |
| 财经监控 | `smart_event_monitor.py` | 事件驱动交易监控 | ✅ |
| 财经推送 | `finance_monitor_feishu.py` | 财经快讯推送 | ✅ |

**Webhook**: 需配置  
**API Token**: 需配置

---

## 🔗 GitHub Skills

| 技能 | 文件 | 功能 | 状态 |
|------|------|------|------|
| GitHub 操作 | `github_ops.py` | 搜索/Trending/Issues/PRs | ✅ |
| GitHub 集成 | `github/` (内置) | gh CLI 集成 | ✅ |

**Token**: 可选 (通过 `GITHUB_TOKEN` 环境变量)

---

## 📈 数据处理 Skills

| 技能 | 文件 | 功能 | 状态 |
|------|------|------|------|
| PDF 工具 | `pdf_tools.py` | PDF 转文本/Markdown/合并/拆分 | ✅ |
| 图表生成 | `chart_generator.py` | 数据图表生成 | ✅ |
| 网页抓取 | `web_scraper.py` | 网页内容提取 | ✅ |

**依赖**: `pypdf` (PDF 工具需要)

---

## ✍️ 内容创作 Skills

| 技能 | 文件 | 功能 | 状态 |
|------|------|------|------|
| 海报生成 | `poster_generator.py` | 营销海报设计 | ✅ |
| 社交文案 | `social_copywriting.py` | 社交媒体文案 | ✅ |
| 工作流 | `workflow_automation.py` | 技能组合工作流 | ✅ |
| 图片生成 | `generate_cat.py` | 猫咪图片生成 | ✅ |
| 图片生成 | `generate_tiger.py` | 老虎图片生成 | ✅ |

---

## 🛠️ 工具实用 Skills

| 技能 | 文件 | 功能 | 状态 |
|------|------|------|------|
| 待办管理 | `todo_manager.py` | 待办事项管理 | ✅ |
| 笑话推送 | `joke_pusher.py` | 定时笑话推送 | ✅ |
| 财经监控 | `finance_monitor.py` | 财经新闻抓取 | ✅ |
| 图片下载 | `download_cat.py` | 图片下载工具 | ✅ |

---

## 📦 ClawHub 已安装 Skills

| 技能 | 来源 | 状态 |
|------|------|------|
| tavily-search | ClawHub | ✅ |
| cron | 内置 | ✅ |
| memory | 内置 | ✅ |
| weather | 内置 | ✅ |
| skill-creator | 内置 | ✅ |
| capability-evolver | ClawHub | ✅ |

---

## ⏳ 待安装 Skills (ClawHub)

由于 ClawHub 速率限制，以下技能待安装：

### 飞书相关
- [ ] feishu-bridge
- [ ] feishu-messaging
- [ ] lark-integration
- [ ] feishu-card
- [ ] feishu-file-sender

### 阿里云相关
- [ ] bailian-web-search
- [ ] bailian-search
- [ ] bailian-knowledge-retrieve
- [ ] qwen-image
- [ ] qwen-audio
- [ ] aliyun-tts

### 数据处理
- [ ] nano-pdf
- [ ] pdf-text-extractor
- [ ] pdf-ocr

### 搜索
- [ ] ddg-web-search
- [ ] brave-api-search

### 语音
- [ ] openai-tts
- [ ] mlx-stt
- [ ] local-stt

### 图像
- [ ] ai-image-generation
- [ ] fal-text-to-image

---

## 🚀 使用示例

### 阿里云百炼 - 图像生成
```bash
python skills/bailian_image.py --prompt "一只可爱的猫咪" --output cat.png
```

### 飞书 - 消息推送
```bash
python skills/feishu_messenger.py --text "Hello World" --webhook YOUR_WEBHOOK
```

### GitHub - 搜索仓库
```bash
python skills/github_ops.py --search "machine learning" --limit 10
```

### PDF - 转文本
```bash
python skills/pdf_tools.py --to-text document.pdf
```

### 待办 - 添加事项
```bash
python skills/todo_manager.py --add "完成项目报告" --priority high --due 2026-03-15
```

### 网页抓取
```bash
python skills/web_scraper.py https://example.com --markdown --save
```

---

## 📝 配置说明

### 环境变量
```bash
# GitHub Token (可选)
set GITHUB_TOKEN=your_github_token

# 飞书 Webhook (在脚本中配置)
FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/...

# 飞书 API Token (用于上传文件)
FEISHU_API_TOKEN=your_api_token
```

### 依赖安装
```bash
# PDF 工具依赖
pip install pypdf

# 其他依赖 (通常已安装)
pip install requests
```

---

## 🔄 更新历史

### 2026-03-10 01:30 - 自我迭代会话
- ✅ 创建 `feishu_messenger.py` - 飞书消息推送
- ✅ 创建 `github_ops.py` - GitHub 操作
- ✅ 创建 `pdf_tools.py` - PDF 处理
- ✅ 创建 `todo_manager.py` - 待办管理
- ✅ 创建 `web_scraper.py` - 网页抓取
- ✅ 创建 `smart_event_monitor.py` - 智能事件监控
- ✅ 创建 `SMART_EVENT_MONITOR.md` - 监控技能文档
- ✅ 配置定时任务 (每天 5 次：09:00, 12:00, 15:00, 18:00, 21:00)

### 2026-03-10 00:00 - 百炼技能会话
- ✅ 创建 `bailian_image.py` - 图像生成
- ✅ 创建 `bailian_tts.py` - 语音合成
- ✅ 创建 `bailian_stt.py` - 语音识别
- ✅ 创建 `bailian_video.py` - 视频生成
- ✅ 创建 `ppt_generator.py` - PPT 生成
- ✅ 创建 `poster_generator.py` - 海报生成
- ✅ 创建 `chart_generator.py` - 图表生成
- ✅ 创建 `social_copywriting.py` - 社交文案
- ✅ 创建 `workflow_automation.py` - 工作流自动化

---

## 📞 支持

遇到问题？查看各技能的详细文档：
- `ALIBABA_BAILIAN_SKILLS.md` - 百炼技能配置
- `SMART_EVENT_MONITOR.md` - 事件监控技能
- 各技能同目录下的 `.md` 文件

---

*Last updated: 2026-03-10 01:30*
