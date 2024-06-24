import sys
sys.path.append("/www/wwwroot/influencer-mgr-be")
from app.models.models import (
    Workflow as WorkflowModel,
    MsgStore as MsgStoreModel,
    Influencer as InfluencerModel,
    NewMsg as NewMsgModel,
    InfluencerAffiliateWorkflow as InfluencerAffiliateWorkflowModel,
)
from datetime import datetime
from app.utils import workflow_manager
from app.utils.chat import send_to_influencer
from app.models.affiliate import Affiliate as AffiliateModel
import os, json

from dotenv import load_dotenv
from sqlalchemy import create_engine, desc, distinct
from sqlalchemy.orm import sessionmaker, attributes
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


# 将从new_msg表中查新消息，下一个阶段由AI判断意图，状态机会自动执行AI判断的函数
async def flush_send_to_AI_workflow():
    db = get_db()
    # 多条new_msg的情况下只需要处理最后一条
    msg_store_ids = (
        db.query(distinct(NewMsgModel.msg_store_id))
        .all()
    )
    for msg_store_id in msg_store_ids:
        new_msgs = (
                db.query(NewMsgModel)
                .order_by(desc(NewMsgModel.id))
                .filter(
                    NewMsgModel.msg_store_id == msg_store_id[0],
                    NewMsgModel.deleted_at == None,
                )
                .all()
            )
        # fix: 根据msg_store_id做区分
        if len(new_msgs) == 0:
            continue
        new_msg = new_msgs[0]
        msg_store = (
            db.query(MsgStoreModel)
            .filter(
                MsgStoreModel.id == new_msg.msg_store_id
            )
            .first()
        )
        influencer = (
            db.query(InfluencerModel)
            .filter(
                InfluencerModel.id == msg_store.influencer_id
            )
            .first()
        )
        # 由于 influencer 现在有新增的字段 current_workflow_id， 所以直接查询这个字段
        if msg_store.affiliate_id is None:
            continue
        db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.id == msg_store.affiliate_id).first()
        db_current_workflow = (
            db.query(InfluencerAffiliateWorkflowModel)
            .filter(InfluencerAffiliateWorkflowModel.influencer_id == msg_store.influencer_id,
                    InfluencerAffiliateWorkflowModel.affiliate_id == db_affiliate.id, 
                    InfluencerAffiliateWorkflowModel.deleted_at == None)
            .order_by(desc(InfluencerAffiliateWorkflowModel.id))
            .first()
        )
        db_workflow = (
            db.query(WorkflowModel)
            .with_for_update(nowait=True, of=WorkflowModel)
            .filter(WorkflowModel.influencer_id == msg_store.influencer_id,
                    WorkflowModel.id == db_current_workflow.current_workflow_id, 
                    WorkflowModel.deleted_at == None)
            .first()
        )
        try:
            matter = workflow_manager.workflow_manager.get_fsm(db, db_workflow, fsm_path="/www/wwwroot/influencer-mgr-be/app/fsm_templates/")
            old_state = matter.workflow.state
            if matter:
                await matter.判断达人合作意愿(msg = msg_store, influencer = influencer)
                if old_state != matter.workflow.state:
                    for msg in msg_store.msg_list:
                        msg["processed"] = True
                    attributes.flag_modified(msg_store, "msg_list")
                    #print("Update {}({}) from {} to {}, task id is {}".format(db_workflow.influencer_id, db_workflow.id, old_state, db_workflow.state, db_workflow.task_id))
                    db_workflow.event = "达人回复"
                    db_workflow.updated_at = datetime.now()
                # 在收到达人回复的最后一条之前的new_msg都标记为已处理并软删除
                for msg in new_msgs:
                    msg.deleted_at = datetime.now()
                db.commit()
                workflow_manager.workflow_manager.remove_fsm(db_workflow.id)
            else:
                return
        except Exception as e:
            db.rollback()
            print(e)


if __name__ == '__main__':
    asyncio.run(flush_send_to_AI_workflow())