import uuid
from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from application import settings


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

class JWTTool(object):
    """JWT工具类"""
    # 异常类
    JWTError = jwt.JWTError
    ExpiredSignatureError = jwt.ExpiredSignatureError

    def create_token(self, data: dict, expire_time: Optional[int] = None):
        """
        生成JWT
        :param data: 需要进行JWT令牌加密的用户信息（解密的时候会用到）
        :param expire_time: 令牌有效期，单位：秒
        :return: jwt
        """
        local_now = datetime.now()

        if expire_time:
            expire = local_now + timedelta(seconds=expire_time)
        else:
            expire = local_now + timedelta(seconds=settings.JWT['expire_time'])

        # 组装载荷数据的标准声明
        payload = {
            "exp": expire,  # 过期时间
            "iat": local_now,  # 生成时间
            "nbf": local_now,  # 启用时间
            "jti": str(uuid.uuid4())  # 唯一标记
        }
        # 组装载荷数据的公共声明
        payload.update(data)
        # 自动生成jwt
        return jwt.encode(payload, settings.JWT['secret_key'], algorithm=settings.JWT['algorithm'])

    def verify_token(self, token: str) -> dict:
        """
        验证token
        :param token: 客户端发送过来的token
        :return: 返回用户信息
        """
        payload = jwt.decode(token, settings.JWT['secret_key'], algorithms=settings.JWT['algorithm'])
        return payload


if __name__ == '__main__':
    # print(Hashing().hash('123456'))
    print(JWTTool().create_token({'id': 1, 'username': 'admin'}))
