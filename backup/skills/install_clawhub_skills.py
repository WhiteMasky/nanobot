# -*- coding: utf-8 -*-
"""
ClawHub 技能批量安装脚本
Batch Installer for ClawHub Skills

使用方法:
    python install_clawhub_skills.py [--category CATEGORY] [--force]

分类:
    - feishu: 飞书相关
    - aliyun: 阿里云相关
    - pdf: PDF 处理
    - search: 搜索相关
    - voice: 语音相关
    - image: 图像相关
    - all: 全部
"""

import subprocess
import sys
import time
import argparse

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 技能列表 ============

SKILLS = {
    'feishu': [
        'feishu-bridge',
        'feishu-messaging',
        'lark-integration',
        'feishu-card',
        'feishu-file-sender',
    ],
    'aliyun': [
        'bailian-web-search',
        'bailian-search',
        'bailian-knowledge-retrieve',
        'qwen-image',
        'qwen-audio',
        'aliyun-tts',
    ],
    'pdf': [
        'nano-pdf',
        'pdf-text-extractor',
        'pdf-ocr',
    ],
    'search': [
        'ddg-web-search',
        'brave-api-search',
    ],
    'voice': [
        'openai-tts',
        'mlx-stt',
        'local-stt',
    ],
    'image': [
        'ai-image-generation',
        'fal-text-to-image',
    ],
    'automation': [
        'n8n-workflow-automation',
        'agentic-workflow-automation',
    ],
    'notion': [
        'notion',
        'notion-skill',
        'notion-cli',
    ],
    'messaging': [
        'discord',
        'slack',
    ],
}

WORKDIR = r"C:\Users\zyc\.nanobot\workspace"
DELAY_SECONDS = 120  # ClawHub 速率限制延迟

# ============ 工具函数 ============

def install_skill(skill_name, force=True):
    """安装单个技能"""
    cmd = [
        'npx', '--yes', 'clawhub@latest', 'install',
        skill_name,
        '--workdir', WORKDIR
    ]
    
    if force:
        cmd.append('--force')
    
    print(f"\n{'='*60}")
    print(f"📦 安装：{skill_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"✅ {skill_name} 安装成功！")
            return True
        else:
            if "Rate limit exceeded" in result.stderr:
                print(f"⚠️  速率限制，等待 {DELAY_SECONDS} 秒...")
                time.sleep(DELAY_SECONDS)
                # 重试一次
                print(f"🔄 重试安装：{skill_name}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    print(f"✅ {skill_name} 安装成功！")
                    return True
                else:
                    print(f"❌ {skill_name} 安装失败：{result.stderr[:200]}")
                    return False
            else:
                print(f"❌ {skill_name} 安装失败：{result.stderr[:200]}")
                return False
    except subprocess.TimeoutExpired:
        print(f"❌ {skill_name} 安装超时")
        return False
    except Exception as e:
        print(f"❌ {skill_name} 安装错误：{e}")
        return False

def install_category(category):
    """安装指定分类的技能"""
    if category not in SKILLS:
        print(f"❌ 未知分类：{category}")
        print(f"可用分类：{', '.join(SKILLS.keys())}")
        return
    
    skills = SKILLS[category]
    print(f"\n🚀 开始安装 {category} 分类 ({len(skills)} 个技能)")
    
    success = 0
    failed = 0
    
    for skill in skills:
        if install_skill(skill):
            success += 1
        else:
            failed += 1
        
        # 每个技能之间延迟
        if skill != skills[-1]:
            print(f"\n⏳ 等待 {DELAY_SECONDS} 秒后继续...")
            time.sleep(DELAY_SECONDS)
    
    print(f"\n{'='*60}")
    print(f"✅ 完成！成功：{success} | 失败：{failed}")
    print(f"{'='*60}")

def install_all():
    """安装所有技能"""
    print("🚀 开始安装所有技能")
    print(f"⚠️  预计耗时：{len(sum(SKILLS.values(), [])) * DELAY_SECONDS / 60:.0f} 分钟")
    
    for category in SKILLS:
        print(f"\n{'='*60}")
        print(f"📂 分类：{category}")
        print(f"{'='*60}")
        install_category(category)

def list_skills():
    """列出所有可用技能"""
    print("\n" + "="*60)
    print("📋 ClawHub 技能列表")
    print("="*60)
    
    for category, skills in SKILLS.items():
        print(f"\n📂 {category} ({len(skills)} 个):")
        for skill in skills:
            print(f"   - {skill}")
    
    print("\n" + "="*60)

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='ClawHub 技能批量安装')
    parser.add_argument('--category', type=str, choices=list(SKILLS.keys()) + ['all'], help='安装分类')
    parser.add_argument('--list', action='store_true', help='列出所有技能')
    parser.add_argument('--no-delay', action='store_true', help='不等待 (可能触发速率限制)')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行 (不实际安装)')
    
    args = parser.parse_args()
    
    global DELAY_SECONDS
    if args.no_delay:
        DELAY_SECONDS = 0
    
    if args.list:
        list_skills()
        sys.exit(0)
    
    if args.dry_run:
        print("🔍 模拟运行模式")
        if args.category:
            if args.category == 'all':
                for cat, skills in SKILLS.items():
                    print(f"\n{cat}: {', '.join(skills)}")
            else:
                print(f"{args.category}: {', '.join(SKILLS[args.category])}")
        else:
            list_skills()
        sys.exit(0)
    
    if args.category:
        if args.category == 'all':
            install_all()
        else:
            install_category(args.category)
    else:
        parser.print_help()
        print("\n示例:")
        print("  python install_clawhub_skills.py --category feishu")
        print("  python install_clawhub_skills.py --category all")
        print("  python install_clawhub_skills.py --list")
        print("  python install_clawhub_skills.py --dry-run")
        sys.exit(1)

if __name__ == '__main__':
    main()
