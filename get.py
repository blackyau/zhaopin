import hashlib
import random
import requests
import time
import json
from setting import headers


md5 = hashlib.md5()
md5.update(str(random.random()).encode('utf-8'))
random_id = str(md5.hexdigest())  # 32位随机ID
now_time = str(int(time.time() * 1000))  # 时间戳
random_num = str(int(random.random() * 1000000))  # 随机6位数
random_all = random_id+'-'+now_time+'-'+random_num
random_v = str(random.random())[:9]  # 随机7位小数


payload = {'pageSize': 90, 'cityId': 530, 'industry': 10100, 'workExperience': -1, 'education': -1, 'companyType': -1, 'employmentType': -1, 'jobWelfareTag': -1, 'kt': 3, '_v': random_v, 'x-zp-page-request-id': random_all}
r = requests.get('https://fe-api.zhaopin.com/c/i/sou', headers=headers, params=payload)
print(r.text)
json_data = json.loads(r.text)
print(json_data)