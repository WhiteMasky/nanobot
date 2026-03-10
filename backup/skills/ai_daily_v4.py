# -*- coding: utf-8 -*-
"""
AI 早报生成器 v4.0 - 极简清新风
修复：中文字体方框问题
优化：简洁排版设计
"""

import sys
import os
import json
import urllib.request
from datetime import datetime
from typing import List, Dict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont

# ============ 配置 ============

OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\ai_daily"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

for d in [OUTPUT_DIR, IMAGE_DIR]:
    os.makedirs(d, exist_ok=True)

FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

IMG_WIDTH = 1080
IMG_HEIGHT = 1920

# ============ 字体加载（关键修复） ============

def load_chinese_font():
    """加载中文字体 - 多种方案确保成功"""
    
    # Windows 字体路径列表
    font_paths = [
        # 微软雅黑（首选）
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        # 黑体
        r"C:\Windows\Fonts\simhei.ttf",
        # 宋体
        r"C:\Windows\Fonts\simsun.ttc",
        # 楷体
        r"C:\Windows\Fonts\simkai.ttf",
    ]
    
    print("正在加载中文字体...")
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                # 测试加载
                test_font = ImageFont.truetype(font_path, 32)
                # 测试中文字符
                test_img = Image.new('RGB', (100, 50), color='white')
                test_draw = ImageDraw.Draw(test_img)
                test_draw.text((10, 10), "测试", font=test_font, fill='black')
                print(f"✓ 字体加载成功：{font_path}")
                return font_path
            except Exception as e:
                print(f"✗ 字体加载失败：{font_path} - {e}")
                continue
    
    print("⚠ 未找到可用中文字体，使用默认字体")
    return None

# 全局字体路径
FONT_PATH = load_chinese_font()

def get_font(size: int, bold: bool = False):
    """获取字体"""
    if FONT_PATH:
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except:
            pass
    return ImageFont.load_default()

# ============ 新闻数据 ============

def get_news() -> List[Dict]:
    """获取新闻数据"""
    return [
        {
            'title': 'OpenAI 发布 GPT-5，性能提升 10 倍',
            'summary': 'OpenAI 今日发布最新大语言模型 GPT-5，在推理能力、代码生成、多模态理解等方面实现重大突破。相比 GPT-4，新模型在数学推理任务上准确率提升 40%。',
            'source': 'OpenAI Blog',
            'category': '模型',
            'importance': 5,
            'time': '09:30'
        },
        {
            'title': '谷歌推出 Gemini 2.0，多模态能力升级',
            'summary': 'Google DeepMind 发布新一代多模态模型 Gemini 2.0，图像理解、视频分析能力显著提升。新模型支持实时视频对话，能够理解复杂图表和科学公式。',
            'source': 'Google AI',
            'category': '模型',
            'importance': 5,
            'time': '10:15'
        },
        {
            'title': 'Anthropic 完成 10 亿美元 C 轮融资',
            'summary': 'AI 安全公司 Anthropic 宣布完成 10 亿美元 C 轮融资，由 Spark Capital 领投，估值达 50 亿美元。资金将用于 Claude 模型研发和 AI 安全研究。',
            'source': 'TechCrunch',
            'category': '融资',
            'importance': 4,
            'time': '11:00'
        },
        {
            'title': '微软 Copilot 日活用户突破 1 亿',
            'summary': '微软宣布 Copilot AI 助手日活跃用户突破 1 亿，企业采用率持续增长。Windows 11 中 Copilot 使用率达 65%，Office 365 集成后生产力提升 30%。',
            'source': 'The Verge',
            'category': '应用',
            'importance': 4,
            'time': '14:20'
        },
        {
            'title': '特斯拉 Optimus 机器人开始工厂测试',
            'summary': '特斯拉宣布 Optimus 人形机器人正式进入工厂测试阶段，执行简单装配任务。马斯克预计 2027 年量产，售价低于 2 万美元。',
            'source': 'Reuters',
            'category': '公司',
            'importance': 4,
            'time': '16:45'
        },
        {
            'title': '欧盟 AI 法案正式生效',
            'summary': '全球首部综合性 AI 监管法规《欧盟 AI 法案》今日正式生效。法案将 AI 系统分为四个风险等级，禁止社会评分等高风险应用。',
            'source': 'BBC',
            'category': '政策',
            'importance': 3,
            'time': '18:00'
        },
    ]

# ============ 图片生成 ============

def generate_image(news_list: List[Dict], date: datetime, output_path: str):
    """生成早报图片 - 极简设计"""
    
    print(f"\n🎨 生成图片...")
    
    # 创建图片（白色背景）
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # 获取字体
    title_font = get_font(72, bold=True)      # 调大
    date_font = get_font(32)                   # 调大
    category_font = get_font(40, bold=True)    # 调大
    news_title_font = get_font(36, bold=True)  # 调大
    summary_font = get_font(26)                # 调大
    meta_font = get_font(24)                   # 调大
    
    # ============ 配色 ============
    COLOR_BG = '#FFFFFF'        # 白色背景
    COLOR_PRIMARY = '#1a1a1a'   # 深灰文字
    COLOR_SECONDARY = '#666666' # 次要文字
    COLOR_ACCENT = '#0066FF'    # 蓝色强调
    COLOR_LINE = '#E5E5E5'      # 分割线
    COLOR_CARD = '#F8F9FA'      # 卡片背景
    
    # ============ 布局参数 ============
    margin_x = 100           # 左右边距（增加）
    margin_top = 150         # 顶部边距（增加）
    card_spacing = 35        # 卡片间距（增加）
    category_spacing = 60    # 分类间距（增加）
    
    current_y = margin_top
    
    # ============ 1. 头部 ============
    
    # 日期
    date_str = date.strftime('%Y年%m月%d日')
    weekday_map = {
        'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三',
        'Thursday': '星期四', 'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'
    }
    weekday = weekday_map.get(date.strftime('%A'), '')
    
    draw.text((margin_x, current_y), date_str, font=date_font, fill=COLOR_SECONDARY)
    draw.text((margin_x + 280, current_y), weekday, font=date_font, fill=COLOR_SECONDARY)
    
    current_y += 70
    
    # 主标题
    title = "AI 产业早报"
    draw.text((margin_x, current_y), title, font=title_font, fill=COLOR_PRIMARY)
    
    current_y += 100
    
    # 分割线
    draw.line([(margin_x, current_y), (IMG_WIDTH - margin_x, current_y)], 
              fill=COLOR_LINE, width=2)
    
    current_y += 60
    
    # ============ 2. 新闻内容 ============
    
    # 按分类整理
    categories = {}
    for news in news_list:
        cat = news.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(news)
    
    category_icons = {
        '模型': '🤖',
        '应用': '📱',
        '融资': '💰',
        '公司': '🏢',
        '政策': '📋',
        '其他': '📌'
    }
    
    for cat_name, cat_news in categories.items():
        # 分类标题
        icon = category_icons.get(cat_name, '📌')
        draw.text((margin_x, current_y), f"{icon} {cat_name}", 
                  font=category_font, fill=COLOR_ACCENT)
        current_y += 50
        
        # 新闻条目
        for news in cat_news[:2]:
            # 卡片背景
            card_height = 180        # 增加卡片高度
            card_rect = [(margin_x, current_y), (IMG_WIDTH - margin_x, current_y + card_height)]
            draw.rectangle(card_rect, fill=COLOR_CARD)
            
            inner_x = margin_x + 40    # 增加内边距
            
            # 新闻标题
            title_text = news['title']
            if len(title_text) > 50:
                title_text = title_text[:48] + '...'
            
            draw.text((inner_x, current_y + 25), title_text, 
                      font=news_title_font, fill=COLOR_PRIMARY)
            
            # 新闻摘要（换行处理）
            summary = news.get('summary', '')
            max_chars = 70
            if len(summary) > max_chars:
                summary = summary[:max_chars] + '...'
            
            # 简单换行
            summary_lines = []
            for i in range(0, len(summary), 35):
                summary_lines.append(summary[i:i+35])
            
            summary_y = current_y + 75
            for i, line in enumerate(summary_lines[:2]):
                draw.text((inner_x, summary_y + i*32), line, 
                          font=summary_font, fill=COLOR_SECONDARY)
            
            # 底部信息
            meta_y = current_y + card_height - 40
            source_text = f"{news.get('source', '')} · {news.get('time', '')}"
            draw.text((inner_x, meta_y), source_text, 
                      font=meta_font, fill=COLOR_SECONDARY)
            
            # 星标
            stars = "★" * news.get('importance', 3)
            draw.text((IMG_WIDTH - margin_x - 30, meta_y), stars, 
                      font=meta_font, fill='#FFB800')
            
            current_y += card_height + card_spacing
        
        current_y += category_spacing  # 分类间距
        
        if current_y > IMG_HEIGHT - 200:
            break
    
    # ============ 3. 底部 ============
    
    footer_y = IMG_HEIGHT - 150
    
    # 分割线
    draw.line([(IMG_WIDTH // 2 - 120, footer_y), (IMG_WIDTH // 2 + 120, footer_y)], 
              fill=COLOR_LINE, width=2)
    
    # 统计
    stats_text = f"本期共 {len(news_list)} 条精选"
    draw.text((IMG_WIDTH // 2, footer_y + 40), stats_text, 
              font=meta_font, fill=COLOR_SECONDARY)
    
    # 版权
    draw.text((IMG_WIDTH // 2, footer_y + 75), "AI Daily · nanobot", 
              font=meta_font, fill=COLOR_SECONDARY)
    
    # ============ 保存 ============
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 图片已保存：{output_path}")
    
    return output_path

# ============ 飞书推送 ============

def send_feishu(title: str, content: str, image_path: str) -> bool:
    """发送飞书"""
    if not FEISHU_WEBHOOK:
        print("⚠ 未配置飞书 Webhook")
        return False
    
    try:
        import base64
        with open(image_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ 读取图片失败：{e}")
        return False
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [[{"tag": "text", "text": content}]]
                }
            }
        }
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(FEISHU_WEBHOOK, data=data, 
                                    headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("✅ 飞书推送成功")
            return True
    except Exception as e:
        print(f"❌ 飞书推送失败：{e}")
        return False

# ============ 主流程 ============

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 早报 v4.0 - 极简风')
    parser.add_argument('--date', type=str, help='日期 YYYY-MM-DD')
    args = parser.parse_args()
    
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()
    
    print(f"\n{'='*60}")
    print(f"📰 AI 产业早报 v4.0")
    print(f"日期：{date.strftime('%Y年%m月%d日')}")
    print(f"{'='*60}")
    
    # 获取新闻
    news_list = get_news()
    
    # 生成图片
    date_str = date.strftime('%Y%m%d')
    image_path = os.path.join(IMAGE_DIR, f"ai_daily_{date_str}.png")
    generate_image(news_list, date, image_path)
    
    # 保存数据
    data_path = os.path.join(OUTPUT_DIR, f"ai_daily_{date_str}.json")
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump({
            'date': date.isoformat(),
            'news_count': len(news_list),
            'news': news_list
        }, f, ensure_ascii=False, indent=2)
    
    # 推送文案
    content = f"🌅 早安！今日 AI 精选 {len(news_list)} 条\n\n"
    for i, news in enumerate(news_list[:5], 1):
        stars = "⭐" * news.get('importance', 3)
        content += f"{i}. {news['title'][:35]}...\n"
        content += f"   {stars} {news.get('source', '')}\n\n"
    content += f"\n📊 完整早报请查看图片"
    
    # 发送飞书
    send_feishu(f"📰 AI 产业早报 {date.strftime('%m-%d')}", content, image_path)
    
    print(f"\n{'='*60}")
    print(f"✅ 生成完成")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
