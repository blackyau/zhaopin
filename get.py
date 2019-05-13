from setting import headers, cookies
import requests


r = requests.get('https://fe-api.zhaopin.com/c/i/sou', headers=headers, cookies=cookies)
print(r.url)
print(r.text)
