#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百炼平台视频生成 API 调用脚本
通用文生图/图生视频功能，支持异步任务
"""

import requests
import sys
import argparse
import time
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# API Key
API_KEY = 'sk-24486854cd0447b3973602d22fe43004'

def generate_video(prompt=None, image_path=None, model='wanx-v2-video',
                   duration=5, poll_interval=5, timeout=600, output_file='output_video.mp4'):
    """
    调用视频生成 API（异步任务）
    
    参数:
        prompt: 文字描述（文生视频时必需）
        image_path: 参考图片路径（图生视频时可选）
        model: 模型名称
        duration: 视频时长（秒）
        poll_interval: 轮询间隔（秒）
        timeout: 超时时间（秒）
        output_file: 输出文件路径
    
    返回:
        str: 输出文件路径，失败返回 None
    """
    print(f'🎬 调用视频生成 API...')
    print(f'模型：{model}')
    print(f'时长：{duration}秒')
    
    if prompt:
        print(f'提示词：{prompt}')
    if image_path:
        print(f'参考图：{image_path}')
        if not os.path.exists(image_path):
            print(f'❌ 图片文件不存在：{image_path}')
            return None
    
    if not prompt and not image_path:
        print('❌ 需要提供提示词或参考图片')
        return None
    
    # 创建任务
    url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/generation'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'X-DashScope-Async': 'enable'
    }
    
    input_data = {}
    if prompt:
        input_data['prompt'] = prompt
    if image_path:
        # 需要先上传图片获取 URL，这里简化处理
        input_data['image'] = image_path
    
    payload = {
        'model': model,
        'input': input_data,
        'parameters': {
            'duration': duration
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            print(f'❌ 创建任务失败：{response.status_code}')
            print(f'响应：{response.text}')
            return None
        
        # 获取任务 ID
        result = response.json()
        task_id = result.get('output', {}).get('task_id')
        
        if not task_id:
            print('❌ 未获取到任务 ID')
            return None
        
        print(f'任务 ID: {task_id}')
        print('等待视频生成完成...')
        
        # 轮询任务状态
        task_url = f'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}'
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            time.sleep(poll_interval)
            
            task_response = requests.get(task_url, headers=headers, timeout=30)
            task_result = task_response.json()
            status = task_result.get('output', {}).get('task_status', 'unknown')
            
            print(f'状态：{status}')
            
            if status == 'SUCCEEDED':
                video_url = task_result.get('output', {}).get('results', [{}])[0].get('url', '')
                
                if video_url:
                    print(f'\n✅ 视频生成成功！')
                    print(f'URL: {video_url}')
                    
                    # 下载视频
                    print('\n正在下载视频...')
                    video_response = requests.get(video_url, timeout=120)
                    if video_response.status_code == 200:
                        with open(output_file, 'wb') as f:
                            f.write(video_response.content)
                        print(f'已保存：{output_file}')
                        return output_file
                    else:
                        print(f'下载失败：{video_response.status_code}')
                        return None
                else:
                    print('❌ 未获取到视频 URL')
                    return None
                    
            elif status == 'FAILED':
                print(f'\n❌ 任务失败')
                print(f'错误：{task_result.get("output", {}).get("message", "Unknown")}')
                return None
            elif status in ['PENDING', 'RUNNING']:
                continue
            else:
                print(f'未知状态：{status}')
        
        print(f'\n⏱️ 查询超时 ({timeout}秒)')
        return None
        
    except Exception as e:
        print(f'❌ 错误：{e}')
        import traceback
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description='百炼平台视频生成')
    parser.add_argument('--prompt', type=str, help='视频描述文字（文生视频）')
    parser.add_argument('--image', type=str, help='参考图片路径（图生视频）')
    parser.add_argument('--model', type=str, default='wanx-v2-video', help='模型名称')
    parser.add_argument('--duration', type=int, default=5, help='视频时长（秒）')
    parser.add_argument('--poll-interval', type=int, default=5, help='轮询间隔（秒）')
    parser.add_argument('--timeout', type=int, default=600, help='超时时间（秒）')
    parser.add_argument('--output', type=str, default='output_video.mp4', help='输出文件路径')
    
    args = parser.parse_args()
    
    if not args.prompt and not args.image:
        parser.error('需要提供 --prompt 或 --image')
    
    result = generate_video(
        prompt=args.prompt,
        image_path=args.image,
        model=args.model,
        duration=args.duration,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
        output_file=args.output
    )
    
    if result:
        print(f'\n📁 视频已保存：{result}')
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
