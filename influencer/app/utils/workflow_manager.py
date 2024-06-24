import json
from transitions import EventData
from transitions.extensions.asyncio import AsyncMachine
from app.models.models import (
    Workflow as WorkflowModel,
    MsgTask as MsgTaskModel,
    InfluencerManualTag as InfluencerManualTagModel,
    NewMsg as NewMsgModel,
    MsgStore as MsgStoreModel,
    Influencer as InfluencerModel,
)
from app.models.promotion import (
    PromotionTasks as PromotionTasksModel,
    PromotionTaskWorkflow as PromotionTaskWorkflowModel,
)
from app.home.schemas.schemas import MsgTaskStates, Msg2Send, MsgTypes
from sqlalchemy.orm import Session
from sqlalchemy import func

from threading import RLock
from app.utils.chat import send_to_influencer
from app.utils.decide_intention import AI_to_determine

TEMPLATE_PATH = "app/fsm_templates/"


class Matter(AsyncMachine):
    def __init__(
        self, db: Session, workflow: WorkflowModel, fsm_path="app/fsm_templates/"
    ) -> None:
        self.workflow = workflow
        self.db = db
        template_id = self.workflow.template_id
        with open(f"{fsm_path}{template_id}.json", encoding="utf-8") as f:
            template = json.load(f)
        AsyncMachine.__init__(
            self,
            states=template["states"],
            transitions=template["transitions"],
            initial=self.workflow.state,
            after_state_change=self.save_state,
            send_event=True,
        )

    async def save_state(self, event: EventData):
        self.workflow.state = self.state
        self.workflow.event = event.event.name

    async def do_nothing(self):
        pass

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

    async def 生成触达需求消息(self, event: EventData):
        influencer = self.workflow.influencer
        # influencer_manual_tag = (
        #     self.db.query(InfluencerManualTagModel)
        #     .filter(
        #         InfluencerManualTagModel.influencer_id == self.workflow.influencer_id
        #     )
        #     .first()
        # )
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
                commission_rate=self.workflow.work_flow_param.param["product_card"][
                    "commission_rate"
                ],
            )

        message = await send_to_influencer(
            influencer.param["name"],
            #influencer_manual_tag.tags if influencer_manual_tag else [],
            influencer.param.get("tags", ""),
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
                    msg_id=2, type=MsgTypes.product_card, content=str(product_cards_id)
                ).model_dump(),
            ],
            affiliate_id=self.workflow.affiliate_id,
            influencer_id=self.workflow.influencer_id,
            state=MsgTaskStates.waiting,
        )
        self.db.add(db_msg_task)
        self.db.flush()
        self.db.refresh(db_msg_task)
        # self.workflow.task_id = db_msg_task.id

    async def 生成样品邀请信息消息(self, event: EventData):
        print("生成定向（样品）信息")
        # Todo 生成message
        db_msg_task = MsgTaskModel(
            task_type="send",
            workflow_id=self.workflow.id,
            workflow_event="发送样品邀请",
            affiliate_id=self.workflow.affiliate_id,
            influencer_id=self.workflow.influencer_id,
            state=MsgTaskStates.waiting,
            msg_list=[
                Msg2Send(
                    msg_id=1, 
                    type=MsgTypes.text, 
                    content="Welcome to apply a sample!"
                ).model_dump()
            ],
        )
        self.db.add(db_msg_task)
        self.db.flush()
        self.db.refresh(db_msg_task)
        # self.workflow.task_id = db_msg_task.id

class WorkflowManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WorkflowManager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.queue = []
        self.lock = RLock()

    def get_fsm(
        self, db: Session, workflow: WorkflowModel, fsm_path="app/fsm_templates/"
    ) -> Matter:
        with self.lock:
            if workflow.id in self.queue:
                return None
            else:
                self.queue.append(workflow.id)
                return Matter(db, workflow, fsm_path=fsm_path)

    def remove_fsm(self, workflow_id: int):
        with self.lock:
            self.queue.remove(workflow_id)


workflow_manager = WorkflowManager()
