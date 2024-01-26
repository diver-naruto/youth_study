import datetime
import time

import jwt


def createToken(username: str) -> str:
    salt = 'zzj'

    payload = {
        'userName': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 过期时间30分钟
    }

    tokenStr = jwt.encode(payload=payload, key=salt, algorithm='HS256')
    return tokenStr


def checkToken(tokenStr: str) -> str:
    salt = 'zzj'
    try:
        data = jwt.decode(tokenStr, salt, algorithms=['HS256'])
        data["authenticated"] = True
        return data
    except Exception as e:
        print(e)
        return '{"authenticated":false}'
    # except jwt.ExpiredSignatureError:
    #     return 'Expiration'
    # except jwt.DecodeError:
    #     return 'Failure'
    # except jwt.InvalidTokenError:
    #     return 'Invalid'


if __name__ == '__main__':
    token = createToken("demo")
    print(token)
    print(checkToken(token))
    time.sleep(61)
    print(checkToken(token))
