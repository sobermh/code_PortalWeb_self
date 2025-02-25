import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.exceptions import HTTPException, RequestValidationError

from .core import middleware, settings
from .apps.common.views import app as common_app
from .apps.users.views import router as users_router
from .database import redis
from .utils import exception_tool


def create_app() -> FastAPI:
    """创建web应用对象"""

    app = FastAPI(
        title=os.environ.get('APP_NAME'),
        summary=os.environ.get('APP_SUMMARY'),
        description=os.environ.get('APP_DESCRIPTION'),
        version=os.environ.get('APP_VERSION'),
        # 注册全局异常处理函数
        exception_handlers={
            HTTPException: exception_tool.global_http_exception_handler,
            RequestValidationError: exception_tool.global_request_exception_handler,
        }
    )

    # 把Tortoise-orm注册到App应用对象中
    register_tortoise(
        app,
        config=settings.TORTOISE_ORM,
        generate_schemas=False,  # 是否自动生成表结构
        add_exception_handlers=True,  # 是否启用自动异常处理
    )

    # redis连接对象注册到App应用对象中
    redis.register_redis(
        app,
        config=settings.REDIS,
    )

    # 注册各个应用分组下的路由信息，合并到App应用对象
    app.include_router(common_app, prefix='')
    app.include_router(users_router, prefix='/users')

    # 注册中间件函数
    http_middleware = app.middleware('http')
    http_middleware(middleware.log_requests)

    return app

