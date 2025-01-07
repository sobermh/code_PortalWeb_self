import secrets
import string


def generate_random_key(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key


# 生成一个符合要求的随机密钥
key = generate_random_key(50)
print(key)
