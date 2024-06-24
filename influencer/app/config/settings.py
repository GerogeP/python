# -*- coding:utf-8 -*-

import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)
    # 调试模式
    APP_DEBUG: bool = True
    # 项目信息
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "FastAPI Starter"
    DESCRIPTION: str = '<a href="/redoc" target="_blank">redoc</a>'
    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    TEMPLATE_DIR: str = os.path.join(STATIC_DIR, "templates")
    # 上传路径URL前缀
    upload_prefix: str = '/api/uploads'
    # 上传文件路径
    UPLOAD_DIR: str = os.path.join(STATIC_DIR, "uploads")
    # 上传图片限制
    UPLOAD_IMAGE_SIZE: int = 1024 * 1024 * 10
    # 上传图片扩展 10
    UPLOAD_IMAGE_EXT: list = ['png', 'jpg', 'jpeg', 'gif', 'ico', 'bmp']
    # 上传音频限制
    UPLOAD_AUDIO_SIZE: int = 1024 * 1024 * 30
    # 上传音频扩展 20
    UPLOAD_AUDIO_EXT: list = ['mp3', 'wma', 'wav', 'ape', 'flac', 'ogg', 'acc']
    # 上传视频限制
    UPLOAD_VIDEO_SIZE: int = 1024 * 1024 * 30
    # 上传视频扩展 30
    UPLOAD_VIDEO_EXT: list = ['mp4', 'avi', 'flv', 'rmvb', 'mov', 'mkv']
    # 上传文件限制
    UPLOAD_FILE_SIZE: int = 1024 * 1024 * 30
    # 上传文件扩展 40
    UPLOAD_FILE_EXT: list = ['txt', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'rar', 'zip', '7z', 'tar', 'gz']

    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]
    # Session
    # SECRET_KEY = "session"
    # SESSION_COOKIE = "session_id"
    # SESSION_MAX_AGE = 14 * 24 * 60 * 60
    # Jwt
    JWT_SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60

    SWAGGER_UI_OAUTH2_REDIRECT_URL: str = "/api/v1/test/oath2"

    # 系统加密字符
    SECRET: str = 'UVTIyzCy'
    # 二维码过期时间
    QRCODE_EXPIRE: int = 60 * 1
    # 时区
    timezone: str = 'America/Los_Angeles'
    # 日期时间格式
    datetime_fmt: str = '%Y-%m-%d %H:%M:%S'
    # 当前域名
    domain: str = 'http://127.0.0.1:6006'


settings = Settings()
