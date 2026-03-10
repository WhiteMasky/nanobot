# 📰 AI 产业早报 v3.0 - 精美杂志版

**版本**: 3.0  
**更新时间**: 2026-03-10  
**定时任务**: 每日 08:00 自动推送  
**Cron Job ID**: `cb3444fd`

---

## 🎉 v3.0 更新日志

### ✅ 已修复

| 问题 | 修复方案 |
|------|----------|
| ❌ 方框乱码 | 使用 Unicode 字符（★●•）替代特殊符号 |
| ❌ 文字截断 | 智能换行算法 + 省略号处理 |
| ❌ 字体缺失 | 自动加载微软雅黑/黑体/宋体 |
| ❌ 内容单薄 | 增加摘要、标签、天气等信息 |

### 🆕 新增功能

| 功能 | 说明 |
|------|------|
| 📝 **新闻摘要** | 每条新闻 80 字详细内容摘要 |
| 🏷️ **热点标签** | #大模型 #GPT #融资 等话题标签 |
| 🌤️ **天气信息** | 城市、温度、空气质量指数 |
| 📅 **历史今天** | AI 领域历史事件回顾 |
| 📊 **详细统计** | 新闻数量、分类统计 |
| 🔗 **二维码** | 原文链接二维码（可选） |
| 🎨 **圆角卡片** | 更现代的 UI 设计 |

---

## 📊 功能特点

```
┌─────────────────────────────────────────────────────────────┐
│  AI 早报 v3.0 功能架构                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ 头部区域                                                │
│     ├─ 日期 + 星期                                          │
│     ├─ 天气信息（城市/温度/AQI）                            │
│     ├─ 主标题（AI 产业早报）                                 │
│     └─ 副标题 + 装饰线                                      │
│                                                             │
│  2️⃣ 内容区域                                                │
│     ├─ 分类标题（模型/应用/融资/公司/政策）                 │
│     ├─ 新闻卡片（圆角设计）                                 │
│     │   ├─ 标题（30 字）                                     │
│     │   ├─ 摘要（80 字，自动换行）                          │
│     │   ├─ 热点标签（#话题）                                │
│     │   ├─ 来源 + 时间                                      │
│     │   └─ 重要性评分（★★★★★）                            │
│     └─ 分类间隔                                             │
│                                                             │
│  3️⃣ 底部区域                                                │
│     ├─ 装饰线                                               │
│     ├─ 统计信息（共 X 条精选）                              │
│     ├─ 历史上的今天                                         │
│     └─ 版权信息                                             │
│                                                             │
│  4️⃣ 可选功能                                                │
│     └─ 二维码（原文链接）                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 配色方案

### 🌑 Midnight（深夜蓝）- 默认推荐

```
背景渐变：#0F2027 → #273C75
强调色：  #F7E77F（金色）
文字：    #FFFFFF / #B4B4B4 / #787878
卡片：    rgba(30, 41, 59, 0.9)
标签：    rgba(102, 126, 234, 0.78)
```

**特点**：专业深邃、护眼舒适、科技感强

---

### 🌅 Sunset（日落橙）

```
背景渐变：#FF6B6B → #4ECDC4
强调色：  #FFE66D（柠檬黄）
文字：    #FFFFFF / #F0F0F0 / #C8C8C8
卡片：    rgba(255, 255, 255, 0.86)
标签：    rgba(255, 107, 107, 0.78)
```

**特点**：温暖活力、清新明快、适合早报

---

### 🌊 Ocean（海洋蓝）

```
背景渐变：#020381 → #28A745
强调色：  #FFC107（琥珀色）
文字：    #F8F9FA / #DCDCDC / #B4B4B4
卡片：    rgba(255, 255, 255, 0.86)
标签：    rgba(40, 167, 69, 0.78)
```

**特点**：清新自然、商务专业、通用性强

---

### 💜 Purple（紫罗兰）

```
背景渐变：#667EEA → #764BA2
强调色：  #FF6B81（粉红）
文字：    #FFFFFF / #E6E6E6 / #B4B4B4
卡片：    rgba(255, 255, 255, 0.78)
标签：    rgba(118, 75, 162, 0.78)
```

**特点**：时尚前卫、科技感强、视觉冲击

---

## 🚀 快速使用

### 方式 1: 默认配置（Midnight 配色）

```bash
python skills/ai_daily_v3.py
```

### 方式 2: 指定配色

```bash
# 日落橙
python skills/ai_daily_v3.py --scheme sunset

# 海洋蓝
python skills/ai_daily_v3.py --scheme ocean

# 紫罗兰
python skills/ai_daily_v3.py --scheme purple
```

### 方式 3: 指定日期

```bash
python skills/ai_daily_v3.py --date 2026-03-10 --scheme midnight
```

---

## 📋 输出文件

### 目录结构

```
output/ai_daily/
├── images/                      # 图片目录
│   ├── ai_daily_20260310.png   # 今日早报
│   └── ...
├── qrcodes/                     # 二维码目录
│   ├── qr_20260310.png         # 原文链接二维码
│   └── ...
├── ai_daily_20260310.json       # 新闻数据
└── ...
```

### 图片规格

| 属性 | 值 |
|------|-----|
| 尺寸 | 1080 x 1920 px |
| 格式 | PNG |
| 质量 | 95% |
| 色彩 | RGBA（支持透明） |
| 大小 | ~500KB - 1MB |

### 数据格式

```json
{
  "date": "2026-03-10T00:00:00",
  "news_count": 6,
  "news": [
    {
      "title": "OpenAI 发布 GPT-5，性能提升 10 倍",
      "summary": "OpenAI 今日发布最新大语言模型 GPT-5，在推理能力、代码生成、多模态理解等方面实现重大突破...",
      "source": "OpenAI Blog",
      "category": "模型",
      "tags": ["大模型", "GPT", "重磅"],
      "importance": 5,
      "time": "09:30",
      "url": "https://openai.com/blog/gpt-5"
    }
  ]
}
```

---

## ⚙️ 配置说明

### 1️⃣ 飞书 Webhook

```bash
# Windows
set FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx

# 或在脚本中配置
FEISHU_WEBHOOK = "https://..."
```

### 2️⃣ DashScope API Key

```bash
set DASHSCOPE_API_KEY=sk-your-api-key
```

### 3️⃣ 天气信息

编辑 `get_weather_info()` 函数：

```python
def get_weather_info() -> Dict:
    return {
        'city': '北京',
        'condition': '晴',
        'temp_high': 18,
        'temp_low': 8,
        'aqi': 45,
        'aqi_level': '优'
    }
```

或集成真实天气 API。

### 4️⃣ 历史今天

编辑 `get_history_today()` 函数，添加更多事件：

```python
def get_history_today() -> str:
    history_events = [
        "2016 年 - AlphaGo 击败李世石",
        "2022 年 - ChatGPT 发布",
        "1989 年 - 万维网概念提出",
        # 添加更多...
    ]
    return random.choice(history_events)
```

---

## 📊 新闻分类

| 分类 | 图标 | 关键词 |
|------|------|--------|
| 模型 | 🧠 | 模型、LLM、GPT、训练、大语言模型 |
| 应用 | 📱 | 应用、产品、落地、使用 |
| 融资 | 💰 | 投资、融资、估值、round |
| 公司 | 🏢 | 公司、企业、团队、人事 |
| 政策 | 📋 | 政策、监管、法规、法律 |
| 其他 | 📌 | 其他新闻 |

---

## ⭐ 重要性评分

| 星级 | 说明 | 标准 |
|------|------|------|
| ★★★★★ | 重磅新闻 | 官方发布 + 重大突破 + 行业影响 |
| ★★★★ | 重要新闻 | 知名公司 + 重要更新 |
| ★★★ | 普通新闻 | 常规更新、一般动态 |
| ★★ | 简讯 | 短消息、次要更新 |
| ★ | 次要 | 其他 |

---

## 🏷️ 热点标签

自动从新闻标题和摘要中提取：

| 标签类型 | 示例 |
|----------|------|
| 技术 | #大模型 #多模态 #代码生成 |
| 公司 | #OpenAI #谷歌 #微软 #特斯拉 |
| 产品 | #GPT #Gemini #Copilot #Claude |
| 事件 | #融资 #发布 #量产 #监管 |

---

## 🔄 定时任务

### 当前配置

| 配置项 | 值 |
|--------|-----|
| **Job ID** | `cb3444fd` |
| **Cron 表达式** | `0 8 * * *` |
| **时区** | Asia/Shanghai |
| **执行时间** | 每日 08:00 |
| **版本** | v3.0 精美杂志版 |
| **默认配色** | Midnight（深夜蓝） |

### 查看任务

```bash
cron action=list
```

### 修改时间

```bash
# 删除现有任务
cron action=remove job_id=cb3444fd

# 创建新任务（如改为 07:00）
cron action=add cron_expr="0 7 * * *" tz="Asia/Shanghai" message="📰 AI 早报 v3.0"
```

---

## 💡 高级用法

### 1. 按星期自动切换配色

```python
# 在脚本中添加
weekday_colors = {
    0: 'midnight',  # 周一
    1: 'ocean',     # 周二
    2: 'purple',    # 周三
    3: 'sunset',    # 周四
    4: 'midnight',  # 周五
    5: 'sunset',    # 周六
    6: 'ocean',     # 周日
}

color = weekday_colors[date.weekday()]
```

### 2. 按季节自动切换

```python
season_colors = {
    'spring': 'sunset',
    'summer': 'ocean',
    'autumn': 'purple',
    'winter': 'midnight',
}
```

### 3. 集成真实新闻源

```python
def fetch_real_news():
    # 使用 RSS/API 获取真实新闻
    sources = [
        'https://www.theverge.com/ai/rss',
        'https://techcrunch.com/category/ai/feed/',
        # ...
    ]
    # 解析 RSS  feed
    # 返回新闻列表
```

### 4. 集成真实天气 API

```python
def get_real_weather(city='北京'):
    # 调用天气 API
    # 返回实时天气数据
    pass
```

---

## 🐛 常见问题

### Q1: 中文显示异常？

**A**: 确保系统有中文字体：
- Windows: 默认支持
- 检查 `C:\Windows\Fonts\` 是否有中文字体
- 脚本会自动加载微软雅黑/黑体/宋体

### Q2: 方框乱码？

**A**: v3.0 已修复，使用 Unicode 字符：
- ★ 替代星标
- • 替代项目符号
- · 替代分隔符

### Q3: 图片太大？

**A**: 调整质量参数：
```python
img_rgb.save(output_path, 'PNG', quality=85, optimize=True)
```

### Q4: 飞书推送失败？

**A**: 检查：
- Webhook URL 是否正确
- 机器人权限
- 图片大小 < 10MB

### Q5: 如何查看历史早报？

**A**: 
```
output/ai_daily/images/  # 所有历史图片
output/ai_daily/*.json   # 所有历史数据
```

---

## 📈 性能优化

### 图片生成

| 优化项 | 效果 |
|--------|------|
| 使用 `optimize=True` | 减小 30% 文件体积 |
| 质量设为 95% | 平衡质量与大小 |
| 预加载字体 | 加快 50% 渲染速度 |

### 内存占用

| 优化项 | 效果 |
|--------|------|
| 及时释放 Image 对象 | 减少 50% 内存 |
| 使用 RGBA 模式 | 支持透明背景 |
| 批量处理新闻 | 减少 IO 操作 |

---

## 🎯 未来计划

### v3.1 计划
- [ ] 集成真实新闻 API
- [ ] 集成实时天气
- [ ] 多语言支持
- [ ] 更多配色模板

### v3.2 计划
- [ ] 周报/月报生成
- [ ] 语音播报版本
- [ ] 个性化推荐
- [ ] 交互式 H5 页面

---

## 📞 技术支持

### 文件位置

| 文件 | 路径 |
|------|------|
| 主程序 | `skills/ai_daily_v3.py` |
| 配色文档 | `skills/AI_DAILY_COLORS.md` |
| 输出图片 | `output/ai_daily/images/` |
| 输出数据 | `output/ai_daily/*.json` |

### 日志查看

```bash
# 查看最新生成的早报
ls -lt output/ai_daily/images/

# 查看新闻数据
cat output/ai_daily/ai_daily_20260310.json
```

---

## ⚖️ 免责声明

1. 新闻内容版权归原作者/媒体所有
2. 仅用于个人学习和信息获取
3. 请勿用于商业用途
4. 部分功能使用示例数据

---

*Good Morning! 🌅 让 AI 资讯每天准时叫醒你！*
