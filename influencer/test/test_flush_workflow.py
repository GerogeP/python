import sys
sys.path.append("..")
from app.models.models import (
    Workflow as WorkflowModel,
    MsgStore as MsgStoreModel,
    InfluencerManualTag as InfluencerManualTagModel,
)
from datetime import datetime
from app.utils import workflow_manager
from app.utils.chat import send_to_influencer
import os, re

from dotenv import load_dotenv
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import asyncio

load_dotenv()

# 从环境变量中获取 DB URL
SQLALCHEMY_DATABASE_URL = os.getenv("PG_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, client_encoding="utf8")
SessionLocal = sessionmaker(autoflush=True, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        print("connect db")
        return db
    finally:
        print("disconnect db")
        db.close()


# 将数据库中所有状态为“已创建”的工作流转换为“待联系”，状态机会自动执行“生成触达需求信息”的函数
async def flush_wait_for_sent_workflow():
    db = get_db()
    db_workflow = (
        db.query(WorkflowModel)
        .with_for_update(nowait=True, of=WorkflowModel)
        .filter(WorkflowModel.state == "已创建", WorkflowModel.deleted_at == None)
        .all()
    )
    for work in db_workflow:
        if not isinstance(work.workflow_param_id, int) or work.workflow_param_id is None:
            continue
        old_state = work.state
        matter = workflow_manager.workflow_manager.get_fsm(db, work, fsm_path="../app/fsm_templates/")
        if matter:
            await matter.dispatch("生成触达需求")
            print("Update {}({}) from {} to {}".format(work.influencer_id, work.id, old_state, work.state))
            work.updated_at = datetime.now()
            db.rollback()
            workflow_manager.workflow_manager.remove_fsm(work.id)

async def flush_send_sample_info_workflow():
    db = get_db()
    db_workflow = (
        db.query(WorkflowModel)
        .with_for_update(nowait=True, of=WorkflowModel)
        .filter(WorkflowModel.state == "达人感兴趣", WorkflowModel.deleted_at == None)
        .all()
    )
    for work in db_workflow:
        if not isinstance(work.workflow_param_id, int) or work.workflow_param_id is None:
            continue
        old_state = work.state
        matter = workflow_manager.workflow_manager.get_fsm(db, work, fsm_path="../app/fsm_templates/")
        if matter:
            await matter.dispatch("生成样品邀请")
            print("Update {}({}) from 达人感兴趣 to {}".format(work.influencer_id, work.id, work.state))
            work.updated_at = datetime.now()
            db.rollback()
            workflow_manager.workflow_manager.remove_fsm(work.id)

async def flush_send_to_AI_workflow():
    db = get_db()
    db_workflow = (
        db.query(WorkflowModel)
        .with_for_update(nowait=True, of=WorkflowModel)
        .filter(WorkflowModel.state == "合作消息已发", WorkflowModel.deleted_at == None)
        .all()
    )
    for work in db_workflow:
        if not isinstance(work.workflow_param_id, int) or work.workflow_param_id is None:
            continue
        influencer = work.influencer
        print(work.influencer_id)
        old_state = work.state
        influencer_manual_tag = (
            db.query(InfluencerManualTagModel)
            .filter(
                InfluencerManualTagModel.influencer_id == work.influencer_id
            )
            .first()
        )
        msg_list = (
            db.query(MsgStoreModel)
            .with_for_update(nowait=True, of=MsgStoreModel)
            .filter(MsgStoreModel.influencer_id == work.influencer_id)
            .first()
        )
        print(msg_list)
        materials = """
        Material 1: Product-related information: {product_name}
        Material 2: The commission rate is {commission_rate}%
        """.format(product_name = work.work_flow_param.param["product_card"]["product_name"], commission_rate = work.work_flow_param.param["product_card"]["commission_rate"])
        dialog = []
        for msg in msg_list.msg_list:
            print(msg)
            if msg['type'] != "text" and not msg['processed']:
                continue
            text = "{} : {}".format(msg['account_type'], msg['content'])
            dialog.append(text)
            print(dialog)
        message = await send_to_influencer(
            influencer.param["name"],
            influencer_manual_tag.tags if influencer_manual_tag else [],
            materials,
            "\n".join(dialog),
        )
        print(message)
        matter = workflow_manager.workflow_manager.get_fsm(db, work, fsm_path="../app/fsm_templates/")
        if matter:
            if "Agree to collaborate" in message['intent_category'] or "Request for samples" in message['intent_category']:
                await matter.dispatch("达人感兴趣")
            elif "Request higher commission" in message['intent_category']:
                await matter.dispatch("人工/达人要求付费")
            elif "Specification request" in message['intent_category']:
                await matter.dispatch("人工/达人要求样品规格")
            else:
                await matter.dispatch("人工/达人无档期")
            print("Update {}({}) from {} to {}".format(work.influencer_id, work.id, old_state, work.state))
            work.updated_at = datetime.now()
            db.rollback()
            workflow_manager.workflow_manager.remove_fsm(work.id)
    # work = (
    #     db.query(WorkflowModel)
    #     .with_for_update(nowait=True, of=WorkflowModel)
    #     .filter(WorkflowModel.influencer_id == 302, WorkflowModel.deleted_at == None)
    #     .order_by(desc(WorkflowModel.updated_at))
    #     .first()
    # )
    # if not isinstance(work.workflow_param_id, int) or work.workflow_param_id is None:
    #     print("workflow_param is None")
    #     return
    # influencer = work.influencer
    # old_state = work.state
    # influencer_manual_tag = (
    #     db.query(InfluencerManualTagModel)
    #     .filter(
    #         InfluencerManualTagModel.influencer_id == work.influencer_id
    #     )
    #     .first()
    # )
    # msg_list = (
    #     db.query(MsgStoreModel)
    #     .with_for_update(nowait=True, of=MsgStoreModel)
    #     .filter(MsgStoreModel.influencer_id == work.influencer_id)
    #     .first()
    # )
    # materials = """
    # Material 1: Product-related information: {product_name}
    # Material 2: The commission rate is {commission_rate}%
    # """.format(product_name = work.work_flow_param.param["product_card"]["product_name"], commission_rate = work.work_flow_param.param["product_card"]["commission_rate"])
    # dialog = []
    # for msg in msg_list.msg_list:
    #     print(msg)
    #     if msg['type'] != "text" and not msg['processed']:
    #         continue
    #     text = "{} : {}".format(msg['account_type'], msg['content'])
    #     dialog.append(text)
    #     print(dialog)
    # message = await send_to_influencer(
    #     influencer.param["name"],
    #     influencer_manual_tag.tags if influencer_manual_tag else [],
    #     materials,
    #     "\n".join(dialog),
    # )
    # print(message)
    

if __name__ == '__main__':
    #asyncio.run(flush_wait_for_sent_workflow())
    #asyncio.run(flush_send_sample_info_workflow())
    asyncio.run(flush_send_to_AI_workflow())