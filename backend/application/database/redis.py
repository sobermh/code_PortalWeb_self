
from fastapi import FastAPI

from redis import asyncio as aioredis
from contextlib import asynccontextmanager


def register_redis(app: FastAPI, config: dict):
    """
    注册Redis连接对象到App应用对象中
    :param app: App应用对象
    :param config: redis配置信息
    :return:
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # 构造 Redis URL
        redis_url = f"redis://{config.get('host')}:{config.get('port')}/{config.get('db')}"
        if config.get('username') and config.get('password'):
            redis_url = f"redis://{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('db')}"
        elif config.get('password'):
            redis_url = f"redis://:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('db')}"

        # 创建 Redis 连接池
        redis = await aioredis.from_url(redis_url, decode_responses=True)
        app.state.redis = redis  # 保存到 app.state 中
        print("Redis 已连接")  # 方便调试

        try:
            yield  # 进入 lifespan 生命周期
        finally:
            # 关闭 Redis 连接池
            await redis.close()
            print("Redis 连接已关闭")  # 方便调试

    # 设置 lifespan 事件处理器
    app.router.lifespan_context = lifespan
