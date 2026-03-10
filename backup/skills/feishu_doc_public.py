# -*- coding: utf-8 -*-
"""
飞书文档分享设置 - 公开可编辑
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

def set_public_edit(token, doc_id):
    """设置文档为公开可编辑"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/public"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "permission": "edit"  # edit = 可编辑，read = 只读
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"响应：{json.dumps(result, indent=2, ensure_ascii=False)}")
            return result.get('code') == 0
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code}: {error_body}")
        return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

if __name__ == '__main__':
    doc_id = "GdZQdfVqao6F9SxCveSc9sd0noc"
    
    print(f"📤 设置文档公开可编辑：{doc_id}")
    
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        sys.exit(1)
    
    if set_public_edit(token, doc_id):
        print("✅ 设置成功！任何人都可以编辑")
        print(f"🔗 文档链接：https://bytedance.feishu.cn/docx/{doc_id}")
    else:
        print("❌ 设置失败")
