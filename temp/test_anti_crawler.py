import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
session = requests.Session()
session.headers.update(headers)

print('=== 分析反爬机制 ===\n')

# 分析验证页面的JS代码
print('验证页面JS分析:')
print('''
关键代码:
if(!getCookie("getsite")){
  var go=true;
  var array=["b","b","b","b","b"];
  array.forEach(function(u){
    var img=new Image();
    img.src="https://m."+u+"/favicon.ico";
    img.onload = function(){
      if(go && this.width>9){
        go=false;
        setCookie("getsite",u,18000);
      }
    }
  });
  get_href()
}else{
  get_href()
}

function get_href(){
  location.href = "/userverify" + window.location.hash.replace('#','');   
}
''')

print('\n反爬机制分析:')
print('1. 正文页检查是否有 getsite cookie')
print('2. 如果没有，跳转到 /userverify 验证页面')
print('3. 验证页面是SPA，需要JavaScript执行')
print('4. 验证通过后会设置 getsite cookie')

print('\n解决方案:')
print('方案1: 使用webView加载正文页')
print('方案2: 在章节URL后添加 ,{"webView":true}')
print('方案3: 使用java.webView获取页面内容')

# 测试方案2：直接在URL中添加webView参数
print('\n\n测试方案：检查是否可以通过webView绕过')
print('在Legado中，可以使用以下方式:')
print('1. 章节URL格式: /book/xxx/1.html,{"webView":true}')
print('2. 或者使用 @js: java.webView() 方法')
