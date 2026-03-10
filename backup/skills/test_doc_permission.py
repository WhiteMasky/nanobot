# -*- coding: utf-8 -*-
"""
飞书文档权限管理 - 测试不同 API
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

def test_api(token, doc_id, user_id):
    """测试不同的 API 端点"""
    
    # 尝试 1: 协作 API
    url1 = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/collaborators"
    
    # 尝试 2: 分享 API
    url2 = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/share"
    
    # 尝试 3: 旧版 API
    url3 = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/permission"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    for i, url in enumerate([url1, url2, url3], 1):
        print(f"\n尝试 {i}: {url}")
        
        # 先 GET 看看文档信息
        req = urllib.request.Request(url, headers=headers, method='GET')
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"✅ GET 成功：{json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"❌ HTTP Error {e.code}: {error_body[:200]}")
        except Exception as e:
            print(f"❌ 错误：{e}")

if __name__ == '__main__':
    doc_id = "GdZQdfVqao6F9SxCveSc9sd0noc"
    user_id = "ou_3f3b67a4cc39eabc1b46c0d79c7f8871"
    
    print(f"测试文档权限 API：{doc_id}")
    
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        sys.exit(1)
    
    test_api(token, doc_id, user_id)
