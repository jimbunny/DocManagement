
import json

with open("test.json", 'r', encoding='utf-8') as load_f:
    load_dict = json.load(load_f)["data"]
    print(json.dumps(load_dict))
