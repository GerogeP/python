# coding:utf-8
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Boolean, func
from app.models.models import Base

__all__ = ['Users']


class Users(Base):
    """用户实体"""

    __tablename__ = 'users'  # 表名
    # 如果需要添加额外的表属性，可以使用 __table_args__ 属性
    __table_args__ = {'comment': '用户表'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, doc='主键')
    username = Column(String(32), nullable=False, default='', doc='用户名')
    password = Column(String(100), nullable=False, default='', doc='用户密码')
    mobile = Column(String(20), nullable=False, default='', doc='电话')
    email = Column(String(50), nullable=False, default='', doc='邮箱')
    nickname = Column(String(32), nullable=False, default='', doc='用户昵称')
    avatar = Column(String(200), nullable=False, default='', doc='头像')
    gender = Column(SmallInteger, nullable=False, default=0, doc='用户性别: [0=保密, 1=男, 2=女]')
    intro = Column(String(200), nullable=False, default='', doc='简介')
    status = Column(SmallInteger, nullable=False, default=1, doc='状态: [0=停用, 1=正常]')
    is_delete = Column(SmallInteger, default=0, doc='是否删除: [0=正常, 1=删除]')
    create_time = Column(DateTime, default=func.now(), doc='创建时间')
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), doc='更新时间')
