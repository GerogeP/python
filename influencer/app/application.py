# coding:utf-8
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .config.settings import settings
from .core import events, middleware
from app.home.routers import home_router
from app import test_router


# 注册事件
def register_event(app: FastAPI):
    app.add_event_handler("startup", events.startup(app))
    app.add_event_handler("shutdown", events.stopping(app))


# 注册中间件
def register_middleware(app: FastAPI):
    app.add_middleware(middleware.BaseMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )


# 路由聚合
def register_router(app: FastAPI):
    # 业务路由
    app.include_router(home_router)
    # Test
    app.include_router(test_router.router)

# 注册静态资源目录


def register_static(app: FastAPI):
    """配置静态资源"""
    from app.config.settings import settings
    # 静态资源路径配置
    app.mount('/', StaticFiles(directory=settings.STATIC_DIR), name="static")
    print(settings.STATIC_DIR)
    # 创建上传路径
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
    # 配置上传路径
    app.mount('/', StaticFiles(directory=settings.UPLOAD_DIR), name='upload')


def create_app() -> FastAPI:
    """创建FastAPI后台应用,并初始化"""
    from app.exceptions.global_exc import configure_exception

    app = FastAPI()
    # 注册路由
    register_router(app)
    # 异常处理
    configure_exception(app)
    # 注册钩子函数
    register_event(app)
    # 注册中间件
    register_middleware(app)
    # 挂载文件夹
    register_static(app)

    return app
