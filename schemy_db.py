from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, distinct
from sqlalchemy import or_, insert, delete, update
from typing import Union
from encryptionUtil import encrypt
from tokenUtil import createToken
import datetime

Protocol = "mysql+pymysql"  # 协议
Username = "zxb"  # 用户名
Password = "123456"  # 密码
Host = "localhost"  # 主机
Port = "3306"  # 端口
Database = "youth-learning"  # 数据库名
SQLALCHEMY_DATABASE_URL = f'{Protocol}://{Username}:{Password}@{Host}:{Port}/{Database}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    # autocommit=True,  # 自动提交事务
    autoflush=True,  # 自动进行flush操作
    bind=engine
)

Base = declarative_base()

# 创建会话
session = SessionLocal()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    key = Column(String(255), nullable=False, comment="密钥")
    class_info_xls_path = Column(String(255), nullable=False, comment="班级信息表路径")
    college = Column(String(255), nullable=False, comment="学院名")
    remark = Column(String(255), nullable=True, comment="负责人信息备注")

    def __str__(self):
        return f"id:{self.id},username:{self.username},password:{self.password},key:{self.key},class_info_xls_path:{self.class_info_xls_path},remark:{self.remark}"


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    schedule = Column(DateTime(), nullable=True, comment="自动提醒时间")
    username = Column(String(255), ForeignKey("user.username", onupdate="CASCADE", ondelete="CASCADE"), nullable=False,
                      comment="负责人用户名")


def login(username: str, password: str) -> str:
    password = encrypt(password)
    user = session.query(User).filter(User.username == username, User.password == password).first()
    if user:
        return createToken(username)
    return "error"


def register(username: str, password: str, key: str = None, class_info_xls_path: str = None, college:str=None,remark: str = None) -> int:
    password = encrypt(password)
    insert_model = insert(User).values(**locals())
    result = session.execute(insert_model)
    return result.rowcount


def getUserInfo(username: str) -> User:
    user = session.query(User).filter(User.username == username).first()
    return user


def setUserInfo(username: str, key: str, class_info_xls_path: str) -> bool:
    update_model = update(User).filter(User.username == username).values(**locals())
    session.execute(update_model)
    session.commit()
    # user.save()
    return False


def getSchedules(username: str) -> list[Schedule]:
    schedules: list = session.query(Schedule).filter(Schedule.username == username).all()
    return schedules


def setSchedules(username: str, schedules: list[datetime.datetime]) -> bool:
    try:
        for s in schedules:
            insert_model = insert(Schedule).values(username=username, schedule=s)
            session.execute(insert_model)
        else:
            return True
    except Exception as e:
        print(e)
        return False


def clearSchedules(username: str):
    delete_model = delete(Schedule).filter(Schedule.username == username)
    session.execute(delete_model)


def deleteSchedule(scheduleId: int):
    delete_model = delete(Schedule).filter(Schedule.id == scheduleId)
    session.execute(delete_model)


if __name__ == '__main__':
    # print(login("demo", "demo"))
    # print(getUserInfo("demo"))
    # print(getSchedules("ikun"))
    # schedulesList = getSchedules("ikun")
    # for s in schedulesList:
    #     print("@@")
    #     print(s.schedule)
    setUserInfo("zzj", "ikun", "ikun")
    # print(register("ikun12", "ikun", "ikun", "ikun", "ikun", ))

    # print(datetime.datetime(2020, 1, 2, 0, 30, 30))
    # setSchedules("ikun", [datetime.datetime(2020, 1, 2, 0, 30, 30), datetime.datetime(2029, 1, 2, 0, 30, 30)])
    # # # clearSchedules("ikun")
    # # deleteSchedule(1)
    # print(getSchedules("ikun"))
    print(getUserInfo("demo"))
