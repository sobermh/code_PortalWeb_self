import string, secrets


def gen_int(length: int = 4) -> str:
    """
    生成指定长度的纯数字字符串
    @param length: 字符长度
    return
    """
    characters = string.digits
    ret = "".join(secrets.choice(characters) for i in range(length))
    return ret


def gen_app_secret(length: int = 50) -> str:
    """
    生成指定长度的字符串
    @param length: 字符长度
    return
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key
