import pymysql
from functools import wraps, partial

Configuration = {
    "host": "localhost",  # 主机名
    "port": 3306,
    "user": "zzj",  # 用户名
    "password": "0605",  # 密码
    "database": "youth-learning"  # 数据库名
}


# 打开数据库连接
# print(**Configuration)

# def execute(sql:str):

def autoConnect(f):
    db = pymysql.connect(**Configuration)
    cursor = db.cursor()

    @wraps(f)
    def wrapper(*args, **kwargs):
        print(cursor)
        try:
            return f(cursor, *args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    return wrapper

# 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")
# cursor.execute("SELECT * FROM USER;")
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
# # print("Database version : %s " % data)
# print(data)
# # 关闭数据库连接
# db.close()
