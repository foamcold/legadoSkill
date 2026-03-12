import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get('https://m.zym888.com', headers=headers, timeout=30)
html = response.text

nav_links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', html)
for i, (link, text) in enumerate(nav_links[:100]):
    print(f'{i+1}. {text.strip()}: {link}')
