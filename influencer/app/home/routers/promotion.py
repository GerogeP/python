import json
import os
from datetime import datetime
from typing import List, Optional, Dict

from fastapi import APIRouter, Query, Path, Depends, Request
from sqlalchemy import insert, and_
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.response import unify_response
from app.dependencies.databases import get_db
from app.exceptions.base import AppException
from app.home.schemas.promotion import PromotionCreate
from app.models.affiliate import Affiliate as AffiliateModel
from app.models.promotion import PromotionTasks as PromotionTasksModel
from app.models.promotion import PromotionTaskWorkflow as PromotionTaskWorkflowModel
from app.models.models import (
    Workflow as WorkflowModel,
    WorkflowParam as WorkflowParamModel,
    InfluencerAffiliateWorkflow as InfluencerAffiliateWorkflowModel,
)

router = APIRouter(prefix="/promotion")


# , response_model=Page[AdminOutDB]
@router.get("/list", summary="推广任务列表")
@unify_response
async def page_list(
        db: Session = Depends(get_db),
        page: int = Query(1, description="页码"),
        limit: int = Query(10, description="每页数量"),
        title: str = Query(None, description="任务名称"),
        site_id: str = Query(None, description="任务站点"),
        product_card_id: Optional[str] = Query(None, description="产品ID"),
):
    start = (page - 1) * limit
    # 查询条件
    query = db.query(PromotionTasksModel).filter(PromotionTasksModel.deleted_at == None).order_by(
        PromotionTasksModel.updated_at.desc())
    if title:
        query = query.filter(PromotionTasksModel.title.like('%{0}%'.format(title)))
    if site_id:
        query = query.filter(PromotionTasksModel.site_id == site_id)
    # 使用 SQLAlchemy 的分页功能
    total = query.count()
    lists = query.offset(start).limit(limit).all()

    return {"lists": lists, "total": total}


@router.get("/{item_id}", summary="查看详情")
@unify_response
async def get_detail(item_id: int = Path(..., description="任务ID"), db: Session = Depends(get_db)):
    item = db.query(PromotionTasksModel).filter(PromotionTasksModel.id == item_id).first()
    return item


@router.post("/create", summary="创建任务")
@unify_response
async def create(request: Request, data_in: PromotionCreate, db: Session = Depends(get_db)):
    if isinstance(data_in, Dict):
        obj_dict = data_in
    else:
        obj_dict = data_in.model_dump()
    # 创建 任务
    affiliate_id = obj_dict.get("affiliate_id")
    affiliate_item = db.query(AffiliateModel).filter(AffiliateModel.id == affiliate_id).first()
    print("affiliate_item", affiliate_item.__dict__)
    if affiliate_item is None:
        raise AppException(msg="机构账号不存在！")

    product_card = obj_dict.get("product_card")
    influencers_list = obj_dict.get("influencers_list")
    if not product_card.get('id'):
        raise AppException(msg='商品卡不能为空')
    if len(influencers_list) == 0:
        raise AppException(msg='请选择达人')
    task_sql = (
        insert(PromotionTasksModel).
        values(
            site_id=obj_dict['site_id'],
            title=obj_dict['title'],
            description=obj_dict['description'],
            product_card_id=product_card.get('id')
        ).
        returning(PromotionTasksModel)
    )
    # 执行插入语句并获取新插入的行
    task_item = db.execute(task_sql).fetchone()
    for in_item in influencers_list:
        print('in_item', in_item)
        # 'affiliate_account': "NovaHomeShop",
        workflow_dict = {
            'template_id': "达人联络工作流",
            'affiliate_id': affiliate_id,
            'influencer_id': in_item.get("id"),
            'state': "已创建",
            'event': "create",
            'op_id': request.state.user_id,
        }
        # 保存 workflow param
        workflow_param_sql = (
            insert(WorkflowParamModel).
            values(
                param={
                    'product_cards_id': product_card.get('product_card_id'),
                    'product_card': product_card
                },
            ).
            returning(WorkflowParamModel)
        )
        workflow_param_item = db.execute(workflow_param_sql).fetchone()
        print("workflow_param_item", workflow_param_item[0].id)
        # 创建 workflow
        workflow_sql = (
            insert(WorkflowModel).
            values(
                **workflow_dict,
                workflow_param_id=workflow_param_item[0].id
            ).
            returning(WorkflowModel)
        )

        workflow_item = db.execute(workflow_sql).fetchone()
        print("workflow_item", workflow_item)
        # 查询是否有正在进行任务
        current_workflow = db.query(InfluencerAffiliateWorkflowModel).filter(and_(
            InfluencerAffiliateWorkflowModel.deleted_at == None,
            InfluencerAffiliateWorkflowModel.influencer_id == in_item.get("id"),
            InfluencerAffiliateWorkflowModel.affiliate_id == affiliate_id
        )).order_by(InfluencerAffiliateWorkflowModel.updated_at.desc()).first()
        if current_workflow:
            current_workflow.current_workflow_id = workflow_item[0].id
        else:
            db.add(InfluencerAffiliateWorkflowModel(
                influencer_id=in_item.get("id"),
                affiliate_id=affiliate_id,
                affiliate_account=affiliate_item.affiliate_account,
                current_workflow_id=workflow_item[0].id
            ))

        # 推广任务记录表
        db.add(PromotionTaskWorkflowModel(
            promotion_task_id=task_item[0].id,
            workflow_id=workflow_item[0].id,
            influencer_id=in_item.get("id"),
            affiliate_id=affiliate_id,
        ))
        # 提交事务
        db.commit()

    return {}


@router.delete("/{item_id}", summary="删除")
@unify_response
async def delete(item_id: int = Path(..., description="ID"), db: Session = Depends(get_db)):
    delete_item = db.query(PromotionTaskWorkflowModel).filter(PromotionTaskWorkflowModel.id == item_id).first()
    if delete_item:
        delete_item.deleted_at = datetime.now()
        # 提交会话
        db.commit()
        return delete_item
    else:
        assert '数据不存在！'
