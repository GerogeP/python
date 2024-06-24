# -*- coding:utf-8 -*-
import os

import aioredis
from aioredis import Redis


async def get_redis() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    redis_pool = aioredis.ConnectionPool.from_url(
        f"redis://{os.getenv('CACHE_HOST', '127.0.0.1')}:{os.getenv('CACHE_PORT', 6379)}",
        db=os.getenv('CACHE_DB', 0),
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=redis_pool)
