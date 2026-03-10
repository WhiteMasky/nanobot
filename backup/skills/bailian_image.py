#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百炼平台图片生成 API 调用脚本
通用文生图功能，支持自定义提示词和参数
"""

import dashscope
from dashscope import ImageSynthesis
import requests
import sys
import argparse

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# API Key
dashscope.api_key = 'sk-24486854cd0447b3973602d22fe43004'

def generate_image(prompt, size='1024*1024', n=1, style=None, output_prefix='output'):
    """
    调用万相 API 生成图片
    
    参数:
        prompt: 文字描述（必需）
        size: 尺寸，可选 '1024*1024', '720*1280', '1280*720'
        n: 生成数量
        style: 风格，可选 'photography', 'art', 'anime' 等
        output_prefix: 输出文件前缀
    
    返回:
        list: 生成的图片文件路径列表
    """
    print(f'📷 调用图片生成 API...')
    print(f'提示词：{prompt}')
    print(f'尺寸：{size}')
    print(f'数量：{n}')
    
    try:
        # 构建参数
        params = {
            'model': 'wanx-v1',
            'prompt': prompt,
            'size': size,
            'n': n
        }
        
        if style:
            params['style'] = style
        
        # 调用 API
        rsp = ImageSynthesis.call(**params)
        
        if rsp.status_code == 200:
            results = rsp.output.get('results', [])
            if results:
                print(f'\n✅ API 调用成功！生成 {len(results)} 张图片')
                
                output_files = []
                for i, result in enumerate(results):
                    image_url = result.get('url', '')
                    if image_url:
                        print(f'\n图片 {i+1}: {image_url}')
                        
                        # 下载图片
                        output_file = f'{output_prefix}_{i+1}.png'
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            with open(output_file, 'wb') as f:
                                f.write(response.content)
                            print(f'已保存：{output_file}')
                            output_files.append(output_file)
                        else:
                            print(f'下载失败：{response.status_code}')
                
                return output_files
            else:
                print('❌ 没有返回结果')
                return []
        else:
            print(f'❌ API 失败：{rsp.code} - {rsp.message}')
            return None
            
    except Exception as e:
        print(f'❌ 错误：{e}')
        import traceback
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description='百炼平台图片生成')
    parser.add_argument('prompt', type=str, help='图片描述文字')
    parser.add_argument('--size', type=str, default='1024*1024', 
                        choices=['1024*1024', '720*1280', '1280*720'],
                        help='图片尺寸')
    parser.add_argument('--n', type=int, default=1, help='生成数量')
    parser.add_argument('--style', type=str, default=None, help='风格')
    parser.add_argument('--output', type=str, default='output', help='输出文件前缀')
    
    args = parser.parse_args()
    
    files = generate_image(
        prompt=args.prompt,
        size=args.size,
        n=args.n,
        style=args.style,
        output_prefix=args.output
    )
    
    if files:
        print(f'\n📁 生成完成：{files}')
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
