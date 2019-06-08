import json

with open("./data/上海_IT服务.json", 'r', encoding='utf-8') as file:
    load_file = json.load(file)
    for a in load_file['all_data']:
        print(sum, a)
