import json
import os
from flask import Flask, render_template


def sort_dict(in_dict):
    out_dict = dict()
    a = sorted(in_dict.items(), key=lambda x: x[1], reverse=True)
    for b in a:
        out_dict[b[0]] = b[1]
    return out_dict


file_list = os.listdir("./data")
all_data = list()
for file_name in file_list:
    path = "./data/" + file_name
    with open(path, 'r', encoding='utf-8') as file:
        try:
            load_file = json.load(file)
        except Warning:
            print(path, "\n数据解析错误,按回车跳过")
            input()
            continue
    for j in load_file['all_data']:
        for i in j['data']['results']:
            try:
                data_dict = dict(jobName=i['jobName'],
                                 city=i['city']['items'][0]['name'],
                                 jobType=i['jobType']['items'][0]['name'],
                                 eduLevel=i['eduLevel']['name'],
                                 salary=i['salary'],
                                 workingExp=i['workingExp']['name'],
                                 welfare=i['welfare'])
            except KeyError:
                continue
            all_data.append(data_dict)
# print(all_data)
print("总数据量:", len(all_data))
jobName_count = dict()
city_count = dict()
jobType_count = dict()
eduLevel_count = dict()
salary_count = dict()
workingExp_count = dict()
welfare_count = dict()
for i in all_data:
    for j in i.keys():
        if j == "jobName":
            temp_jobName = i[j]
            temp_jobName = temp_jobName.upper()
            if "JAVA" in temp_jobName:
                temp_jobName = "JAVA"
            elif "C" in temp_jobName:
                temp_jobName = "C/C++"
            elif "ANDORID" in temp_jobName or "安卓" in temp_jobName:
                temp_jobName = "Andorid"
            elif "IOS" in temp_jobName:
                temp_jobName = "IOS"
            elif "PYTHON" in temp_jobName:
                temp_jobName = "Python"
            elif ".NET" in temp_jobName:
                temp_jobName = ".NET"
            elif "前端" in temp_jobName:
                temp_jobName = "前端"
            if temp_jobName in jobName_count:
                jobName_count[temp_jobName] = jobName_count[temp_jobName] + 1
            else:
                jobName_count[temp_jobName] = 1
        elif j == "city":
            if i[j] in city_count:
                city_count[i[j]] = city_count[i[j]] + 1
            else:
                city_count[i[j]] = 1
        elif j == "jobType":
            if i[j] in jobType_count:
                jobType_count[i[j]] = jobType_count[i[j]] + 1
            else:
                jobType_count[i[j]] = 1
        elif j == "eduLevel":
            if i[j] in eduLevel_count:
                eduLevel_count[i[j]] = eduLevel_count[i[j]] + 1
            else:
                eduLevel_count[i[j]] = 1
        elif j == "salary":
            if i[j] in salary_count:
                salary_count[i[j]] = salary_count[i[j]] + 1
            else:
                salary_count[i[j]] = 1
        elif j == "workingExp":
            if i[j] in workingExp_count:
                workingExp_count[i[j]] = workingExp_count[i[j]] + 1
            else:
                workingExp_count[i[j]] = 1
        else:
            for welfare_key_word in i[j]:
                if welfare_key_word in welfare_count:
                    welfare_count[welfare_key_word] = welfare_count[welfare_key_word] + 1
                else:
                    welfare_count[welfare_key_word] = 1

jobName_count = sort_dict(jobName_count)
city_count = sort_dict(city_count)
jobType_count = sort_dict(jobType_count)
eduLevel_count = sort_dict(eduLevel_count)
salary_count = sort_dict(salary_count)
# workingExp_count = sort_dict(workingExp_count)
welfare_count = sort_dict(welfare_count)
# print(jobName_count)
# print(city_count)
# print(jobType_count)
# print(eduLevel_count)
# print(salary_count)
# print(workingExp_count)
# print(welfare_count)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", city_count=list(city_count.items()),
                           salary_count=list(salary_count.items())[:40],
                           workingExp_count=list(workingExp_count.items()),
                           eduLevel_count=list(eduLevel_count.items())
                           )


@app.route("/test")
def test():
    return render_template("test.html", salary_count=list(salary_count.items())[:40],
                           workingExp_count=list(workingExp_count.items())
                           )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
