from fastapi import FastAPI

from redis import asyncio as aioredis


def register_redis(app: FastAPI, config: dict):
    """
    注册Redis连接对象到App应用对象中
    :param app: App应用对象
    :param config: redis配置信息
    :return:
    """

    async def redis_pool():
        # Handle case when the username is empty
        redis_url = f"redis://{config.get('host')}:{config.get('port')}/{config.get('db')}"

        if config.get('username') and config.get('password'):
            redis_url = f"redis://{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('db')}"
        elif config.get('password'):
            redis_url = f"redis://:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('db')}"

        redis = await aioredis.from_url(redis_url, decode_responses=True)
        return redis

    @app.on_event("startup")  # startup事件：当App应用对象启动时，自动执行这里
    async def startup_event():
        app.state.redis = await redis_pool()
