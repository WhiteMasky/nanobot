# -*- coding: utf-8 -*-
"""
飞书文档权限管理
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

def grant_doc_permission(token, doc_id, user_id, permission="edit"):
    """给用户授予文档权限"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/members"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # permission: "edit" 编辑权限, "read" 只读权限
    payload = {
        "members": [
            {
                "member_id": user_id,
                "member_type": "user",
                "permission": permission
            }
        ]
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
    if len(sys.argv) < 3:
        print("用法：python feishu_doc_permission.py <文档 ID> <用户 ID> [权限]")
        print("权限：edit (编辑) / read (只读)")
        sys.exit(1)
    
    doc_id = sys.argv[1]
    user_id = sys.argv[2]
    permission = sys.argv[3] if len(sys.argv) > 3 else "edit"
    
    print(f"📤 授予权限：{doc_id} -> {user_id} ({permission})")
    
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        sys.exit(1)
    
    if grant_doc_permission(token, doc_id, user_id, permission):
        print("✅ 权限授予成功！")
    else:
        print("❌ 权限授予失败")
