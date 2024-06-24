import json
from app.models.models import (
    Workflow as WorkflowModel,
    MsgTask as MsgTaskModel,
    InfluencerManualTag as InfluencerManualTagModel,
    NewMsg as NewMsgModel,
    MsgStore as MsgStoreModel,
    Influencer as InfluencerModel,
)
from app.home.schemas.schemas import MsgTaskStates, Msg2Send, MsgTypes
from sqlalchemy.orm import Session
from tortoise.expressions import Q

from app.home.service.product_cards import ProductCardsService
from threading import RLock
from app.utils.chat import send_to_influencer
from app.utils.decide_intention import AI_to_determine
# from datetime import datetime

async def 判断达人合作意愿(self, msg: MsgStoreModel, influencer: InfluencerModel):
    result = await AI_to_determine(self.workflow, msg, influencer)
    self.db.commit()
        # match result:
        #     case 1 | 3:
        #         await self.dispatch("达人感兴趣")
        #     case 2:
        #         await self.dispatch("达人要求更高佣金")
        #     case 4:
        #         await self.dispatch("达人要求样品规格")
        #     case 6:
        #         await self.dispatch("达人无档期")
        #     case 9:
        #         await self.do_nothing()
        #     case _:
        #         await self.dispatch("人工处理")
    match result:
        case 1 | 3:
            await self.to_达人感兴趣()
        case 2:
            await self.to_达人要求更高佣金()
        case 4:
            await self.to_达人要求样品规格()
        case 6:
            await self.to_达人无档期()
        case 9:
            await self.do_nothing()
        case _:
            await self.to_人工处理()
        # return result

async def 生成触达需求消息(self):
    influencer = self.workflow.influencer
    influencer_manual_tag = (
        self.db.query(InfluencerManualTagModel)
        .filter(
            InfluencerManualTagModel.influencer_id == self.workflowinfluencer_id
        )
        .first()
    )
    materials = """
    Material 1: Product-related information: {product_name}
    Material 2: The commission rate is {commission_rate}%
    """
    product_cards_id = None
    if self.workflow.work_flow_param:
        product_cards_id = self.workflow.work_flow_param.param["product_card"]["product_card_id"]
        # print(self.workflow.work_flow_param.param['product_cards_id'])
        # model_service = ProductCardsService()
        # product = await model_service.get_id(product_cards_id)
        materials = materials.format(
            product_name=self.workflow.work_flow_param.param["product_card"][
            "product_name"
            ],
            commission_rate=self.workflow.work_flow_param.para["product_card"][
                "commission_rate"
            ],
        )

    message = await send_to_influencer(
        influencer.param["name"],
        influencer_manual_tag.tags if influencer_manual_tag else [],
        materials,
        "",
    )
    db_msg_task = MsgTaskModel(
        task_type="send",
        workflow_id=self.workflow.id,
        workflow_event="发送合作消息",
        msg_list=[
            Msg2Send(
                msg_id=1, type=MsgTypes.text, content=message["message"]
            ).model_dump(),
            Msg2Send(
                msg_id=2, type=MsgTypes.product_card, content=st(product_cards_id)
            ).model_dump(),
        ],
        affiliate_account=self.workflow.affiliate_account,
        influencer_id=self.workflow.influencer_id,
        state=MsgTaskStates.waiting,
    )
    self.db.add(db_msg_task)
    self.db.flush()
    self.db.refresh(db_msg_task)
    # self.workflow.task_id = db_msg_task.id

async def 生成样品邀请信息消息(self):
    print("生成定向（样品）信息")
    # Todo 生成message
    db_msg_task = MsgTaskModel(
        task_type="send",
        workflow_id=self.workflow.id,
        workflow_event="发送样品邀请",
        affiliate_account=self.workflow.affiliate_account,
        influencer_id=self.workflow.influencer_id,
        state=MsgTaskStates.waiting,
        msg_list=[
            Msg2Send(
                msg_id=1, type=MsgTypes.text, content="Welcome to apply asample!"
            ).model_dump()
        ],
    )
    self.db.add(db_msg_task)
    self.db.flush()
    self.db.refresh(db_msg_task)
    # self.workflow.task_id = db_msg_task.id