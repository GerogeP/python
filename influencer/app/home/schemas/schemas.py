from datetime import datetime
import enum
from pydantic import BaseModel, Field
from typing import List, Optional, Union


class MsgTypes(str, enum.Enum):
    text = "text"
    product_card = "product_card"
    invitation_card = "invitation_card"
    image = "image"


class TaskTypes(str, enum.Enum):
    send = "send"  # 消息发送
    pull = "pull"  # 消息拉取


# 工作流模型
class Workflow(BaseModel):
    affiliate_id: Union[str, int]
    affiliate_account: str
    influencer_id: Union[str, int]
    template_id: str
    state: str
    event: Optional[str]
    op_id: Union[str, int]
    # task_id: Optional[int] = Field(None)
    workflow_param_id: Optional[int] = Field(None)
    param: Optional[dict] = Field(None)  # 商品 { product_cards_id: "" }


class WorkflowParam(BaseModel):
    param: dict


class MsgTaskStates(str, enum.Enum):
    waiting = "waiting"
    sent = "sent"
    in_store = "in_store"
    failed = "failed"

class Msg2Send(BaseModel):
    msg_id: Optional[int] = Field(None)
    type: MsgTypes
    content: Optional[str] = Field(None)
    product_id: Optional[str] = Field(None)
    valid_until: Optional[str] = Field(None)
    commission_rate: Optional[str] = Field(None)
    invitation_name: Optional[str] = Field(None)

# 消息发送任务模型
class MsgTask(BaseModel):
    task_type: TaskTypes
    affiliate_id: Optional[int] = Field(None)
    affiliate_account: Optional[str] = Field(None)
    influencer_id: int
    state: MsgTaskStates = MsgTaskStates.waiting
    error_msg: Optional[str] = Field(None)
    msg_list: List[Msg2Send]
    workflow_id: Optional[int] = Field(None)
    workflow_event: Optional[str] = Field(None)


class Msg(BaseModel):
    type: str
    message: str
    chat_time: str
    account: str
    processed: Optional[bool] = Field(False)


class Dialog(BaseModel):
    affiliate_account: str
    influencer_account: str
    timeZone: Optional[str] = Field(None)
    site_id: str
    dialogs: List[Msg]
    reversed: int = 0


class AccountTypes(str, enum.Enum):
    influencer = "influencer"
    affiliate = "affiliate"


class MsgInDB(BaseModel):
    direction: str
    account_type: AccountTypes
    type: MsgTypes
    content: str
    chat_time: str
    processed: bool


# 消息存储模型
class MsgStore(BaseModel):
    affiliate_account: str
    influencer_id: int
    msg_list: Optional[List[MsgInDB | Msg]] = Field(None)
    msg_updated_at: Optional[datetime] = Field(None)


# 查询对话详情
class MsgDetailIn(BaseModel):
    site_id: Optional[str] = Field('tiktok')
    affiliate_id: Union[int, str]
    influencer_id: Union[int, str]


class MsgStoreDbOut(BaseModel):
    id: int
    influencer_id: int
    affiliate_account: str
    msg_list: Optional[List[MsgInDB | Msg]] = Field(None)
    msg_updated_at: Optional[datetime] = Field(None)


class NewMsg(BaseModel):
    msg_store_id: int


# 达人信息模型
class Influencer(BaseModel):
    site_id: str
    influencer_account: str
    param: Optional[dict]


# 达人标签模型
class InfluencerTag(BaseModel):
    influencer_id: int
    tags: list[str]


class TimeModel(BaseModel):
    created_at: Optional[datetime] = Field(None)
    updated_at: Optional[datetime] = Field(None)
    deleted_at: Optional[datetime] = Field(None)


class IdModel(BaseModel):
    id: int


class WorkFlowResponse(IdModel, TimeModel, Workflow):
    pass


class MsgTaskResponse(IdModel, TimeModel, MsgTask):
    site_id: Optional[str] = Field(None)
    influencer_account: Optional[str] = Field(None)


class MsgStoreResponse(IdModel, TimeModel, MsgStore):
    pass


class InfluencerResponse(IdModel, TimeModel, Influencer):
    pass


class InfluencerTagResponse(IdModel, TimeModel, InfluencerTag):
    pass


class OutboxMsgs(BaseModel):
    affiliate_account: str
    site_id: str
    influencer_account: str
    msgs: List[Msg2Send]
