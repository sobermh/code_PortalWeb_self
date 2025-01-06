from passlib.context import CryptContext


class Hashing(object):
    """密码工具类"""

    def __init__(self, schemes: str = 'bcrypt'):
        self.crypt = CryptContext(schemes=[schemes], deprecated="auto")

    def hash(self, raw_pwd: str) -> str:
        """
        密码加密
        :param raw_pwd: 用户输入的原始密码
        :return: 密码的哈希值
        """
        return self.crypt.hash(raw_pwd)

    def verify(self, raw_pwd: str, hashed_pwd: str) -> bool:
        """
        验证密码是否正确
        :param raw_pwd: 用户输入的原始密码
        :param hashed_pwd: 密码的哈希值
        :return: bool
        """
        return self.crypt.verify(raw_pwd, hashed_pwd)


# def get_wechat_info(code):
#     """
#     获取微信用户信息
#     文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
#     :param code: 小程序端用户的授权码
#     :return:
#     """
#     url = f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.WECHAT['app_id']}&secret={settings.WECHAT['app_secret']}&js_code={code}&grant_type=authorization_code"
#     response = requests.get(url)
#     return response.json()
