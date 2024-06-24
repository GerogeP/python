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
        #old_state = work.state
        matter = workflow_manager.workflow_manager.get_fsm(db, work, fsm_path="/www/wwwroot/influencer-mgr-be/app/fsm_templates/")
        if matter:
            await matter.dispatch("生成触达需求")
            #print("Update {}({}) from {} to {}, task id is {}".format(work.influencer_id, work.id, old_state, work.state, work.task_id))
            work.updated_at = datetime.now()
            db.commit()
            db.refresh(work)
            workflow_manager.workflow_manager.remove_fsm(work.id)

if __name__ == '__main__':
    asyncio.run(flush_wait_for_sent_workflow())