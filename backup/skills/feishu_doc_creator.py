# -*- coding: utf-8 -*-
"""
飞书云文档创建工具
创建小红书文案并分享到群聊
"""

import urllib.request
import urllib.error
import json
import sys
import base64

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置 ============
APP_ID = "cli_a924c3fc05f89cee"
APP_SECRET = "43MXrfLFa7sORlI3aMapEdG0aHVJqZ3E"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

# ============ 工具函数 ============

def get_tenant_access_token():
    """获取 tenant_access_token"""
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result.get('tenant_access_token')
            else:
                print(f"❌ 获取 token 失败：{result}")
                return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def create_doc(token, title, content):
    """创建飞书云文档"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "title": title,
        "document_type": 1  # 1 = 文档
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                doc_id = result.get('data', {}).get('document', {}).get('document_id')
                print(f"✅ 文档创建成功！ID: {doc_id}")
                return doc_id
            else:
                print(f"❌ 创建文档失败：{result}")
                return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def update_doc_content(token, doc_id, content):
    """更新文档内容"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 将内容转换为飞书文档格式
    blocks = []
    lines = content.split('\n')
    
    for line in lines:
        if line.strip():
            block = {
                "block_type": 1,  # 文本块
                "text": {
                    "elements": [
                        {
                            "text_run": {
                                "content": line + "\n"
                            }
                        }
                    ]
                }
            }
            blocks.append(block)
    
    payload = {
        "children": blocks
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                print(f"✅ 文档内容更新成功！")
                return True
            else:
                print(f"❌ 更新内容失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

def share_doc_to_chat(token, doc_id, chat_id):
    """分享文档到群聊"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/share"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "scope": "public",  # 公开可访问
        "scope_value": {
            "chat_id": chat_id
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                print(f"✅ 文档分享成功！")
                return True
            else:
                print(f"❌ 分享失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

def send_doc_link_to_chat(token, chat_id, doc_title, doc_url):
    """发送文档链接到群聊"""
    url = f"{FEISHU_API_BASE}/im/v1/messages"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 创建卡片消息
    card_content = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "📱 小红书文案已生成"
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{doc_title}**\n\n点击链接查看完整内容👇"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📄 查看文档"
                        },
                        "type": "primary",
                        "url": doc_url
                    }
                ]
            }
        ]
    }
    
    payload = {
        "receive_id": chat_id,
        "msg_type": "interactive",
        "content": json.dumps(card_content)
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                print(f"✅ 消息发送成功！")
                return True
            else:
                print(f"❌ 发送失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

# ============ 主函数 ============

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法：python feishu_doc_creator.py <标题> <内容文件> <群聊 ID>")
        sys.exit(1)
    
    title = sys.argv[1]
    content_file = sys.argv[2]
    chat_id = sys.argv[3]
    
    # 读取内容
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📤 创建飞书文档：{title}")
    print(f"📍 分享到群聊：{chat_id}")
    
    # 1. 获取 token
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取访问令牌")
        sys.exit(1)
    print(f"✅ 获取 token 成功")
    
    # 2. 创建文档
    doc_id = create_doc(token, title, content)
    if not doc_id:
        print("❌ 创建文档失败")
        sys.exit(1)
    
    # 3. 更新文档内容
    if not update_doc_content(token, doc_id, content):
        print("⚠️ 更新内容失败，但文档已创建")
    
    # 4. 分享文档
    share_doc_to_chat(token, doc_id, chat_id)
    
    # 5. 发送链接到群聊
    doc_url = f"https://bytedance.feishu.cn/docx/{doc_id}"
    send_doc_link_to_chat(token, chat_id, title, doc_url)
    
    print(f"\n🎉 完成！文档链接：{doc_url}")
