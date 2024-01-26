from flask import Flask
from flask import request
from flask_cors import CORS
from schemy_db import login, register, getUserInfo, setUserInfo, getSchedules, clearSchedules, deleteSchedule
from tokenUtil import checkToken
import os
# from youth_study.extract import extract
from extract import extract

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/test', methods=["get", "post"])
def test():
    # print(request.json)
    return "helloworld"


@app.route('/login', methods=["post"])
def appLogin():
    data = request.json
    username = data.get("username")
    password = data.get("password")
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
        path = f"youth_study/db/static/{username}.xlsx"
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
    username=request.args.get('username',"demo") #用户名
    print(username)
    user=getUserInfo(username)
    college=user.college # 学院名
    class_info_xls_path=user.class_info_xls_path #路径
    key=user.key # api key
    print(key,username,college,class_info_xls_path)
    result = extract
    return result

    

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        # debug=
    )
