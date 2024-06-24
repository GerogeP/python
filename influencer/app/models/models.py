# coding: utf-8
from typing import Optional
from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text, JSON,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    relationship,
    declarative_base,
    Mapped,
    mapped_column,
    declarative_mixin,
)

Base = declarative_base()
metadata = Base.metadata


@declarative_mixin
class TimestampedMixin:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)


class Influencer(Base, TimestampedMixin):
    __tablename__ = "influencers"
    __table_args__ = (UniqueConstraint("site_id", "influencer_account"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('influencers_id_seq'::regclass)"),
    )
    site_id = Column(String)
    influencer_account = Column(String, nullable=False)
    param = Column(JSONB(astext_type=Text()), default={}, nullable=False)
    current_workflow_id = Column(Integer)


class MsgTask(Base, TimestampedMixin):
    __tablename__ = "msg_tasks"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('msg_tasks_id_seq'::regclass)"),
    )
    task_type = Column(String, nullable=False)
    # affiliate_account = Column(String, nullable=False)
    affiliate_id = Column(Integer)
    influencer_id = Column(ForeignKey("influencers.id"), nullable=False)
    state = Column(String, nullable=False)
    error_msg = Column(String)
    msg_list = Column(JSONB(astext_type=Text()))
    workflow_id = Column(ForeignKey("workflows.id"))
    workflow_event = Column(String)

    influencer = relationship("Influencer")
    work_flow = relationship(
        "Workflow", primaryjoin="MsgTask.workflow_id == Workflow.id"
    )


class WorkflowParam(Base):
    __tablename__ = "workflow_params"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('workflow_params_id_seq'::regclass)"),
    )
    param = Column(JSONB(astext_type=Text()), nullable=False)


class Workflow(Base, TimestampedMixin):
    __tablename__ = "workflows"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('workflows_id_seq'::regclass)"),
    )
    template_id = Column(String, nullable=False)
    state = Column(String, nullable=False)
    event = Column(String)
    # affiliate_id = Column(String, nullable=False)
    # affiliate_account = Column(String, nullable=False)
    affiliate_id = Column(Integer)
    influencer_id = Column(ForeignKey("influencers.id"))
    op_id = Column(String, nullable=False)
    # task_id = Column(ForeignKey("msg_tasks.id"))
    workflow_param_id = Column(ForeignKey("workflow_params.id"))

    influencer = relationship("Influencer")
    # task = relationship("MsgTask", primaryjoin="Workflow.task_id == MsgTask.id")
    work_flow_param = relationship("WorkflowParam")


class InfluencerManualTag(Base, TimestampedMixin):
    __tablename__ = "influencer_manual_tags"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('influencer_manual_tags_id_seq'::regclass)"),
    )
    influencer_id = Column(ForeignKey("influencers.id"), unique=True)
    tags = Column(ARRAY(String(length=255)), nullable=False)
    affiliate_id = Column(Integer)
    influencer = relationship("Influencer", uselist=False)

class InfluencerAffiliateWorkflow(Base, TimestampedMixin):
    __tablename__ = "influencer_affiliate_workflow"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('influencer_affiliate_workflow_id_seq'::regclass)"),
    )
    influencer_id = Column(ForeignKey("influencers.id"), unique=True)
    affiliate_id = Column(String, nullable=False)
    affiliate_account = Column(String, nullable=False)
    current_workflow_id = Column(Integer)
    influencer = relationship("Influencer", uselist=False)

class InfluencerParamHistory(Base, TimestampedMixin):
    __tablename__ = "influencer_param_histories"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('influencer_param_histories_id_seq'::regclass)"),
    )
    influencer_id = Column(ForeignKey("influencers.id"))
    param = Column(JSONB(astext_type=Text()), nullable=False)

    influencer = relationship("Influencer")


class MsgStore(Base, TimestampedMixin):
    __tablename__ = "msg_store"
    __table_args__ = (UniqueConstraint("affiliate_account", "influencer_id"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('msg_store_id_seq'::regclass)"),
    )
    affiliate_account = Column(String)
    affiliate_id = Column(Integer)
    influencer_id = Column(ForeignKey("influencers.id"))
    msg_list = Column(JSONB(astext_type=Text()))
    msg_updated_at = Column(DateTime)

    influencer = relationship("Influencer", uselist=False)


class NewMsg(Base, TimestampedMixin):
    __tablename__ = "new_msgs"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('new_msgs_id_seq'::regclass)"),
    )
    msg_store_id = Column(ForeignKey("msg_store.id"))

    msg_store = relationship("MsgStore")
