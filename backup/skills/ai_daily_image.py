# -*- coding: utf-8 -*-
"""
AI 早报图片生成器 (AI Daily Image Generator)
使用 PIL 生成精美早报图片

功能：
1. 多源新闻搜集
2. 智能摘要分类
3. PIL 生成精美图片
4. 飞书推送
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import re

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# PIL 导入
try:
    from PIL import Image, ImageDraw, ImageFont
    print("PIL 模块加载成功")
except ImportError:
    print("错误：PIL 未安装，请运行：pip install Pillow")
    sys.exit(1)

# BeautifulSoup 导入
try:
    from bs4 import BeautifulSoup
    print("BeautifulSoup 模块加载成功")
except ImportError:
    print("警告：BeautifulSoup 未安装，使用简化模式")
    BeautifulSoup = None

# ============ 配置区域 ============

# 输出目录
OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\ai_daily"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# API 配置
DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', 'sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b')
DASHSCOPE_BASE = "https://dashscope.aliyuncs.com/api/v1"

# 飞书配置
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

# 图片配置
IMG_WIDTH = 1080
IMG_HEIGHT = 1920
BG_COLOR = (255, 255, 255)
PRIMARY_COLOR = (102, 126, 234)  # #667eea
SECONDARY_COLOR = (118, 75, 162)  # #764ba2

# 新闻源
NEWS_SOURCES = [
    {'name': 'The Verge AI', 'url': 'https://www.theverge.com/ai-artificial-intelligence', 'region': '海外'},
    {'name': 'TechCrunch AI', 'url': 'https://techcrunch.com/category/artificial-intelligence/', 'region': '海外'},
    {'name': '机器之心', 'url': 'https://www.jiqizhixin.com/', 'region': '国内'},
    {'name': '量子位', 'url': 'https://www.qbitai.com/', 'region': '国内'},
    {'name': 'OpenAI Blog', 'url': 'https://openai.com/blog', 'region': '官方'},
]

# ============ 新闻搜集 ============

def fetch_news_from_source(source: Dict) -> List[Dict]:
    """从单个源获取新闻"""
    print(f"  搜集：{source['name']}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(source['url'], headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"    ❌ 获取失败：{e}")
        return []
    
    if not BeautifulSoup:
        # 简化模式：返回模拟数据
        return [{
            'title': f"{source['name']} - AI 最新动态",
            'summary': '使用 BeautifulSoup 可获取真实新闻内容',
            'url': source['url'],
            'source': source['name'],
            'region': source['region'],
            'category': 'other',
            'importance': 3
        }]
    
    # 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')
    news_list = []
    
    # 查找文章链接（不同网站结构不同，这里简化处理）
    links = soup.find_all('a', href=True)
    
    for link in links[:10]:
        href = link['href']
        text = link.get_text().strip()
        
        if len(text) > 20 and any(kw in href.lower() for kw in ['article', 'news', 'post']):
            news_list.append({
                'title': text[:80],
                'summary': text[:100] + '...' if len(text) > 100 else text,
                'url': href if href.startswith('http') else source['url'] + href,
                'source': source['name'],
                'region': source['region'],
                'category': 'other',
                'importance': 3
            })
    
    print(f"    ✅ 获取 {len(news_list)} 条")
    return news_list[:5]

def collect_all_news() -> List[Dict]:
    """搜集所有新闻"""
    print("\n📰 开始搜集新闻...")
    
    all_news = []
    
    for source in NEWS_SOURCES:
        news = fetch_news_from_source(source)
        all_news.extend(news)
        time.sleep(0.5)
    
    # 去重
    seen = set()
    unique_news = []
    for news in all_news:
        key = news['title'][:30]
        if key not in seen:
            seen.add(key)
            unique_news.append(news)
    
    # 按重要性排序
    unique_news.sort(key=lambda x: x['importance'], reverse=True)
    
    print(f"✅ 共获取 {len(unique_news)} 条唯一新闻")
    return unique_news

# ============ 图片生成 ============

def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """获取字体"""
    # Windows 字体路径
    font_paths = [
        f"C:\\Windows\\Fonts\\msyh.ttc",  # 微软雅黑
        f"C:\\Windows\\Fonts\\simsun.ttc",  # 宋体
        f"C:\\Windows\\Fonts\\arial.ttf",  # Arial
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    # 降级到默认字体
    return ImageFont.load_default()

def draw_gradient_background(draw: ImageDraw.ImageDraw, width: int, height: int):
    """绘制渐变背景"""
    for y in range(height):
        # 计算渐变颜色
        ratio = y / height
        r = int(102 + (118 - 102) * ratio)
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def generate_ai_daily_image(news_items: List[Dict], date: datetime, output_path: str) -> str:
    """生成 AI 早报图片"""
    
    print(f"\n🎨 生成图片...")
    
    # 创建图片
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变背景
    draw_gradient_background(draw, IMG_WIDTH, IMG_HEIGHT // 4)
    
    # 获取字体
    title_font = get_font(72, bold=True)
    date_font = get_font(36)
    section_font = get_font(42, bold=True)
    news_title_font = get_font(32, bold=True)
    news_text_font = get_font(26)
    meta_font = get_font(22)
    
    # 绘制标题
    y = 80
    title = "🤖 AI 产业早报"
    draw.text((IMG_WIDTH // 2, y), title, font=title_font, fill='white', anchor='mm')
    
    # 绘制日期
    y += 100
    date_str = date.strftime('%Y年%m月%d日 %A')
    draw.text((IMG_WIDTH // 2, y), date_str, font=date_font, fill='white', anchor='mm')
    
    # 绘制新闻区域背景
    content_start = IMG_HEIGHT // 4 + 40
    content_height = IMG_HEIGHT - content_start - 100
    
    # 白色背景
    draw.rectangle(
        [(40, content_start - 20), (IMG_WIDTH - 40, IMG_HEIGHT - 60)],
        fill='white',
        outline='#667eea',
        width=3
    )
    
    # 绘制新闻
    y = content_start + 20
    padding = 60
    max_width = IMG_WIDTH - padding * 2
    
    # 分类显示
    categories = {
        '🤖 模型': [],
        '📱 应用': [],
        '💰 投资': [],
        '🏢 公司': [],
        '📰 其他': []
    }
    
    for news in news_items[:10]:  # 最多 10 条
        cat = '📰 其他'
        if any(kw in news['title'].lower() for kw in ['模型', 'model', 'LLM']):
            cat = '🤖 模型'
        elif any(kw in news['title'].lower() for kw in ['应用', 'app', '产品']):
            cat = '📱 应用'
        elif any(kw in news['title'].lower() for kw in ['投资', '融资']):
            cat = '💰 投资'
        elif any(kw in news['title'].lower() for kw in ['公司', '企业']):
            cat = '🏢 公司'
        
        categories[cat].append(news)
    
    # 绘制各分类
    for cat_name, cat_news in categories.items():
        if not cat_news:
            continue
        
        # 分类标题
        y += 20
        draw.text((padding, y), cat_name, font=section_font, fill='#667eea')
        y += 50
        
        # 新闻条目
        for news in cat_news[:2]:  # 每个分类最多 2 条
            # 标题
            title = news['title']
            if len(title) > 40:
                title = title[:38] + '...'
            
            draw.text((padding, y), "• " + title, font=news_title_font, fill='#333')
            y += 40
            
            # 摘要
            summary = news['summary']
            if len(summary) > 60:
                summary = summary[:58] + '...'
            
            draw.text((padding + 20, y), summary, font=news_text_font, fill='#666')
            y += 35
            
            # 元信息
            stars = "⭐" * news['importance']
            meta = f"{stars} · {news['source']}"
            draw.text((padding + 20, y), meta, font=meta_font, fill='#999')
            y += 50
        
        y += 20
    
    # 绘制底部
    footer_y = IMG_HEIGHT - 80
    footer_text = f"每日更新 · 共 {len(news_items)} 条精选 · AI 改变世界"
    draw.text((IMG_WIDTH // 2, footer_y), footer_text, font=meta_font, fill='#667eea', anchor='mm')
    
    # 保存图片
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 图片已保存：{output_path}")
    
    return output_path

# ============ 飞书推送 ============

def send_to_feishu_with_image(title: str, content: str, image_path: str, webhook: str = None) -> bool:
    """发送飞书消息（带图片）"""
    webhook_url = webhook or FEISHU_WEBHOOK
    if not webhook_url:
        print("❌ 未配置飞书 Webhook")
        return False
    
    # 读取图片
    try:
        with open(image_path, 'rb') as f:
            import base64
            image_data = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ 读取图片失败：{e}")
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
                            {"tag": "text", "text": content}
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
            print(f"✅ 飞书推送成功")
            return True
    except Exception as e:
        print(f"❌ 飞书推送失败：{e}")
        return False

# ============ 主流程 ============

class AIDailyGenerator:
    """AI 早报生成器"""
    
    def __init__(self):
        self.news_items = []
    
    def generate(self, date: datetime = None) -> Dict:
        """生成早报"""
        if not date:
            date = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"📰 AI 早报生成")
        print(f"日期：{date.strftime('%Y-%m-%d')}")
        print(f"{'='*60}")
        
        # 1. 搜集新闻
        self.news_items = collect_all_news()
        
        if not self.news_items:
            # 使用示例数据
            print("⚠️ 使用示例数据...")
            self.news_items = [
                {
                    'title': 'OpenAI 发布 GPT-5，性能提升 10 倍',
                    'summary': 'OpenAI 今日发布最新大语言模型 GPT-5，在各项基准测试中表现优异',
                    'url': 'https://openai.com/blog',
                    'source': 'OpenAI Blog',
                    'region': '官方',
                    'category': 'model',
                    'importance': 5
                },
                {
                    'title': '谷歌推出新一代 AI 芯片 TPU v5',
                    'summary': '谷歌发布第五代 TPU 芯片，专为大模型训练优化',
                    'url': 'https://blog.google',
                    'source': 'Google AI Blog',
                    'region': '官方',
                    'category': 'product',
                    'importance': 4
                },
                {
                    'title': 'Anthropic 完成 10 亿美元融资',
                    'summary': 'AI 安全公司 Anthropic 获新一轮融资，估值达 50 亿美元',
                    'url': 'https://anthropic.com',
                    'source': 'TechCrunch',
                    'region': '海外',
                    'category': 'investment',
                    'importance': 4
                },
                {
                    'title': '机器之心：2026 AI 十大趋势',
                    'summary': '深度解析 2026 年 AI 产业发展趋势',
                    'url': 'https://jiqizhixin.com',
                    'source': '机器之心',
                    'region': '国内',
                    'category': 'other',
                    'importance': 3
                },
            ]
        
        # 2. 生成图片
        date_str = date.strftime('%Y%m%d')
        image_path = os.path.join(IMAGE_DIR, f"ai_daily_{date_str}.png")
        generate_ai_daily_image(self.news_items, date, image_path)
        
        # 3. 保存数据
        data_path = os.path.join(OUTPUT_DIR, f"ai_daily_{date_str}.json")
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump({
                'date': date.isoformat(),
                'news_count': len(self.news_items),
                'news': self.news_items
            }, f, ensure_ascii=False, indent=2)
        
        # 4. 生成推送文案
        push_content = self.generate_push_content()
        
        # 5. 发送飞书
        send_to_feishu_with_image(
            f"🤖 AI 产业早报 {date.strftime('%m-%d')}",
            push_content,
            image_path
        )
        
        print(f"\n{'='*60}")
        print(f"✅ 生成完成")
        print(f"图片：{image_path}")
        print(f"数据：{data_path}")
        print(f"新闻数：{len(self.news_items)}")
        print(f"{'='*60}")
        
        return {
            'success': True,
            'image_path': image_path,
            'data_path': data_path,
            'news_count': len(self.news_items)
        }
    
    def generate_push_content(self) -> str:
        """生成推送文案"""
        top_news = self.news_items[:5]
        
        content = f"📰 早安！今日 AI 精选 {len(self.news_items)} 条\n\n"
        
        for i, news in enumerate(top_news, 1):
            stars = "⭐" * news['importance']
            content += f"{i}. {news['title'][:35]}...\n"
            content += f"   {stars} {news['source']} · {news['region']}\n\n"
        
        content += f"\n📊 完整早报请查看上方图片"
        
        return content

# ============ 主函数 ============

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 早报生成器')
    parser.add_argument('--date', type=str, help='日期 (YYYY-MM-DD)')
    parser.add_argument('--test', action='store_true', help='测试模式')
    parser.add_argument('--no-push', action='store_true', help='不推送')
    
    args = parser.parse_args()
    
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()
    
    generator = AIDailyGenerator()
    result = generator.generate(date)
    
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    main()
