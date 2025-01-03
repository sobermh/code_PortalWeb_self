from fastapi import status


def base_response(code, msg, data=None):
    """
    基础返回格式
    :param code: 状态码
    :param msg: 提示信息
    :param data: 返回数据
    :return:
    """
    if data is None:
        data = []
    result = {
        "code": code,
        "message": msg,
        "data": data
    }
    return result


def success_response(data=None, msg=''):
    """
    成功返回格式
    :param data: 返回数据
    :param msg: 提示信息
    :return:
    """
    return base_response(200, msg, data)


def fail_response(data, code=status.HTTP_400_BAD_REQUEST, msg='fail'):
    """
    失败返回格式
    :param code: 状态码
    :param msg: 提示信息
    :param data: 返回数据
    :return:
    """
    return base_response(code, msg, data)
