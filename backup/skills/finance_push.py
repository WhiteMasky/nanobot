# -*- coding: utf-8 -*-
"""
财经快讯推送脚本
读取监控结果并推送到飞书群
"""

import json
import urllib.request
import urllib.error
import sys
import os
from datetime import datetime

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

# 飞书 Webhook URL（需要替换成你的）
# 注意：这里使用群聊机器人 webhook，或者使用 nanobot 的消息工具
FEISHU_WEBHOOK = ""  # 留空则使用文件输出

# 输入文件
INPUT_FILE = r"C:\Users\zyc\.nanobot\workspace\finance_news_output.json"

# 已推送记录
PUSHED_FILE = r"C:\Users\zyc\.nanobot\workspace\finance_pushed.json"

# ============ 工具函数 ============

def load_pushed():
    """加载已推送记录"""
    try:
        with open(PUSHED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_pushed(pushed):
    """保存已推送记录"""
    with open(PUSHED_FILE, 'w', encoding='utf-8') as f:
        json.dump(pushed, f, ensure_ascii=False, indent=2)

def send_feishu_message(content):
    """发送飞书消息"""
    if not FEISHU_WEBHOOK:
        print("未配置飞书 Webhook，跳过推送")
        return False
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "red",
                "title": {
                    "content": "🔴 财经快讯",
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            FEISHU_WEBHOOK,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('StatusCode') == 0 or result.get('code') == 0:
                print("✅ 推送成功")
                return True
            else:
                print(f"❌ 推送失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 推送异常：{e}")
        return False

def format_news(news_list):
    """格式化新闻内容"""
    lines = []
    lines.append("**📰 财经快讯监控**")
    lines.append(f"_更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
    
    for i, news in enumerate(news_list, 1):
        # 根据类别添加图标
        categories = news.get('categories', [])
        if 'AI 大模型' in categories:
            icon = "🤖"
        elif '公司动态' in categories:
            icon = "🏢"
        elif '宏观经济' in categories:
            icon = "📊"
        elif '股市期货' in categories:
            icon = "📈"
        else:
            icon = "📰"
        
        source = news.get('source', '未知')
        time = news.get('time', '')
        content = news.get('content', '')
        
        # 清理内容（去掉时间前缀）
        content = content.replace(f"{time}财联社", "财联社")
        content = content.replace("财联社", f"**[{source}]**")
        
        lines.append(f"{icon} **{i}. {content}**")
        lines.append("")
    
    lines.append("---")
    lines.append("_💡 监控频率：每 30 分钟 | 关键词：AI/芯片/港股/宏观_")
    
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("财经快讯推送")
    print("=" * 60)
    
    # 检查输入文件
    if not os.path.exists(INPUT_FILE):
        print("⏭️ 没有新的监控数据")
        return
    
    # 读取监控结果
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取失败：{e}")
        return
    
    news_list = data.get('news', [])
    if not news_list:
        print("⏭️ 没有新消息")
        return
    
    # 加载已推送记录
    pushed = load_pushed()
    
    # 过滤已推送的
    new_news = [n for n in news_list if n['id'] not in pushed]
    
    if not new_news:
        print("⏭️ 所有消息已推送")
        return
    
    print(f"\n待推送：{len(new_news)} 条")
    
    # 格式化内容
    content = format_news(new_news)
    print("\n" + content)
    print("\n" + "=" * 60)
    
    # 推送
    if FEISHU_WEBHOOK:
        success = send_feishu_message(content)
        if success:
            # 更新已推送记录
            for news in new_news:
                pushed.append(news['id'])
            save_pushed(pushed[-200:])  # 只保留最近 200 条
    else:
        print("\n⚠️ 未配置飞书 Webhook，消息已显示在上方")
        print("💡 提示：可以使用 nanobot 的飞书消息工具推送")
    
    print("\n完成")

if __name__ == "__main__":
    main()
