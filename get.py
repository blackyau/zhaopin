import hashlib
import random
import requests
import time
from setting import headers

md5 = hashlib.md5()
md5.update(str(random.random()).encode('utf-8'))
random_id = str(md5.hexdigest())  # 32位随机ID
now_time = str(int(time.time() * 1000))  # 时间戳
random_num = str(int(random.random() * 1000000))  # 随机6位数
random_all = random_id + '-' + now_time + '-' + random_num
random_v = str(random.random())[:10]  # 随机7位小数


def get_sou(random_v_in, random_request_id, page=1, page_size=90, city_id=489, industry=0, kt=3, kw="", **more_information):
    payload = {'start': page, 'pageSize': page_size, 'cityId': city_id, 'industry': industry, 'workExperience': -1,
               'education': -1, 'companyType': -1, 'employmentType': -1, 'jobWelfareTag': -1, 'kw': kw, 'kt': kt,
               '_v': random_v_in, 'x-zp-page-request-id': random_request_id}

    if more_information:  # 把关键字参数写入
        for key in more_information.keys():
            payload[key] = more_information[key]

    if payload['start'] <= 1:  # 只获取第一页不需要带这个参数
        payload.pop('start')
    else:  # 计算页数
        payload['start'] = (payload['start']-1)*payload['pageSize']
    if payload['kw'] == '':  # 不要关键字就不带参数
        payload.pop('kw')
    if payload['industry'] == 0:  # 不要行业就不带参数
        payload.pop('industry')

    r = requests.get('https://fe-api.zhaopin.com/c/i/sou', headers=headers, params=payload)
    print(random_v_in)
    print(random_request_id)

    if "\"results\":[]" in r.text:
        raise Warning("返回数据异常!以下是 API 返回信息\n"+r.text)
    else:
        return r


print(get_sou(random_v, random_all, 1).text)
