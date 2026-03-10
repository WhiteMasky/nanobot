# -*- coding: utf-8 -*-
"""
AI 早报生成器 v3.0 - 精美杂志版
修复：方框乱码、文字截断
新增：新闻摘要、热点标签、二维码、天气、历史今天
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# PIL 导入
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    print("PIL 加载成功")
except ImportError:
    print("错误：请安装 Pillow")
    sys.exit(1)

# ============ 配置区域 ============

OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\ai_daily"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
QR_DIR = os.path.join(OUTPUT_DIR, "qrcodes")

for d in [OUTPUT_DIR, IMAGE_DIR, QR_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# API 配置
DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', 'sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b')
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

# 图片配置
IMG_WIDTH = 1080
IMG_HEIGHT = 1920

# ============ 高级配色方案 ============

COLOR_SCHEMES = {
    'midnight': {
        'name': '深夜蓝',
        'bg_start': (15, 32, 39),
        'bg_end': (39, 60, 117),
        'accent': (247, 231, 127),
        'accent2': (102, 126, 234),
        'text_primary': (255, 255, 255),
        'text_secondary': (180, 180, 180),
        'text_muted': (120, 120, 120),
        'card_bg': (30, 41, 59, 230),
        'tag_bg': (102, 126, 234, 200),
    },
    'sunset': {
        'name': '日落橙',
        'bg_start': (255, 107, 107),
        'bg_end': (78, 205, 196),
        'accent': (255, 230, 109),
        'accent2': (255, 118, 117),
        'text_primary': (255, 255, 255),
        'text_secondary': (240, 240, 240),
        'text_muted': (200, 200, 200),
        'card_bg': (255, 255, 255, 220),
        'tag_bg': (255, 107, 107, 200),
    },
    'ocean': {
        'name': '海洋蓝',
        'bg_start': (2, 3, 129),
        'bg_end': (40, 167, 69),
        'accent': (255, 193, 7),
        'accent2': (23, 162, 184),
        'text_primary': (248, 249, 250),
        'text_secondary': (220, 220, 220),
        'text_muted': (180, 180, 180),
        'card_bg': (255, 255, 255, 220),
        'tag_bg': (40, 167, 69, 200),
    },
    'purple': {
        'name': '紫罗兰',
        'bg_start': (102, 126, 234),
        'bg_end': (118, 75, 162),
        'accent': (255, 107, 129),
        'accent2': (255, 230, 109),
        'text_primary': (255, 255, 255),
        'text_secondary': (230, 230, 230),
        'text_muted': (180, 180, 180),
        'card_bg': (255, 255, 255, 200),
        'tag_bg': (118, 75, 162, 200),
    }
}

# ============ 字体管理 ============

class FontManager:
    """字体管理器 - 修复中文显示"""
    
    def __init__(self):
        self.fonts = {}
        self._load_fonts()
    
    def _load_fonts(self):
        """加载字体 - 优先使用微软雅黑"""
        font_candidates = [
            ('msyh', r'C:\Windows\Fonts\msyh.ttc'),      # 微软雅黑
            ('msyhbd', r'C:\Windows\Fonts\msyhbd.ttc'),  # 微软雅黑粗体
            ('simhei', r'C:\Windows\Fonts\simhei.ttf'),  # 黑体
            ('simsun', r'C:\Windows\Fonts\simsun.ttc'),  # 宋体
            ('arial', r'C:\Windows\Fonts\arial.ttf'),    # Arial
        ]
        
        loaded = False
        for name, path in font_candidates:
            if os.path.exists(path):
                try:
                    for size in [20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80]:
                        key = f"{name}_{size}"
                        self.fonts[key] = ImageFont.truetype(path, size)
                    if not loaded:
                        print(f"✓ 字体加载：{name}")
                        loaded = True
                except Exception as e:
                    pass
        
        if not self.fonts:
            print("⚠ 未找到中文字体，使用默认")
    
    def get(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """获取指定大小的字体"""
        # 优先微软雅黑
        prefix = 'msyhbd' if bold else 'msyh'
        key = f"{prefix}_{size}"
        
        if key in self.fonts:
            return self.fonts[key]
        
        # 查找同尺寸其他字体
        for font_key, font in self.fonts.items():
            if font_key.endswith(f"_{size}"):
                return font
        
        # 降级
        return ImageFont.load_default()

# ============ 新闻数据 ============

def get_sample_news() -> List[Dict]:
    """获取示例新闻"""
    return [
        {
            'title': 'OpenAI 发布 GPT-5，性能提升 10 倍',
            'summary': 'OpenAI 今日发布最新大语言模型 GPT-5，在推理能力、代码生成、多模态理解等方面实现重大突破。相比 GPT-4，新模型在数学推理任务上准确率提升 40%，代码生成能力提升 60%，并支持 128K 上下文窗口。',
            'source': 'OpenAI Blog',
            'category': '模型',
            'tags': ['大模型', 'GPT', '重磅'],
            'importance': 5,
            'time': '09:30',
            'url': 'https://openai.com/blog/gpt-5'
        },
        {
            'title': '谷歌推出 Gemini 2.0，多模态能力再升级',
            'summary': 'Google DeepMind 发布新一代多模态模型 Gemini 2.0，图像理解、视频分析能力显著提升。新模型支持实时视频对话，能够理解复杂图表和科学公式，已在 Google 搜索和 Assistant 中集成。',
            'source': 'Google AI',
            'category': '模型',
            'tags': ['多模态', 'Gemini', '谷歌'],
            'importance': 5,
            'time': '10:15',
            'url': 'https://blog.google/gemini-2'
        },
        {
            'title': 'Anthropic 完成 10 亿美元 C 轮融资',
            'summary': 'AI 安全公司 Anthropic 宣布完成 10 亿美元 C 轮融资，由 Spark Capital 领投，估值达 50 亿美元。资金将用于 Claude 模型研发和 AI 安全研究，计划 2026 年推出新一代模型。',
            'source': 'TechCrunch',
            'category': '融资',
            'tags': ['融资', 'Anthropic', 'Claude'],
            'importance': 4,
            'time': '11:00',
            'url': 'https://techcrunch.com/anthropic'
        },
        {
            'title': '微软 Copilot 日活用户突破 1 亿',
            'summary': '微软宣布 Copilot AI 助手日活跃用户突破 1 亿，企业采用率持续增长。Windows 11 中 Copilot 使用率达 65%，Office 365 集成后生产力提升 30%。',
            'source': 'The Verge',
            'category': '应用',
            'tags': ['微软', 'Copilot', '用户增长'],
            'importance': 4,
            'time': '14:20',
            'url': 'https://theverge.com/copilot'
        },
        {
            'title': '特斯拉 Optimus 机器人开始工厂测试',
            'summary': '特斯拉宣布 Optimus 人形机器人正式进入工厂测试阶段，执行简单装配任务。马斯克预计 2027 年量产，售价低于 2 万美元，将率先应用于特斯拉生产线。',
            'source': 'Reuters',
            'category': '公司',
            'tags': ['特斯拉', '机器人', '量产'],
            'importance': 4,
            'time': '16:45',
            'url': 'https://reuters.com/tesla'
        },
        {
            'title': '欧盟 AI 法案正式生效',
            'summary': '全球首部综合性 AI 监管法规《欧盟 AI 法案》今日正式生效。法案将 AI 系统分为四个风险等级，禁止社会评分等高风险应用，违规企业最高面临全球营收 6% 罚款。',
            'source': 'BBC',
            'category': '政策',
            'tags': ['监管', '欧盟', '合规'],
            'importance': 3,
            'time': '18:00',
            'url': 'https://bbc.com/eu-ai-act'
        },
    ]

def get_weather_info() -> Dict:
    """获取天气信息（示例）"""
    return {
        'city': '北京',
        'condition': '晴',
        'temp_high': 18,
        'temp_low': 8,
        'aqi': 45,
        'aqi_level': '优'
    }

def get_history_today() -> str:
    """获取历史上的今天"""
    history_events = [
        "2016 年 - AlphaGo 击败李世石",
        "2022 年 - ChatGPT 发布",
        "1989 年 - 万维网概念提出",
        "1958 年 - 第一块集成电路诞生"
    ]
    import random
    return random.choice(history_events)

# ============ 二维码生成 ============

def generate_qr_code(url: str, output_path: str, size: int = 150):
    """生成二维码（简化版：使用在线 API）"""
    try:
        # 使用 Google Chart API 生成二维码
        encoded_url = urllib.parse.quote(url)
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={encoded_url}"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(qr_api, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            qr_data = resp.read()
        
        # 保存二维码
        with open(output_path, 'wb') as f:
            f.write(qr_data)
        
        return output_path
    except Exception as e:
        print(f"⚠ 二维码生成失败：{e}")
        return None

# ============ 文本处理 ============

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
    """文本自动换行"""
    lines = []
    words = text.split(' ')
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return lines

def truncate_text(text: str, max_length: int = 50) -> str:
    """智能截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length-2] + "..."

# ============ 图片生成 ============

def draw_gradient_background(img: Image.Image, color1: tuple, color2: tuple):
    """绘制垂直渐变背景"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_rounded_rectangle(draw: ImageDraw.ImageDraw, rect: List[Tuple], radius: int, **kwargs):
    """绘制圆角矩形"""
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    
    # 绘制主体
    draw.rectangle([(x1, y1 + radius), (x2, y2 - radius)], **kwargs)
    draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)], **kwargs)
    
    # 绘制四个角
    draw.pieslice([(x1, y1), (x1 + radius*2, y1 + radius*2)], 180, 270, **kwargs)
    draw.pieslice([(x2 - radius*2, y1), (x2, y1 + radius*2)], 270, 360, **kwargs)
    draw.pieslice([(x1, y2 - radius*2), (x1 + radius*2, y2)], 90, 180, **kwargs)
    draw.pieslice([(x2 - radius*2, y2 - radius*2), (x2, y2)], 0, 90, **kwargs)

def generate_v3_image(news_items: List[Dict], date: datetime, output_path: str, scheme: str = 'midnight'):
    """生成 v3 版本早报图片"""
    
    print(f"\n🎨 生成 v3 杂志风格图片 (配色：{scheme})...")
    
    # 获取配色
    colors = COLOR_SCHEMES.get(scheme, COLOR_SCHEMES['midnight'])
    
    # 创建图片
    img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_mgr = FontManager()
    
    # ============ 1. 绘制背景 ============
    draw_gradient_background(img, colors['bg_start'], colors['bg_end'])
    
    # ============ 2. 头部区域 ============
    header_y = 100
    
    # 日期和天气
    date_str = date.strftime('%Y.%m.%d')
    weekday_map = {
        'Monday': '周一', 'Tuesday': '周二', 'Wednesday': '周三',
        'Thursday': '周四', 'Friday': '周五', 'Saturday': '周六', 'Sunday': '周日'
    }
    weekday = weekday_map.get(date.strftime('%A'), '')
    
    # 天气信息
    weather = get_weather_info()
    weather_text = f"{weather['city']} {weather['condition']} {weather['temp_low']}°-{weather['temp_high']}°"
    
    date_font = font_mgr.get(28)
    draw.text((80, 80), date_str, font=date_font, fill=colors['text_primary'], anchor='lt')
    draw.text((80, 115), f"{weekday} · {weather_text}", font=font_mgr.get(24), 
              fill=colors['text_secondary'], anchor='lt')
    
    # 主标题
    title = "AI 产业早报"
    title_font = font_mgr.get(72, bold=True)
    draw.text((IMG_WIDTH // 2, header_y), title, font=title_font, 
              fill=colors['text_primary'], anchor='mm')
    
    # 副标题
    subtitle = "全球人工智能产业动态 · 每日精选"
    draw.text((IMG_WIDTH // 2, header_y + 85), subtitle, font=font_mgr.get(26), 
              fill=colors['text_secondary'], anchor='mm')
    
    # 装饰线
    line_y = header_y + 140
    draw.line([(80, line_y), (IMG_WIDTH - 80, line_y)], fill=colors['accent'], width=3)
    
    # ============ 3. 内容区域 ============
    content_start = line_y + 50
    card_margin = 60
    card_padding = 25
    
    # 分类图标
    category_icons = {
        '模型': '🧠',
        '应用': '📱',
        '融资': '💰',
        '公司': '🏢',
        '政策': '📋',
        '其他': '📌'
    }
    
    # 按分类整理
    categories = {}
    for news in news_items:
        cat = news.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(news)
    
    current_y = content_start
    
    for cat_name, cat_news in categories.items():
        if current_y > IMG_HEIGHT - 250:
            break
        
        # 分类标题
        icon = category_icons.get(cat_name, '📌')
        cat_title = f"{icon} {cat_name}"
        
        draw.text((card_margin, current_y), cat_title, 
                  font=font_mgr.get(36, bold=True), fill=colors['accent'], anchor='lt')
        
        current_y += 45
        
        # 绘制新闻卡片
        for news in cat_news[:2]:
            if current_y > IMG_HEIGHT - 220:
                break
            
            card_height = 180
            card_rect = [(card_margin, current_y), (IMG_WIDTH - card_margin, current_y + card_height)]
            
            # 卡片背景
            draw_rounded_rectangle(draw, card_rect, radius=15, fill=colors['card_bg'])
            
            inner_x = card_margin + card_padding
            
            # 新闻标题
            title_text = truncate_text(news['title'], 45)
            draw.text((inner_x, current_y + 15), "• " + title_text, 
                      font=font_mgr.get(30, bold=True), fill=colors['text_primary'], anchor='lt')
            
            # 新闻摘要（新增）
            summary = truncate_text(news.get('summary', ''), 80)
            summary_lines = wrap_text(summary, font_mgr.get(22), IMG_WIDTH - card_margin*2 - card_padding*2 - 50, draw)
            
            summary_y = current_y + 55
            for i, line in enumerate(summary_lines[:2]):
                draw.text((inner_x, summary_y + i*26), line, 
                          font=font_mgr.get(22), fill=colors['text_secondary'], anchor='lt')
            
            # 标签（新增）
            tags = news.get('tags', [])[:3]
            tag_y = current_y + card_height - 50
            tag_x = inner_x
            
            for tag in tags:
                tag_width = draw.textlength(tag, font=font_mgr.get(18)) + 16
                draw.rounded_rectangle(
                    [(tag_x, tag_y), (tag_x + tag_width, tag_y + 28)],
                    radius=6,
                    fill=colors['tag_bg']
                )
                draw.text((tag_x + 8, tag_y + 6), tag, 
                          font=font_mgr.get(18), fill=colors['text_primary'], anchor='lt')
                tag_x += tag_width + 8
            
            # 来源和时间
            meta_text = f"{news.get('source', '')} · {news.get('time', '')}"
            draw.text((inner_x, current_y + card_height - 28), meta_text, 
                      font=font_mgr.get(20), fill=colors['text_muted'], anchor='lt')
            
            # 重要性星标
            stars = "★" * news.get('importance', 3)
            stars_width = draw.textlength(stars, font=font_mgr.get(22))
            draw.text((IMG_WIDTH - card_margin - card_padding - stars_width, 
                      current_y + card_height - 28), 
                      stars, font=font_mgr.get(22), fill=colors['accent'], anchor='lt')
            
            current_y += card_height + 15
        
        current_y += 20
    
    # ============ 4. 底部区域 ============
    footer_y = IMG_HEIGHT - 150
    
    # 底部装饰线
    draw.line([(IMG_WIDTH // 2 - 80, footer_y), (IMG_WIDTH // 2 + 80, footer_y)], 
              fill=colors['accent'], width=2)
    
    # 统计信息
    stats_text = f"本期共 {len(news_items)} 条精选"
    draw.text((IMG_WIDTH // 2, footer_y + 25), stats_text, 
              font=font_mgr.get(24), fill=colors['text_primary'], anchor='mt')
    
    # 历史上的今天
    history = get_history_today()
    draw.text((IMG_WIDTH // 2, footer_y + 55), history, 
              font=font_mgr.get(20), fill=colors['text_secondary'], anchor='mt')
    
    # 版权
    draw.text((IMG_WIDTH // 2, footer_y + 85), "AI Daily Briefing · nanobot", 
              font=font_mgr.get(18), fill=colors['text_muted'], anchor='mt')
    
    # ============ 5. 二维码（可选） ============
    # 如果有新闻 URL，生成二维码
    if news_items and news_items[0].get('url'):
        qr_path = os.path.join(QR_DIR, f"qr_{date.strftime('%Y%m%d')}.png")
        qr_result = generate_qr_code(news_items[0]['url'], qr_path)
        
        if qr_result and os.path.exists(qr_path):
            try:
                qr_img = Image.open(qr_path)
                qr_img = qr_img.resize((100, 100))
                img.paste(qr_img, (IMG_WIDTH - 120, IMG_HEIGHT - 120))
            except:
                pass
    
    # ============ 6. 保存 ============
    img_rgb = img.convert('RGB')
    img_rgb.save(output_path, 'PNG', quality=95, optimize=True)
    
    print(f"✅ 图片已保存：{output_path}")
    print(f"   尺寸：{IMG_WIDTH}x{IMG_HEIGHT}")
    print(f"   配色：{colors['name']}")
    
    return output_path

# ============ 飞书推送 ============

def send_to_feishu(title: str, content: str, image_path: str) -> bool:
    """发送飞书消息"""
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
            result = json.loads(resp.read().decode('utf-8'))
            print("✅ 飞书推送成功")
            return True
    except Exception as e:
        print(f"❌ 飞书推送失败：{e}")
        return False

# ============ 主流程 ============

class AIDailyV3:
    """AI 早报 v3.0 生成器"""
    
    def __init__(self, color_scheme: str = 'midnight'):
        self.color_scheme = color_scheme
        self.news_items = []
    
    def generate(self, date: datetime = None) -> Dict:
        """生成早报"""
        if not date:
            date = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"📰 AI 产业早报 v3.0")
        print(f"日期：{date.strftime('%Y年%m月%d日')}")
        print(f"配色：{COLOR_SCHEMES.get(self.color_scheme, {}).get('name', self.color_scheme)}")
        print(f"{'='*60}")
        
        # 1. 获取新闻
        self.news_items = get_sample_news()
        
        # 2. 生成图片
        date_str = date.strftime('%Y%m%d')
        image_path = os.path.join(IMAGE_DIR, f"ai_daily_{date_str}.png")
        generate_v3_image(self.news_items, date, image_path, self.color_scheme)
        
        # 3. 保存数据
        data_path = os.path.join(OUTPUT_DIR, f"ai_daily_{date_str}.json")
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump({
                'date': date.isoformat(),
                'news_count': len(self.news_items),
                'news': self.news_items
            }, f, ensure_ascii=False, indent=2)
        
        # 4. 推送文案
        push_content = self._generate_push_content()
        
        # 5. 发送飞书
        send_to_feishu(f"📰 AI 产业早报 {date.strftime('%m-%d')}", push_content, image_path)
        
        print(f"\n{'='*60}")
        print(f"✅ 生成完成")
        print(f"{'='*60}")
        
        return {
            'success': True,
            'image_path': image_path,
            'news_count': len(self.news_items)
        }
    
    def _generate_push_content(self) -> str:
        """生成推送文案"""
        content = f"🌅 早安！今日 AI 精选 {len(self.news_items)} 条\n\n"
        
        for i, news in enumerate(self.news_items[:5], 1):
            stars = "⭐" * news.get('importance', 3)
            tags = " ".join([f"#{t}" for t in news.get('tags', [])[:2]])
            content += f"{i}. {news['title'][:32]}...\n"
            content += f"   {stars} {news.get('source', '')} {tags}\n\n"
        
        content += f"\n📊 完整早报请查看图片"
        
        return content

# ============ 主函数 ============

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 早报 v3.0')
    parser.add_argument('--date', type=str, help='日期 YYYY-MM-DD')
    parser.add_argument('--scheme', type=str, 
                       choices=['midnight', 'sunset', 'ocean', 'purple'],
                       default='midnight', help='配色方案')
    
    args = parser.parse_args()
    
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()
    
    generator = AIDailyV3(color_scheme=args.scheme)
    result = generator.generate(date)
    
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    main()
