#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社交媒体文案生成器 - 自动生成各平台营销文案
支持小红书、微博、朋友圈、Twitter 等风格
"""

import sys
import argparse
import random
import json
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 各平台风格模板
PLATFORM_TEMPLATES = {
    'xiaohongshu': {
        'name': '小红书',
        'max_length': 1000,
        'emoji_style': 'heavy',
        'hashtags': True,
        'templates': [
            """
✨【{title}】✨

{opening}

🌟 {highlight1}
🌟 {highlight2}
🌟 {highlight3}

{details}

💡 {tips}

{hashtags}
            """,
            """
🔥 绝了！{title}

{opening}

✅ {point1}
✅ {point2}
✅ {point3}

{call_to_action}

{hashtags}
            """,
            """
姐妹们！{title} 真的太好用了！

{story}

👉 {feature1}
👉 {feature2}

{conclusion}

{hashtags}
            """
        ]
    },
    'weibo': {
        'name': '微博',
        'max_length': 140,
        'emoji_style': 'medium',
        'hashtags': True,
        'templates': [
            """#{hashtag1}# {content} {hashtags}"""
        ]
    },
    'wechat': {
        'name': '朋友圈',
        'max_length': 500,
        'emoji_style': 'light',
        'hashtags': False,
        'templates': [
            """
{title}

{content}

{emoji}
            """
        ]
    },
    'twitter': {
        'name': 'Twitter/X',
        'max_length': 280,
        'emoji_style': 'medium',
        'hashtags': True,
        'templates': [
            """{content} {hashtags}"""
        ]
    },
    'linkedin': {
        'name': 'LinkedIn',
        'max_length': 3000,
        'emoji_style': 'minimal',
        'hashtags': True,
        'templates': [
            """
{title}

{content}

{key_points}

{call_to_action}

{hashtags}
            """
        ]
    }
}

# Emoji 库
EMOJIS = {
    'heavy': ['✨', '🔥', '💖', '🌟', '⭐', '💫', '🎉', '🎊', '💝', '🌈', '🦋', '🌸', '🍀', '🎀', '💕'],
    'medium': ['👍', '❤️', '😊', '🎯', '💡', '📌', '✅', '🔔', '📢', '🎁'],
    'light': ['👌', '😊', '👍', '✨', '🎉'],
    'minimal': ['💼', '📊', '🎯', '✅', '🔗']
}

def generate_hashtags(keywords, platform='xiaohongshu'):
    """生成话题标签"""
    if not keywords:
        return ''
    
    keyword_list = keywords.split(',') if ',' in keywords else [keywords]
    
    if platform == 'xiaohongshu':
        tags = [f'#{kw.strip()}#' for kw in keyword_list[:5]]
        tags.extend(['#好物分享', '#种草', '#推荐'])
        return ' '.join(tags)
    elif platform == 'weibo':
        tags = [f'#{kw.strip()}#' for kw in keyword_list[:3]]
        return ' '.join(tags)
    elif platform == 'twitter':
        tags = [f'#{kw.strip()}' for kw in keyword_list[:3]]
        return ' '.join(tags)
    elif platform == 'linkedin':
        tags = [f'#{kw.strip()}' for kw in keyword_list[:3]]
        return '\n' + ' '.join(tags)
    else:
        return ''

def random_emoji(style='medium', count=1):
    """随机选择 emoji"""
    emoji_list = EMOJIS.get(style, EMOJIS['medium'])
    if count == 1:
        return random.choice(emoji_list)
    return ''.join(random.sample(emoji_list, min(count, len(emoji_list))))

def generate_copywriting(topic, platform='xiaohongshu', keywords='', 
                         tone='friendly', custom_content=''):
    """
    生成社交媒体文案
    
    参数:
        topic: 主题/产品
        platform: 平台类型
        keywords: 关键词（用于生成 hashtag）
        tone: 语气 (friendly, professional, enthusiastic)
        custom_content: 自定义内容要点
    
    返回:
        str: 生成的文案
    """
    print(f'📝 开始生成文案...')
    print(f'平台：{platform}')
    print(f'主题：{topic}')
    print(f'语气：{tone}')
    
    config = PLATFORM_TEMPLATES.get(platform, PLATFORM_TEMPLATES['xiaohongshu'])
    emoji_style = config['emoji_style']
    
    # 解析自定义内容
    content_points = []
    if custom_content:
        if Path(custom_content).exists():
            content_text = Path(custom_content).read_text(encoding='utf-8')
        else:
            content_text = custom_content
        
        content_points = [p.strip() for p in content_text.split('\n') if p.strip()]
    
    # 生成内容
    template = random.choice(config['templates'])
    
    # 填充模板变量
    replacements = {
        'title': f'{random_emoji(emoji_style)} {topic} {random_emoji(emoji_style)}',
        'topic': topic,
        'opening': content_points[0] if len(content_points) > 0 else f'今天给大家分享一下{topic}！',
        'highlight1': content_points[1] if len(content_points) > 1 else '亮点一',
        'highlight2': content_points[2] if len(content_points) > 2 else '亮点二',
        'highlight3': content_points[3] if len(content_points) > 3 else '亮点三',
        'point1': content_points[1] if len(content_points) > 1 else '优点一',
        'point2': content_points[2] if len(content_points) > 2 else '优点二',
        'point3': content_points[3] if len(content_points) > 3 else '优点三',
        'details': '\n'.join(content_points[4:]) if len(content_points) > 4 else '',
        'tips': '小贴士：赶紧收藏起来吧！',
        'story': f'最近发现了{topic}，真的被惊艳到了！',
        'feature1': content_points[1] if len(content_points) > 1 else '特色功能一',
        'feature2': content_points[2] if len(content_points) > 2 else '特色功能二',
        'conclusion': '真心推荐给大家！',
        'content': content_points[0] if content_points else f'关于{topic}的一些分享',
        'key_points': '\n'.join([f'• {p}' for p in content_points[:5]]) if content_points else '',
        'call_to_action': '欢迎评论区交流～',
        'hashtag1': keywords.split(',')[0].strip() if keywords else topic,
        'hashtags': generate_hashtags(keywords, platform),
        'emoji': random_emoji(emoji_style, 3)
    }
    
    # 替换模板
    copywriting = template
    for key, value in replacements.items():
        copywriting = copywriting.replace(f'{{{key}}}', str(value))
    
    # 清理空白行
    copywriting = '\n'.join([line for line in copywriting.split('\n') if line.strip()])
    copywriting = copywriting.strip()
    
    # 检查长度
    max_len = config['max_length']
    if len(copywriting) > max_len:
        print(f'⚠️ 文案超出限制 ({len(copywriting)}/{max_len})，已截断')
        copywriting = copywriting[:max_len-3] + '...'
    
    print(f'\n✅ 文案生成成功！')
    print(f'字数：{len(copywriting)}/{max_len}')
    
    return copywriting

def main():
    parser = argparse.ArgumentParser(description='社交媒体文案生成器')
    parser.add_argument('--topic', type=str, required=True, help='主题/产品')
    parser.add_argument('--platform', type=str, default='xiaohongshu',
                        choices=['xiaohongshu', 'weibo', 'wechat', 'twitter', 'linkedin'],
                        help='平台类型')
    parser.add_argument('--keywords', type=str, default='', help='关键词（用于 hashtag）')
    parser.add_argument('--tone', type=str, default='friendly',
                        choices=['friendly', 'professional', 'enthusiastic'],
                        help='语气')
    parser.add_argument('--content', type=str, default='', help='内容要点文件路径或文字')
    parser.add_argument('--output', type=str, default='', help='输出文件路径（可选）')
    
    args = parser.parse_args()
    
    result = generate_copywriting(
        topic=args.topic,
        platform=args.platform,
        keywords=args.keywords,
        tone=args.tone,
        custom_content=args.content
    )
    
    print('\n' + '='*50)
    print(result)
    print('='*50)
    
    if args.output:
        Path(args.output).write_text(result, encoding='utf-8')
        print(f'\n已保存到：{args.output}')
    
    sys.exit(0)

if __name__ == '__main__':
    main()
