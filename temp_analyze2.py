import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get('https://m.zym888.com/fenlei1/', headers=headers, timeout=30)
html = response.text

# 保存HTML到文件
with open('G:/Project/阅读SKills/legadoSkill-main/temp_fenlei1.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML已保存到 temp_fenlei1.html")
print(f"HTML长度: {len(html)}")

# 查找书籍链接
book_links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', html)
print("\n前30个链接:")
for i, (link, text) in enumerate(book_links[:30]):
    print(f'{i+1}. {text.strip()}: {link}')
