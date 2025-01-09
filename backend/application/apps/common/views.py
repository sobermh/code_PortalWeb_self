import os
from fastapi import APIRouter
from starlette.requests import Request

from application.core import settings
from application.core.schemas import BaseResp
from application.utils import comm_tool, aliyunclound, logs
from application.utils.response import fail_response, success_response

logger = logs.get_logger(os.environ.get('APP_NAME'))

app = APIRouter()


@app.get('/api')
async def api() -> dict:
    """
    测试接口
    :return:
    """
    return {'title': f'{os.environ.get("APP_NAME")}测试接口'}


@app.get('/sms/{mobile}', summary="发送短信验证码", response_model=BaseResp)
async def sms(request: Request, mobile: str) -> dict:
    """
    发送短信验证码
    :param request: 请求对象
    :param mobile: 手机号
    :return:
    """
    sms_key = f'sms_{mobile}'
    redis = request.app.state.redis
    # 判断验证码是否失效
    existing_code = await redis.get(sms_key)
    if existing_code is not None:
        return fail_response("验证码仍有效，请稍后再试")
    # 生成指定长度随机验证码[纯数字]
    sms_code = comm_tool.gen_int(int(settings.SMS['length']))
    # 发送验证码短信
    aliyun = aliyunclound.AliYunClound(settings.ALIYUN['key'], settings.ALIYUN['secret'])
    data = {
        'code': sms_code
    }
    result = await aliyun.sms_async(mobile, data, settings.ALIYUN['sms']['sign_name'],
                                    settings.ALIYUN['sms']['template_code'])
    if result.code != 'OK':
        return fail_response(f'短信发送失败！{result.message}')
    # 调用redis保存验证码和手机号
    await redis.setex(sms_key, settings.SMS['expire'], sms_code)
    return success_response("短信发送成功")
