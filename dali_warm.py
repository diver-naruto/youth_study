import json
import requests
# 爬取爱词霸每日鸡汤
def get_iciba_everyday_chicken_soup():
    url = 'http://open.iciba.com/dsapi/'  # 词霸免费开放的jsonAPI接口
    r = requests.get(url)
    all_content = json.loads(r.text)  # 获取到json格式的内容，内容很多,json.loads: 将str转成dict
    English = all_content['content']  # 提取json中的英文鸡汤
    Chinese = all_content['note']  # 提取json中的中文鸡汤
    everyday_soup =  f"毒鸡汤：\n{Chinese}({English}) "  # 合并需要的字符串内容
    return everyday_soup  # 返回结果

print(get_iciba_everyday_chicken_soup())

"""
结果:
It's so easy to be careless, but it takes curse and courage to take cares.  
想要不在乎太容易了，但要有无穷的勇气才能学会在乎。
"""
