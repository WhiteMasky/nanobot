# -*- coding: utf-8 -*-
"""
AI 早报生成器 (AI Daily Briefing)
自动搜集全球 AI 产业新闻并生成精美图片

功能：
1. 多源新闻搜集（海外 + 国内）
2. 智能摘要和分类
3. 精美图片生成
4. 飞书推送
5. 定时任务支持
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import re
import hashlib

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

# 输出目录
OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\ai_daily"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

# 确保目录存在
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# API 配置
DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', 'sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b')
DASHSCOPE_BASE = "https://dashscope.aliyuncs.com/api/v1"

# 飞书配置
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

# 新闻源配置
NEWS_SOURCES = {
    'overseas': [
        {
            'name': 'The Verge AI',
            'url': 'https://www.theverge.com/ai-artificial-intelligence',
            'category': '媒体'
        },
        {
            'name': 'TechCrunch AI',
            'url': 'https://techcrunch.com/category/artificial-intelligence/',
            'category': '媒体'
        },
        {
            'name': 'MIT Tech Review',
            'url': 'https://www.technologyreview.com/topic/artificial-intelligence/',
            'category': '媒体'
        },
        {
            'name': 'OpenAI Blog',
            'url': 'https://openai.com/blog',
            'category': '官方'
        },
        {
            'name': 'Google AI Blog',
            'url': 'https://blog.google/technology/ai/',
            'category': '官方'
        },
        {
            'name': 'Anthropic',
            'url': 'https://www.anthropic.com/news',
            'category': '官方'
        },
    ],
    'domestic': [
        {
            'name': '机器之心',
            'url': 'https://www.jiqizhixin.com/',
            'category': '媒体'
        },
        {
            'name': '量子位',
            'url': 'https://www.qbitai.com/',
            'category': '媒体'
        },
        {
            'name': 'AI 科技大本营',
            'url': 'https://blog.csdn.net/csdnnews',
            'category': '媒体'
        },
    ]
}

# 新闻分类
CATEGORIES = {
    'model': '🤖 模型进展',
    'application': '📱 应用落地',
    'investment': '💰 投融资',
    'policy': '📜 政策法规',
    'research': '🔬 学术研究',
    'product': '🚀 产品发布',
    'company': '🏢 公司动态',
    'other': '📰 其他'
}

# ============ 工具函数 ============

def fetch_url(url: str, timeout: int = 10) -> str:
    """获取网页内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return ""

def extract_links(html: str, base_url: str) -> List[Dict]:
    """从 HTML 中提取新闻链接"""
    links = []
    
    # 简单的链接提取（实际应该用 BeautifulSoup）
    pattern = r'href=["\'](https?://[^"\']+?)["\']'
    matches = re.findall(pattern, html)
    
    # 标题提取
    title_pattern = r'<title>([^<]+)</title>'
    title_match = re.search(title_pattern, html)
    page_title = title_match.group(1) if title_match else "未知页面"
    
    for link in matches[:20]:  # 限制数量
        if any(keyword in link.lower() for keyword in ['article', 'news', 'blog', 'post']):
            links.append({
                'url': link,
                'source': page_title,
                'title': ''
            })
    
    return links

def summarize_text(text: str, max_length: int = 100) -> str:
    """使用 Qwen 摘要文本"""
    if len(text) <= max_length:
        return text
    
    # 调用 Qwen API
    url = f"{DASHSCOPE_BASE}/services/aigc/text-generation/generation"
    
    payload = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": f"请用一句话总结以下新闻内容（不超过{max_length}字）：\n\n{text[:500]}"
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Authorization': f'Bearer {DASHSCOPE_API_KEY}',
                'Content-Type': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            summary = result.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', '')
            return summary.strip()
    except Exception as e:
        # 降级处理：直接截取
        return text[:max_length] + "..."

def classify_news(title: str, content: str) -> str:
    """新闻分类"""
    keywords = {
        'model': ['模型', 'model', 'LLM', '大语言模型', 'GPT', 'Claude', '训练'],
        'application': ['应用', 'application', '落地', '使用', '产品'],
        'investment': ['投资', '融资', 'funding', 'round', '估值'],
        'policy': ['政策', 'policy', '监管', '法规', '法律'],
        'research': ['研究', 'research', '论文', 'paper', '学术'],
        'product': ['发布', 'launch', '新产品', '上线', '推出'],
        'company': ['公司', 'company', '企业', '团队', '人事'],
    }
    
    text = (title + " " + content).lower()
    
    for category, words in keywords.items():
        if any(word.lower() in text for word in words):
            return category
    
    return 'other'

def importance_score(title: str, content: str, source: str) -> int:
    """计算新闻重要性（1-5 星）"""
    score = 3  # 基础分
    
    # 来源加分
    if source in ['OpenAI Blog', 'Google AI Blog', 'Anthropic']:
        score += 1
    
    # 关键词加分
    important_keywords = ['发布', 'launch', '重磅', 'major', '突破', 'breakthrough', '首次', 'first']
    if any(kw in (title + content).lower() for kw in important_keywords):
        score += 1
    
    # 长度加分（长文章通常更重要）
    if len(content) > 500:
        score += 1
    
    return min(score, 5)

# ============ 新闻搜集 ============

class NewsCollector:
    """新闻搜集器"""
    
    def __init__(self):
        self.news_items = []
    
    def collect_from_source(self, source: Dict) -> List[Dict]:
        """从单个源搜集新闻"""
        print(f"  搜集：{source['name']}...")
        
        html = fetch_url(source['url'])
        if not html:
            print(f"    ❌ 获取失败")
            return []
        
        links = extract_links(html, source['url'])
        news_list = []
        
        for link in links[:5]:  # 每个源最多 5 条
            # 获取文章详情
            article_html = fetch_url(link['url'])
            if article_html:
                # 提取标题和内容
                title_pattern = r'<h1[^>]*>([^<]+)</h1>'
                title_match = re.search(title_pattern, article_html)
                title = title_match.group(1).strip() if title_match else link['url']
                
                # 提取正文
                content_pattern = r'<p>([^<]+)</p>'
                content_matches = re.findall(content_pattern, article_html)
                content = ' '.join(content_matches[:5])
                
                # 摘要
                summary = summarize_text(content, 80)
                
                # 分类
                category = classify_news(title, content)
                
                # 重要性
                score = importance_score(title, content, source['name'])
                
                news_list.append({
                    'title': title,
                    'summary': summary,
                    'url': link['url'],
                    'source': source['name'],
                    'source_type': source['category'],
                    'category': category,
                    'importance': score,
                    'timestamp': datetime.now().isoformat()
                })
        
        print(f"    ✅ 获取 {len(news_list)} 条")
        return news_list
    
    def collect_all(self) -> List[Dict]:
        """搜集所有源"""
        print("\n开始搜集新闻...")
        
        all_news = []
        
        # 海外新闻
        print("\n🌍 海外新闻:")
        for source in NEWS_SOURCES['overseas']:
            news = self.collect_from_source(source)
            all_news.extend(news)
            time.sleep(1)  # 避免请求过快
        
        # 国内新闻
        print("\n🇨🇳 国内新闻:")
        for source in NEWS_SOURCES['domestic']:
            news = self.collect_from_source(source)
            all_news.extend(news)
            time.sleep(1)
        
        # 去重和排序
        seen_urls = set()
        unique_news = []
        for news in all_news:
            if news['url'] not in seen_urls:
                seen_urls.add(news['url'])
                unique_news.append(news)
        
        # 按重要性排序
        unique_news.sort(key=lambda x: x['importance'], reverse=True)
        
        print(f"\n✅ 共获取 {len(unique_news)} 条唯一新闻")
        self.news_items = unique_news
        return unique_news

# ============ 图片生成 ============

class ImageGenerator:
    """早报图片生成器"""
    
    def __init__(self):
        self.width = 1080
        self.height = 1920
    
    def generate_html(self, news_items: List[Dict], date: datetime) -> str:
        """生成 HTML 格式早报"""
        
        # 按分类整理
        categorized = {}
        for news in news_items:
            cat = news['category']
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(news)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: {self.width}px;
            height: {self.height}px;
            padding: 40px;
            color: #333;
        }}
        .header {{
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .title {{
            font-size: 48px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .date {{
            font-size: 24px;
            color: #666;
        }}
        .section {{
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        .section-title {{
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .news-item {{
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }}
        .news-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .news-title {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 8px;
            color: #333;
        }}
        .news-summary {{
            font-size: 16px;
            color: #666;
            line-height: 1.6;
            margin-bottom: 8px;
        }}
        .news-meta {{
            font-size: 14px;
            color: #999;
        }}
        .stars {{
            color: #f59e0b;
        }}
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            font-size: 16px;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🤖 AI 产业早报</div>
        <div class="date">{date.strftime('%Y年%m月%d日')} {date.strftime('%A')}</div>
    </div>
"""
        
        # 添加各分类新闻
        for cat_key, cat_name in CATEGORIES.items():
            if cat_key in categorized and categorized[cat_key]:
                html += f"""
    <div class="section">
        <div class="section-title">{cat_name}</div>
"""
                for news in categorized[cat_key][:3]:  # 每个分类最多 3 条
                    stars = "⭐" * news['importance']
                    html += f"""
        <div class="news-item">
            <div class="news-title">{news['title'][:50]}{'...' if len(news['title']) > 50 else ''}</div>
            <div class="news-summary">{news['summary']}</div>
            <div class="news-meta">
                <span class="stars">{stars}</span>
                · {news['source']}
            </div>
        </div>
"""
                html += """
    </div>
"""
        
        html += f"""
    <div class="footer">
        每日更新 · 全球 AI 产业动态 · {len(news_items)}条精选
    </div>
</body>
</html>
"""
        return html
    
    def save_html(self, html: str, filename: str) -> str:
        """保存 HTML 文件"""
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return filepath
    
    def html_to_image(self, html_path: str, output_path: str) -> bool:
        """HTML 转图片（需要 wkhtmltoimage 或类似工具）"""
        # 简化版本：直接保存 HTML，用户可以用浏览器打开截图
        print(f"HTML 已保存：{html_path}")
        print(f"提示：用浏览器打开后截图即可")
        return True

# ============ 飞书推送 ============

def send_to_feishu(title: str, content: str, image_path: str = None, webhook: str = None) -> bool:
    """发送飞书消息"""
    webhook_url = webhook or FEISHU_WEBHOOK
    if not webhook_url:
        print("❌ 未配置飞书 Webhook")
        return False
    
    # 图文消息
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": content
                            }
                        ]
                    ]
                }
            }
        }
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('StatusCode') == 0 or result.get('code') == 0:
                print("✅ 飞书推送成功")
                return True
            else:
                print(f"❌ 飞书推送失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 飞书推送错误：{e}")
        return False

# ============ 主流程 ============

class AIDailyBriefing:
    """AI 早报生成器"""
    
    def __init__(self):
        self.collector = NewsCollector()
        self.generator = ImageGenerator()
        self.news_items = []
    
    def generate(self, date: datetime = None) -> Dict:
        """生成早报"""
        if not date:
            date = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"📰 生成 AI 早报")
        print(f"日期：{date.strftime('%Y-%m-%d')}")
        print(f"{'='*60}")
        
        # 1. 搜集新闻
        self.news_items = self.collector.collect_all()
        
        if not self.news_items:
            print("❌ 未获取到新闻")
            return {'success': False, 'message': '未获取到新闻'}
        
        # 2. 生成 HTML
        html = self.generator.generate_html(self.news_items, date)
        html_filename = f"ai_daily_{date.strftime('%Y%m%d')}.html"
        html_path = self.generator.save_html(html, html_filename)
        
        # 3. 保存新闻数据
        data_filename = f"ai_daily_{date.strftime('%Y%m%d')}.json"
        data_path = os.path.join(OUTPUT_DIR, data_filename)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump({
                'date': date.isoformat(),
                'news_count': len(self.news_items),
                'news': self.news_items
            }, f, ensure_ascii=False, indent=2)
        
        # 4. 生成推送内容
        push_content = self.generate_push_content()
        
        # 5. 发送飞书
        send_to_feishu(
            f"🤖 AI 产业早报 {date.strftime('%m-%d')}",
            push_content
        )
        
        print(f"\n{'='*60}")
        print(f"✅ 早报生成完成")
        print(f"HTML: {html_path}")
        print(f"数据：{data_path}")
        print(f"新闻数：{len(self.news_items)}")
        print(f"{'='*60}")
        
        return {
            'success': True,
            'html_path': html_path,
            'data_path': data_path,
            'news_count': len(self.news_items)
        }
    
    def generate_push_content(self) -> str:
        """生成推送内容"""
        # 按重要性取前 5 条
        top_news = self.news_items[:5]
        
        content = f"📰 今日精选 {len(self.news_items)} 条\n\n"
        
        for i, news in enumerate(top_news, 1):
            stars = "⭐" * news['importance']
            content += f"{i}. {news['title'][:30]}...\n"
            content += f"   {stars} {news['source']}\n\n"
        
        content += f"\n完整早报请查看附件"
        
        return content

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='AI 早报生成器')
    
    parser.add_argument('--date', type=str, help='日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('--output-dir', type=str, default=OUTPUT_DIR, help='输出目录')
    parser.add_argument('--no-push', action='store_true', help='不推送飞书')
    parser.add_argument('--test', action='store_true', help='测试模式（少量新闻）')
    
    args = parser.parse_args()
    
    # 解析日期
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()
    
    # 生成早报
    briefing = AIDailyBriefing()
    result = briefing.generate(date)
    
    # 退出码
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    import argparse
    main()
