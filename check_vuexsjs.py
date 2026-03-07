#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查jsLib中VUEXSJS的暴露方式"""
import json
import re

# 加载书源
with open('3a.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    if isinstance(data, list):
        data = data[0]

js_lib = data.get('jsLib', '')

# 检查VUEXSJS的暴露方式
print('=== 检查VUEXSJS的暴露方式 ===')

# 搜索VUEXSJS相关代码
patterns = [
    r'VUEXSJS\s*=',
    r'\.VUEXSJS\s*=',
    r'global\.VUEXSJS',
    r'window\.VUEXSJS',
    r'this\.VUEXSJS',
    r'XSVUE\s*=',
    r'XSVUE\.decompressFromBase64',
]

for pattern in patterns:
    matches = re.findall(pattern, js_lib)
    if matches:
        print(f'Pattern "{pattern}": Found {len(matches)} matches')
        for match in matches[:3]:
            print(f'  - {match}')
    else:
        print(f'Pattern "{pattern}": No matches')

# 检查jsLib结尾
print(f'\n=== jsLib结尾500字符 ===')
print(js_lib[-500:])
