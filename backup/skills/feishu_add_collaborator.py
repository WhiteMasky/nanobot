# -*- coding: utf-8 -*-
"""
飞书文档 - 添加协作者
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

def add_collaborator(token, doc_id, user_id):
    """添加协作者到文档"""
    # 尝试不同的 API 端点
    endpoints = [
        f"/docx/v1/documents/{doc_id}/memberships",
        f"/docx/v1/documents/{doc_id}/members",
        f"/docx/v1/documents/{doc_id}/collaborators",
        f"/drive/v1/files/{doc_id}/permissions",
    ]
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 不同的 payload 格式
    payloads = [
        {"memberships": [{"member_id": user_id, "member_type": "user", "role": "editor"}]},
        {"members": [{"member_id": user_id, "member_type": "user", "permission": "edit"}]},
        {"collaborators": [{"user_id": user_id, "permission": "edit"}]},
        {"permissions": [{"user_id": user_id, "role": "writer"}]},
    ]
    
    for endpoint in endpoints:
        url = f"{FEISHU_API_BASE}{endpoint}"
        print(f"\n📍 尝试：{url}")
        
        for i, payload in enumerate(payloads, 1):
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    print(f"✅ 格式 {i} 成功：{json.dumps(result, indent=2, ensure_ascii=False)}")
                    return True
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                if e.code != 404:
                    print(f"⚠️ 格式 {i} - HTTP {e.code}: {error_body[:100]}")
    
    return False

if __name__ == '__main__':
    doc_id = "GdZQdfVqao6F9SxCveSc9sd0noc"
    user_id = "ou_3f3b67a4cc39eabc1b46c0d79c7f8871"
    
    print(f"📄 文档：{doc_id}")
    print(f"👤 用户：{user_id}")
    print(f"🎯 目标：添加编辑权限")
    
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        sys.exit(1)
    
    if add_collaborator(token, doc_id, user_id):
        print("\n✅ 权限授予成功！")
    else:
        print("\n❌ 所有尝试都失败了")
