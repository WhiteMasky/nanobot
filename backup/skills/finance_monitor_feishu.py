# -*- coding: utf-8 -*-
"""
财经快讯监控 + 推送（整合版）
直接调用 nanobot 飞书消息工具推送
"""

import urllib.request
import urllib.error
import json
import re
import sys
import os
from datetime import datetime

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

# 监控关键词
KEYWORDS = {
    "AI 大模型": ["MiniMax", "阶跃星辰", "OpenAI", "Anthropic", "Claude", "大模型", "AI", "人工智能", "芯片", "半导体", "激光雷达"],
    "公司动态": ["阿里巴巴", "腾讯", "小米", "美团", "京东", "拼多多", "字节跳动", "百度", "IPO", "上市"],
    "宏观经济": ["美联储", "利率", "CPI", "非农", "降准", "降息", "央行", "通胀", "纽约联储"],
    "股市期货": ["港股", "A 股", "美股", "恒指", "恒生科技", "期货", "原油", "黄金", "科创板"]
}

# 已推送消息记录文件
HISTORY_FILE = r"C:\Users\zyc\.nanobot\workspace\finance_news_history.json"

# 输出文件（JSON 格式，供 nanobot 读取）
OUTPUT_FILE = r"C:\Users\zyc\.nanobot\workspace\finance_news_for_feishu.json"

# ============ 工具函数 ============

def load_history():
    """加载已推送消息历史"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"sent_ids": [], "last_check": None}

def save_history(history):
    """保存已推送消息历史"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def fetch_cls_telegraph():
    """抓取财联社电报"""
    url = "https://www.cls.cn/telegraph"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            return parse_cls_content(html)
    except Exception as e:
        print(f"财联社抓取失败：{e}")
        return []

def parse_cls_content(html):
    """解析财联社内容"""
    news_list = []
    
    # 提取包含时间的快讯
    pattern = r'(\d{2}:\d{2}:\d{2}) 财联社 (.*?)(?=\d{2}:\d{2}:\d{2} 财联社|$)'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for time_str, content in matches:
        content = content.strip()
        content = re.sub(r'<[^>]+>', '', content)  # 清理 HTML 标签
        
        if len(content) > 10:
            news_id = f"cls_{time_str}_{content[:20]}"
            news_list.append({
                "id": news_id,
                "content": f"{time_str} {content}",
                "source": "财联社",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    # 如果正则匹配失败，尝试简单提取
    if not news_list:
        simple_pattern = r'(\d{2}:\d{2}:\d{2}.*?电，.*?)'
        matches = re.findall(simple_pattern, html)
        for content in matches[:20]:
            content = re.sub(r'<[^>]+>', '', content)
            if len(content) > 10:
                news_list.append({
                    "id": f"cls_{len(news_list)}",
                    "content": content,
                    "source": "财联社",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    return news_list[:20]

def match_keywords(content):
    """匹配关键词，返回匹配的类别"""
    matched = []
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in content.lower():
                matched.append(category)
                break
    return list(set(matched))  # 去重

def format_feishu_message(news_list):
    """格式化飞书消息"""
    lines = []
    lines.append("📰 **财经快讯监控**")
    lines.append(f"_更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
    
    for i, news in enumerate(news_list, 1):
        # 根据类别添加图标
        categories = news.get('categories', [])
        if 'AI 大模型' in categories:
            icon = "🤖"
            priority = "🔴"
        elif '公司动态' in categories:
            icon = "🏢"
            priority = "🟡"
        elif '宏观经济' in categories:
            icon = "📊"
            priority = "🟡"
        elif '股市期货' in categories:
            icon = "📈"
            priority = "🟢"
        else:
            icon = "📰"
            priority = "⚪"
        
        content = news.get('content', '')
        
        lines.append(f"{priority} {icon} **{i}. {content}**")
        lines.append("")
    
    lines.append("---")
    lines.append("_💡 监控频率：每 30 分钟 | 关键词：AI/芯片/港股/宏观_")
    
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("财经快讯监控")
    print("=" * 60)
    
    # 加载历史
    history = load_history()
    sent_ids = history.get("sent_ids", [])
    
    # 抓取新闻
    print("\n正在抓取财联社...")
    cls_news = fetch_cls_telegraph()
    print(f"抓取到 {len(cls_news)} 条")
    
    # 过滤已推送的
    new_news = [n for n in cls_news if n["id"] not in sent_ids]
    print(f"新消息：{len(new_news)} 条")
    
    # 匹配关键词
    matched_news = []
    for news in new_news:
        categories = match_keywords(news["content"])
        if categories:
            news["categories"] = categories
            matched_news.append(news)
    
    print(f"匹配关键词：{len(matched_news)} 条")
    
    # 输出结果（供 nanobot 读取）
    if matched_news:
        # 格式化飞书消息
        message = format_feishu_message(matched_news)
        
        output = {
            "has_news": True,
            "count": len(matched_news),
            "message": message,
            "news": matched_news
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 已输出到 {OUTPUT_FILE}")
        print("\n" + message)
        
        # 更新历史
        for news in matched_news:
            sent_ids.append(news["id"])
        history["sent_ids"] = sent_ids[-500:]
        history["last_check"] = datetime.now().isoformat()
        save_history(history)
    else:
        output = {
            "has_news": False,
            "count": 0,
            "message": "暂无新的匹配消息"
        }
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print("\n⏭️ 没有新的匹配消息")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
