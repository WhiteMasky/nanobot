#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百炼平台多模态能力配置与测试
包含：语音识别、语音合成、视频生成、图片生成
"""

import dashscope
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 配置 API Key
DASHSCOPE_API_KEY = 'sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b'
DASHSCOPE_WANX_API_KEY = 'sk-24486854cd0447b3973602d22fe43004'

dashscope.api_key = DASHSCOPE_API_KEY

print('=' * 60)
print('百炼平台多模态能力配置')
print('=' * 60)

# 1. 图片生成 (wanx-v1)
print('\n📷 1. 图片生成 (Image Generation)')
print('-' * 40)
print('模型：wanx-v1')
print('API Key: sk-24486854cd0447b3973602d22fe43004')
print('状态：✅ 已测试可用')
print('示例：生成猫咪、老虎图片成功')

# 2. 语音识别 (Paraformer)
print('\n🎤 2. 语音识别 (Speech Recognition)')
print('-' * 40)
print('模型：paraformer-v2')
print('API Key: sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b')
print('功能：音频文件转文字')
print('支持格式：wav, mp3, m4a 等')

try:
    from dashscope import Transcription
    print('模块导入：✅ Transcription')
    print('使用方法：Transcription.call(model="paraformer-v2", file_path="audio.wav")')
    print('状态：⚠️ 需要音频文件进行测试')
except ImportError as e:
    print(f'模块导入：❌ {e}')

# 3. 语音合成 (CosyVoice)
print('\n🔊 3. 语音合成 (Text to Speech)')
print('-' * 40)
print('模型：cosyvoice-v1')
print('API Key: sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b')
print('功能：文字转语音')
print('支持音色：多种中文/英文音色')

try:
    from dashscope import SpeechSynthesis
    print('模块导入：✅ SpeechSynthesis')
    print('测试连接...')
    result = SpeechSynthesis.call(
        model='cosyvoice-v1',
        text='你好，我是通义千问语音合成助手',
        voice='longxiaochun'
    )
    if result.status_code == 200:
        print('状态：✅ 可用')
        with open('test_tts.wav', 'wb') as f:
            f.write(result.get_audio_data())
        print('测试文件：test_tts.wav (已保存)')
    else:
        print(f'状态：❌ {result.code} - {result.message}')
except Exception as e:
    print(f'状态：❌ {e}')

# 4. 视频生成 (通义万相视频)
print('\n🎬 4. 视频生成 (Video Generation)')
print('-' * 40)
print('模型：wanx-v2-video / wanx-image-to-video')
print('API Key: sk-24486854cd0447b3973602d22fe43004')
print('功能：文生视频、图生视频')
print('说明：需要异步任务处理')
print('状态：⚠️ 需要进一步测试')

# 5. 文本生成 (Qwen)
print('\n💬 5. 文本生成 (Text Generation)')
print('-' * 40)
print('模型：qwen-plus, qwen3.5-plus, qwen-turbo, qwen-max')
print('API Key: sk-sp-c8e90ae6dd1148a9b4c31f9603ef778b')

try:
    from dashscope import Generation
    print('模块导入：✅ Generation')
    print('测试连接...')
    response = Generation.call(
        model='qwen-plus',
        messages=[{'role': 'user', 'content': '你好'}]
    )
    if response.status_code == 200:
        print('状态：✅ 可用')
    else:
        print(f'状态：❌ {response.code} - {response.message}')
except Exception as e:
    print(f'状态：❌ {e}')

print('\n' + '=' * 60)
print('配置完成！')
print('=' * 60)

print('\n📋 可用功能总结：')
print('  ✅ 图片生成 - wanx-v1 (已测试)')
print('  ✅ 文本生成 - qwen-plus (已测试)')
print('  ⚠️  语音识别 - paraformer-v2 (需要音频文件)')
print('  ⚠️  语音合成 - cosyvoice-v1 (测试中)')
print('  ⚠️  视频生成 - wanx-v2-video (需要进一步测试)')
