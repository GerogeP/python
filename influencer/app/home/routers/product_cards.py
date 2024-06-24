from datetime import datetime
import json
from typing import List, Optional, Dict

from fastapi import APIRouter, Query, Path, Depends
from sqlalchemy.orm import Session

from app.core.response import unify_response
from app.dependencies.databases import get_db
from app.home.schemas.product_cards import ProductCardsBase, ProductCardsUpdate
from app.models.product_cards import ProductCards as ProductCardsModel

router = APIRouter(prefix="/product_cards")


@router.get("/list", summary="列表")
@unify_response
async def page_list(
        db: Session = Depends(get_db),
        page: int = Query(1, description="页码"),
        limit: int = Query(10, description="每页数量"),
        product_name: str = Query(None, description="产品名称"),
        site_id: str = Query(None, description="达人来源"),
        product_card_id: Optional[str] = Query(None, description="产品ID"),
):
    start = (page - 1) * limit
    # 查询条件
    query = db.query(ProductCardsModel).filter(ProductCardsModel.deleted_at == None).order_by(
        ProductCardsModel.updated_at.desc())
    if product_name:
        query = query.filter(ProductCardsModel.product_name.like('%{0}%'.format(product_name)))
    if product_card_id:
        query = query.filter(ProductCardsModel.product_card_id == product_card_id)
    if site_id:
        query = query.filter(ProductCardsModel.site_id == site_id)
    # 使用 SQLAlchemy 的分页功能
    total = query.count()
    lists = query.offset(start).limit(limit).all()

    return {"lists": lists, "total": total}


@router.get("/{item_id}", summary="查看商品卡")
@unify_response
async def get_detail(db: Session = Depends(get_db), item_id: int = Path(..., description="商品卡ID"), ):
    item_obj = db.query(ProductCardsModel).filter(ProductCardsModel.id == item_id).first()
    if not item_obj:
        raise "数据不存在"
    return item_obj


@router.post("/create", summary="创建商品卡")
@unify_response
async def create(data_in: ProductCardsBase, db: Session = Depends(get_db)):
    if isinstance(data_in, Dict):
        obj_dict = data_in
    else:
        obj_dict = data_in.model_dump()
    obj_dict.update({"params": json.dumps({})})
    add_item = ProductCardsModel(**obj_dict)
    # 将模型实例添加到会话
    result = db.add(add_item)
    db.commit()
    db.refresh(add_item)
    if not add_item:
        raise "创建失败"
    return "操作成功"


@router.post("/update", summary="更新用户")
@unify_response
async def update(data_in: ProductCardsUpdate, db: Session = Depends(get_db)):
    if isinstance(data_in, Dict):
        obj_dict = data_in
    else:
        obj_dict = data_in.model_dump()
    item_to_update = (db.query(ProductCardsModel).filter(ProductCardsModel.id == data_in.id)
                      .update(obj_dict, synchronize_session='fetch'))
    db.commit()
    if item_to_update >= 1:
        return item_to_update
    else:
        assert '数据不存在！'


@router.delete("/{item_id}", summary="删除用户")
@unify_response
async def delete(item_id: int = Path(..., description="用户ID"), db: Session = Depends(get_db)):
    item_to_update = db.query(ProductCardsModel).filter(ProductCardsModel.id == item_id).first()
    if item_to_update:
        # 修改记录
        item_to_update.deleted_at = datetime.now()
        # 提交会话
        db.commit()
        return item_to_update
    else:
        assert '数据不存在！'
