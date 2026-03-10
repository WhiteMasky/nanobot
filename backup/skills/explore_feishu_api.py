# -*- coding: utf-8 -*-
"""
飞书 API 探索 - 查找正确的文档权限 API
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

def explore_apis(token, doc_id):
    """探索可用的 API 端点"""
    
    endpoints = [
        # 云文档 API v1
        f"/docx/v1/documents/{doc_id}",
        f"/docx/v1/documents/{doc_id}/settings",
        
        # 云文档 API v2
        f"/docx/v2/documents/{doc_id}",
        
        # 知识库 API
        f"/wiki/v1/nodes/{doc_id}",
        
        # 云空间 API
        f"/drive/v1/files/{doc_id}",
        f"/drive/v1/files/{doc_id}/permissions",
        
        # 旧版 API
        f"/open-apis/docx/v1/documents/{doc_id}",
    ]
    
    headers = {'Authorization': f'Bearer {token}'}
    
    for endpoint in endpoints:
        url = f"{FEISHU_API_BASE}{endpoint}"
        req = urllib.request.Request(url, headers=headers, method='GET')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"\n✅ {endpoint}")
                print(f"   响应：{json.dumps(result, ensure_ascii=False)[:200]}")
        except urllib.error.HTTPError as e:
            # 只打印非 404 的错误
            if e.code != 404:
                print(f"\n⚠️ {endpoint} - HTTP {e.code}")
        except Exception as e:
            pass

if __name__ == '__main__':
    doc_id = "GdZQdfVqao6F9SxCveSc9sd0noc"
    
    print("🔍 探索飞书 API 端点...")
    
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        sys.exit(1)
    
    explore_apis(token, doc_id)
