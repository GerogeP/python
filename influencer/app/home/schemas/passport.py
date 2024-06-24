# coding:utf-8
from datetime import datetime

from pydantic import BaseModel, Field


class AccountLogin(BaseModel):
    username: str = Field(..., description="用户名", example="admin")
    password: str = Field(..., description="密码", example="123456")


class JWTOut(BaseModel):
    access_token: str
    username: str


class JWTPayload(BaseModel):
    user_id: int
    username: str
    is_superuser: bool
    exp: datetime
