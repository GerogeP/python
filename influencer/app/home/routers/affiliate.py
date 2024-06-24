import json
import os
from datetime import datetime
from typing import List, Optional, Dict

import pandas as pd
from fastapi import APIRouter, Body, Depends, HTTPException, Query, UploadFile, Path
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.response import unify_response
from app.dependencies.databases import get_db
from app.home.schemas.affiliate import AffiliateBase, AffiliateUpdate
from app.models.affiliate import Affiliate as AffiliateModel



router = APIRouter(prefix='/affiliate')


@router.get("/list", summary="列表")
@unify_response
async def page_list(
        db: Session = Depends(get_db),
        page: int = Query(1, description="页码"),
        limit: int = Query(10, description="每页数量"),
        account: str = Query(None, description="账号名称"),
        site_id: str = Query(None, description="达人来源"),
):
    start = (page - 1) * limit
    # 查询条件
    query = db.query(AffiliateModel).filter(AffiliateModel.deleted_at == None).order_by(
        AffiliateModel.updated_at.desc())
    if account:
        query = query.filter(AffiliateModel.affiliate_account.like('%{0}%'.format(account)))
    if site_id:
        query = query.filter(AffiliateModel.site_id == site_id)
    # 使用 SQLAlchemy 的分页功能
    total = query.count()
    lists = query.offset(start).limit(limit).all()

    return {"lists": lists, "total": total}



@router.post("/create", summary="添加机构账号")
@unify_response
async def create(data_in: AffiliateBase, db: Session = Depends(get_db)):
    if isinstance(data_in, Dict):
        obj_dict = data_in
    else:
        obj_dict = data_in.model_dump()
    add_item = AffiliateModel(**obj_dict)
    # 将模型实例添加到会话
    result = db.add(add_item)
    db.commit()
    db.refresh(add_item)
    if not add_item:
        raise "创建失败"
    return "操作成功"


@router.post("/update", summary="更新机构账号")
@unify_response
async def update(data_in: AffiliateUpdate, db: Session = Depends(get_db)):
    if isinstance(data_in, Dict):
        obj_dict = data_in
    else:
        obj_dict = data_in.model_dump()
    item_to_update = (db.query(AffiliateModel).filter(AffiliateModel.id == data_in.id)
                      .update(obj_dict, synchronize_session='fetch'))
    db.commit()
    if item_to_update >= 1:
        return item_to_update
    else:
        assert '数据不存在！'


@router.delete("/{item_id}", summary="删除机构账号")
@unify_response
async def delete(item_id: int = Path(..., description="用户ID"), db: Session = Depends(get_db)):
    item_to_update = db.query(AffiliateModel).filter(AffiliateModel.id == item_id).first()
    if item_to_update:
        # 修改记录
        item_to_update.deleted_at = datetime.now()
        # 提交会话
        db.commit()
        return item_to_update
    else:
        assert '数据不存在！'

