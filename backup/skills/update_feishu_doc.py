# -*- coding: utf-8 -*-
"""
飞书文档内容更新
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

def update_doc_content(token, doc_id, content):
    """更新文档内容 - 分批添加"""
    url = f"{FEISHU_API_BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 将内容转换为飞书文档块
    blocks = []
    lines = content.split('\n')
    
    for line in lines:
        if line.strip():
            # 判断是否是标题
            if line.startswith('#'):
                block_type = 2  # 标题
                text = line.lstrip('#').strip()
            else:
                block_type = 1  # 普通文本
                text = line
            
            block = {
                "block_type": block_type,
                "text": {
                    "elements": [
                        {
                            "text_run": {
                                "content": text + "\n"
                            }
                        }
                    ]
                }
            }
            blocks.append(block)
    
    # 分批添加，每批最多 50 个块
    batch_size = 50
    total_batches = (len(blocks) + batch_size - 1) // batch_size
    
    print(f"📊 总共 {len(blocks)} 个块，分 {total_batches} 批添加")
    
    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i+batch_size]
        batch_num = i // batch_size + 1
        print(f"  📝 添加第 {batch_num}/{total_batches} 批...")
        
        payload = {"children": batch}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('code') != 0:
                    print(f"  ⚠️ 第 {batch_num} 批失败：{result}")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"  ❌ 第 {batch_num} 批 HTTP {e.code}: {error_body[:200]}")
    
    return True

if __name__ == '__main__':
    doc_id = "GdZQdfVqao6F9SxCveSc9sd0noc"
    content_file = "output/xiaohongshu/meiyi_day1_content.txt"
    
    print(f"📝 更新文档：{doc_id}")
    
    # 读取内容
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取 token")
        sys.exit(1)
    
    if update_doc_content(token, doc_id, content):
        print("✅ 内容更新成功！")
    else:
        print("❌ 内容更新失败")
