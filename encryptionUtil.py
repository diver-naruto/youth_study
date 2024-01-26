import hashlib


def encrypt(password: str) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(password.encode())
    result = hash_obj.hexdigest()
    return result


if __name__ == '__main__':
    print(encrypt("demo"))
