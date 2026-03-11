import requests
import re
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print('Step 1: Getting homepage...')
response = requests.get('https://m.zym888.com/', headers=headers)
html = response.text

params = {}
var_pattern = r'var\s+(\w+)\s*=\s*"([^"]+)"'
matches = re.findall(var_pattern, html)

for name, value in matches:
    params[name] = value

print(f'Extracted {len(params)} parameters')

print('Step 2: Waiting 6 seconds...')
time.sleep(6)

params['q'] = '斗破'

print('Step 3: Sending search request...')
search_url = 'https://m.zym888.com/api/search'
search_response = requests.post(search_url, data=params, headers=headers)
print(f'Status code: {search_response.status_code}')
result = search_response.json()
print(f'Code: {result.get("code")}')
print(f'Msg: {result.get("msg")}')

if result.get('code') == 0 and result.get('data'):
    data = result['data']
    print(f'Data type: {type(data).__name__}')
    if isinstance(data, list):
        print(f'List length: {len(data)}')
        if len(data) > 0:
            print('First item:')
            print(json.dumps(data[0], ensure_ascii=False, indent=2))
    elif isinstance(data, dict):
        print(f'Keys: {list(data.keys())}')
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1500])
