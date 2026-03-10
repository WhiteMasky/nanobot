# -*- coding: utf-8 -*-
"""
飞书消息推送技能
Feishu Message Pusher

功能：
1. 发送文本消息
2. 发送卡片消息
3. 发送文件
4. @提及用户
"""

import urllib.request
import urllib.error
import json
import sys
import argparse

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

# 飞书 Bot Webhook URL (从飞书开放平台获取)
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK"

# 飞书 API Base
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

# API Token (从飞书开放平台获取)
FEISHU_API_TOKEN = "YOUR_API_TOKEN"

# ============ 消息发送函数 ============

def send_text_message(content, webhook=None):
    """发送文本消息"""
    if not webhook:
        webhook = FEISHU_WEBHOOK
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    
    return _send_webhook(webhook, payload)

def send_post_message(content_list, webhook=None):
    """发送富文本消息（支持格式）"""
    if not webhook:
        webhook = FEISHU_WEBHOOK
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "消息通知",
                    "content": content_list
                }
            }
        }
    }
    
    return _send_webhook(webhook, payload)

def send_interactive_card(card_content, webhook=None):
    """发送交互式卡片消息"""
    if not webhook:
        webhook = FEISHU_WEBHOOK
    
    payload = {
        "msg_type": "interactive",
        "card": card_content
    }
    
    return _send_webhook(webhook, payload)

def send_image_message(image_key, webhook=None):
    """发送图片消息（需要先上传图片）"""
    if not webhook:
        webhook = FEISHU_WEBHOOK
    
    payload = {
        "msg_type": "image",
        "content": {
            "image_key": image_key
        }
    }
    
    return _send_webhook(webhook, payload)

def upload_image(file_path):
    """上传图片获取 image_key"""
    url = f"{FEISHU_API_BASE}/open-apis/im/v1/images"
    
    # 读取图片
    with open(file_path, 'rb') as f:
        image_data = f.read()
    
    # 构建 multipart/form-data 请求
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="image"; filename="image.png"\r\n'
        f'Content-Type: image/png\r\n\r\n'
    ).encode('utf-8') + image_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
    
    headers = {
        'Authorization': f'Bearer {FEISHU_API_TOKEN}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result.get('data', {}).get('image_key')
            else:
                print(f"❌ 上传失败：{result.get('msg')}")
                return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def send_file_message(file_key, webhook=None):
    """发送文件消息（需要先上传文件）"""
    if not webhook:
        webhook = FEISHU_WEBHOOK
    
    payload = {
        "msg_type": "file",
        "content": {
            "file_key": file_key
        }
    }
    
    return _send_webhook(webhook, payload)

def upload_file(file_path, file_name=None):
    """上传文件获取 file_key"""
    import os
    if not file_name:
        file_name = os.path.basename(file_path)
    
    url = f"{FEISHU_API_BASE}/open-apis/im/v1/files"
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
        f'Content-Type: application/octet-stream\r\n\r\n'
    ).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
    
    headers = {
        'Authorization': f'Bearer {FEISHU_API_TOKEN}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result.get('data', {}).get('file_key')
            else:
                print(f"❌ 上传失败：{result.get('msg')}")
                return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def _send_webhook(webhook, payload):
    """发送 webhook 请求"""
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(webhook, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('StatusCode') == 0 or result.get('code') == 0:
                print("✅ 发送成功！")
                return True
            else:
                print(f"❌ 发送失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

def create_text_card(title, content, footer=None):
    """创建文本卡片"""
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            }
        ]
    }
    
    if footer:
        card["elements"].append({
            "tag": "hr",
            "element_type": "hr"
        })
        card["elements"].append({
            "tag": "note",
            "elements": [
                {
                    "tag": "plain_text",
                    "content": footer
                }
            ]
        })
    
    return card

def create_button_card(title, content, buttons):
    """创建带按钮的卡片"""
    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": content
            }
        },
        {
            "tag": "action",
            "actions": []
        }
    ]
    
    for btn in buttons:
        elements[1]["actions"].append({
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": btn["text"]
            },
            "type": btn.get("type", "primary"),
            "url": btn.get("url"),
            "value": btn.get("value")
        })
    
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title
            },
            "template": "blue"
        },
        "elements": elements
    }
    
    return card

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='飞书消息推送')
    parser.add_argument('--text', type=str, help='发送文本消息')
    parser.add_argument('--card', type=str, help='发送卡片消息 (JSON 文件路径)')
    parser.add_argument('--image', type=str, help='发送图片 (文件路径)')
    parser.add_argument('--file', type=str, help='发送文件 (文件路径)')
    parser.add_argument('--webhook', type=str, help='Webhook URL')
    parser.add_argument('--title', type=str, default='消息通知', help='卡片标题')
    parser.add_argument('--content', type=str, help='卡片内容')
    parser.add_argument('--test', action='store_true', help='发送测试消息')
    
    args = parser.parse_args()
    
    webhook = args.webhook or FEISHU_WEBHOOK
    
    if args.test:
        print("📤 发送测试消息...")
        send_text_message("这是一条测试消息", webhook)
        sys.exit(0)
    
    if args.text:
        print("📤 发送文本消息...")
        send_text_message(args.text, webhook)
        sys.exit(0)
    
    if args.card:
        print("📤 发送卡片消息...")
        with open(args.card, 'r', encoding='utf-8') as f:
            card = json.load(f)
        send_interactive_card(card, webhook)
        sys.exit(0)
    
    if args.title and args.content:
        print("📤 发送文本卡片...")
        card = create_text_card(args.title, args.content)
        send_interactive_card(card, webhook)
        sys.exit(0)
    
    if args.image:
        print("📤 上传图片并发送...")
        image_key = upload_image(args.image)
        if image_key:
            send_image_message(image_key, webhook)
        sys.exit(0)
    
    if args.file:
        print("📤 上传文件并发送...")
        file_key = upload_file(args.file)
        if file_key:
            send_file_message(file_key, webhook)
        sys.exit(0)
    
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    main()
