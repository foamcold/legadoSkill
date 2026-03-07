#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试正文内容解析"""
import json
import sys
import urllib.request
import ssl
sys.path.insert(0, '.')
from debugger.js_engine import execute_js

# 加载书源
with open('3a.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    if isinstance(data, list):
        data = data[0]

js_lib = data.get('jsLib', '')

# 获取正文数据
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

url = 'https://www.aaawz.cc/api-chapter-30763-21-2566797'
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

print('=== 获取正文数据 ===')
with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
    content = response.read().decode('utf-8')
    print(f'Content Length: {len(content)}')
    print(f'Content Preview: {content[:200]}...')
    
    # 测试正文规则
    js_code = '''
    console.log('Testing content parsing...');
    console.log('result length: ' + result.length);
    console.log('result preview: ' + result.substring(0, 100));
    
    // 第一步：调用_0x3ed9ab
    var step1 = _0x3ed9ab(result);
    console.log('step1 (_0x3ed9ab result) type: ' + typeof step1);
    console.log('step1 length: ' + (step1 ? step1.length : 'null'));
    console.log('step1 preview: ' + (step1 ? step1.substring(0, 100) : 'null'));
    
    // 第二步：调用XSVUE.decompressFromBase64
    if (step1) {
        var step2 = XSVUE.decompressFromBase64(step1);
        console.log('step2 (XSVUE.decompressFromBase64 result) type: ' + typeof step2);
        console.log('step2 length: ' + (step2 ? step2.length : 'null'));
        console.log('step2 preview: ' + (step2 ? step2.substring(0, 200) : 'null'));
        
        body = step2;
    } else {
        console.log('step1 is null/false, cannot proceed');
    }
    
    result = body;
    '''
    
    print('\n=== 执行正文规则 ===')
    result = execute_js(js_code, {'result': content, 'body': ''}, js_lib)
    print(f'Success: {result.success}')
    print(f'Result Length: {len(result.result) if result.result else 0}')
    print(f'Result Preview: {result.result[:300] if result.result else "None"}...')
    print(f'\nConsole Output:')
    for line in result.console_output:
        print(f'  {line}')
