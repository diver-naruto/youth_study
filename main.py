from flask import Flask
from flask import request
from flask_cors import CORS
from schemy_db import login, register, getUserInfo, setUserInfo, getSchedules, clearSchedules, deleteSchedule
from tokenUtil import checkToken
from auto_get_cook import get_youth_cook
from extract import extract,notification_only,notification_all

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/test', methods=["get", "post"])
def test():
    return "helloworld"


@app.route('/login', methods=["post"])
def appLogin():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    res=login(username, password)
    print(res,"*"*10)
    return login(username, password)


@app.route('/register', methods=["post"])
def appRegister():
    data = request.json
    try:
        register(**data)
        return "true"
    except Exception as e:
        print(e)
        return "error"


@app.route("/authenticated")
def authenticated():
    headers = request.headers
    token = headers.get("token")
    res = checkToken(token)
    return res


@app.route('/upload', methods=['POST'])
def upload():
    try:
        username = request.form.get("username")
        key = request.form.get("key")
        path = f"youth_study/static/{username}.xlsx"
        table = request.files.get("table")
        table.save(path)
        setUserInfo(
            username=username,
            key=key,
            class_info_xls_path=path,
        )
        
        return "true"
    except Exception as e:
        print(e)
        return "error"
    

@app.route('/unlearnedStudents', methods=['get'])
def get_unlearing_students():
    get_youth_cook()
    username=request.args.get('username') #用户名
    print(username)
    user=getUserInfo(username)
    college=user.college # 学院名
    class_info_xls_path=user.class_info_xls_path #路径
    key=user.key # api key
    print(key,username,college,class_info_xls_path)
    result = extract(username,college)
    return result

@app.route('/notification', methods=['get'])
def notification():
    username=request.args.get('username') #用户名
    number=request.args.get('number') #用户名

    user=getUserInfo(username)
    key=user.key # api key
    result=notification_only(key,number)
    return result

@app.route('/notificationAll', methods=['post'])
def notificationAll():
    username=request.json.get("username")
    numberList=request.json.get("numberList")
    name_list=request.json.get("nameList")
    print(type(name_list))
    print(name_list)
    # print(username,numberList)
    user=getUserInfo(username)
    key=user.key # api key
    result = notification_all(key,name_list,numberList)
    return result


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        # debug=
    )
