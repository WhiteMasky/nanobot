# -*- coding: utf-8 -*-
"""
网页抓取技能
Web Scraper

功能：
1. 抓取网页内容
2. 提取标题和正文
3. 提取链接
4. 提取图片
5. 保存为 Markdown
"""

import urllib.request
import urllib.error
import re
import sys
import os
import json
import argparse
from html import unescape
from datetime import datetime

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output\web"

# 用户代理
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# ============ 工具函数 ============

def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def get_output_path(filename):
    """获取输出文件路径"""
    ensure_output_dir()
    return os.path.join(OUTPUT_DIR, filename)

def fetch_html(url):
    """抓取网页 HTML"""
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    print(f"🌐 抓取：{url}")
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            print(f"✅ 成功！大小：{len(html):,} 字节")
            return html
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP 错误：{e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"❌ 网络错误：{e.reason}")
        return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def extract_title(html):
    """提取网页标题"""
    match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if match:
        return unescape(match.group(1)).strip()
    return "无标题"

def extract_body_text(html):
    """提取正文文本"""
    # 移除 script 和 style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.IGNORECASE | re.DOTALL)
    
    # 移除注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 提取常见内容区域
    content_patterns = [
        r'<article[^>]*>(.*?)</article>',
        r'<main[^>]*>(.*?)</main>',
        r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>',
    ]
    
    content = ''
    for pattern in content_patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1)
            break
    
    if not content:
        # 如果没有找到特定区域，使用整个 body
        match = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1)
        else:
            content = html
    
    # 移除所有 HTML 标签
    text = re.sub(r'<[^>]+>', '', content)
    
    # 解码 HTML 实体
    text = unescape(text)
    
    # 清理空白
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def extract_links(html, base_url=None):
    """提取链接"""
    links = []
    pattern = r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
    
    for match in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
        href = match.group(1)
        text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        text = unescape(text)
        
        # 转换为绝对 URL
        if base_url and not href.startswith(('http://', 'https://', '#', 'mailto:', 'javascript:')):
            if href.startswith('/'):
                from urllib.parse import urlparse
                parsed = urlparse(base_url)
                href = f"{parsed.scheme}://{parsed.netloc}{href}"
            else:
                href = f"{base_url.rstrip('/')}/{href}"
        
        links.append({
            'url': href,
            'text': text[:100] if text else href
        })
    
    return links

def extract_images(html, base_url=None):
    """提取图片"""
    images = []
    pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>'
    
    for match in re.finditer(pattern, html, re.IGNORECASE):
        src = match.group(1)
        alt = ''
        
        # 提取 alt 属性
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', match.group(0))
        if alt_match:
            alt = alt_match.group(1)
        
        # 转换为绝对 URL
        if base_url and not src.startswith(('http://', 'https://', 'data:')):
            if src.startswith('/'):
                from urllib.parse import urlparse
                parsed = urlparse(base_url)
                src = f"{parsed.scheme}://{parsed.netloc}{src}"
            else:
                src = f"{base_url.rstrip('/')}/{src}"
        
        images.append({
            'url': src,
            'alt': alt
        })
    
    return images

def html_to_markdown(html, url=None):
    """将 HTML 转换为 Markdown"""
    title = extract_title(html)
    text = extract_body_text(html)
    
    md = f"# {title}\n\n"
    if url:
        md += f"_来源：{url}_\n\n"
    md += f"_抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n"
    md += "---\n\n"
    md += f"{text}\n"
    
    return md

def save_markdown(content, url):
    """保存为 Markdown 文件"""
    # 从 URL 生成文件名
    from urllib.parse import urlparse
    parsed = urlparse(url)
    filename = parsed.netloc.replace('.', '_') + '_' + parsed.path.replace('/', '_').strip('_')
    filename = filename[:50] + '.md' if len(filename) > 50 else filename
    
    output_path = get_output_path(filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='网页抓取技能')
    parser.add_argument('url', type=str, help='要抓取的 URL')
    parser.add_argument('--title', action='store_true', help='只提取标题')
    parser.add_argument('--text', action='store_true', help='只提取正文')
    parser.add_argument('--links', action='store_true', help='提取链接')
    parser.add_argument('--images', action='store_true', help='提取图片')
    parser.add_argument('--markdown', action='store_true', help='转换为 Markdown')
    parser.add_argument('--save', action='store_true', help='保存到文件')
    parser.add_argument('--limit', type=int, default=20, help='链接/图片数量限制')
    
    args = parser.parse_args()
    
    # 抓取 HTML
    html = fetch_html(args.url)
    if not html:
        sys.exit(1)
    
    # 提取标题
    if args.title:
        title = extract_title(html)
        print(f"\n📰 标题：{title}")
        sys.exit(0)
    
    # 提取正文
    if args.text:
        text = extract_body_text(html)
        print(f"\n📝 正文 ({len(text)} 字符):")
        print(text[:1000] + ('...' if len(text) > 1000 else ''))
        sys.exit(0)
    
    # 提取链接
    if args.links:
        links = extract_links(html, args.url)[:args.limit]
        print(f"\n🔗 链接 ({len(links)} 个):")
        for i, link in enumerate(links, 1):
            print(f"{i}. {link['text'][:50]}")
            print(f"   {link['url']}")
        sys.exit(0)
    
    # 提取图片
    if args.images:
        images = extract_images(html, args.url)[:args.limit]
        print(f"\n🖼️  图片 ({len(images)} 个):")
        for i, img in enumerate(images, 1):
            print(f"{i}. {img['alt'] or '无描述'}")
            print(f"   {img['url']}")
        sys.exit(0)
    
    # 转换为 Markdown
    if args.markdown or args.save:
        md = html_to_markdown(html, args.url)
        print(f"\n{md[:2000]}{'...' if len(md) > 2000 else ''}")
        
        if args.save:
            output_path = save_markdown(md, args.url)
            print(f"\n✅ 已保存：{output_path}")
        sys.exit(0)
    
    # 默认显示摘要
    title = extract_title(html)
    text = extract_body_text(html)
    links = extract_links(html, args.url)[:5]
    
    print("\n" + "="*60)
    print(f"📰 {title}")
    print("="*60)
    print(f"🔗 {args.url}")
    print(f"📝 正文：{len(text)} 字符")
    print(f"🔗 链接：{len(links)} 个")
    print()
    print(text[:500] + ('...' if len(text) > 500 else ''))
    print("="*60)
    
    sys.exit(0)

if __name__ == '__main__':
    main()
