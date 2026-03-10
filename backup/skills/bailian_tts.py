#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百炼平台语音合成 API 调用脚本
通用文字转语音功能
"""

import requests
import sys
import argparse
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# API Key
API_KEY = 'sk-24486854cd0447b3973602d22fe43004'

def generate_speech(text, model='cosyvoice-v1', voice='longxiaochun', 
                    format='wav', output_file='output_tts.wav'):
    """
    调用语音合成 API
    
    参数:
        text: 要合成的文字（必需）
        model: 模型名称
        voice: 音色
        format: 输出格式 (wav, mp3)
        output_file: 输出文件路径
    
    返回:
        str: 输出文件路径，失败返回 None
    """
    print(f'🔊 调用语音合成 API...')
    print(f'文字：{text}')
    print(f'模型：{model}')
    print(f'音色：{voice}')
    print(f'格式：{format}')
    
    # 使用 OpenAI 兼容接口
    url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/audio/speech'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'input': text,
        'voice': voice,
        'response_format': format
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f'\n✅ 合成成功！')
            print(f'已保存：{output_file}')
            return output_file
        else:
            print(f'\n❌ API 失败：{response.status_code}')
            print(f'响应：{response.text}')
            return None
            
    except Exception as e:
        print(f'❌ 错误：{e}')
        import traceback
        traceback.print_exc()
        return None

def list_voices():
    """列出可用音色"""
    print('\n📋 可用音色参考：')
    voices = {
        'cosyvoice-v1': [
            'longxiaochun (男声)',
            'longxiaoyan (女声)',
            'longxiaoguai (可爱)',
            'longxiaomei (甜美)',
            'longxiaoxiong (雄浑)'
        ]
    }
    for model, voice_list in voices.items():
        print(f'\n{model}:')
        for v in voice_list:
            print(f'  - {v}')

def main():
    parser = argparse.ArgumentParser(description='百炼平台语音合成')
    parser.add_argument('text', type=str, help='要合成的文字')
    parser.add_argument('--model', type=str, default='cosyvoice-v1', help='模型名称')
    parser.add_argument('--voice', type=str, default='longxiaochun', help='音色')
    parser.add_argument('--format', type=str, default='wav', choices=['wav', 'mp3'], help='输出格式')
    parser.add_argument('--output', type=str, default='output_tts.wav', help='输出文件路径')
    parser.add_argument('--list-voices', action='store_true', help='列出可用音色')
    
    args = parser.parse_args()
    
    if args.list_voices:
        list_voices()
        sys.exit(0)
    
    result = generate_speech(
        text=args.text,
        model=args.model,
        voice=args.voice,
        format=args.format,
        output_file=args.output
    )
    
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
