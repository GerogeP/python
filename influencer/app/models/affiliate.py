# coding:utf-8
from sqlalchemy import Column, Integer, text, String, UniqueConstraint, DateTime

from app.dependencies.databases import Base, TimestampedMixin

__all__ = [
    'Affiliate',
]


class Affiliate(Base, TimestampedMixin):
    """机构管理表"""
    __tablename__ = "affiliates"
    __table_args__ = (UniqueConstraint("site_id", "affiliate_account"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('affiliates_id_seq'::regclass)"),
    )
    site_id = Column(String(32), nullable=False, default='', doc='站点来源（tiktok, ins）')
    affiliate_account = Column(String(100), nullable=False, doc='机构账号')
    nickname = Column(String(500), nullable=False, default='', doc='帐号昵称')
    home_page = Column(String(500), nullable=False, default='', doc='帐号主页')
    deleted_at = Column(DateTime, default=None, doc='删除时间')
