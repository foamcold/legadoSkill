#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查密钥生成和VUEXSJS对象"""
import json
import sys
sys.path.insert(0, '.')
from debugger.js_engine import execute_js

# 加载书源
with open('3a.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    if isinstance(data, list):
        data = data[0]

js_lib = data.get('jsLib', '')

# 测试密钥生成
js_code = '''
// 检查密钥生成
const _0x491596 = [
  String.fromCharCode(49, 50, 51, 35, 50, 94),
  String.fromCharCode(48, 64, 48, 118, 109, 64),
  String.fromCharCode(48, 56, 46, 98, 56, 57),
  String.fromCharCode(48, 49, 50, 51, 103, 52),
  String.fromCharCode(53, 54, 55, 56, 57, 48, 49, 50)
];
const _0x47950f = _0x491596.join("");

console.log('Key parts:');
for (var i = 0; i < _0x491596.length; i++) {
  console.log('  [' + i + '] ' + _0x491596[i] + ' (length: ' + _0x491596[i].length + ')');
}
console.log('Full key: ' + _0x47950f);
console.log('Key length: ' + _0x47950f.length);
console.log('Key check (must be 32): ' + (_0x47950f.length === 32 ? 'PASS' : 'FAIL'));

// 检查VUEXSJS对象
console.log('\\nVUEXSJS check:');
console.log('  typeof VUEXSJS: ' + typeof VUEXSJS);
if (typeof VUEXSJS !== 'undefined') {
  console.log('  VUEXSJS.enc: ' + typeof VUEXSJS.enc);
  console.log('  VUEXSJS.AES: ' + typeof VUEXSJS.AES);
  console.log('  VUEXSJS.mode: ' + typeof VUEXSJS.mode);
  console.log('  VUEXSJS.pad: ' + typeof VUEXSJS.pad);
}
'''

print('=== 检查密钥生成和VUEXSJS对象 ===')
result = execute_js(js_code, {}, js_lib)
print(f'Success: {result.success}')
print(f'Console Output:')
for line in result.console_output:
    print(f'  {line}')
