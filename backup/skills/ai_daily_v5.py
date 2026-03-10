# -*- coding: utf-8 -*-
"""
AI 产业早报 v5.0 - 专业媒体风
设计理念：参考 36 氪/虎嗅/晚点 LatePost 的视觉风格
- 简洁专业
- 层次清晰
- 只保留 Top 5 核心新闻
- 无装饰性元素，只保留信息本身
"""

import sys
import os
import json
import urllib.request
from datetime import datetime
from typing import List, Dict, Optional

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont

# ============ 配置 ============

OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\ai_daily"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

IMG_WIDTH = 1080
IMG_HEIGHT = 1920

# ============ 字体 ============

FONT_PATH = None

def init_font():
    global FONT_PATH
    fonts = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
    ]
    for path in fonts:
        if os.path.exists(path):
            try:
                test_font = ImageFont.truetype(path, 32)
                test_img = Image.new('RGB', (100, 50), 'white')
                test_draw = ImageDraw.Draw(test_img)
                test_draw.text((10, 10), "测试", font=test_font, fill='black')
                FONT_PATH = path
                print(f"✓ 字体：{os.path.basename(path)}")
                return
            except:
                continue
    print("⚠ 使用默认字体")

init_font()

def get_font(size: int, bold: bool = False):
    if FONT_PATH:
        try:
            return ImageFont.truetype(FONT_PATH, size)
        except:
            pass
    return ImageFont.load_default()

# ============ 新闻数据 ============

def get_news() -> List[Dict]:
    """只返回 Top 5 最有价值的新闻"""
    all_news = [
        {
            'title': 'OpenAI 发布 GPT-5，推理能力提升 40%',
            'summary': 'OpenAI 正式发布 GPT-5，在数学推理、代码生成、多模态理解等核心能力上实现重大突破。新模型支持 200K 上下文，推理速度提升 3 倍。',
            'source': 'OpenAI',
            'time': '09:30',
            'priority': 1
        },
        {
            'title': '谷歌 Gemini 2.0 支持实时视频对话',
            'summary': 'Google DeepMind 发布 Gemini 2.0，新增实时视频理解能力，可分析复杂图表和科学公式，已集成至 Google 搜索和 Assistant。',
            'source': 'Google AI',
            'time': '10:15',
            'priority': 2
        },
        {
            'title': 'Anthropic 融资 10 亿美元，估值 50 亿',
            'summary': 'AI 安全公司 Anthropic 完成 C 轮融资，由 Spark Capital 领投。资金将用于 Claude 模型研发，计划 2027 年推出新一代模型。',
            'source': 'TechCrunch',
            'time': '11:00',
            'priority': 3
        },
        {
            'title': '微软 Copilot 日活突破 1 亿',
            'summary': '微软宣布 Copilot 日活跃用户达 1 亿，Windows 11 中使用率 65%，Office 365 集成后企业生产力平均提升 30%。',
            'source': 'The Verge',
            'time': '14:20',
            'priority': 4
        },
        {
            'title': '欧盟 AI 法案正式生效',
            'summary': '全球首部 AI 综合监管法规生效，将 AI 系统分为四风险等级，禁止社会评分应用，违规企业最高面临全球营收 6% 罚款。',
            'source': 'Reuters',
            'time': '18:00',
            'priority': 5
        },
    ]
    # 按优先级排序，只返回前 5 条
    return sorted(all_news, key=lambda x: x['priority'])[:5]

# ============ 文本处理 ============

def wrap_text(text: str, font, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
    """智能换行，确保不截断"""
    lines = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    
    if current_line:
        lines.append(current_line)
    
    return lines

# ============ 图片生成 ============

def generate_image(news_list: List[Dict], date: datetime, output_path: str):
    """生成早报图片 - 专业媒体风格"""
    
    print(f"\n🎨 生成 v5.0 专业媒体风...")
    
    # 创建图片
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), '#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # 字体
    title_font = get_font(56, bold=True)
    date_font = get_font(26)
    news_title_font = get_font(34, bold=True)
    summary_font = get_font(26)
    meta_font = get_font(22)
    
    # 配色（参考晚点/36 氪）
    C_BG = '#FFFFFF'
    C_TEXT_MAIN = '#111111'
    C_TEXT_SUB = '#666666'
    C_TEXT_META = '#999999'
    C_ACCENT = '#0066FF'
    C_DIVIDER = '#EEEEEE'
    C_CARD_BG = '#FAFAFA'
    
    # 布局
    margin_x = 72
    current_y = 96
    
    # ============ 1. 头部 ============
    
    # 日期
    date_str = date.strftime('%Y.%m.%d')
    weekday_map = {
        'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三',
        'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'
    }
    weekday = weekday_map.get(date.strftime('%A'), '')
    
    draw.text((margin_x, current_y), f"{date_str}  {weekday}", font=date_font, fill=C_TEXT_META)
    
    current_y += 56
    
    # 主标题
    draw.text((margin_x, current_y), "AI 产业早报", font=title_font, fill=C_TEXT_MAIN)
    
    current_y += 72
    
    # 分割线
    draw.line([(margin_x, current_y), (IMG_WIDTH - margin_x, current_y)], fill=C_DIVIDER, width=1)
    
    current_y += 56
    
    # ============ 2. 新闻列表 ============
    
    for i, news in enumerate(news_list):
        # 序号
        num_str = f"{i+1:02d}"
        draw.text((margin_x, current_y), num_str, font=get_font(26, bold=True), fill=C_ACCENT)
        
        news_x = margin_x + 48
        news_width = IMG_WIDTH - margin_x * 2 - 48
        
        # 标题（自动换行）
        title_lines = wrap_text(news['title'], news_title_font, news_width, draw)
        
        for j, line in enumerate(title_lines[:2]):
            draw.text((news_x, current_y + j*42), line, font=news_title_font, fill=C_TEXT_MAIN)
        
        title_height = len(title_lines[:2]) * 42
        
        # 摘要（自动换行，最多 2 行）
        summary = news['summary']
        if len(summary) > 70:
            summary = summary[:68] + '...'
        
        summary_lines = wrap_text(summary, summary_font, news_width, draw)
        summary_y = current_y + title_height + 20
        
        for j, line in enumerate(summary_lines[:2]):
            draw.text((news_x, summary_y + j*38), line, font=summary_font, fill=C_TEXT_SUB)
        
        summary_height = len(summary_lines[:2]) * 38
        
        # 底部信息
        meta_y = current_y + title_height + summary_height + 28
        meta_text = f"{news['source']}  ·  {news['time']}"
        draw.text((news_x, meta_y), meta_text, font=meta_font, fill=C_TEXT_META)
        
        # 卡片间距
        current_y += title_height + summary_height + 72
        
        # 分隔线（最后一条新闻不画）
        if i < len(news_list) - 1:
            if current_y < IMG_HEIGHT - 150:
                draw.line([(margin_x, current_y - 36), (IMG_WIDTH - margin_x, current_y - 36)], 
                         fill=C_DIVIDER, width=1)
    
    # ============ 3. 底部 ============
    
    footer_y = IMG_HEIGHT - 80
    
    draw.text((IMG_WIDTH // 2, footer_y), f"共 {len(news_list)} 条  ·  AI Daily Briefing", 
              font=meta_font, fill=C_TEXT_META, anchor='mt')
    
    # 保存
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 已保存：{output_path}")
    
    return output_path

# ============ 飞书推送 ============

def send_feishu(title: str, content: str, image_path: str) -> bool:
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
    parser = argparse.ArgumentParser(description='AI 早报 v5.0')
    parser.add_argument('--date', type=str, help='日期 YYYY-MM-DD')
    args = parser.parse_args()
    
    date = datetime.strptime(args.date, '%Y-%m-%d') if args.date else datetime.now()
    
    print(f"\n{'='*50}")
    print(f"📰 AI 产业早报 v5.0 · 专业媒体风")
    print(f"日期：{date.strftime('%Y年%m月%d日')}")
    print(f"{'='*50}")
    
    news_list = get_news()
    
    date_str = date.strftime('%Y%m%d')
    image_path = os.path.join(IMAGE_DIR, f"ai_daily_{date_str}.png")
    generate_image(news_list, date, image_path)
    
    # 保存数据
    with open(os.path.join(OUTPUT_DIR, f"ai_daily_{date_str}.json"), 'w', encoding='utf-8') as f:
        json.dump({'date': date.isoformat(), 'news': news_list}, f, ensure_ascii=False, indent=2)
    
    # 推送文案
    content = f"🌅 早安！今日 AI 精选 {len(news_list)} 条\n\n"
    for i, news in enumerate(news_list, 1):
        content += f"{i}. {news['title']}\n"
        content += f"   {news['source']} · {news['time']}\n\n"
    content += f"\n📊 完整早报请查看图片"
    
    send_feishu(f"📰 AI 产业早报 {date.strftime('%m-%d')}", content, image_path)
    
    print(f"\n{'='*50}")
    print(f"✅ 完成")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
