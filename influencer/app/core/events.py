# coding:utf-8
# -*- coding:utf-8 -*-
"""
fastapi事件监听
"""

from typing import Callable
from fastapi import FastAPI
# from aioredis import Redis
# from app.dependencies.mysql import register_mysql, close_mysql
# from app.dependencies.redis import get_redis


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """
    async def app_start() -> None:
        # APP启动完成后触发
        print("FastAPI 已启动")
        # 注册数据库
        # await register_mysql(app)
        # 注入缓存到app state
        # app.state.redis = await get_redis()

        pass
    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """
    async def stop_app() -> None:
        # APP停止时触发
        print("FastAPI 已停止")
        # cache: Redis = await app.state.redis
        # await cache.close()
        # 关闭数据库链接
        # await close_mysql()

    return stop_app
