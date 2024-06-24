# coding:utf-8
from sqlalchemy import Integer, Column, String, SmallInteger, DateTime

from app.dependencies.databases import Base, TimestampedMixin

__all__ = [
    'PromotionTasks',
    'PromotionTaskWorkflow'
]


class PromotionTasks(Base, TimestampedMixin):
    """推广任务表"""
    __tablename__ = 'promotion_tasks'  # 表名
    # 如果需要添加额外的表属性，可以使用 __table_args__ 属性
    __table_args__ = {'comment': '推广任务表'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, doc='主键')
    site_id = Column(String(32), nullable=False, default='', doc='站点来源（tiktok, ins）')
    title = Column(String(100), nullable=False, default='', doc='任务名称')
    description = Column(String(200), nullable=True, default='', doc='任务描述')
    product_card_id = Column(Integer, nullable=False, doc='产品卡ID')
    deleted_at = Column(DateTime, default=None, doc='删除时间')


# 任务一对多工作流，每个达人一个工作流，一次任务多选达人
class PromotionTaskWorkflow(Base, TimestampedMixin):
    """任务工作流关联表"""
    __tablename__ = 'promotion_task_workflow'  # 表名
    # 如果需要添加额外的表属性，可以使用 __table_args__ 属性
    __table_args__ = {'comment': '任务工作流关联表'}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, doc='主键')
    promotion_task_id = Column(Integer, nullable=True, doc='任务ID')
    workflow_id = Column(Integer, nullable=True, doc='工作流ID')
    influencer_id = Column(Integer, nullable=True, doc='达人ID')
    affiliate_id = Column(Integer, nullable=True, doc='机构ID')
    status = Column(Integer, default=0, doc='任务状态')
    deleted_at = Column(DateTime, default=None, doc='删除时间')
