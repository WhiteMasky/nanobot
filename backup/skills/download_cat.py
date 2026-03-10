#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download cat image from URL
"""

import requests
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Read URL from file
with open('cat_image_url.txt', 'r', encoding='utf-8') as f:
    image_url = f.read().strip()

print(f'Downloading from: {image_url}')

# Download image
response = requests.get(image_url)
if response.status_code == 200:
    with open('cat_image.png', 'wb') as f:
        f.write(response.content)
    print('SUCCESS! Saved to cat_image.png')
else:
    print(f'Failed: {response.status_code}')
