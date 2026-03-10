# -*- coding: utf-8 -*-
"""
发送飞书消息
"""

import urllib.request
import urllib.error
import json
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

APP_ID = "cli_a924c3fc05f89cee"
APP_SECRET = "43MXrfLFa7sORlI3aMapEdG0aHVJqZ3E"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"

def get_tenant_access_token():
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result.get('tenant_access_token')

def send_doc_link(chat_id, doc_title, doc_url):
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        return False
    
    url = f"{FEISHU_API_BASE}/im/v1/messages"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    card_content = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "📱 小红书文案已生成"},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{doc_title}**\n\n📄 飞书文档已创建，点击查看详情👇"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "🔗 查看文档"},
                        "type": "primary",
                        "url": doc_url
                    }
                ]
            },
            {
                "tag": "hr"
            },
            {
                "tag": "note",
                "elements": [
                    {"tag": "plain_text", "content": "💡 每天自动更新，敬请期待～"}
                ]
            }
        ]
    }
    
    payload = {
        "receive_id": chat_id,
        "receive_id_type": "chat_id",
        "msg_type": "interactive",
        "content": json.dumps(card_content, ensure_ascii=False)
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
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

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法：python send_feishu_doc.py <群聊 ID> <文档标题> <文档链接>")
        sys.exit(1)
    
    chat_id = sys.argv[1]
    doc_title = sys.argv[2]
    doc_url = sys.argv[3]
    
    print(f"📤 发送文档链接到：{chat_id}")
    send_doc_link(chat_id, doc_title, doc_url)
