from application.apps.users.utils import Hashing


def test_hash():
    hashing = Hashing()
    # 对原始密码进行哈希加密
    password_hash1 = hashing.hash("123456")
    print(password_hash1)
    password_hash2 = hashing.hash("123456")
    print(password_hash2)

    # 判断原始密码是否和密码哈希值是否匹配
    ret = hashing.verify("123455", password_hash1)
    print(ret)
    ret = hashing.verify("123456", password_hash2)
    print(ret)


if __name__ == '__main__':
    pass
    # test_hash()
