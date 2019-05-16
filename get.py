import hashlib
import random
import requests
import time
from setting import headers


def random_info():
    md5 = hashlib.md5()
    md5.update(str(random.random()).encode('utf-8'))
    random_id = str(md5.hexdigest())  # 32位随机ID
    now_time = str(int(time.time() * 1000))  # 时间戳
    random_num = str(int(random.random() * 1000000))  # 随机6位数
    random_all_out = random_id + '-' + now_time + '-' + random_num
    random_v_out = str(random.random())[:10]  # 随机8位小数
    return random_v_out, random_all_out


def city_info(str_in):
    if type(str_in) != str:
        raise TypeError("只能传入字符串,地区名的全称")
    else:
        if str_in == "全国":
            return 489
        else:
            payload = {"ipCity": str_in}
            r = requests.get("https://fe-api.zhaopin.com/c/i/city-page/user-city", headers=headers, params=payload)
            return r.json()["data"]["code"]


def sou(random_v_in, random_request_id, page=1, page_size=90, city_name="全国", industry_value=0, kt=3, kw="",
        **more_information):
    payload = {'start': page, 'pageSize': page_size, 'cityId': city_info(city_name), 'industry': industry_value,
               'workExperience': -1,
               'education': -1, 'companyType': -1, 'employmentType': -1, 'jobWelfareTag': -1, 'kw': kw, 'kt': kt,
               '_v': random_v_in, 'x-zp-page-request-id': random_request_id}

    if more_information:  # 把关键字参数写入
        for key in more_information.keys():
            payload[key] = more_information[key]

    if payload['start'] <= 1:  # 只获取第一页不需要带这个参数
        payload.pop('start')
    else:  # 计算页数
        payload['start'] = (payload['start'] - 1) * payload['pageSize']
    if payload['kw'] == '':  # 不要关键字就不带参数
        payload.pop('kw')
    if payload['industry'] == 0:  # 不要行业就不带参数
        payload.pop('industry')

    r = requests.get('https://fe-api.zhaopin.com/c/i/sou', headers=headers, params=payload)

    if "\"results\":[]" in r.text:
        raise Warning("返回数据异常!以下是 API 返回信息\n" + r.text)
    else:
        return r


# TODO extractTag extractSkillTag, 职位亮点 welfare, 工资 salary, workingExp workingExp["name"], jobName,eduLevel eduLevel["name"],
# TODO city city["display"], companySum company["size"][""name""], companyType company["type"][""name""], jobType["items"]["name"](多个)


if __name__ == "__main__":
    start_time = time.time()
    true_start_time = start_time
    city_tup = ("全国", "北京", "上海", "广州", "深圳", "成都", "重庆")
    industry_dict = {160400: "计算机软件", 160600: "网络游戏", 160000: "IT服务", 160200: "计算机硬件", 210500: "互联网_电子商务"}
    for city in city_tup:
        for industry in industry_dict.keys():
            # TODO 判断是否创建路径
            with open("./data/" + city + "_" + industry_dict[industry] + ".json", mode="w", encoding="utf-8") as file:
                random_v, random_all = random_info()
                for page_sum in range(1, 13):
                    try:
                        result = sou(random_v, random_all, page_sum, 90, city, industry)
                        file.write(result.text)
                        print("city:", city, " industry:", industry_dict[industry], " page:", page_sum, "爬取完毕 等待3s ")
                        time.sleep(3)
                        start_time = start_time - 3
                    except Warning as Warning_info:
                        print("Page", page_sum, Warning_info)
                        break
    end_time = time.time()
    print("总共耗时:", end_time-true_start_time, "\n除去等待时间耗时:", end_time-start_time)
