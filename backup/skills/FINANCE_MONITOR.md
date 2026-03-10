# 📈 财经快讯监控配置指南

## ✅ 已完成配置

| 项目 | 状态 | 说明 |
|------|------|------|
| 监控脚本 | ✅ 完成 | `skills/finance_monitor_feishu.py` |
| 关键词配置 | ✅ 完成 | AI 大模型/公司动态/宏观经济/股市期货 |
| 测试运行 | ✅ 成功 | 已抓取并匹配到 3 条消息 |
| 输出文件 | ✅ 生成 | `finance_news_for_feishu.json` |

---

## 📋 监控关键词

### 🤖 AI 大模型（🔴 高优先级）
- MiniMax, 阶跃星辰，OpenAI, Anthropic, Claude
- 大模型，AI, 人工智能，芯片，半导体，激光雷达

### 🏢 公司动态（🟡 中优先级）
- 阿里巴巴，腾讯，小米，美团，京东，拼多多
- 字节跳动，百度，IPO, 上市

### 📊 宏观经济（🟡 中优先级）
- 美联储，利率，CPI, 非农，降准，降息
- 央行，通胀，纽约联储

### 📈 股市期货（🟢 一般优先级）
- 港股，A 股，美股，恒指，恒生科技
- 期货，原油，黄金，科创板

---

## 🚀 使用方式

### 方式 1：手动运行（立即测试）

```bash
python C:\Users\zyc\.nanobot\workspace\skills\finance_monitor_feishu.py
```

### 方式 2：定时任务（推荐）

**选项 A：Windows 任务计划程序**

1. 打开「任务计划程序」
2. 创建基本任务 → 命名为「财经快讯监控」
3. 触发器：每 30 分钟
4. 操作：启动程序
   - 程序：`python.exe`
   - 参数：`C:\Users\zyc\.nanobot\workspace\skills\finance_monitor_feishu.py`
   - 起始于：`C:\Users\zyc\.nanobot\workspace\skills`

**选项 B：使用 nanobot HEARTBEAT（待配置）**

在 `HEARTBEAT.md` 中添加定时任务，每 30 分钟检查一次。

---

## 📱 飞书推送配置

### 当前状态
- ⚠️ 监控脚本已就绪
- ⚠️ 飞书推送需要配置

### 配置方法

**方法 1：使用飞书群机器人 Webhook**

1. 在飞书群里添加「自定义机器人」
2. 获取 Webhook URL
3. 在推送脚本中配置 Webhook

**方法 2：使用 nanobot 飞书消息工具（推荐）**

创建一个 nanobot 技能，读取输出文件并推送：

```python
# 读取 finance_news_for_feishu.json
# 使用 nanobot 的 message 工具发送到飞书群
```

---

## 📊 测试结果

**测试时间：** 2026-03-09 23:17

**抓取结果：**
- 总消息：16 条
- 新消息：12 条
- 匹配关键词：3 条 ✅

**匹配到的消息：**
1. 🟡 思格新能源港股 IPO
2. 🟡 江苏泽景汽车电子通过上市聆讯
3. 🔴 星宸科技发布激光雷达芯片（AI 大模型）

---

## 🔧 下一步

### 立即可做：
1. ✅ 手动运行脚本测试
2. ⏳ 配置飞书推送
3. ⏳ 设置定时任务

### 优化建议：
1. 增加监控源（华尔街见闻、金十数据）
2. 添加更多关键词（特定公司/人物）
3. 配置推送频率（避免骚扰）
4. 添加重要性评分（过滤低价值消息）

---

## 📝 文件清单

| 文件 | 路径 | 用途 |
|------|------|------|
| 监控脚本 | `skills/finance_monitor_feishu.py` | 抓取 + 匹配 |
| 输出文件 | `finance_news_for_feishu.json` | 临时数据 |
| 历史记录 | `finance_news_history.json` | 去重记录 |
| 配置文档 | `skills/FINANCE_MONITOR.md` | 说明文档 |

---

*最后更新：2026-03-09 23:17*
