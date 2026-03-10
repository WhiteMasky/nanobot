#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表生成器 - 自动生成数据可视化图表
支持柱状图、折线图、饼图、散点图等
"""

import sys
import argparse
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    
    # 配置中文字体
    if sys.platform == 'win32':
        matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
        matplotlib.rcParams['axes.unicode_minus'] = False
    
    import numpy as np
except ImportError:
    print("❌ 缺少依赖：matplotlib, numpy")
    print("请运行：pip install matplotlib numpy")
    sys.exit(1)

# 图表样式
STYLES = ['default', 'seaborn-v0_8', 'classic', 'dark_background']

# 配色方案
COLOR_PALETTES = {
    'default': ['#2E86AB', '#A23B72', '#M18F76', '#F38181', '#EAA221'],
    'vibrant': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
    'pastel': ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF'],
    'professional': ['#1A1A2E', '#16213E', '#0F3460', '#E94560', '#533483'],
}

def parse_data(data_str):
    """解析数据字符串"""
    try:
        # 尝试 JSON 格式
        data = json.loads(data_str)
        return data
    except:
        # 简单格式：label1:value1,label2:value2
        data = {}
        for item in data_str.split(','):
            if ':' in item:
                label, value = item.split(':')
                data[label.strip()] = float(value.strip())
        return data

def create_bar_chart(data, title='柱状图', xlabel='', ylabel='', 
                     output_file='chart.png', style='default', palette='default'):
    """创建柱状图"""
    plt.style.use(style)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = list(data.keys())
    values = list(data.values())
    colors = COLOR_PALETTES.get(palette, COLOR_PALETTES['default'])
    
    bars = ax.bar(range(len(labels)), values, color=colors[:len(labels)])
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # 添加数值标签
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{value}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file

def create_line_chart(data, title='折线图', xlabel='', ylabel='',
                      output_file='chart.png', style='default'):
    """创建折线图"""
    plt.style.use(style)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = list(data.keys())
    values = list(data.values())
    
    ax.plot(range(len(labels)), values, marker='o', linewidth=2, markersize=8,
            color=COLOR_PALETTES['default'][0])
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.grid(True, alpha=0.3)
    
    # 添加数值标签
    for i, value in enumerate(values):
        ax.text(i, value + 0.1, f'{value}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file

def create_pie_chart(data, title='饼图', output_file='chart.png', 
                     style='default', palette='default'):
    """创建饼图"""
    plt.style.use(style)
    fig, ax = plt.subplots(figsize=(8, 8))
    
    labels = list(data.keys())
    values = list(data.values())
    colors = COLOR_PALETTES.get(palette, COLOR_PALETTES['default'])
    
    # 突出显示最大值
    explode = [0.05 if v == max(values) else 0 for v in values]
    
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                       colors=colors[:len(labels)],
                                       explode=explode, shadow=True)
    
    # 设置字体
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_file

def generate_chart(data, chart_type='bar', title='图表', xlabel='', ylabel='',
                   output_file='chart.png', style='default', palette='default'):
    """
    生成图表
    
    参数:
        data: 数据 (dict 或 JSON 字符串)
        chart_type: 图表类型 (bar, line, pie)
        title: 标题
        xlabel: X 轴标签
        ylabel: Y 轴标签
        output_file: 输出文件路径
        style: 样式
        palette: 配色方案
    
    返回:
        str: 输出文件路径
    """
    print(f'📊 开始生成图表...')
    print(f'类型：{chart_type}')
    print(f'标题：{title}')
    
    # 解析数据
    if isinstance(data, str):
        data = parse_data(data)
    
    if not data:
        print('❌ 没有数据')
        return None
    
    print(f'数据点：{len(data)}')
    
    # 生成图表
    if chart_type == 'bar':
        result = create_bar_chart(data, title, xlabel, ylabel, output_file, style, palette)
    elif chart_type == 'line':
        result = create_line_chart(data, title, xlabel, ylabel, output_file, style)
    elif chart_type == 'pie':
        result = create_pie_chart(data, title, output_file, style, palette)
    else:
        print(f'❌ 不支持的图表类型：{chart_type}')
        return None
    
    if result:
        print(f'\n✅ 图表生成成功！')
        print(f'已保存：{output_file}')
    
    return result

def main():
    parser = argparse.ArgumentParser(description='图表生成器')
    parser.add_argument('--data', type=str, required=True, 
                        help='数据 (JSON 或 label1:value1,label2:value2)')
    parser.add_argument('--type', type=str, default='bar',
                        choices=['bar', 'line', 'pie'],
                        help='图表类型')
    parser.add_argument('--title', type=str, default='图表', help='标题')
    parser.add_argument('--xlabel', type=str, default='', help='X 轴标签')
    parser.add_argument('--ylabel', type=str, default='', help='Y 轴标签')
    parser.add_argument('--output', type=str, default='chart.png', help='输出文件路径')
    parser.add_argument('--style', type=str, default='default',
                        choices=STYLES, help='样式')
    parser.add_argument('--palette', type=str, default='default',
                        choices=['default', 'vibrant', 'pastel', 'professional'],
                        help='配色方案')
    
    args = parser.parse_args()
    
    result = generate_chart(
        data=args.data,
        chart_type=args.type,
        title=args.title,
        xlabel=args.xlabel,
        ylabel=args.ylabel,
        output_file=args.output,
        style=args.style,
        palette=args.palette
    )
    
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
