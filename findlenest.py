import requests
import re

url="https://www.jianshu.com"

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

resp=requests.get(url,headers=headers)
print(resp.text)
li = re.findall(r'<p class="abstract">(.*?)</p>',resp.text)[0]

print(li)

