# -*- coding: utf-8 -*-
"""
GitHub 技能
GitHub Operations

功能：
1. 搜索仓库
2. 获取 Trending 仓库
3. 获取用户信息
4. 获取 Issue/PR 状态
5. 创建 Issue
"""

import urllib.request
import urllib.error
import json
import sys
import argparse
import os
from datetime import datetime

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

# GitHub API Base
GITHUB_API_BASE = "https://api.github.com"

# GitHub Token (可选，用于提高速率限制)
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

# ============ 工具函数 ============

def _get_headers():
    """获取请求头"""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'nanobot-github-skill'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def _fetch(url):
    """发送 GET 请求"""
    req = urllib.request.Request(url, headers=_get_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP 错误：{e.code}")
        if e.code == 403:
            print("⚠️  可能触发了速率限制，请设置 GITHUB_TOKEN")
        return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

# ============ 功能函数 ============

def search_repositories(query, sort='stars', order='desc', per_page=10):
    """搜索仓库"""
    url = f"{GITHUB_API_BASE}/search/repositories?q={query}&sort={sort}&order={order}&per_page={per_page}"
    print(f"🔍 搜索：{query}")
    result = _fetch(url)
    if result:
        return result.get('items', [])
    return []

def get_trending(since='daily', language=None):
    """获取 Trending 仓库（通过搜索 API 模拟）"""
    # GitHub 没有官方的 trending API，用搜索 API 模拟
    query = "stars:>1000"
    if language:
        query += f" language:{language}"
    
    # 按最近创建时间排序来模拟 trending
    url = f"{GITHUB_API_BASE}/search/repositories?q={query}&sort=stars&order=desc&per_page=25"
    print(f"📈 获取 Trending (since={since}, language={language or 'all'})")
    result = _fetch(url)
    if result:
        return result.get('items', [])[:15]
    return []

def get_user_info(username):
    """获取用户信息"""
    url = f"{GITHUB_API_BASE}/users/{username}"
    print(f"👤 获取用户：{username}")
    return _fetch(url)

def get_user_repos(username, per_page=10):
    """获取用户仓库"""
    url = f"{GITHUB_API_BASE}/users/{username}/repos?sort=updated&per_page={per_page}"
    print(f"📦 获取 {username} 的仓库")
    result = _fetch(url)
    if result:
        return result
    return []

def get_repo_info(owner, repo):
    """获取仓库信息"""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    print(f"📦 获取仓库：{owner}/{repo}")
    return _fetch(url)

def get_repo_issues(owner, repo, state='open', per_page=10):
    """获取仓库 Issues"""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues?state={state}&per_page={per_page}"
    print(f"📋 获取 Issues: {owner}/{repo}")
    result = _fetch(url)
    if result:
        return result
    return []

def get_repo_prs(owner, repo, state='open', per_page=10):
    """获取仓库 Pull Requests"""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls?state={state}&per_page={per_page}"
    print(f"🔀 获取 PRs: {owner}/{repo}")
    result = _fetch(url)
    if result:
        return result
    return []

def create_issue(owner, repo, title, body, labels=None):
    """创建 Issue"""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    
    payload = {
        'title': title,
        'body': body
    }
    if labels:
        payload['labels'] = labels
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=_get_headers(), method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Issue 创建成功：{result.get('html_url')}")
            return result
    except Exception as e:
        print(f"❌ 创建失败：{e}")
        return None

def get_my_profile():
    """获取当前用户资料"""
    if not GITHUB_TOKEN:
        print("❌ 需要设置 GITHUB_TOKEN")
        return None
    url = f"{GITHUB_API_BASE}/user"
    return _fetch(url)

def get_my_repos(per_page=10):
    """获取当前用户的仓库"""
    if not GITHUB_TOKEN:
        print("❌ 需要设置 GITHUB_TOKEN")
        return []
    url = f"{GITHUB_API_BASE}/user/repos?per_page={per_page}"
    result = _fetch(url)
    if result:
        return result
    return []

# ============ 格式化输出 ============

def format_repo(repo, index=None):
    """格式化仓库信息"""
    prefix = f"{index}. " if index else ""
    stars = repo.get('stargazers_count', 0)
    forks = repo.get('forks_count', 0)
    language = repo.get('language', 'Unknown')
    desc = repo.get('description', '无描述') or '无描述'
    
    return f"""
{prefix}📦 {repo.get('full_name')}
   ⭐ {stars:,} | 🔀 {forks:,} | 💻 {language}
   📝 {desc[:80]}{'...' if len(desc) > 80 else ''}
   🔗 {repo.get('html_url')}"""

def format_user(user):
    """格式化用户信息"""
    if not user:
        return "用户不存在"
    
    return f"""
👤 {user.get('login')}
   📛 {user.get('name', 'N/A')}
   📍 {user.get('location', 'N/A')}
   🔗 {user.get('blog', 'N/A')}
   📊 仓库：{user.get('public_repos', 0)} | 粉丝：{user.get('followers', 0):,}
   🔗 {user.get('html_url')}"""

def format_issue(issue, index=None):
    """格式化 Issue 信息"""
    prefix = f"{index}. " if index else ""
    labels = ', '.join([l.get('name') for l in issue.get('labels', [])])
    
    return f"""
{prefix}#{issue.get('number')} {issue.get('title')}
   👤 {issue.get('user', {}).get('login')}
   🏷️  {labels or '无标签'}
   📅 创建：{issue.get('created_at', '')[:10]}
   🔗 {issue.get('html_url')}"""

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='GitHub 技能')
    parser.add_argument('--search', type=str, help='搜索仓库')
    parser.add_argument('--trending', action='store_true', help='获取 Trending 仓库')
    parser.add_argument('--language', type=str, help='按语言过滤 (用于 trending)')
    parser.add_argument('--user', type=str, help='获取用户信息')
    parser.add_argument('--user-repos', type=str, help='获取用户仓库')
    parser.add_argument('--repo', type=str, help='获取仓库信息 (格式：owner/repo)')
    parser.add_argument('--issues', type=str, help='获取仓库 Issues (格式：owner/repo)')
    parser.add_argument('--prs', type=str, help='获取仓库 PRs (格式：owner/repo)')
    parser.add_argument('--create-issue', type=str, help='创建 Issue (格式：owner/repo)')
    parser.add_argument('--title', type=str, help='Issue 标题')
    parser.add_argument('--body', type=str, help='Issue 内容')
    parser.add_argument('--labels', type=str, help='Issue 标签 (逗号分隔)')
    parser.add_argument('--my-profile', action='store_true', help='获取我的资料')
    parser.add_argument('--my-repos', action='store_true', help='获取我的仓库')
    parser.add_argument('--limit', type=int, default=10, help='结果数量限制')
    
    args = parser.parse_args()
    
    if args.search:
        repos = search_repositories(args.search, per_page=args.limit)
        if repos:
            print("\n" + "="*60)
            for i, repo in enumerate(repos, 1):
                print(format_repo(repo, i))
            print("="*60)
        sys.exit(0)
    
    if args.trending:
        repos = get_trending(language=args.language)
        if repos:
            print("\n" + "="*60)
            print(f"📈 GitHub Trending ({args.language or 'All'} Languages)")
            print("="*60)
            for i, repo in enumerate(repos, 1):
                print(format_repo(repo, i))
            print("="*60)
        sys.exit(0)
    
    if args.user:
        user = get_user_info(args.user)
        if user:
            print(format_user(user))
        sys.exit(0)
    
    if args.user_repos:
        repos = get_user_repos(args.user_repos, per_page=args.limit)
        if repos:
            print("\n" + "="*60)
            for i, repo in enumerate(repos, 1):
                print(format_repo(repo, i))
            print("="*60)
        sys.exit(0)
    
    if args.repo:
        parts = args.repo.split('/')
        if len(parts) != 2:
            print("❌ 格式错误，应为 owner/repo")
            sys.exit(1)
        repo = get_repo_info(parts[0], parts[1])
        if repo:
            print(format_repo(repo))
        sys.exit(0)
    
    if args.issues:
        parts = args.issues.split('/')
        if len(parts) != 2:
            print("❌ 格式错误，应为 owner/repo")
            sys.exit(1)
        issues = get_repo_issues(parts[0], parts[1], per_page=args.limit)
        if issues:
            print("\n" + "="*60)
            for i, issue in enumerate(issues, 1):
                print(format_issue(issue, i))
            print("="*60)
        sys.exit(0)
    
    if args.prs:
        parts = args.prs.split('/')
        if len(parts) != 2:
            print("❌ 格式错误，应为 owner/repo")
            sys.exit(1)
        prs = get_repo_prs(parts[0], parts[1], per_page=args.limit)
        if prs:
            print("\n" + "="*60)
            print("🔀 Pull Requests")
            print("="*60)
            for i, pr in enumerate(prs, 1):
                print(format_issue(pr, i))
            print("="*60)
        sys.exit(0)
    
    if args.create_issue:
        parts = args.create_issue.split('/')
        if len(parts) != 2:
            print("❌ 格式错误，应为 owner/repo")
            sys.exit(1)
        if not args.title:
            print("❌ 需要 --title 参数")
            sys.exit(1)
        labels = args.labels.split(',') if args.labels else None
        create_issue(parts[0], parts[1], args.title, args.body or '', labels)
        sys.exit(0)
    
    if args.my_profile:
        user = get_my_profile()
        if user:
            print(format_user(user))
        sys.exit(0)
    
    if args.my_repos:
        repos = get_my_repos(per_page=args.limit)
        if repos:
            print("\n" + "="*60)
            print("📦 我的仓库")
            print("="*60)
            for i, repo in enumerate(repos, 1):
                print(format_repo(repo, i))
            print("="*60)
        sys.exit(0)
    
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    main()
