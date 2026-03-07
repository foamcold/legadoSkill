#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查_0x3ed9ab函数的完整实现"""
import json
import re

# 加载书源
with open('3a.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    if isinstance(data, list):
        data = data[0]

js_lib = data.get('jsLib', '')

# 提取_0x3ed9ab函数定义 - 找到完整的函数
idx = js_lib.find('function _0x3ed9ab')
if idx >= 0:
    # 找到函数结束位置
    brace_count = 0
    start = idx
    in_function = False
    for i in range(idx, min(len(js_lib), idx + 8000)):
        if js_lib[i] == '{':
            brace_count += 1
            in_function = True
        elif js_lib[i] == '}':
            brace_count -= 1
            if in_function and brace_count == 0:
                func_def = js_lib[start:i+1]
                print(f'=== _0x3ed9ab函数完整定义 ===')
                print(func_def)
                break
