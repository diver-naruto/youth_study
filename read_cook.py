import os
import json
# filepath = "/root/autodaka2.0/cook"

# filepath = "/root/autodaka2.0/cook"
filepath = "youth_study/youth_cook"

def read_json(name):
    p = f"{filepath}/{name}.json"
    if os.path.exists(p):
        f = open(p, "r")
        dict_data = json.loads(f.read())
        return dict_data


# cookies = read_json("20191158017")
# print(type(cookies))
test = 55
print(test//2)