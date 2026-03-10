# -*- coding: utf-8 -*-
"""
Tavily 搜索工具
使用 Tavily API 进行网络搜索
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import urllib.error
import json
import os

# ============ 配置 ============
TAVILY_API_KEY = "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"
TAVILY_API_URL = "https://api.tavily.com/search"

def tavily_search(query, max_results=5):
    """
    使用 Tavily API 进行搜索
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量 (1-10)
    
    Returns:
        list: 搜索结果列表
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TAVILY_API_KEY}"
    }
    
    payload = {
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "include_raw_content": False,
        "max_results": max_results
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(TAVILY_API_URL, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('results', [])
    
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = json.loads(e.read().decode('utf-8'))
            print(f"Error details: {error_body}")
        except:
            pass
        return []
    
    except Exception as e:
        print(f"Search failed: {e}")
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tavily_search.py <search_query> [max_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"🔍 搜索：{query}")
    print(f"最多返回：{max_results} 条结果\n")
    
    results = tavily_search(query, max_results)
    
    if results:
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.get('title', '无标题')}")
            print(f"   URL: {r.get('url', '无链接')}")
            print(f"   摘要：{r.get('content', '无摘要')[:200]}...")
            print()
    else:
        print("❌ 未找到搜索结果")
