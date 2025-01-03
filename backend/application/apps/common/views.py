import os
from fastapi import APIRouter, HTTPException

app = APIRouter()


@app.get('/api')
async def api() -> dict:
    """
    测试接口
    :return:
    """
    return {'title': f'{os.environ.get("APP_NAME")}测试接口'}


@app.get('/exception')
async def exception(name: str) -> dict:
    """
    测试异常的接口
    :param name:
    :return:
    """
    try:
        print(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'title': 'exception'}
