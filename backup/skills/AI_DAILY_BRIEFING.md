# 📰 AI 产业早报自动生成器

**版本**: 1.0  
**创建时间**: 2026-03-10 01:42  
**定时任务**: 每日 08:00 自动推送  
**Cron Job ID**: `9edd39f8`

---

## 🎯 功能特点

```
┌─────────────────────────────────────────────────────────────┐
│  📊 AI 早报系统                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ 多源新闻搜集                                            │
│     ├─ 海外：The Verge, TechCrunch, MIT Tech Review        │
│     ├─ 国内：机器之心，量子位，AI 科技大本营                    │
│     └─ 官方：OpenAI, Google AI, Anthropic                  │
│                                                             │
│  2️⃣ 智能处理                                                │
│     ├─ 自动摘要（Qwen）                                     │
│     ├─ 重要性评分（⭐⭐⭐⭐⭐）                                 │
│     └─ 分类整理（模型/应用/投资/公司）                      │
│                                                             │
│  3️⃣ 精美图片生成                                            │
│     ├─ 1080x1920 高清图片                                   │
│     ├─ 渐变背景 + 专业排版                                  │
│     └─ 日期/天气/统计信息                                   │
│                                                             │
│  4️⃣ 自动推送                                                │
│     └─ 每日 08:00 飞书自动推送                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速使用

### 方式 1: 手动生成（立即测试）

```bash
python skills/ai_daily_image.py
```

### 方式 2: 指定日期

```bash
python skills/ai_daily_image.py --date 2026-03-10
```

### 方式 3: 测试模式（使用示例数据）

```bash
python skills/ai_daily_image.py --test
```

---

## 📋 输出文件

### 目录结构

```
output/ai_daily/
├── images/                      # 图片目录
│   ├── ai_daily_20260310.png   # 今日早报图片
│   └── ...
├── ai_daily_20260310.json       # 新闻数据
└── ...
```

### 图片示例

- **尺寸**: 1080x1920（手机屏幕比例）
- **格式**: PNG
- **风格**: 渐变紫色背景 + 白色内容区
- **内容**: 标题、日期、分类新闻、重要性评分

### 数据格式

```json
{
  "date": "2026-03-10T00:00:00",
  "news_count": 10,
  "news": [
    {
      "title": "OpenAI 发布 GPT-5，性能提升 10 倍",
      "summary": "OpenAI 今日发布最新大语言模型...",
      "url": "https://openai.com/blog",
      "source": "OpenAI Blog",
      "region": "官方",
      "category": "model",
      "importance": 5
    }
  ]
}
```

---

## ⚙️ 配置说明

### 1️⃣ 飞书 Webhook（可选）

设置环境变量：

```bash
# Windows
set FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx

# 或在脚本中直接配置
FEISHU_WEBHOOK = "https://..."
```

### 2️⃣ DashScope API Key

已配置默认 Key，也可自定义：

```bash
set DASHSCOPE_API_KEY=sk-your-api-key
```

### 3️⃣ 新闻源配置

编辑 `ai_daily_image.py` 中的 `NEWS_SOURCES`：

```python
NEWS_SOURCES = [
    {'name': 'The Verge AI', 'url': 'https://...', 'region': '海外'},
    {'name': '机器之心', 'url': 'https://...', 'region': '国内'},
    # 添加更多源...
]
```

---

## 📊 新闻分类

| 分类 | 关键词 | 图标 |
|------|--------|------|
| 模型 | 模型，model, LLM, GPT, 训练 | 🤖 |
| 应用 | 应用，app, 产品，落地 | 📱 |
| 投资 | 投资，融资，funding, 估值 | 💰 |
| 公司 | 公司，企业，团队，人事 | 🏢 |
| 其他 | 其他新闻 | 📰 |

---

## ⭐ 重要性评分

| 星级 | 说明 | 标准 |
|------|------|------|
| ⭐⭐⭐⭐⭐ | 重磅新闻 | 官方发布 + 重大突破 |
| ⭐⭐⭐⭐ | 重要新闻 | 知名公司 + 重要更新 |
| ⭐⭐⭐ | 普通新闻 | 常规更新 |
| ⭐⭐ | 简讯 | 短消息 |
| ⭐ | 次要 | 其他 |

---

## 🔄 定时任务

### 当前配置

| 项目 | 值 |
|------|-----|
| **Cron 表达式** | `0 8 * * *` |
| **时区** | Asia/Shanghai |
| **执行时间** | 每日 08:00 |
| **Job ID** | `9edd39f8` |
| **状态** | ✅ 已激活 |

### 查看定时任务

```bash
# 查看已配置的任务
cron action=list
```

### 修改执行时间

```bash
# 删除现有任务
cron action=remove job_id=9edd39f8

# 创建新任务（例如改为 07:00）
cron action=add cron_expr="0 7 * * *" tz="Asia/Shanghai" message="🤖 AI 早报"
```

### 常见时间配置

| 时间 | Cron 表达式 |
|------|------------|
| 07:00 | `0 7 * * *` |
| 08:00 | `0 8 * * *` |
| 09:00 | `0 9 * * *` |
| 工作日 08:00 | `0 8 * * 1-5` |

---

## 💡 高级用法

### 1. 自定义新闻源

```python
# 添加特定关注的公司/机构
NEWS_SOURCES.extend([
    {'name': 'DeepMind Blog', 'url': 'https://deepmind.google/blog/', 'region': '官方'},
    {'name': 'Hugging Face', 'url': 'https://huggingface.co/blog', 'region': '官方'},
    {'name': 'Stability AI', 'url': 'https://stability.ai/blog', 'region': '官方'},
])
```

### 2. 关键词过滤

```python
# 只关注特定关键词的新闻
KEYWORDS_FILTER = ['GPT', 'Claude', 'Gemini', '大模型', 'AI']

def filter_news(news_items):
    return [n for n in news_items if any(kw in n['title'] for kw in KEYWORDS_FILTER)]
```

### 3. 多群推送

```python
# 配置多个飞书 Webhook
WEBHOOKS = [
    'https://.../hook/abc123',  # 主群
    'https://.../hook/def456',  # 测试群
]

for webhook in WEBHOOKS:
    send_to_feishu_with_image(..., webhook=webhook)
```

### 4. 生成周报/月报

```bash
# 修改脚本生成周报
python skills/ai_daily_image.py --period weekly

# 生成月报
python skills/ai_daily_image.py --period monthly
```

---

## 🐛 常见问题

### Q1: 新闻获取失败？

**A**: 部分网站可能有反爬限制，解决方式：
- 使用示例数据（测试模式）
- 添加 User-Agent 头
- 降低请求频率
- 使用 RSS 源替代

### Q2: 图片字体显示异常？

**A**: 确保系统有中文支持：
- Windows: 默认支持
- Linux: 安装 `fonts-wqy-zenhei`
- macOS: 默认支持

### Q3: 飞书推送失败？

**A**: 检查：
- Webhook URL 是否正确
- 机器人权限是否足够
- 图片大小是否超限（<10MB）

### Q4: 如何查看历史早报？

**A**: 查看输出目录：
```
output/ai_daily/images/  # 所有历史图片
output/ai_daily/*.json   # 所有历史数据
```

### Q5: 如何停止自动推送？

**A**: 删除定时任务：
```bash
cron action=remove job_id=9edd39f8
```

---

## 📈 优化建议

### 新闻质量

1. **增加新闻源**: 添加更多高质量 AI 媒体
2. **去重优化**: 使用更智能的相似度检测
3. **质量评分**: 基于来源权威性、内容长度等

### 图片美观

1. **模板多样化**: 提供多种配色方案
2. **图标优化**: 使用 SVG 图标
3. **二维码**: 添加原文链接二维码

### 推送体验

1. **个性化**: 根据用户兴趣筛选
2. **交互**: 添加点击跳转链接
3. **摘要**: 提供语音播报版本

---

## 🔄 更新日志

### v1.0 (2026-03-10)
- ✅ 多源新闻搜集
- ✅ 智能摘要分类
- ✅ PIL 图片生成
- ✅ 飞书推送
- ✅ 定时任务（每日 08:00）
- ✅ 重要性评分
- ✅ 数据持久化

---

## 📞 技术支持

### 日志文件
- `output/ai_daily/ai_daily_*.json`

### 图片目录
- `output/ai_daily/images/`

### 脚本位置
- `skills/ai_daily_image.py`
- `skills/ai_daily_briefing.py`

---

## ⚖️ 免责声明

1. 新闻内容版权归原作者/媒体所有
2. 仅用于个人学习和信息获取
3. 请勿用于商业用途
4. 部分新闻源可能有访问限制

---

## 🎉 效果展示

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    🤖 AI 产业早报                           │
│                  2026 年 03 月 10 日 星期二                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🤖 模型进展                                                │
│  • OpenAI 发布 GPT-5，性能提升 10 倍                         │
│    OpenAI 今日发布最新大语言模型 GPT-5...                   │
│    ⭐⭐⭐⭐⭐ · OpenAI Blog · 官方                            │
│                                                             │
│  📱 应用落地                                                │
│  • 谷歌推出新一代 AI 芯片 TPU v5                             │
│    谷歌发布第五代 TPU 芯片，专为大模型训练优化...            │
│    ⭐⭐⭐⭐ · Google AI Blog · 官方                          │
│                                                             │
│  💰 投融资                                                  │
│  • Anthropic 完成 10 亿美元融资                              │
│    AI 安全公司 Anthropic 获新一轮融资...                     │
│    ⭐⭐⭐⭐ · TechCrunch · 海外                              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│         每日更新 · 共 10 条精选 · AI 改变世界                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

*Good Morning! 🌅 让 AI 资讯每天准时叫醒你！*
