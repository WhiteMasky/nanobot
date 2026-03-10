# -*- coding: utf-8 -*-
"""
飞书文档权限设置
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

def get_doc_info(token, doc_id):
    """获取文档信息"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}"
    headers = {'Authorization': f'Bearer {token}'}
    req = urllib.request.Request(url, headers=headers, method='GET')
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result.get('data', {})

def set_doc_share(token, doc_id, scope="public", permission="edit"):
    """设置文档分享权限"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/share"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 尝试不同的 payload 格式
    payloads = [
        # 格式 1
        {"scope": scope, "permission": permission},
        # 格式 2
        {"scope": scope, "scope_value": {"permission": permission}},
        # 格式 3
        {"share_setting": {"scope": scope, "permission": permission}},
    ]
    
    for i, payload in enumerate(payloads, 1):
        print(f"\n尝试格式 {i}: {payload}")
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"✅ 成功：{json.dumps(result, indent=2, ensure_ascii=False)}")
                return True
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP {e.code}: {error_body[:200]}")
    
    return False

if __name__ == '__main__':
    doc_id = "GdZQdfVqao6F9SxCveSc9sd0noc"
    
    print(f"📄 文档 ID: {doc_id}")
    
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        sys.exit(1)
    
    # 获取文档信息
    doc_info = get_doc_info(token, doc_id)
    print(f"\n📋 文档信息：{json.dumps(doc_info, indent=2, ensure_ascii=False)[:500]}")
    
    # 设置分享权限
    print("\n🔐 设置分享权限...")
    set_doc_share(token, doc_id, "public", "edit")
