#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查jsLib的IIFE格式"""
import json

# 加载书源
with open('3a.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    if isinstance(data, list):
        data = data[0]

js_lib = data.get('jsLib', '')

print('=== jsLib开头1000字符 ===')
print(js_lib[:1000])

print('\n=== 搜索IIFE模式 ===')
import re
# 搜索IIFE模式
iife_patterns = [
    r'\(function\s*\([^)]*\)\s*\{',
    r'\(function\s*\(\s*\)\s*\{',
]
for pattern in iife_patterns:
    matches = list(re.finditer(pattern, js_lib[:2000]))
    for match in matches:
        start = match.start()
        print(f'\nFound IIFE at position {start}:')
        print(js_lib[start:start+200])
