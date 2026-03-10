#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Call DashScope Wanx API using official SDK
"""

import dashscope
from dashscope import ImageSynthesis
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Set API key
dashscope.api_key = 'sk-24486854cd0447b3973602d22fe43004'

print('Calling Wanx API with official SDK...')

try:
    # Call Wanx text-to-image
    rsp = ImageSynthesis.call(
        model='wanx-v1',
        prompt='一只可爱的橘色猫咪，毛茸茸的，大眼睛，坐在窗台上，阳光洒在身上，温馨治愈，高清摄影风格，4K',
        size='1024*1024',
        n=1
    )
    
    print(f'Status: {rsp.status_code}')
    print(f'Response: {rsp}')
    
    if rsp.status_code == 200:
        results = rsp.output.get('results', [])
        if results:
            image_url = results[0].get('url', '')
            print(f'\nSUCCESS!')
            print(f'Image URL: {image_url}')
            with open('cat_image_url.txt', 'w', encoding='utf-8') as f:
                f.write(image_url)
            print('URL saved to cat_image_url.txt')
    else:
        print(f'Error: {rsp.code} - {rsp.message}')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
