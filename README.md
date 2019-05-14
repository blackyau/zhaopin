# zhaopin

zhaopin.com 智联招聘 爬虫

## api 分析

### 城市ID

https://fe-api.zhaopin.com/c/i/city-page/user-city


| key | value | 
| -- | -- |
| ipCity | 北京 |

value 可以取任意一个城市名，要经过 URL编码。返回结果如下

https://fe-api.zhaopin.com/c/i/city-page/user-city?ipCity=%E5%8C%97%E4%BA%AC

```json
{
    "code": 200,
    "data": {
        "name": "北京",
        "url": "//www.zhaopin.com/beijing/",
        "code": "530",
        "pinyin": "beijing",
        "priority": 1,
        "isIp": true,
        "isNew": true
    }
}
```

### 搜索结果

https://fe-api.zhaopin.com/c/i/sou

https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=530&industry=10100&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&_v=0.73135487&x-zp-page-request-id=df5808fd884b48adb0ab8a98d19a0431-1557819514764-957416&kw=java

| key | value | mark
| -- | -- | -- |
| start | 90 | 从第几条数据开始 |
| pageSize | 90 | 一页多少条数据 |
| cityId | 530 | 城市 |
| industry | 10100 | 行业 |
| workExperience | -1 | 工作经验 |
| education | -1 | 学历要求 |
| companyType | -1 | 公司性质 |
| employmentType | -1 | 职位类别 |
| jobWelfareTag | -1 | 职位标签 |
| kw | java | 搜索关键字 |
| kt | 3 | 未知但是必带 |
| _v | 0.73135487 | 校验位 |
| x-zp-page-request-id | df5808fd8... | 校验位2 |

`_v` 就是一个随机的8位小数

`x-zp-page-request-id` 可以在网页的源代码中看到生成方式

```html
<script>var zpPageRequestId = "bc026e5698b04fc1a7a295cd071249f6-" + (new Date()).valueOf() + "-" + parseInt(Math.random() * 1000000)</script>
```

- `bc026e5698b04fc1a7a295cd071249f6` 随机数 MD5 后的结果

- `(new Date()).valueOf()` 时间戳

- `parseInt(Math.random() * 1000000)` 随机数 * 1000000 后取整数部分

这部分用 Python 这样解决

```python
# 32位随机ID
md5 = hashlib.md5()
md5.update(str(random.random()).encode('utf-8'))
random_id = str(md5.hexdigest())

# 时间戳
now_time = str(int(time.time() * 1000))

# 随机6位数
random_num = str(int(random.random() * 1000000))

# _v
random_v = str(random.random())[:9]
```

这部分主要都来自 [CSDN@学习才能变得强大 - 爬虫智联招聘](https://blog.csdn.net/qq_42583549/article/details/85015406) 感谢

个人感觉这两个字段主要用来区分不同的用户。加上有时间戳就可以防止数据更新后，如果要翻页，数据就可能会出现之前看过的数据。