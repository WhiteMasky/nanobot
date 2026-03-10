# -*- coding: utf-8 -*-
"""
财经快讯监控脚本
抓取财联社/华尔街见闻快讯，匹配关键词后推送
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
os.environ['PYTHONIOENCODING'] = 'utf-8'

# ============ 配置区域 ============

# 监控关键词
KEYWORDS = {
    "AI 大模型": ["MiniMax", "阶跃星辰", "OpenAI", "Anthropic", "Claude", "大模型", "AI", "人工智能", "芯片", "半导体"],
    "公司动态": ["阿里巴巴", "腾讯", "小米", "美团", "京东", "拼多多", "字节跳动", "百度"],
    "宏观经济": ["美联储", "利率", "CPI", "非农", "降准", "降息", "央行", "通胀"],
    "股市期货": ["港股", "A 股", "美股", "恒指", "恒生科技", "期货", "原油", "黄金"]
}

# 已推送消息记录文件
HISTORY_FILE = r"C:\Users\zyc\.nanobot\workspace\finance_news_history.json"

# 输出文件（用于飞书推送）
OUTPUT_FILE = r"C:\Users\zyc\.nanobot\workspace\finance_news_output.json"

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
    """解析财联社内容（简化版）"""
    news_list = []
    
    # 尝试提取快讯内容（需要根据实际 HTML 结构调整）
    patterns = [
        r'<div[^>]*class="[^"]*telegraph[^"]*"[^>]*>(.*?)</div>',
        r'<a[^>]*href="/detail/(\d+)"[^>]*>(.*?)</a>',
        r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.DOTALL)
        for match in matches:
            if isinstance(match, tuple):
                news_id, content = match
            else:
                news_id = str(len(news_list))
                content = match
            
            # 清理 HTML 标签
            content = re.sub(r'<[^>]+>', '', content)
            content = content.strip()
            
            if len(content) > 10:  # 过滤太短的内容
                news_list.append({
                    "id": f"cls_{news_id}",
                    "content": content,
                    "source": "财联社",
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    return news_list[:20]  # 最多返回 20 条

def fetch_wallstreetcn():
    """抓取华尔街见闻快讯"""
    url = "https://www.wallstreetcn.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            return parse_wallstreet_content(html)
    except Exception as e:
        print(f"华尔街见闻抓取失败：{e}")
        return []

def parse_wallstreet_content(html):
    """解析华尔街见闻内容（简化版）"""
    news_list = []
    
    # 尝试提取快讯内容
    patterns = [
        r'<a[^>]*href="/news/(\d+)"[^>]*>(.*?)</a>',
        r'<div[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</div>',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.DOTALL)
        for match in matches:
            if isinstance(match, tuple):
                news_id, content = match
            else:
                news_id = str(len(news_list))
                content = match
            
            content = re.sub(r'<[^>]+>', '', content)
            content = content.strip()
            
            if len(content) > 10:
                news_list.append({
                    "id": f"wscn_{news_id}",
                    "content": content,
                    "source": "华尔街见闻",
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
    return matched

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
    
    print("\n正在抓取华尔街见闻...")
    wscn_news = fetch_wallstreetcn()
    print(f"抓取到 {len(wscn_news)} 条")
    
    # 合并新闻
    all_news = cls_news + wscn_news
    
    # 过滤已推送的
    new_news = [n for n in all_news if n["id"] not in sent_ids]
    
    print(f"\n新消息：{len(new_news)} 条")
    
    # 匹配关键词
    matched_news = []
    for news in new_news:
        categories = match_keywords(news["content"])
        if categories:
            news["categories"] = categories
            matched_news.append(news)
    
    print(f"匹配关键词：{len(matched_news)} 条")
    
    # 输出结果
    if matched_news:
        output = {
            "time": datetime.now().isoformat(),
            "news": matched_news
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 已输出到 {OUTPUT_FILE}")
        
        # 更新历史
        for news in matched_news:
            sent_ids.append(news["id"])
        history["sent_ids"] = sent_ids[-500:]  # 只保留最近 500 条
        history["last_check"] = datetime.now().isoformat()
        save_history(history)
    else:
        print("\n⏭️ 没有新的匹配消息")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
