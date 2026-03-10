# -*- coding: utf-8 -*-
"""
调试飞书消息
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

def send_simple_text(chat_id, text):
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        return False
    
    # 使用旧版 API
    url = f"{FEISHU_API_BASE}/message/v4/send"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # content 应该是对象，不是字符串
    payload = {
        "chat_id": chat_id,
        "msg_type": "text",
        "content": {"text": text}
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
            return result.get('StatusCode') == 0 or result.get('code') == 0
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

if __name__ == '__main__':
    chat_id = "oc_4076208853ff65a3348480bf4227f668"
    doc_url = "https://bytedance.feishu.cn/docx/GdZQdfVqao6F9SxCveSc9sd0noc"
    
    text = f"""📱 小红书文案已生成！

🔥 美伊冲突 Day1 - 小红书文案

📄 飞书文档：{doc_url}

💡 每天自动更新，敬请期待～"""
    
    print(f"📤 发送文档链接到：{chat_id}")
    if send_simple_text(chat_id, text):
        print("✅ 发送成功！")
    else:
        print("❌ 发送失败")
