#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查jsLib中VUEXSJS的定义"""
import json
import re

# 加载书源
with open('3a.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    if isinstance(data, list):
        data = data[0]

js_lib = data.get('jsLib', '')

# 搜索VUEXSJS的定义
print('=== 搜索VUEXSJS的定义 ===')

# 找到VUEXSJS =的位置
idx = js_lib.find('VUEXSJS =')
if idx >= 0:
    # 显示上下文
    start = max(0, idx - 500)
    end = min(len(js_lib), idx + 500)
    print(f'Context (position {idx}):')
    print(js_lib[start:end])
else:
    print('VUEXSJS = not found')
    
# 搜索this.VUEXSJS
idx2 = js_lib.find('.VUEXSJS =')
if idx2 >= 0:
    print(f'\n=== .VUEXSJS = found at position {idx2} ===')
    start = max(0, idx2 - 200)
    end = min(len(js_lib), idx2 + 200)
    print(js_lib[start:end])

# 检查jsLib的IIFE结构
print('\n=== 检查jsLib的IIFE结构 ===')
# 找到第一个IIFE
iife_start = js_lib.find('(function')
if iife_start >= 0:
    print(f'First IIFE starts at position {iife_start}')
    # 找到IIFE的结束
    brace_count = 0
    in_iife = False
    for i in range(iife_start, min(len(js_lib), iife_start + 10000)):
        if js_lib[i] == '(' and js_lib[i:i+8] == '(function':
            in_iife = True
        if in_iife:
            if js_lib[i] == '{':
                brace_count += 1
            elif js_lib[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    print(f'IIFE ends at position {i}')
                    print(f'IIFE content length: {i - iife_start + 1}')
                    break
