#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Call DashScope Wanx API to generate tiger image
"""

import dashscope
from dashscope import ImageSynthesis
import sys
import requests

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Set API key
dashscope.api_key = 'sk-24486854cd0447b3973602d22fe43004'

print('Calling Wanx API to generate tiger image...')

try:
    # Call Wanx text-to-image
    rsp = ImageSynthesis.call(
        model='wanx-v1',
        prompt='一只威风凛凛的老虎，丛林之王，金色毛发带黑色条纹，锐利的眼神，站在岩石上，阳光透过树林，霸气十足，高清摄影风格，4K，国家地理风格',
        size='1024*1024',
        n=1
    )
    
    print(f'Status: {rsp.status_code}')
    
    if rsp.status_code == 200:
        results = rsp.output.get('results', [])
        if results:
            image_url = results[0].get('url', '')
            print(f'\nSUCCESS!')
            print(f'Image URL: {image_url}')
            
            # Download image
            print('\nDownloading image...')
            response = requests.get(image_url)
            if response.status_code == 200:
                with open('tiger_image.png', 'wb') as f:
                    f.write(response.content)
                print('Saved to tiger_image.png')
            else:
                print(f'Download failed: {response.status_code}')
    else:
        print(f'Error: {rsp.code} - {rsp.message}')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
