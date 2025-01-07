from fastapi import status


def base_response(code, msg, data):
    """
    基础返回格式
    :param code: 状态码
    :param msg: 提示信息
    :param data: 返回数据
    :return:
    """
    result = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return result


def success_response(data, msg='success', code=status.HTTP_200_OK):
    """
    成功返回格式
    :param data: 返回数据
    :param msg: 提示信息
    :param code: 状态码
    :return:
    """
    return base_response(code, msg, data)


def fail_response(msg, data=None, code=status.HTTP_400_BAD_REQUEST):
    """
    失败返回格式
    :param msg: 提示信息
    :param data: 返回数据
    :param code: 状态码
    :return:
    """
    return base_response(code, msg, data)
