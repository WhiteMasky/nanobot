#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海报生成器 - 自动生成营销海报、活动海报、宣传图
支持自定义模板、文字、图片、二维码
"""

import sys
import argparse
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import requests
    from io import BytesIO
except ImportError:
    print("❌ 缺少依赖：Pillow, requests")
    print("请运行：pip install Pillow requests")
    sys.exit(1)

# 海报模板尺寸
TEMPLATES = {
    'social': (1080, 1080),      # 社交媒体正方形
    'story': (1080, 1920),       # 故事/短视频
    'poster': (2480, 3508),      # A3 海报 (300dpi)
    'banner': (1920, 1080),      # 横幅
    'card': (800, 1200),         # 卡片
}

# 配色方案
COLOR_SCHEMES = {
    'vibrant': {
        'background': '#FF6B6B',
        'primary': '#4ECDC4',
        'secondary': '#FFE66D',
        'text': '#FFFFFF',
        'accent': '#FF8E72'
    },
    'professional': {
        'background': '#1A1A2E',
        'primary': '#16213E',
        'secondary': '#0F3460',
        'text': '#E94560',
        'accent': '#FFFFFF'
    },
    'minimal': {
        'background': '#FFFFFF',
        'primary': '#000000',
        'secondary': '#666666',
        'text': '#333333',
        'accent': '#FF6B6B'
    },
    'nature': {
        'background': '#2D5016',
        'primary': '#4A7C23',
        'secondary': '#8BC34A',
        'text': '#FFFFFF',
        'accent': '#FFC107'
    }
}

def get_font(size=40, bold=False):
    """获取字体"""
    # Windows 系统字体路径
    font_paths = [
        'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
        'C:/Windows/Fonts/simhei.ttf',    # 黑体
        'C:/Windows/Fonts/simkai.ttf',    # 楷体
        'C:/Windows/Fonts/arial.ttf',     # Arial
    ]
    
    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    # 回退到默认字体
    return ImageFont.load_default()

def create_gradient_background(width, height, color1, color2, direction='vertical'):
    """创建渐变背景"""
    base = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(base)
    
    if direction == 'vertical':
        for i in range(height):
            ratio = i / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line((0, i, width, i), fill=(r, g, b))
    else:
        for i in range(width):
            ratio = i / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line((i, 0, i, height), fill=(r, g, b))
    
    return base

def hex_to_rgb(hex_color):
    """十六进制颜色转 RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_poster(title, subtitle='', description='', template='social',
                    color_scheme='vibrant', image_path=None, output_file='poster.png'):
    """
    生成海报
    
    参数:
        title: 主标题
        subtitle: 副标题
        description: 描述文字
        template: 模板尺寸
        color_scheme: 配色方案
        image_path: 背景图片路径（可选）
        output_file: 输出文件路径
    
    返回:
        str: 输出文件路径
    """
    print(f'🎨 开始生成海报...')
    print(f'标题：{title}')
    print(f'模板：{template}')
    print(f'配色：{color_scheme}')
    
    # 获取尺寸和配色
    width, height = TEMPLATES.get(template, TEMPLATES['social'])
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES['vibrant'])
    
    # 创建背景
    if image_path and Path(image_path).exists():
        try:
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
            # 添加暗色遮罩让文字更清晰
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 128))
            bg_image = Image.alpha_composite(bg_image.convert('RGBA'), overlay)
            img = bg_image.convert('RGB')
        except Exception as e:
            print(f'⚠️ 图片加载失败，使用渐变背景：{e}')
            img = create_gradient_background(
                width, height,
                hex_to_rgb(colors['background']),
                hex_to_rgb(colors['primary'])
            )
    else:
        img = create_gradient_background(
            width, height,
            hex_to_rgb(colors['background']),
            hex_to_rgb(colors['primary'])
        )
    
    draw = ImageDraw.Draw(img)
    
    # 计算布局
    padding = width // 20
    text_y_start = height // 4
    
    # 主标题
    title_font_size = width // 12
    title_font = get_font(title_font_size, bold=True)
    
    # 文字换行
    max_chars_per_line = width // (title_font_size // 2)
    title_lines = []
    for line in title.split('\n'):
        if len(line) > max_chars_per_line:
            for i in range(0, len(line), max_chars_per_line):
                title_lines.append(line[i:i+max_chars_per_line])
        else:
            title_lines.append(line)
    
    # 绘制标题
    current_y = text_y_start
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, current_y), line, font=title_font, fill=colors['text'])
        current_y += title_font_size * 1.2
    
    # 副标题
    if subtitle:
        subtitle_font_size = width // 20
        subtitle_font = get_font(subtitle_font_size)
        current_y += subtitle_font_size // 2
        
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, current_y), subtitle, font=subtitle_font, fill=colors['secondary'])
        current_y += subtitle_font_size * 1.5
    
    # 描述文字
    if description:
        desc_font_size = width // 30
        desc_font = get_font(desc_font_size)
        current_y += desc_font_size
        
        # 添加分隔线
        line_y = current_y + desc_font_size
        draw.line(
            (padding, line_y, width - padding, line_y),
            fill=colors['accent'],
            width=3
        )
        current_y += desc_font_size * 2
        
        # 绘制描述
        desc_lines = []
        for line in description.split('\n'):
            if len(line) > max_chars_per_line:
                for i in range(0, len(line), max_chars_per_line):
                    desc_lines.append(line[i:i+max_chars_per_line])
            else:
                desc_lines.append(line)
        
        for line in desc_lines:
            bbox = draw.textbbox((0, 0), line, font=desc_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, current_y), line, font=desc_font, fill=colors['accent'])
            current_y += desc_font_size * 1.3
    
    # 保存
    img.save(output_file, 'PNG', quality=95)
    print(f'\n✅ 海报生成成功！')
    print(f'尺寸：{width}x{height}')
    print(f'已保存：{output_file}')
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='海报生成器')
    parser.add_argument('--title', type=str, required=True, help='主标题')
    parser.add_argument('--subtitle', type=str, default='', help='副标题')
    parser.add_argument('--description', type=str, default='', help='描述文字')
    parser.add_argument('--template', type=str, default='social',
                        choices=['social', 'story', 'poster', 'banner', 'card'],
                        help='模板尺寸')
    parser.add_argument('--color', type=str, default='vibrant',
                        choices=['vibrant', 'professional', 'minimal', 'nature'],
                        help='配色方案')
    parser.add_argument('--image', type=str, help='背景图片路径')
    parser.add_argument('--output', type=str, default='poster.png', help='输出文件路径')
    
    args = parser.parse_args()
    
    result = generate_poster(
        title=args.title,
        subtitle=args.subtitle,
        description=args.description,
        template=args.template,
        color_scheme=args.color,
        image_path=args.image,
        output_file=args.output
    )
    
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
