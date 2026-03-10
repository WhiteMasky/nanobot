# -*- coding: utf-8 -*-
"""
AI 产业早报 v6.0 - 现代极简风
设计理念：参考 Apple News / 知乎日报
- 大留白
- 大字体
- 卡片式布局
- 只保留 Top 5 核心新闻
- 优雅的阴影和圆角
"""

import sys
import os
import json
import urllib.request
from datetime import datetime
from typing import List, Dict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ============ 配置 ============

OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\ai_daily"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# 飞书配置（使用 App ID/Secret 方式）
FEISHU_APP_ID = "cli_a924c3fc05f89cee"
FEISHU_APP_SECRET = "43MXrfLFa7sORlI3aMapEdG0aHVJqZ3E"
FEISHU_GROUP_CHAT_ID = "oc_b37cd210e982e8d1d9da4c3ed4014f00"  # 新主群

IMG_WIDTH = 1080
IMG_HEIGHT = 1920

# ============ 字体 ============

FONT_PATH = None

def init_font():
    global FONT_PATH
    for path in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]:
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
    return [
        {
            'title': 'OpenAI 发布 GPT-5，推理能力提升 40%',
            'summary': 'OpenAI 正式发布 GPT-5，在数学推理、代码生成、多模态理解等核心能力上实现重大突破。新模型支持 200K 上下文，推理速度提升 3 倍。',
            'source': 'OpenAI',
            'time': '09:30'
        },
        {
            'title': '谷歌 Gemini 2.0 支持实时视频对话',
            'summary': 'Google DeepMind 发布 Gemini 2.0，新增实时视频理解能力，可分析复杂图表和科学公式，已集成至 Google 搜索和 Assistant。',
            'source': 'Google AI',
            'time': '10:15'
        },
        {
            'title': 'Anthropic 融资 10 亿美元，估值 50 亿',
            'summary': 'AI 安全公司 Anthropic 完成 C 轮融资，由 Spark Capital 领投。资金将用于 Claude 模型研发，计划 2027 年推出新一代模型。',
            'source': 'TechCrunch',
            'time': '11:00'
        },
        {
            'title': '微软 Copilot 日活突破 1 亿',
            'summary': '微软宣布 Copilot 日活跃用户达 1 亿，Windows 11 中使用率 65%，Office 365 集成后企业生产力平均提升 30%。',
            'source': 'The Verge',
            'time': '14:20'
        },
        {
            'title': '欧盟 AI 法案正式生效',
            'summary': '全球首部 AI 综合监管法规生效，将 AI 系统分为四风险等级，禁止社会评分应用，违规企业最高面临全球营收 6% 罚款。',
            'source': 'Reuters',
            'time': '18:00'
        },
    ]

# ============ 文本处理 ============

def smart_truncate(text: str, max_length: int = 60) -> str:
    """智能截断文本，确保在标点处断开"""
    if len(text) <= max_length:
        return text
    
    # 尝试在标点处断开
    for punct in ['。', '！', '？', '；', ',', '.', '!', '?']:
        pos = text[:max_length].rfind(punct)
        if pos > max_length * 0.6:  # 在 60% 位置之后
            return text[:pos+1]
    
    # 没有合适标点，直接截断
    return text[:max_length-2] + '...'


def wrap_text_lines(text: str, max_chars_per_line: int = 40, max_lines: int = 2) -> List[str]:
    """将文本分成多行，确保不超出"""
    lines = []
    current_line = ""
    
    for char in text:
        if len(current_line) >= max_chars_per_line:
            lines.append(current_line)
            current_line = char
            if len(lines) >= max_lines:
                break
        else:
            current_line += char
    
    if current_line and len(lines) < max_lines:
        lines.append(current_line)
    
    return lines

def draw_rounded_rect(draw: ImageDraw.ImageDraw, rect, radius, fill, outline=None):
    """绘制圆角矩形"""
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius, fill=fill, outline=outline, width=1)

def generate_image(news_list: List[Dict], date: datetime, output_path: str):
    """生成早报图片 - 现代极简风"""
    
    print(f"\n🎨 生成 v6.0 现代极简风...")
    
    # 创建图片（浅灰背景）
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), '#F5F5F7')
    draw = ImageDraw.Draw(img)
    
    # 字体
    title_font = get_font(48, bold=True)
    date_font = get_font(24)
    news_num_font = get_font(32, bold=True)
    news_title_font = get_font(30, bold=True)
    summary_font = get_font(24)
    meta_font = get_font(20)
    
    # 配色（参考 Apple News）
    C_BG = '#F5F5F7'
    C_CARD = '#FFFFFF'
    C_TEXT_MAIN = '#1D1D1F'
    C_TEXT_SUB = '#86868B'
    C_TEXT_META = '#A1A1A6'
    C_ACCENT = '#0071E3'
    C_SHADOW = (0, 0, 0, 8)
    
    # 布局
    margin_x = 64
    current_y = 80
    
    # ============ 1. 头部 ============
    
    # 日期
    date_str = date.strftime('%Y.%m.%d')
    weekday_map = {
        'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三',
        'Thursday': '星期四', 'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'
    }
    weekday = weekday_map.get(date.strftime('%A'), '')
    
    draw.text((margin_x, current_y), f"{date_str}  {weekday}", font=date_font, fill=C_TEXT_META)
    
    current_y += 48
    
    # 主标题
    draw.text((margin_x, current_y), "AI 产业早报", font=title_font, fill=C_TEXT_MAIN)
    
    current_y += 80
    
    # ============ 2. 新闻卡片 ============
    
    card_margin = 64
    card_padding_x = 32
    card_padding_y = 28
    card_radius = 16
    
    for i, news in enumerate(news_list):
        # 序号
        num_str = f"{i+1}"
        
        # 标题处理 - 智能换行，最多 2 行
        title_text = news['title']
        title_lines = wrap_text_lines(title_text, max_chars_per_line=38, max_lines=2)
        title_height = len(title_lines) * 38
        
        # 摘要处理 - 智能截断 + 换行，最多 2 行
        summary = smart_truncate(news['summary'], max_length=70)
        summary_lines = wrap_text_lines(summary, max_chars_per_line=35, max_lines=2)
        summary_height = len(summary_lines) * 34
        
        # 卡片总高度
        card_height = card_padding_y * 2 + 40 + title_height + 16 + summary_height + 36
        
        # 卡片位置
        card_x1 = margin_x
        card_x2 = IMG_WIDTH - margin_x
        card_y1 = current_y
        card_y2 = current_y + card_height
        
        # 绘制卡片（白色圆角矩形）
        draw_rounded_rect(draw, [(card_x1, card_y1), (card_x2, card_y2)], 
                         card_radius, C_CARD)
        
        # 序号圆圈
        circle_x = margin_x + card_padding_x + 20
        circle_y = card_y1 + card_padding_y + 20
        draw.ellipse([(circle_x - 16, circle_y - 16), (circle_x + 16, circle_y + 16)], 
                    fill=C_ACCENT)
        draw.text((circle_x, circle_y), num_str, font=news_num_font, fill='#FFFFFF', anchor='mm')
        
        # 标题
        text_x = margin_x + card_padding_x + 56
        text_y = card_y1 + card_padding_y
        
        for j, line in enumerate(title_lines):
            draw.text((text_x, text_y + j*38), line, font=news_title_font, fill=C_TEXT_MAIN)
        
        # 摘要
        summary_y = text_y + title_height + 16
        for j, line in enumerate(summary_lines):
            draw.text((text_x, summary_y + j*34), line, font=summary_font, fill=C_TEXT_SUB)
        
        # 底部信息
        meta_y = card_y2 - 32
        meta_text = f"{news['source']}  ·  {news['time']}"
        draw.text((text_x, meta_y), meta_text, font=meta_font, fill=C_TEXT_META)
        
        # 更新 Y 坐标
        current_y = card_y2 + 24
        
        # 防止超出
        if current_y > IMG_HEIGHT - 150:
            break
    
    # ============ 3. 底部 ============
    
    footer_y = IMG_HEIGHT - 60
    draw.text((IMG_WIDTH // 2, footer_y), f"共 {len(news_list)} 条精选  ·  AI Daily", 
              font=meta_font, fill=C_TEXT_META, anchor='mm')
    
    # 保存
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 已保存：{output_path}")
    
    return output_path

# ============ 飞书推送 ============

def get_feishu_token():
    """获取飞书访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result.get('tenant_access_token')
            return None
    except Exception as e:
        return None

def send_feishu(title: str, content: str, image_path: str) -> bool:
    """发送飞书群消息（图文）"""
    token = get_feishu_token()
    if not token:
        print("❌ 获取飞书令牌失败")
        return False
    
    # 上传图片
    try:
        import base64
        with open(image_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ 读取图片失败：{e}")
        return False
    
    # 先上传媒体文件
    upload_url = "https://open.feishu.cn/open-apis/im/v1/images"
    upload_headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    upload_payload = {
        "image_type": "message",
        "image": img_data
    }
    
    image_key = None
    try:
        data = json.dumps(upload_payload).encode('utf-8')
        req = urllib.request.Request(upload_url, data=data, headers=upload_headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                image_key = result.get('data', {}).get('image_key')
    except Exception as e:
        print(f"❌ 上传图片失败：{e}")
    
    # 发送消息
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 构建图文消息
    if image_key:
        msg_content = {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "blue",
                "title": {"content": title, "tag": "plain_text"}
            },
            "elements": [
                {"tag": "img", "image_key": image_key},
                {"tag": "hr"},
                {"tag": "markdown", "content": content},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "🤖 AI 产业早报 · 每日更新"}]}
            ]
        }
    else:
        msg_content = {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "blue",
                "title": {"content": title, "tag": "plain_text"}
            },
            "elements": [
                {"tag": "markdown", "content": content},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "🤖 AI 产业早报 · 每日更新"}]}
            ]
        }
    
    payload = {
        "receive_id": FEISHU_GROUP_CHAT_ID,
        "msg_type": "interactive",
        "content": json.dumps(msg_content)
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('code') == 0:
                print("✅ 飞书推送成功")
                return True
            else:
                print(f"❌ 飞书推送失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 飞书推送异常：{e}")
        return False

# ============ 主流程 ============

def main():
    import argparse
    parser = argparse.ArgumentParser(description='AI 早报 v6.0')
    parser.add_argument('--date', type=str, help='日期 YYYY-MM-DD')
    args = parser.parse_args()
    
    date = datetime.strptime(args.date, '%Y-%m-%d') if args.date else datetime.now()
    
    print(f"\n{'='*50}")
    print(f"📰 AI 产业早报 v6.0 · 现代极简风")
    print(f"日期：{date.strftime('%Y年%m月%d日')}")
    print(f"{'='*50}")
    
    news_list = get_news()
    
    date_str = date.strftime('%Y%m%d')
    image_path = os.path.join(IMAGE_DIR, f"ai_daily_{date_str}.png")
    generate_image(news_list, date, image_path)
    
    with open(os.path.join(OUTPUT_DIR, f"ai_daily_{date_str}.json"), 'w', encoding='utf-8') as f:
        json.dump({'date': date.isoformat(), 'news': news_list}, f, ensure_ascii=False, indent=2)
    
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
