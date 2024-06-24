from typing import Optional, List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from datetime import datetime
from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.core.response import unify_response
from app.home.routers.workflow import fire_workflow_event, update_workflow_state
from app.home.schemas import schemas
from app.models.models import MsgTask as MsgTaskModel, Influencer as InfluencerModel, Workflow as WorkflowModel
from app.models.affiliate import Affiliate as AffiliateModel
from app.dependencies.databases import get_db

msg_task_router = APIRouter(prefix="/msg_tasks")


# 查看消息发送任务
@msg_task_router.get("/{task_id}", response_model=schemas.MsgTaskResponse)
async def get_msg_task(task_id: int = Path(...), db: Session = Depends(get_db)):
    db_msg_task = db.query(MsgTaskModel).filter(MsgTaskModel.id == task_id).first()
    if db_msg_task:
        return db_msg_task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MsgTask not found"
        )


# 创建消息发送任务
@msg_task_router.post("/", response_model=schemas.MsgTaskResponse)
async def create_msg_task(msg_task: schemas.MsgTask, db: Session = Depends(get_db)):
    db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.id == msg_task.affiliate_id).first()
    msg_task.affiliate_id = db_affiliate.id
    db_msg_task = MsgTaskModel(**msg_task.model_dump())
    db_msg_task.state = "waiting"
    db_workflow = db.query(WorkflowModel).filter(WorkflowModel.id == db_msg_task.workflow_id).first()
    db.add(db_msg_task)
    db.commit()
    db.refresh(db_msg_task)
    # 后台人工处理后更新workflow
    db_workflow.state = "已人工处理"
    db_workflow.event = "人工处理"
    # db_workflow.task_id = db_msg_task.id
    db.commit()
    return db_msg_task


# 更新消息发送任务
@msg_task_router.put("/{task_id}", response_model=schemas.MsgTaskResponse)
async def update_msg_task(
    task_id: int = Path(...),
    msg_task: schemas.MsgTask = Body(...),
    db: Session = Depends(get_db),
):
    db_msg_task = db.query(MsgTaskModel).filter(MsgTaskModel.id == task_id).first()
    db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.affiliate_account == msg_task.affiliate_account).first()
    if db_msg_task:
        db_msg_task.task_type = msg_task.task_type
        db_msg_task.affiliate_id = db_affiliate.id
        db_msg_task.influencer_id = msg_task.influencer_id
        db_msg_task.state = msg_task.state
        db_msg_task.msg_list = msg_task.msg_list
        db_msg_task.workflow_id = msg_task.workflow_id
        db_msg_task.workflow_event = msg_task.workflow_event
        db_msg_task.updated_at = datetime.now()
        db.commit()
        db.refresh(db_msg_task)
        return db_msg_task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MsgTask not found"
        )


# 获取消息发送任务列表 response_model=List[schemas.MsgTaskResponse]
@msg_task_router.get("")
@unify_response
async def get_msg_task_list(
    task_type: Optional[schemas.TaskTypes] = Query(None),
    state: Optional[schemas.MsgTaskStates] = Query(None),
    affiliate_account: Optional[str] = Query(None),
    influencer_account: Optional[str] = Query(None),
    site_id: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    # fix: 在没有输入 influencer_account 的情况下，需要按 influencer.id 排序
    influencer = None
    if influencer_account:
        influencer = (
            db.query(InfluencerModel)
            .filter(
                InfluencerModel.influencer_account == influencer_account,
                InfluencerModel.site_id == site_id,
            )
            .first()
        )
    # 返回的msg_task按照id排序
    query = db.query(MsgTaskModel).filter(MsgTaskModel.deleted_at == None)
    if task_type:
        query = query.filter(MsgTaskModel.task_type == task_type)
    if state:
        query = query.filter(MsgTaskModel.state == state)
    if affiliate_account:
        db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.affiliate_account == affiliate_account).first()
        query = query.filter(MsgTaskModel.affiliate_id == db_affiliate.id)
    if influencer:
        query = query.filter(MsgTaskModel.influencer_id == influencer.id).order_by(asc(MsgTaskModel.id))
    else:
        query = query.order_by(asc(MsgTaskModel.influencer_id), asc(MsgTaskModel.id))
    query = query.limit(limit)
    tasks = []
    for task in query.all():
        res = schemas.MsgTaskResponse.model_validate(task, from_attributes=True)
        if influencer:
            res.influencer_account = influencer.influencer_account
            res.site_id = influencer.site_id
            res.affiliate_account = affiliate_account
        elif task.influencer_id:
            res.influencer_account = task.influencer.influencer_account
            res.site_id = task.influencer.site_id
            res.affiliate_account = affiliate_account
        tasks.append(res)
    return tasks


# 更新消息发送任务状态
@msg_task_router.patch("/{task_id}", response_model=schemas.MsgTaskResponse)
async def update_msg_task_state(
    task_id: int = Path(...),
    state: schemas.MsgTaskStates = Body(...),
    error_msg: str = Body(None),
    db: Session = Depends(get_db),
):
    db_msg_task = (
        db.query(MsgTaskModel)
        .with_for_update(nowait=True, of=MsgTaskModel)
        .filter(MsgTaskModel.id == task_id)
        .first()
    )
    if db_msg_task:
        db_msg_task.state = state
        db_msg_task.error_msg = error_msg
        db_msg_task.updated_at = datetime.now()
        db.commit()
        db.refresh(db_msg_task)
        if state == schemas.MsgTaskStates.sent and db_msg_task.workflow_id:
            await fire_workflow_event(
                db_msg_task.workflow_id, db_msg_task.workflow_event, db
            )
        elif state == schemas.MsgTaskStates.failed and db_msg_task.workflow_id:
            await fire_workflow_event(
                db_msg_task.workflow_id, "消息发送失败", db
            )
            db_workflow = db.query(WorkflowModel).filter(WorkflowModel.id == db_msg_task.workflow_id).first()
            db_workflow.event = "人工处理"
            db.commit()
        return db_msg_task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MsgTask not found"
        )
