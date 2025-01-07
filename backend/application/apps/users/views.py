from fastapi import APIRouter, HTTPException, status
from starlette.requests import Request

from .scheams import *
from . import models
from .utils import JWTTool
from ...utils.response import fail_response, success_response

app = APIRouter()


@app.post('/register', summary="用户注册", response_model=UserRegisterResp)
async def register(request: Request, user_info: UserRegisterReq) -> dict:
    """
    用户注册
    :param request:请求对象
    :param user_info: 用户信息
    :return:
    """
    sms_key = f'sms_{user_info.mobile}'
    user = await models.User.filter(username=user_info.username).first()
    if user:
        return fail_response('当前账号已存在！')
    user = await models.User.filter(mobile=sms_key).first()
    if user:
        return fail_response('当前手机号已注册！')

    redis = request.app.state.redis
    redis_sms = await redis.get(f'sms_{user_info.mobile}')
    if redis_sms is None:
        return fail_response('验证码不存在或已过期！')
    if redis_sms != user_info.sms_code:
        return fail_response('验证码不正确！')

    # wechat_user = wechat_tools.get_wechat_info(user_info.code)

    user = await models.User.create(
        **dict(user_info),
        # username=user_info.mobile,
        # avatar=user_info.avatarUrl,
    )
    data = {
        'username': user.username,
        'token': JWTTool().create_token({'id': user.id, 'username': user.username})
    }
    await redis.delete(sms_key)
    return success_response(data)


@app.post('/login', response_model=UserLoginReq, summary="用户登录")
async def login(user_info: UserLoginOutResp) -> dict:
    """用户登录"""
    # # 0. 判断验证码是否正确
    # redis = request.app.state.redis
    # sms_code = await redis.get(f'sms_{user_info.mobile}')
    #
    # if not sms_code:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='验证码不存在或填写错误！')
    #
    # if sms_code != user_info.sms_code:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='验证码不存在或填写错误！')

    # 判断当前用户是否存在
    # # 1. 基于code请求微信服务器获取用户的OpenID以及将来调用用户信息的session_key
    # result = wechat_tools.get_wechat_info(user_info.code)

    # 0. 根据手机号或微信OpenID判断是否重复注册
    # user = await models.User.filter(Q(mobile=user_info.mobile) | Q(openid=result['openid'])).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='当前用户不存在！')

    # # 判断密码是否正确
    # hashing = tools.Hashing()
    # ret = hashing.verify(user_info.password, user.password)
    # if not ret:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='当前账号或密码错误！')
    # # 生成token
    # token = JwtToken.create_token({
    #     'id': user.id,
    #     'username': user.username
    # })
    #
    # # 记录用户的登陆历史
    # await models.UserLoginHistory.create(user=user)
    #
    # # 保存Token到redis中
    # await redis.setex(f'token_{user.id}', settings.JWT['expire_time'], token)
    #
    # # 如果打开限流功能，则初始化用户每天免费使用AI助理的次数到redis中，次日过期
    # if settings.AI_ROBOT['limit'] == '1':
    #     current_time = datetime.now()
    #     tomorrow = current_time + timedelta(days=1)
    #     tomorrow_zero = datetime.strptime(f'{tomorrow.year}-{tomorrow.month}-{tomorrow.day}', '%Y-%m-%d')
    #     delta = tomorrow_zero - current_time
    #     redis.setex(f'api_{user.id}', delta.seconds, settings.AI_ROBOT['count'])
    #
    # # 删除短信验证码，一码多用
    # await redis.delete(f'sms_{user_info.mobile}')

    # is_exit
    user = await models.User.filter(username=user_info.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='当前用户不存在！')
    # validate
    if user_info.password != user.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='当前账号或密码错误！')

    return {
        'username': user.username,
    }
