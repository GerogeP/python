from datetime import date, datetime
from typing import Union, Optional

from fastapi import Query
from pydantic import BaseModel, Field, constr


class UserListIn(BaseModel):
    """用户列表参数"""
    page: int = Query(1, ge=1, alias="pageNo", description="页码")
    limit: int = Query(20, ge=1, le=100, alias="pageSize", description="每页显示的记录数")
    keyword: Optional[Union[str, int, None]] = Query(None, description="搜索关键词")  # 搜索关键词
    status: Optional[Union[str, int, None]] = Query(None, description="账号状态")
    start_time: Optional[str] = Query(None, alias='startTime', description="开始时间")  # 搜索关键词
    end_time: Optional[str] = Query(None, alias='endTime', description="结束时间")  # 搜索关键词


class UserDetailIn(BaseModel):
    """用户列表参数"""
    id: int = Query(gt=0)


class UserID(BaseModel):
    """用户ID"""
    id: int


class UserEditIn(BaseModel):
    id: int
    username: constr(min_length=4, max_length=32)
    nickname: constr(min_length=4, max_length=32)
    password: Optional[str] = None
    status: Optional[int]


class UserCreateIn(BaseModel):
    """
    创建用户
    """
    username: constr(min_length=4, max_length=32)
    nickname: constr(min_length=4, max_length=32)
    password: str
    # email: str
    # mobile: int
    status: int


class UserDBOut(BaseModel):
    """
    用户信息DB输出
    """
    id: int  # 主键
    username: str
    mobile: str
    email: str
    nickname: str
    avatar: Union[str, None] = None
    gender: int
    intro: Union[str, None] = None
    status: int
    is_delete: int
    create_time: datetime
    update_time: datetime
