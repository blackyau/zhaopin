from setting import headers, cookies
import requests, hashlib, random, time


md5 = hashlib.md5()
md5.update(str(random.random()).encode('utf-8'))
random_id = str(md5.hexdigest())  # 32位随机ID
now_time = str(int(time.time() * 1000))  # 时间戳
random_num = str(int(random.random() * 1000000))  # 随机6位数
random_v = str(random.random())[:9]  # 随机7位小数

# r = requests.get('https://fe-api.zhaopin.com/c/i/sou', headers=headers, cookies=cookies)
# print(r.url)
# print(r.text)
