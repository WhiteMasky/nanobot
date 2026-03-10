#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能组合工作流示例 - 自动化内容创作流水线
演示如何将多个技能组合使用
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

SKILLS_DIR = Path(__file__).parent

def run_skill(script, args, description=''):
    """运行技能脚本"""
    print(f'\n{"="*60}')
    print(f'🔧 {description}')
    print(f'命令：python {script} {" ".join(args)}')
    print(f'{"="*60}\n')
    
    cmd = [sys.executable, str(SKILLS_DIR / script)] + args
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0

def workflow_marketing_campaign(product_name, features, target_platform='xiaohongshu'):
    """
    营销活动工作流
    1. 生成文案
    2. 生成海报
    3. 生成数据图表（可选）
    """
    print(f'\n🚀 启动营销活动工作流')
    print(f'产品：{product_name}')
    print(f'平台：{target_platform}')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. 生成文案
    success = run_skill(
        'social_copywriting.py',
        ['--topic', product_name, '--platform', target_platform, 
         '--keywords', f'{product_name},营销，推荐', '--content', features],
        '📝 生成社交媒体文案'
    )
    
    if not success:
        print('❌ 文案生成失败')
        return False
    
    # 2. 生成海报
    success = run_skill(
        'poster_generator.py',
        ['--title', product_name, '--subtitle', '限时优惠',
         '--description', features, '--template', 'social',
         '--color', 'vibrant', '--output', f'campaign_{timestamp}.png'],
        '🎨 生成营销海报'
    )
    
    if not success:
        print('❌ 海报生成失败')
        return False
    
    print(f'\n✅ 营销活动工作流完成！')
    print(f'输出文件：campaign_{timestamp}.png')
    return True

def workflow_data_report(title, data, output_prefix='report'):
    """
    数据报告工作流
    1. 生成图表
    2. 生成 PPT
    """
    print(f'\n🚀 启动数据报告工作流')
    print(f'标题：{title}')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. 生成图表
    success = run_skill(
        'chart_generator.py',
        ['--data', data, '--type', 'bar', '--title', title,
         '--palette', 'professional', '--output', f'{output_prefix}_{timestamp}.png'],
        '📊 生成数据图表'
    )
    
    if not success:
        print('❌ 图表生成失败')
        return False
    
    # 2. 生成 PPT
    content = f"{title}\n\n数据概览\n\n{data.replace(',', '\n')}"
    success = run_skill(
        'ppt_generator.py',
        ['--title', title, '--subtitle', '数据报告',
         '--content', content, '--theme', 'dark',
         '--output', f'{output_prefix}_{timestamp}.pptx'],
        '📊 生成 PPT 报告'
    )
    
    if not success:
        print('❌ PPT 生成失败')
        return False
    
    print(f'\n✅ 数据报告工作流完成！')
    return True

def workflow_multimodal_content(topic, image_prompt=None):
    """
    多模态内容工作流
    1. 生成图片（可选）
    2. 生成文案
    3. 生成海报
    """
    print(f'\n🚀 启动多模态内容工作流')
    print(f'主题：{topic}')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 1. 生成图片（如果提供提示词）
    if image_prompt:
        success = run_skill(
            'bailian_image.py',
            [image_prompt, '--output', f'content_{timestamp}'],
            '📷 生成 AI 图片'
        )
        
        if not success:
            print('⚠️ 图片生成失败，继续其他步骤')
    
    # 2. 生成文案
    success = run_skill(
        'social_copywriting.py',
        ['--topic', topic, '--platform', 'xiaohongshu',
         '--keywords', f'{topic},AI 生成', '--output', f'content_{timestamp}.txt'],
        '📝 生成社交媒体文案'
    )
    
    if not success:
        print('❌ 文案生成失败')
        return False
    
    # 3. 生成海报
    success = run_skill(
        'poster_generator.py',
        ['--title', topic, '--template', 'social',
         '--color', 'vibrant', '--output', f'content_{timestamp}.png'],
        '🎨 生成内容海报'
    )
    
    if not success:
        print('❌ 海报生成失败')
        return False
    
    print(f'\n✅ 多模态内容工作流完成！')
    return True

def main():
    parser = argparse.ArgumentParser(description='技能组合工作流')
    parser.add_argument('workflow', type=str,
                        choices=['marketing', 'report', 'multimodal'],
                        help='工作流类型')
    parser.add_argument('--topic', type=str, required=True, help='主题/产品名称')
    parser.add_argument('--content', type=str, default='', help='内容/特性描述')
    parser.add_argument('--data', type=str, default='', help='数据（用于报告工作流）')
    parser.add_argument('--image-prompt', type=str, default='', help='图片提示词')
    parser.add_argument('--platform', type=str, default='xiaohongshu',
                        choices=['xiaohongshu', 'weibo', 'wechat', 'twitter'],
                        help='目标平台')
    parser.add_argument('--output', type=str, default='output', help='输出文件前缀')
    
    args = parser.parse_args()
    
    if args.workflow == 'marketing':
        success = workflow_marketing_campaign(
            product_name=args.topic,
            features=args.content or '优质产品，值得拥有',
            target_platform=args.platform
        )
    elif args.workflow == 'report':
        if not args.data:
            print('❌ 报告工作流需要提供 --data 参数')
            sys.exit(1)
        success = workflow_data_report(
            title=args.topic,
            data=args.data,
            output_prefix=args.output
        )
    elif args.workflow == 'multimodal':
        success = workflow_multimodal_content(
            topic=args.topic,
            image_prompt=args.image_prompt
        )
    else:
        print(f'❌ 未知工作流：{args.workflow}')
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
