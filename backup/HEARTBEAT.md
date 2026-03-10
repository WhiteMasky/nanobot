# Heartbeat Tasks

This file is checked every 30 minutes by your nanobot agent.
Add tasks below that you want the agent to work on periodically.

If this file has no tasks (only headers and comments), the agent will skip the heartbeat.

## Active Tasks

<!-- Add your periodic tasks below this line -->

<!-- ⏸️ 财经监控已暂停，移至 Completed 部分 -->


## Completed

<!-- Move completed tasks here or delete them -->

### 📈 财经快讯监控（每 30 分钟）- ⏸️ 已暂停

**暂停原因：** 2026-03-10 用户要求暂停推送到钉钉群

**任务说明：** 抓取财联社快讯，匹配关键词后推送到群聊

**监控源：**
- https://www.cls.cn/telegraph (财联社电报)

**关键词：**
- AI 相关：MiniMax, 阶跃星辰，OpenAI, Anthropic, 大模型，AI, 芯片
- 公司相关：阿里巴巴，腾讯，小米，美团，京东，拼多多，IPO
- 宏观相关：美联储，利率，CPI, 非农，降准，降息
- 股市期货：港股，A 股，美股，恒指，恒生科技

**输出文件：**
- `finance_news_for_feishu.json` (供 nanobot 读取推送)
- `finance_news_history.json` (历史推送记录)

**恢复推送：** 将此任务移回 Active Tasks 部分，并修改推送目标群 ID

