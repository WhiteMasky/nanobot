#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百炼平台语音识别 API 调用脚本
通用音频转文字功能，支持异步任务
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

def transcribe_audio(file_path, model='paraformer-v2', language='zh-CN', 
                     poll_interval=3, timeout=300):
    """
    调用语音识别 API（异步任务）
    
    参数:
        file_path: 音频文件路径（必需）
        model: 模型名称
        language: 语言代码 (zh-CN, en-US 等)
        poll_interval: 轮询间隔（秒）
        timeout: 超时时间（秒）
    
    返回:
        str: 识别结果文字，失败返回 None
    """
    print(f'🎤 调用语音识别 API...')
    print(f'文件：{file_path}')
    print(f'模型：{model}')
    print(f'语言：{language}')
    
    if not os.path.exists(file_path):
        print(f'❌ 文件不存在：{file_path}')
        return None
    
    # 上传文件并创建任务
    url = 'https://dashscope.aliyuncs.com/api/v1/services/audio/transcription/generation'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'X-DashScope-Async': 'enable'
    }
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'model': model,
                'language': language
            }
            
            print('正在上传文件...')
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
        
        if response.status_code != 200:
            print(f'❌ 上传失败：{response.status_code}')
            print(f'响应：{response.text}')
            return None
        
        # 获取任务 ID
        result = response.json()
        task_id = result.get('output', {}).get('task_id')
        
        if not task_id:
            print('❌ 未获取到任务 ID')
            return None
        
        print(f'任务 ID: {task_id}')
        print('等待识别完成...')
        
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
                transcript = task_result.get('output', {}).get('transcription', {}).get('transcription', '')
                print(f'\n✅ 识别成功！')
                print(f'文字：{transcript}')
                return transcript
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
    parser = argparse.ArgumentParser(description='百炼平台语音识别')
    parser.add_argument('file', type=str, help='音频文件路径')
    parser.add_argument('--model', type=str, default='paraformer-v2', help='模型名称')
    parser.add_argument('--language', type=str, default='zh-CN', 
                        choices=['zh-CN', 'en-US', 'ja-JP', 'ko-KR'],
                        help='语言代码')
    parser.add_argument('--poll-interval', type=int, default=3, help='轮询间隔（秒）')
    parser.add_argument('--timeout', type=int, default=300, help='超时时间（秒）')
    
    args = parser.parse_args()
    
    result = transcribe_audio(
        file_path=args.file,
        model=args.model,
        language=args.language,
        poll_interval=args.poll_interval,
        timeout=args.timeout
    )
    
    if result:
        print(f'\n📝 最终结果：{result}')
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
