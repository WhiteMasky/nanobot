# -*- coding: utf-8 -*-
"""
PDF 处理技能
PDF Operations

功能：
1. PDF 转文本
2. PDF 转 Markdown
3. 提取 PDF 元数据
4. 合并 PDF
5. 拆分 PDF
"""

import sys
import os
import argparse
import json
from datetime import datetime

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============ 配置区域 ============

OUTPUT_DIR = r"C:\Users\zyc\.nanobot\workspace\output"

# ============ 工具函数 ============

def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def get_output_path(filename):
    """获取输出文件路径"""
    ensure_output_dir()
    return os.path.join(OUTPUT_DIR, filename)

# ============ PDF 处理函数 ============

def pdf_to_text(pdf_path):
    """PDF 转文本（使用 pypdf）"""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("❌ 需要安装 pypdf: pip install pypdf")
        return None
    
    print(f"📄 读取 PDF: {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        print(f"📊 共 {len(reader.pages)} 页")
        
        for i, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            text += f"\n--- 第 {i} 页 ---\n"
            text += page_text
        
        # 保存输出
        output_path = get_output_path(os.path.basename(pdf_path).replace('.pdf', '.txt'))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✅ 转换成功！")
        print(f"📁 已保存：{output_path}")
        return text
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return None

def pdf_to_markdown(pdf_path):
    """PDF 转 Markdown"""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("❌ 需要安装 pypdf: pip install pypdf")
        return None
    
    print(f"📄 读取 PDF: {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        markdown = f"# {os.path.basename(pdf_path)}\n\n"
        markdown += f"_转换时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n"
        markdown += f"**共 {len(reader.pages)} 页**\n\n---\n\n"
        
        for i, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            markdown += f"## 第 {i} 页\n\n"
            markdown += page_text
            markdown += "\n\n---\n\n"
        
        # 保存输出
        output_path = get_output_path(os.path.basename(pdf_path).replace('.pdf', '.md'))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        print(f"✅ 转换成功！")
        print(f"📁 已保存：{output_path}")
        return markdown
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def get_pdf_metadata(pdf_path):
    """获取 PDF 元数据"""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("❌ 需要安装 pypdf: pip install pypdf")
        return None
    
    print(f"📄 读取 PDF: {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        
        info = {
            "文件名": os.path.basename(pdf_path),
            "页数": len(reader.pages),
            "标题": metadata.get('/Title', 'N/A'),
            "作者": metadata.get('/Author', 'N/A'),
            "主题": metadata.get('/Subject', 'N/A'),
            "关键词": metadata.get('/Keywords', 'N/A'),
            "创建者": metadata.get('/Creator', 'N/A'),
            "生产者": metadata.get('/Producer', 'N/A'),
            "创建时间": str(metadata.get('/CreationDate', 'N/A')),
            "修改时间": str(metadata.get('/ModDate', 'N/A')),
        }
        
        print("\n" + "="*60)
        print("📋 PDF 元数据")
        print("="*60)
        for key, value in info.items():
            print(f"{key}: {value}")
        print("="*60)
        
        return info
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def merge_pdfs(pdf_list, output_name='merged.pdf'):
    """合并多个 PDF"""
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        print("❌ 需要安装 pypdf: pip install pypdf")
        return None
    
    print(f"📚 合并 {len(pdf_list)} 个 PDF")
    
    try:
        writer = PdfWriter()
        
        for pdf_path in pdf_list:
            if os.path.exists(pdf_path):
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)
                print(f"  ✅ 添加：{pdf_path}")
            else:
                print(f"  ⚠️  不存在：{pdf_path}")
        
        # 保存输出
        output_path = get_output_path(output_name)
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        print(f"\n✅ 合并成功！")
        print(f"📁 已保存：{output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def split_pdf(pdf_path, pages=None):
    """拆分 PDF"""
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError:
        print("❌ 需要安装 pypdf: pip install pypdf")
        return None
    
    print(f"📄 拆分 PDF: {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        base_name = os.path.basename(pdf_path).replace('.pdf', '')
        
        if pages:
            # 按指定页码拆分
            for i, page_range in enumerate(pages):
                writer = PdfWriter()
                start, end = page_range
                for j in range(start-1, min(end, len(reader.pages))):
                    writer.add_page(reader.pages[j])
                
                output_path = get_output_path(f"{base_name}_pages{start}-{end}.pdf")
                with open(output_path, 'wb') as f:
                    writer.write(f)
                print(f"  ✅ 保存：{output_path}")
        else:
            # 每页单独保存
            for i, page in enumerate(reader.pages, 1):
                writer = PdfWriter()
                writer.add_page(page)
                
                output_path = get_output_path(f"{base_name}_page{i}.pdf")
                with open(output_path, 'wb') as f:
                    writer.write(f)
                print(f"  ✅ 保存：{output_path}")
        
        print(f"\n✅ 拆分成功！")
        return True
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

def extract_images(pdf_path):
    """提取 PDF 中的图片"""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("❌ 需要安装 pypdf: pip install pypdf")
        return None
    
    print(f"🖼️  提取图片：{pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        base_name = os.path.basename(pdf_path).replace('.pdf', '')
        output_dir = get_output_path(f"{base_name}_images")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        count = 0
        for i, page in enumerate(reader.pages, 1):
            images = page.images
            for j, image in enumerate(images):
                image_path = os.path.join(output_dir, f"page{i}_image{j}.{image.name}")
                with open(image_path, 'wb') as f:
                    f.write(image.data)
                count += 1
                print(f"  ✅ 提取：{image.name}")
        
        print(f"\n✅ 共提取 {count} 张图片！")
        print(f"📁 保存目录：{output_dir}")
        return count
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description='PDF 处理技能')
    parser.add_argument('--to-text', type=str, help='PDF 转文本')
    parser.add_argument('--to-md', type=str, help='PDF 转 Markdown')
    parser.add_argument('--metadata', type=str, help='获取 PDF 元数据')
    parser.add_argument('--merge', type=str, nargs='+', help='合并 PDF (多个文件路径)')
    parser.add_argument('--output', type=str, default='merged.pdf', help='合并输出文件名')
    parser.add_argument('--split', type=str, help='拆分 PDF')
    parser.add_argument('--pages', type=str, help='拆分页码 (格式：1-5,6-10)')
    parser.add_argument('--images', type=str, help='提取 PDF 中的图片')
    
    args = parser.parse_args()
    
    if args.to_text:
        pdf_to_text(args.to_text)
        sys.exit(0)
    
    if args.to_md:
        pdf_to_markdown(args.to_md)
        sys.exit(0)
    
    if args.metadata:
        get_pdf_metadata(args.metadata)
        sys.exit(0)
    
    if args.merge:
        merge_pdfs(args.merge, args.output)
        sys.exit(0)
    
    if args.split:
        pages = None
        if args.pages:
            pages = []
            for p in args.pages.split(','):
                start, end = map(int, p.split('-'))
                pages.append((start, end))
        split_pdf(args.split, pages)
        sys.exit(0)
    
    if args.images:
        extract_images(args.images)
        sys.exit(0)
    
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    main()
