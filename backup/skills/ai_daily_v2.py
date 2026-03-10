# -*- coding: utf-8 -*-
"""
AI 早报生成器 v2.0 - 精美杂志风
支持完美中文显示 + 高级配色 + 杂志级排版
"""

import sys
import os
import json
import time
import urllib.request
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# PIL 导入
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    print("PIL 加载成功")
except ImportError:
    print("错误：请安装 Pillow")
    sys.exit(1)

# ============ 配置区域 ============

OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\ai_daily"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

for d in [OUTPUT_DIR, IMAGE_DIR]:
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
    'sunset': {
        'bg_start': (255, 107, 107),    # 珊瑚红
        'bg_end': (78, 205, 196),       # 青绿色
        'accent': (255, 230, 109),      # 柠檬黄
        'text_dark': (44, 62, 80),
        'text_light': (255, 255, 255),
        'card_bg': (255, 255, 255, 240),
    },
    'ocean': {
        'bg_start': (2, 3, 129),        # 深蓝
        'bg_end': (40, 167, 69),        # 绿色
        'accent': (255, 193, 7),
        'text_dark': (33, 37, 41),
        'text_light': (248, 249, 250),
        'card_bg': (255, 255, 255, 245),
    },
    'purple': {
        'bg_start': (102, 126, 234),    # 紫蓝
        'bg_end': (118, 75, 162),       # 深紫
        'accent': (255, 107, 129),
        'text_dark': (45, 52, 54),
        'text_light': (255, 255, 255),
        'card_bg': (255, 255, 255, 248),
    },
    'midnight': {
        'bg_start': (15, 32, 39),       # 深夜蓝
        'bg_end': (39, 60, 117),        # 深蓝
        'accent': (247, 231, 127),      # 金色
        'text_dark': (236, 240, 241),
        'text_light': (255, 255, 255),
        'card_bg': (30, 41, 59, 230),
    }
}

# 默认使用 midnight 配色（高级感）
DEFAULT_SCHEME = 'midnight'

# ============ 字体管理 ============

class FontManager:
    """字体管理器"""
    
    def __init__(self):
        self.fonts = {}
        self._load_fonts()
    
    def _load_fonts(self):
        """加载字体"""
        # Windows 中文字体路径
        font_candidates = [
            # 微软雅黑（推荐）
            ('msyh', r'C:\Windows\Fonts\msyh.ttc'),
            ('msyhbd', r'C:\Windows\Fonts\msyhbd.ttc'),
            # 思源黑体
            ('source', r'C:\Windows\Fonts\SourceHanSansCN-Regular.otf'),
            # 苹方（如果有）
            ('pingfang', r'C:\Windows\Fonts\PingFang.ttc'),
            # 宋体
            ('simsun', r'C:\Windows\Fonts\simsun.ttc'),
            # 黑体
            ('simhei', r'C:\Windows\Fonts\simhei.ttf'),
            # 英文字体备用
            ('arial', r'C:\Windows\Fonts\arial.ttf'),
        ]
        
        for name, path in font_candidates:
            if os.path.exists(path):
                try:
                    # 尝试不同字号
                    for size in [24, 28, 32, 36, 42, 48, 56, 72, 80]:
                        key = f"{name}_{size}"
                        self.fonts[key] = ImageFont.truetype(path, size)
                    print(f"✓ 字体加载：{name}")
                except Exception as e:
                    pass
        
        # 如果没有任何中文字体，使用默认
        if not self.fonts:
            print("⚠ 未找到中文字体，使用默认字体")
    
    def get(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """获取字体"""
        # 优先使用微软雅黑
        prefix = 'msyhbd' if bold else 'msyh'
        key = f"{prefix}_{size}"
        
        if key in self.fonts:
            return self.fonts[key]
        
        # 降级查找
        for font_key, font in self.fonts.items():
            if font_key.endswith(f"_{size}"):
                return font
        
        # 最后降级
        return ImageFont.load_default()

# ============ 新闻数据 ============

def get_sample_news() -> List[Dict]:
    """获取示例新闻（用于测试）"""
    return [
        {
            'title': 'OpenAI 发布 GPT-5，性能提升 10 倍',
            'summary': 'OpenAI 今日发布最新大语言模型 GPT-5，在推理、代码、多模态等方面实现重大突破',
            'source': 'OpenAI Blog',
            'category': '🤖 模型',
            'importance': 5,
            'time': '09:30'
        },
        {
            'title': '谷歌推出 Gemini 2.0，多模态能力再升级',
            'summary': 'Google DeepMind 发布新一代多模态模型，图像理解能力提升显著',
            'source': 'Google AI',
            'category': '🤖 模型',
            'importance': 5,
            'time': '10:15'
        },
        {
            'title': 'Anthropic 完成 10 亿美元 C 轮融资',
            'summary': 'AI 安全公司估值达 50 亿美元，由 Spark Capital 领投',
            'source': 'TechCrunch',
            'category': '💰 融资',
            'importance': 4,
            'time': '11:00'
        },
        {
            'title': '微软 Copilot 日活用户突破 1 亿',
            'summary': 'AI 助手普及加速，企业采用率持续增长',
            'source': 'The Verge',
            'category': '📱 应用',
            'importance': 4,
            'time': '14:20'
        },
        {
            'title': '特斯拉 Optimus 机器人开始工厂测试',
            'summary': '人形机器人正式进入实际工作场景，预计 2027 年量产',
            'source': 'Reuters',
            'category': '🏢 公司',
            'importance': 4,
            'time': '16:45'
        },
        {
            'title': '欧盟 AI 法案正式生效',
            'summary': '全球首部综合性 AI 监管法规开始实施，影响深远',
            'source': 'BBC',
            'category': '📜 政策',
            'importance': 3,
            'time': '18:00'
        },
    ]

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

def draw_decorative_elements(draw: ImageDraw.ImageDraw, width: int, height: int, accent_color: tuple):
    """绘制装饰元素"""
    # 顶部装饰线
    draw.line([(100, 80), (width-100, 80)], fill=accent_color, width=3)
    
    # 底部装饰点
    for i in range(5):
        x = width // 2 - 100 + i * 50
        y = height - 100
        draw.ellipse([(x-4, y-4), (x+4, y+4)], fill=accent_color)

def generate_magazine_style_image(news_items: List[Dict], date: datetime, output_path: str, scheme: str = 'midnight'):
    """生成杂志风格早报图片"""
    
    print(f"\n🎨 生成杂志风格图片 (配色：{scheme})...")
    
    # 获取配色方案
    colors = COLOR_SCHEMES.get(scheme, COLOR_SCHEMES['midnight'])
    
    # 创建图片
    img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_mgr = FontManager()
    
    # ============ 绘制背景 ============
    draw_gradient_background(img, colors['bg_start'], colors['bg_end'])
    
    # ============ 头部区域 ============
    header_y = 120
    
    # 日期标签
    date_text = date.strftime('%Y.%m.%d')
    date_font = font_mgr.get(28)
    date_width = draw.textlength(date_text, font=date_font)
    draw.text((IMG_WIDTH - 100 - date_width, 80), date_text, 
              font=date_font, fill=colors['text_light'], anchor='rt')
    
    # 星期
    weekday = date.strftime('%A')
    weekday_map = {
        'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三',
        'Thursday': '星期四', 'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'
    }
    weekday_cn = weekday_map.get(weekday, '')
    draw.text((IMG_WIDTH - 100, 115), weekday_cn, 
              font=font_mgr.get(24), fill=colors['text_light'], anchor='rt')
    
    # 主标题
    title = "AI 产业早报"
    title_font = font_mgr.get(80, bold=True)
    draw.text((IMG_WIDTH // 2, header_y), title, 
              font=title_font, fill=colors['text_light'], anchor='mm')
    
    # 副标题
    subtitle = "全球人工智能产业动态 · 每日精选"
    subtitle_font = font_mgr.get(28)
    draw.text((IMG_WIDTH // 2, header_y + 90), subtitle, 
              font=subtitle_font, fill=colors['text_light'], anchor='mm')
    
    # 装饰线
    line_y = header_y + 150
    draw.line([(100, line_y), (IMG_WIDTH - 100, line_y)], 
              fill=colors['accent'], width=2)
    
    # ============ 内容区域 ============
    content_start = line_y + 60
    card_margin = 60
    card_padding = 30
    
    # 按分类整理新闻
    categories = {}
    for news in news_items:
        cat = news.get('category', '📰 其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(news)
    
    # 绘制各分类
    current_y = content_start
    
    category_icons = {
        '🤖 模型': '🧠',
        '📱 应用': '📲',
        '💰 融资': '💵',
        '🏢 公司': '🏛️',
        '📜 政策': '📋',
        '📰 其他': '📌'
    }
    
    for cat_name, cat_news in categories.items():
        if current_y > IMG_HEIGHT - 200:
            break
        
        # 分类标题栏
        icon = category_icons.get(cat_name, '📌')
        cat_title = f"{icon}  {cat_name.replace('🤖 ', '').replace('📱 ', '').replace('💰 ', '').replace('🏢 ', '').replace('📜 ', '')}"
        
        cat_font = font_mgr.get(36, bold=True)
        draw.text((card_margin, current_y), cat_title, 
                  font=cat_font, fill=colors['accent'], anchor='lt')
        
        current_y += 50
        
        # 绘制每条新闻
        for news in cat_news[:2]:  # 每个分类最多 2 条
            if current_y > IMG_HEIGHT - 180:
                break
            
            # 卡片背景
            card_height = 140
            card_rect = [
                (card_margin, current_y),
                (IMG_WIDTH - card_margin, current_y + card_height)
            ]
            
            # 圆角矩形背景
            draw.rounded_rectangle(
                card_rect,
                radius=12,
                fill=colors['card_bg']
            )
            
            # 新闻标题
            title_text = news['title']
            if len(title_text) > 45:
                title_text = title_text[:43] + '...'
            
            title_font = font_mgr.get(32, bold=True)
            text_color = colors['text_dark'] if scheme != 'midnight' else colors['text_light']
            draw.text((card_margin + card_padding, current_y + 15), 
                      "• " + title_text, 
                      font=title_font, fill=text_color, anchor='lt')
            
            # 新闻来源和时间
            meta_text = f"{news.get('source', '未知')} · {news.get('time', '')}"
            meta_font = font_mgr.get(24)
            meta_color = (150, 150, 150) if scheme != 'midnight' else (180, 180, 180)
            draw.text((card_margin + card_padding, current_y + 65), 
                      meta_text, 
                      font=meta_font, fill=meta_color, anchor='lt')
            
            # 重要性星标
            stars = "★" * news.get('importance', 3)
            stars_font = font_mgr.get(24)
            stars_width = draw.textlength(stars, font=stars_font)
            draw.text((IMG_WIDTH - card_margin - card_padding - stars_width, current_y + 65), 
                      stars, 
                      font=stars_font, fill=colors['accent'], anchor='lt')
            
            current_y += card_height + 15
        
        current_y += 25  # 分类间距
    
    # ============ 底部区域 ============
    footer_y = IMG_HEIGHT - 100
    
    # 底部装饰线
    draw.line([(IMG_WIDTH // 2 - 100, footer_y - 20), 
               (IMG_WIDTH // 2 + 100, footer_y - 20)], 
              fill=colors['accent'], width=2)
    
    # 统计信息
    stats_text = f"本期共 {len(news_items)} 条精选 · AI 改变世界"
    stats_font = font_mgr.get(26)
    draw.text((IMG_WIDTH // 2, footer_y + 10), stats_text, 
              font=stats_font, fill=colors['text_light'], anchor='mt')
    
    # 版权信息
    copyright_text = "AI Daily Briefing · Generated by nanobot"
    copyright_font = font_mgr.get(20)
    draw.text((IMG_WIDTH // 2, footer_y + 50), copyright_text, 
              font=copyright_font, fill=colors['text_light'], anchor='mt')
    
    # ============ 保存 ============
    # 转换为 RGB 并保存
    img_rgb = img.convert('RGB')
    img_rgb.save(output_path, 'PNG', quality=95, optimize=True)
    
    print(f"✅ 图片已保存：{output_path}")
    print(f"   尺寸：{IMG_WIDTH}x{IMG_HEIGHT}")
    print(f"   配色：{scheme}")
    
    return output_path

# ============ 飞书推送 ============

def send_to_feishu(title: str, content: str, image_path: str) -> bool:
    """发送飞书消息"""
    if not FEISHU_WEBHOOK:
        print("⚠ 未配置飞书 Webhook，跳过推送")
        return False
    
    # 读取图片并转 base64
    try:
        import base64
        with open(image_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ 读取图片失败：{e}")
        return False
    
    # 发送图文消息
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
        req = urllib.request.Request(
            FEISHU_WEBHOOK,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            print("✅ 飞书推送成功")
            return True
    except Exception as e:
        print(f"❌ 飞书推送失败：{e}")
        return False

# ============ 主流程 ============

class AIDailyMagazine:
    """AI 早报杂志生成器"""
    
    def __init__(self, color_scheme: str = 'midnight'):
        self.color_scheme = color_scheme
        self.news_items = []
    
    def generate(self, date: datetime = None) -> Dict:
        """生成早报"""
        if not date:
            date = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"📰 AI 产业早报 · 杂志版")
        print(f"日期：{date.strftime('%Y年%m月%d日')}")
        print(f"配色：{self.color_scheme}")
        print(f"{'='*60}")
        
        # 1. 获取新闻
        self.news_items = get_sample_news()
        
        # 2. 生成图片
        date_str = date.strftime('%Y%m%d')
        image_path = os.path.join(IMAGE_DIR, f"ai_daily_{date_str}.png")
        generate_magazine_style_image(
            self.news_items, 
            date, 
            image_path,
            self.color_scheme
        )
        
        # 3. 保存数据
        data_path = os.path.join(OUTPUT_DIR, f"ai_daily_{date_str}.json")
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump({
                'date': date.isoformat(),
                'news_count': len(self.news_items),
                'news': self.news_items
            }, f, ensure_ascii=False, indent=2)
        
        # 4. 生成推送文案
        push_content = self._generate_push_content()
        
        # 5. 发送飞书
        send_to_feishu(
            f"📰 AI 产业早报 {date.strftime('%m-%d')}",
            push_content,
            image_path
        )
        
        print(f"\n{'='*60}")
        print(f"✅ 生成完成")
        print(f"图片：{image_path}")
        print(f"{'='*60}")
        
        return {
            'success': True,
            'image_path': image_path,
            'news_count': len(self.news_items)
        }
    
    def _generate_push_content(self) -> str:
        """生成推送文案"""
        content = f"🌅 早安！今日 AI 产业精选\n\n"
        
        for i, news in enumerate(self.news_items[:5], 1):
            stars = "⭐" * news.get('importance', 3)
            content += f"{i}. {news['title'][:35]}...\n"
            content += f"   {stars} {news.get('source', '')}\n\n"
        
        content += f"\n📊 完整早报共 {len(self.news_items)} 条，请查看图片"
        
        return content

# ============ 主函数 ============

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 早报生成器 v2.0 - 杂志风')
    parser.add_argument('--date', type=str, help='日期 YYYY-MM-DD')
    parser.add_argument('--scheme', type=str, 
                       choices=['sunset', 'ocean', 'purple', 'midnight'],
                       default='midnight', help='配色方案')
    parser.add_argument('--test', action='store_true', help='测试模式')
    
    args = parser.parse_args()
    
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()
    
    generator = AIDailyMagazine(color_scheme=args.scheme)
    result = generator.generate(date)
    
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    main()
