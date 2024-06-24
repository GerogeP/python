import json
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Path
from datetime import datetime
from sqlalchemy.orm import Session

from app.home.schemas import schemas
from app.models.models import (
    Workflow as WorkflowModel,
    WorkflowParam as WorkflowParamModel,
    InfluencerAffiliateWorkflow as InfluencerAffiliateWorkflowModel,
)
from app.models.affiliate import Affiliate as AffiliateModel
from app.dependencies.databases import get_db
from app.utils.workflow_manager import workflow_manager

workflow_router = APIRouter(prefix="/workflows")


# 查看工作流
@workflow_router.get("/{workflow_id}", response_model=schemas.WorkFlowResponse)
async def get_workflow(workflow_id: int = Path(...), db: Session = Depends(get_db)):
    db_workflow = (
        db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    )
    if db_workflow:
        return db_workflow
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )


# 更新工作流
@workflow_router.put("/{workflow_id}", response_model=schemas.WorkFlowResponse)
async def update_workflow(
        workflow_id: int = Path(...),
        workflow: schemas.Workflow = Body(...),
        db: Session = Depends(get_db),
):
    db_workflow = (
        db.query(WorkflowModel)
        .with_for_update(nowait=True, of=WorkflowModel)
        .filter(WorkflowModel.id == workflow_id)
        .first()
    )
    db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.affiliate_account == workflow.affiliate_account).first()
    if db_workflow:
        db_workflow.template_id = workflow.template_id
        db_workflow.state = workflow.state
        db_workflow.event = workflow.event
        db_workflow.affiliate_id = db_affiliate.id
        db_workflow.influencer_id = workflow.influencer_id
        db_workflow.op_id = workflow.op_id
        # db_workflow.task_id = workflow.task_id
        if workflow.workflow_param_id:
            db_workflow.workflow_param_id = workflow.workflow_param_id
        else:
            db_workflow_param = WorkflowParamModel(param=workflow.param)
            db.add(db_workflow_param)
            db.flush()
            db.refresh(db_workflow_param)
            db_workflow.workflow_param_id = db_workflow_param.id
        db_workflow.updated_at = datetime.now()
        db.commit()
        db.refresh(db_workflow)
        return db_workflow
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )


# 创建工作流
@workflow_router.post("/", response_model=schemas.WorkFlowResponse)
async def create_workflow(
        workflow: schemas.Workflow = Body(...), db: Session = Depends(get_db)
):
    # TODO： 创建工作流的同时把新的工作流的ID赋予给 influencer 的 current_workflow_id 字段
    db_workflow = WorkflowModel(**workflow.model_dump(exclude=["param"]))
    if workflow.workflow_param_id is None and workflow.param:
        db_workflow_param = WorkflowParamModel(param=workflow.param)
        db.add(db_workflow_param)
        db.flush()
        db.refresh(db_workflow_param)
        db_workflow.workflow_param_id = db_workflow_param.id
    db.add(db_workflow)
    # 固定测试账号的工作流ID
    # if db_workflow.influencer_id != 302:
    db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.id == db_workflow.affiliate_id).first()
    db_current_workflow = (
        db.query(InfluencerAffiliateWorkflowModel)
        .with_for_update(nowait=True, of=InfluencerAffiliateWorkflowModel)
        .filter(InfluencerAffiliateWorkflowModel.affiliate_id == db_affiliate.id,
                InfluencerAffiliateWorkflowModel.influencer_id == db_workflow.influencer_id)
        .first()
    )
    if not db_current_workflow:
        db.add(db_current_workflow)
        db.flush()
        db.refresh(db_current_workflow)
    db_current_workflow.current_workflow_id = db_workflow.id
    db.commit()
    db.refresh(db_workflow)
    return db_workflow


# 获取工作流列表response_model=List[schemas.WorkFlowResponse]
@workflow_router.get("/")
async def get_workflow_list(
        page: int = Query(1, description="页码"),
        limit: int = Query(10, description="每页数量"),
        promotion_id: Optional[str] = Query(None, description="推广任务"),
        template_id: Optional[str] = Query(None),
        state: Optional[str] = Query(None, description="任务状态"),
        db: Session = Depends(get_db),
):
    query = db.query(WorkflowModel).filter(WorkflowModel.deleted_at == None)
    if template_id:
        query = query.filter(WorkflowModel.template_id == template_id)
    if not state.isspace() and len(state) > 0:
        if state == '人工处理':
            query = query.filter(WorkflowModel.state.like("人工/"))
        else:
            query = query.filter(WorkflowModel.state.like(f"%{state}%"))
    total = query.count()
    lists = query.all()
    return {"data": lists, "total": total, "page": page, "limit": limit, "msg": "success", "code": 200}


# 触发工作流事件
@workflow_router.patch("/{workflow_id}/event/{event}")
async def fire_workflow_event(
        workflow_id: int = Path(...), event: str = Path(...), db: Session = Depends(get_db)
):
    db_workflow = (
        db.query(WorkflowModel)
        .with_for_update(nowait=True, of=WorkflowModel)
        .filter(WorkflowModel.id == workflow_id, WorkflowModel.deleted_at == None)
        .first()
    )
    if db_workflow:
        try:
            matter = workflow_manager.get_fsm(db, db_workflow)
            if matter:
                await matter.dispatch(event)
                db_workflow.updated_at = datetime.now()
                db.commit()
                db.refresh(db_workflow)
                return db_workflow
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
                )
        finally:
            workflow_manager.remove_fsm(workflow_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )


# 更新工作流状态
@workflow_router.patch("/{workflow_id}", response_model=schemas.WorkFlowResponse)
async def update_workflow_state(
        workflow_id: int = Path(...),
        state: str = Body(),
        event: str = Body(),
        db: Session = Depends(get_db),
):
    db_workflow = (
        db.query(WorkflowModel)
        .with_for_update(nowait=True, of=WorkflowModel)
        .filter(WorkflowModel.id == workflow_id)
        .first()
    )
    if db_workflow:
        db_workflow.state = state
        db_workflow.event = event
        db_workflow.updated_at = datetime.now()
        db.commit()
        db.refresh(db_workflow)
        return db_workflow
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )
