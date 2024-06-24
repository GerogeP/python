# coding:utf-8
from sqlalchemy import Column, Integer, text, String, Text, UniqueConstraint, Numeric, SmallInteger, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from app.dependencies.databases import Base, TimestampedMixin

__all__ = [
    'ProductCards',
]


class ProductCards(Base, TimestampedMixin):
    """商品卡表"""
    __tablename__ = "product_cards"
    __table_args__ = (UniqueConstraint("site_id", "product_card_id"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('product_cards_id_seq'::regclass)"),
    )
    site_id = Column(String(32), nullable=False, default='', doc='站点来源（tiktok, ins）')
    product_card_id = Column(String(100), nullable=False, default='', doc='商品卡ID')
    product_name = Column(String(500), nullable=False, default='', doc='产品名称，可能较长，类似淘宝')
    params = Column(JSONB(astext_type=Text()), nullable=False, default={}, doc='形参，如果有的话 JSON')
    commission_rate = Column(Numeric, nullable=False, default=0, doc='佣金比例，例如20，就是20%')
    deleted_at = Column(DateTime, default=None, doc='删除时间')
