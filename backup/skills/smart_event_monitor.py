# -*- coding: utf-8 -*-
"""
智能事件监控 - 事件驱动交易机会捕捉
Smart Event Monitor for Trading Opportunities

功能：
1. 多源监控（财联社、华尔街见闻、推特等）
2. 智能关联（事件→股票）
3. 重要性评分
4. 飞书推送
"""

import urllib.request
import urllib.error
import json
import re
import sys
import os
from datetime import datetime, timedelta

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

# 股票关联数据库
STOCK_MAPPING = {
    # AI/大模型
    "MiniMax": {"stock": "未上市", "market": "一级市场", "keywords": ["阶跃星辰"]},
    "阶跃星辰": {"stock": "未上市", "market": "一级市场"},
    "OpenAI": {"stock": "未上市", "market": "一级市场", "related": ["微软 MSFT"]},
    "Anthropic": {"stock": "未上市", "market": "一级市场", "related": ["亚马逊 AMZN"]},
    "Claude": {"stock": "未上市", "market": "一级市场", "parent": "Anthropic"},
    
    # 中国科技公司
    "阿里巴巴": {"stock": "9988.HK", "market": "港股", "keywords": ["阿里", "BABA"]},
    "腾讯": {"stock": "0700.HK", "market": "港股", "keywords": ["腾讯控股", "Tencent"]},
    "小米": {"stock": "1810.HK", "market": "港股", "keywords": ["小米集团", "Xiaomi"]},
    "美团": {"stock": "3690.HK", "market": "港股", "keywords": ["美团点评"]},
    "京东": {"stock": "9618.HK", "market": "港股", "keywords": ["JD.com"]},
    "拼多多": {"stock": "PDD", "market": "美股", "keywords": ["PDD", "Temu"]},
    "字节跳动": {"stock": "未上市", "market": "一级市场", "keywords": ["抖音", "TikTok"]},
    "百度": {"stock": "9888.HK", "market": "港股", "keywords": ["Baidu"]},
    
    # 芯片/半导体
    "星宸科技": {"stock": "未上市", "market": "A 股", "keywords": ["芯片", "激光雷达"]},
    "思格新能源": {"stock": "IPO 中", "market": "港股", "keywords": ["新能源", "IPO"]},
    "中芯国际": {"stock": "0981.HK", "market": "港股", "keywords": ["SMIC", "半导体"]},
    "华为": {"stock": "未上市", "market": "私有", "keywords": ["Huawei", "海思"]},
    
    # 宏观经济
    "美联储": {"impact": "全局", "keywords": ["利率", "CPI", "非农", "通胀"]},
    "央行": {"impact": "全局", "keywords": ["降准", "降息", "MLF", "LPR"]},
}

# 重要性评分规则
IMPORTANCE_RULES = {
    "🔴 极高": ["IPO", "上市", "并购", "重组", "财报", "盈利", "亏损", "裁员", "调查", "起诉", "爆炸", "袭击", "战争", "制裁"],
    "🟡 高": ["发布", "合作", "投资", "融资", "战略", "新品", "技术突破", "原油", "美股", "港股", "A 股", "恒指", "纳指", "标普"],
    "🟢 中": ["计划", "预计", "可能", "传闻", "消息", "会议", "收跌", "收涨", "拉升"],
}

# 监控关键词分类
MONITOR_CATEGORIES = {
    "AI 大模型": ["MiniMax", "阶跃星辰", "OpenAI", "Anthropic", "Claude", "大模型", "AI", "人工智能", "芯片", "半导体", "激光雷达"],
    "公司动态": ["阿里巴巴", "腾讯", "小米", "美团", "京东", "拼多多", "字节跳动", "百度", "IPO", "上市", "融资"],
    "宏观经济": ["美联储", "利率", "CPI", "非农", "降准", "降息", "央行", "通胀", "纽约联储"],
    "股市期货": ["港股", "A 股", "美股", "恒指", "恒生科技", "期货", "原油", "黄金", "科创板"],
}

# 输出文件
OUTPUT_FILE = r"C:\Users\zyc\.nanobot\workspace\smart_event_output.json"
HISTORY_FILE = r"C:\Users\zyc\.nanobot\workspace\smart_event_history.json"

# ============ 工具函数 ============

def load_history():
    """加载历史记录"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"events": [], "last_check": None}

def save_history(history):
    """保存历史记录"""
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
        print(f"❌ 财联社抓取失败：{e}")
        return []

def parse_cls_content(html):
    """解析财联社内容"""
    news_list = []
    
    # 提取快讯
    pattern = r'(\d{2}:\d{2}:\d{2}) 财联社 (.*?)(?=\d{2}:\d{2}:\d{2} 财联社|$)'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for time_str, content in matches:
        content = content.strip()
        content = re.sub(r'<[^>]+>', '', content)
        
        if len(content) > 10:
            news_list.append({
                "id": f"cls_{time_str}_{content[:30]}",
                "content": f"{time_str} {content}",
                "source": "财联社",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    # 备用方案
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
    
    return news_list[:30]

def match_stock(event_content):
    """匹配相关股票"""
    matched = []
    for company, info in STOCK_MAPPING.items():
        if company in event_content or any(k in event_content for k in info.get('keywords', [])):
            matched.append({
                "company": company,
                "stock": info.get('stock', '未知'),
                "market": info.get('market', '未知'),
                "related": info.get('related', [])
            })
    return matched

def calculate_importance(event_content):
    """计算重要性评分"""
    score = 0
    level = "🟢 中"
    
    for importance, keywords in IMPORTANCE_RULES.items():
        for keyword in keywords:
            if keyword in event_content:
                level = importance
                if importance == "🔴 极高":
                    score = 100
                elif importance == "🟡 高":
                    score = 70
                else:
                    score = 40
                break
        if score > 0:
            break
    
    return level, score

def match_category(event_content):
    """匹配事件分类"""
    matched = []
    for category, keywords in MONITOR_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in event_content.lower():
                matched.append(category)
                break
    return list(set(matched))

def format_feishu_card(events):
    """格式化飞书卡片消息"""
    if not events:
        return None
    
    lines = []
    lines.append("🚨 **智能事件监控**")
    lines.append(f"_扫描时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
    
    for event in events:
        importance = event.get('importance', '🟢')
        category = event.get('categories', ['其他'])[0]
        content = event.get('content', '')
        stocks = event.get('stocks', [])
        
        # 股票信息
        stock_info = ""
        if stocks:
            stock_list = [f"{s['company']}({s['stock']})" for s in stocks[:3]]
            stock_info = " | 📈 " + ", ".join(stock_list)
        
        lines.append(f"{importance} **{content}**{stock_info}")
        lines.append(f"   _分类：{category} | 来源：{event.get('source', '未知')}_")
        lines.append("")
    
    lines.append("---")
    lines.append("_💡 智能监控 | 事件驱动 | 股票关联_")
    
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("🚨 智能事件监控")
    print("=" * 60)
    
    # 加载历史
    history = load_history()
    event_ids = [e.get('id', '') for e in history.get('events', [])]
    
    # 抓取新闻
    print("\n📡 正在抓取财联社...")
    news_list = fetch_cls_telegraph()
    print(f"✅ 抓取到 {len(news_list)} 条")
    
    # 显示前 5 条预览
    if news_list:
        print("\n📋 最新快讯预览:")
        for i, n in enumerate(news_list[:5], 1):
            print(f"  {i}. {n['content'][:80]}...")
    
    # 过滤已处理
    new_events = [n for n in news_list if n['id'] not in event_ids]
    print(f"\n🆕 新事件：{len(new_events)} 条")
    
    # 智能分析
    analyzed_events = []
    for event in new_events:
        # 匹配股票
        stocks = match_stock(event['content'])
        
        # 匹配分类
        categories = match_category(event['content'])
        
        # 计算重要性
        importance, score = calculate_importance(event['content'])
        
        # 只保留有股票关联或高重要性的事件
        if stocks or score >= 70 or categories:
            event['stocks'] = stocks
            event['categories'] = categories if categories else ['其他']
            event['importance'] = importance
            event['score'] = score
            analyzed_events.append(event)
    
    print(f"🎯 匹配事件：{len(analyzed_events)} 条")
    
    # 输出结果
    if analyzed_events:
        # 按重要性排序
        analyzed_events.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        output = {
            "time": datetime.now().isoformat(),
            "count": len(analyzed_events),
            "events": analyzed_events,
            "message": format_feishu_card(analyzed_events)
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 已输出到 {OUTPUT_FILE}")
        print("\n" + format_feishu_card(analyzed_events))
        
        # 更新历史
        history['events'].extend(analyzed_events)
        history['events'] = history['events'][-200:]  # 保留最近 200 条
        history['last_check'] = datetime.now().isoformat()
        save_history(history)
    else:
        output = {
            "time": datetime.now().isoformat(),
            "count": 0,
            "events": [],
            "message": "暂无重要事件"
        }
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print("\n⏭️ 暂无重要事件")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
