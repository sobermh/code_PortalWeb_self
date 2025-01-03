# from passlib.context import CryptContext
#
#
# class Hashing(object):
#     """密码工具类"""
#
#     def __init__(self, schemes: str = 'bcrypt'):
#         self.crypt = CryptContext(schemes=[schemes], deprecated="auto")
#
#     def hash(self, raw_pwd: str) -> str:
#         """
#         密码加密
#         :param raw_pwd: 用户输入的原始密码
#         :return: 密码的哈希值
#         """
#         return self.crypt.hash(raw_pwd)
#
#     def verify(self, raw_pwd: str, hashed_pwd: str) -> bool:
#         """
#         验证密码是否正确
#         :param raw_pwd: 用户输入的原始密码
#         :param hashed_pwd: 密码的哈希值
#         :return: bool
#         """
#         return self.crypt.verify(raw_pwd, hashed_pwd)
#
#
# if __name__ == '__main__':
#     hashing = Hashing()
#     # 对原始密码进行哈希加密
#     password_hash1 = hashing.hash("123456")
#     print(password_hash1)
#     password_hash2 = hashing.hash("123456")
#     print(password_hash2)
#
#     # 判断原始密码是否和密码哈希值是否匹配
#     ret = hashing.verify("123455", password_hash1)
#     print(ret)
#     ret = hashing.verify("123456", password_hash2)
#     print(ret)