# -*- coding: utf-8 -*-
"""
待办事项管理技能
Todo List Manager

功能：
1. 添加待办
2. 完成待办
3. 删除待办
4. 列出待办
5. 按优先级排序
"""

import json
import os
import sys
import argparse
from datetime import datetime

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

TODO_FILE = r"C:\Users\zyc\.nanobot\workspace\todo_list.json"

# ============ 工具函数 ============

def load_todos():
    """加载待办列表"""
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"todos": [], "next_id": 1}

def save_todos(data):
    """保存待办列表"""
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_priority_icon(priority):
    """获取优先级图标"""
    icons = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🟢'
    }
    return icons.get(priority, '⚪')

def format_todo(todo):
    """格式化待办事项"""
    priority_icon = get_priority_icon(todo.get('priority', 'medium'))
    status_icon = '✅' if todo.get('completed') else '⬜'
    due_date = todo.get('due_date', '')
    due_str = f" | 📅 {due_date}" if due_date else ""
    tags_str = f" | 🏷️  {', '.join(todo.get('tags', []))}" if todo.get('tags') else ""
    
    return f"{status_icon} {priority_icon} #{todo['id']} {todo['title']}{due_str}{tags_str}"

# ============ 功能函数 ============

def add_todo(title, priority='medium', due_date=None, tags=None):
    """添加待办事项"""
    data = load_todos()
    
    todo = {
        'id': data['next_id'],
        'title': title,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'due_date': due_date,
        'tags': tags or []
    }
    
    data['todos'].append(todo)
    data['next_id'] += 1
    save_todos(data)
    
    print(f"✅ 已添加：{format_todo(todo)}")
    return todo

def complete_todo(todo_id):
    """完成待办事项"""
    data = load_todos()
    
    for todo in data['todos']:
        if todo['id'] == todo_id:
            todo['completed'] = True
            todo['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            save_todos(data)
            print(f"✅ 已完成：{format_todo(todo)}")
            return todo
    
    print(f"❌ 未找到 ID 为 {todo_id} 的待办")
    return None

def delete_todo(todo_id):
    """删除待办事项"""
    data = load_todos()
    
    for i, todo in enumerate(data['todos']):
        if todo['id'] == todo_id:
            deleted = data['todos'].pop(i)
            save_todos(data)
            print(f"🗑️  已删除：{format_todo(deleted)}")
            return deleted
    
    print(f"❌ 未找到 ID 为 {todo_id} 的待办")
    return None

def list_todos(status='all', priority=None, tag=None):
    """列出待办事项"""
    data = load_todos()
    todos = data['todos']
    
    # 过滤
    if status == 'active':
        todos = [t for t in todos if not t.get('completed')]
    elif status == 'completed':
        todos = [t for t in todos if t.get('completed')]
    
    if priority:
        todos = [t for t in todos if t.get('priority') == priority]
    
    if tag:
        todos = [t for t in todos if tag in t.get('tags', [])]
    
    # 排序（按优先级和创建时间）
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    todos.sort(key=lambda x: (priority_order.get(x.get('priority'), 1), x.get('created_at', '')))
    
    # 输出
    print("\n" + "="*60)
    print(f"📋 待办列表 ({len(todos)} 项)")
    print("="*60)
    
    if not todos:
        print("暂无待办事项 🎉")
    else:
        for todo in todos:
            print(format_todo(todo))
    
    print("="*60)
    
    # 统计
    total = len(data['todos'])
    completed = len([t for t in data['todos'] if t.get('completed')])
    active = total - completed
    
    print(f"📊 统计：总计 {total} | 已完成 {completed} | 进行中 {active}")
    print(f"📈 完成率：{completed/total*100:.1f}%" if total > 0 else "")
    print("="*60)
    
    return todos

def clear_completed():
    """清除已完成的待办"""
    data = load_todos()
    
    completed_count = len([t for t in data['todos'] if t.get('completed')])
    data['todos'] = [t for t in data['todos'] if not t.get('completed')]
    save_todos(data)
    
    print(f"🗑️  已清除 {completed_count} 个已完成的待办")
    return completed_count

def search_todos(keyword):
    """搜索待办事项"""
    data = load_todos()
    
    results = [t for t in data['todos'] if keyword.lower() in t['title'].lower()]
    
    print("\n" + "="*60)
    print(f"🔍 搜索结果：'{keyword}' ({len(results)} 项)")
    print("="*60)
    
    for todo in results:
        print(format_todo(todo))
    
    print("="*60)
    
    return results

def get_stats():
    """获取统计信息"""
    data = load_todos()
    todos = data['todos']
    
    total = len(todos)
    completed = len([t for t in todos if t.get('completed')])
    active = total - completed
    
    by_priority = {
        'high': len([t for t in todos if t.get('priority') == 'high' and not t.get('completed')]),
        'medium': len([t for t in todos if t.get('priority') == 'medium' and not t.get('completed')]),
        'low': len([t for t in todos if t.get('priority') == 'low' and not t.get('completed')])
    }
    
    print("\n" + "="*60)
    print("📊 待办统计")
    print("="*60)
    print(f"总计：{total}")
    print(f"已完成：{completed} ✅")
    print(f"进行中：{active} 🔄")
    print(f"完成率：{completed/total*100:.1f}%" if total > 0 else "N/A")
    print()
    print("按优先级（进行中）:")
    print(f"  🔴 高优先级：{by_priority['high']}")
    print(f"  🟡 中优先级：{by_priority['medium']}")
    print(f"  🟢 低优先级：{by_priority['low']}")
    print("="*60)
    
    return {
        'total': total,
        'completed': completed,
        'active': active,
        'by_priority': by_priority
    }

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='待办事项管理')
    
    # 添加
    parser.add_argument('--add', type=str, help='添加待办事项')
    parser.add_argument('--priority', type=str, choices=['high', 'medium', 'low'], default='medium', help='优先级')
    parser.add_argument('--due', type=str, help='截止日期 (YYYY-MM-DD)')
    parser.add_argument('--tags', type=str, help='标签 (逗号分隔)')
    
    # 操作
    parser.add_argument('--complete', type=int, help='完成待办 (ID)')
    parser.add_argument('--delete', type=int, help='删除待办 (ID)')
    parser.add_argument('--clear', action='store_true', help='清除已完成的')
    
    # 查询
    parser.add_argument('--list', action='store_true', help='列出待办')
    parser.add_argument('--status', type=str, choices=['all', 'active', 'completed'], default='all', help='状态过滤')
    parser.add_argument('--search', type=str, help='搜索待办')
    parser.add_argument('--stats', action='store_true', help='统计信息')
    
    args = parser.parse_args()
    
    if args.add:
        tags = args.tags.split(',') if args.tags else None
        add_todo(args.add, args.priority, args.due, tags)
        sys.exit(0)
    
    if args.complete is not None:
        complete_todo(args.complete)
        sys.exit(0)
    
    if args.delete is not None:
        delete_todo(args.delete)
        sys.exit(0)
    
    if args.clear:
        clear_completed()
        sys.exit(0)
    
    if args.list:
        list_todos(args.status)
        sys.exit(0)
    
    if args.search:
        search_todos(args.search)
        sys.exit(0)
    
    if args.stats:
        get_stats()
        sys.exit(0)
    
    # 默认显示列表
    list_todos('active')
    sys.exit(0)

if __name__ == '__main__':
    main()
