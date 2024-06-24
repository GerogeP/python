# coding:utf-8

from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Boolean, func
from app.models.models import Base

__all__ = [
    'Upload',
    'UploadFolder',
]


class Upload(Base):
    """上传实体"""
    __tablename__ = 'upload'  # 表名
    # 如果需要添加额外的表属性，可以使用 __table_args__ 属性
    __table_args__ = {'comment': '上传文件'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, doc='主键')
    folder_id = Column(Integer, nullable=False, default=0, doc='分类ID')
    channel = Column(SmallInteger, nullable=False, default=0, doc='上传来源（1 管理后台 2 Web端）')
    uid = Column(Integer, nullable=False, default=0, doc='用户ID')
    storage = Column(String(20), nullable=False, default='local', doc='存储方式')
    file_type = Column(Integer, nullable=False, default=0, doc='文件类型: [10=图片, 20=视频，30=音频，40=文件]')
    name = Column(String(100), nullable=False, default='', doc='文件名称')
    url = Column(String(200), nullable=False, default='', doc='文件路径')
    ext = Column(String(10), nullable=False, default='', doc='文件扩展')
    size = Column(Integer, nullable=False, default=0, doc='文件大小')
    is_delete = Column(SmallInteger, default=0, doc='是否删除: [0=正常, 1=删除]')
    create_time = Column(DateTime, default=func.now(), doc='创建时间')
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), doc='更新时间')


class UploadFolder(Base):
    """上传文件分组实体"""
    __tablename__ = 'upload_folder'  # 表名
    # 如果需要添加额外的表属性，可以使用 __table_args__ 属性
    __table_args__ = {'comment': '文件目录分组'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, doc='主键')
    pid = Column(Integer, nullable=False, default=0, doc='上级ID')
    name = Column(String(100), nullable=False, default='', doc='名称')
    sort = Column(SmallInteger, nullable=False, default=10, doc='排序')
    is_delete = Column(SmallInteger, default=0, doc='是否删除: [0=正常, 1=删除]')
    create_time = Column(DateTime, default=func.now(), doc='创建时间')
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), doc='更新时间')
