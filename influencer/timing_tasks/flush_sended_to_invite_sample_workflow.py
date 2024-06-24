import sys
sys.path.append("/www/wwwroot/influencer-mgr-be")
from app.models.models import (
    Workflow as WorkflowModel
)
from datetime import datetime
from app.utils import workflow_manager
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
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


# 将数据库中所有状态为“达人感兴趣”的工作流转换为“样品邀请待发送”，状态机会自动执行“生成触达需求信息”的函数
# 现阶段默认达人都感兴趣，后续数据能支撑交给AI判断达人是否感兴趣后再完善流程
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
        #old_state = work.state
        matter = workflow_manager.workflow_manager.get_fsm(db, work, fsm_path="/www/wwwroot/influencer-mgr-be/app/fsm_templates/")
        if matter:
            await matter.dispatch("生成样品邀请")
            #print("Update {}({}) from {} to {}, task id is {}".format(work.influencer_id, work.id, old_state, work.state, work.task_id))
            work.updated_at = datetime.now()
            db.commit()
            db.refresh(work)
            workflow_manager.workflow_manager.remove_fsm(work.id)

if __name__ == '__main__':
    asyncio.run(flush_send_sample_info_workflow())