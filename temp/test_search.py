import requests
import re
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get('https://m.zym888.com/', headers=headers)
html = response.text

params = {}
var_pattern = r'var\s+(\w+)\s*=\s*"([^"]+)"'
matches = re.findall(var_pattern, html)

for name, value in matches:
    params[name] = value

print('提取到的参数数量:', len(params))

print('\n等待5秒后搜索...')
time.sleep(5)

params['q'] = '斗破'

search_url = 'https://m.zym888.com/api/search'
search_response = requests.post(search_url, data=params, headers=headers)
print(f'搜索请求状态码: {search_response.status_code}')
result = search_response.json()
print(f'\n返回码: {result.get("code")}')
print(f'消息: {result.get("msg")}')

if result.get('code') == 0 and result.get('data'):
    data = result['data']
    print(f'\n数据类型: {type(data)}')
    if isinstance(data, list) and len(data) > 0:
        print(f'数据条数: {len(data)}')
        print(f'\n第一条数据:')
        print(json.dumps(data[0], ensure_ascii=False, indent=2))
    elif isinstance(data, dict):
        print(f'\n数据字段: {list(data.keys())}')
        if 'search' in data:
            search_list = data['search']
            print(f'搜索结果数量: {len(search_list) if isinstance(search_list, list) else "N/A"}')
            if isinstance(search_list, list) and len(search_list) > 0:
                print(f'\n第一条搜索结果:')
                print(json.dumps(search_list[0], ensure_ascii=False, indent=2))
