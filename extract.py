import pandas as pd
import requests
import json
import os



#将班里学习的人提取出来
def extract(excel_name,colledge_name):
    current_dir=os.path.dirname(os.path.abspath(__file__))
    data = pd.read_excel(f"{current_dir}/youth_excel/1.xlsx")
    data = data[data["三级单位"]==colledge_name]
    
    data = data["人员姓名"]
    data2 = pd.read_excel(f"{current_dir}/static/{excel_name}.xlsx")
    data_id = data2["学号"]
    data_name = data2["姓名"]
    data_num = data2["电话号"]

    
    

    dict_number = []
    
# 找到未学习的人
    diffrence = set(data_name).difference(set(data))
    print(diffrence)
    list_id=list(data_id)
    list_name=list(data_name)
    list_num=list(data_num)
    res=[]
    for i in range(len(list_id)):
        id_id=list_id[i]
        name_name=list_name[i]
        num_num=list_num[i]
        stu={}
        stu["id"]=id_id
        stu["name"]=name_name
        stu["number"]=num_num
        res.append(stu)

    # print(res)
    result=[]
    for stu in res:
        if(stu["name"] in diffrence):
            result.append(stu)
    
    for i in result:
        dict_number.append(i["number"])
    return result


#提醒全部
def notification_all(notice_url,dict_name,dict_number):

    url = notice_url
    headers = {"Content-Type": "application/json; charset=utf-8"}
    range_num = len(dict_number)
    data = {
            # "title": "小黑子",
            "msgtype": "text",
            "text": {"content": "记得青年大学习:\n" + ",".join(dict_name) +f"\n未学习人数:{range_num}" },
            }
            # 发送请求
    requests.post(url, data=json.dumps(data).encode("utf8"), headers=headers,)
    if range_num <= 50:
        data = {
            "msgtype": "text",
            "text": {"content": "记得青年大学习:\n"  },
            "at": {"atMobiles" : f"{dict_number}"}
            }   
        requests.post(url, data=json.dumps(data).encode("utf8"), headers=headers,)     
    if range_num > 50 :
        dict_number1 = dict_number[0:50]
        dict_number2 = dict_number[50:range_num]
        dict_number = [dict_number1,dict_number2]
        for i in dict_number:
            data = {
                "msgtype": "text",
                "text": {"content": "记得青年大学习:\n"  },
                "at": {"atMobiles" : f"{i}"}
            }
            requests.post(url, data=json.dumps(data).encode("utf8"), headers=headers,)
    return "success"

#单独提醒
def notification_only(notice_url,phone_number):
    url = notice_url
    number = []
    number.append(phone_number)
    print(url)
    print(phone_number)
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
            "msgtype": "text",
            "text": {"content": "记得青年大学习:\n"  },
            "at": {"atMobiles" :  [phone_number]}
            }   
    requests.post(url, data=json.dumps(data).encode("utf8"), headers=headers,)
    return "success"
            

if __name__ == "__main__":
    extract("demo","大数据与智能工程学院")

