import json
import os
from datetime import datetime
from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, Body, Depends, HTTPException, Query, UploadFile, Request
from sqlalchemy import select, or_, and_, insert, update
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.response import unify_response
from app.home.schemas.influencer import InfluencerDBOut
from app.models.upload import Upload as UploadModel
from app.home.schemas import schemas
from app.models.models import (
    Influencer as InfluencerModel,
    InfluencerManualTag as InfluencerManualTagModel,
)

from app.dependencies.databases import get_db
from app.plugins.storage.storage_driver import StorageDriver

router = APIRouter(prefix="/influencers")


@router.get("", response_model=List[schemas.InfluencerResponse])
@unify_response
async def get_influencer_list(
        db: Session = Depends(get_db),
        page: int = Query(1, description="页码"),
        limit: int = Query(10, description="每页数量"),
        site_id: str = Query(None, description="达人来源"),
        account: str = Query(None, description="达人账号，用于搜索"),
):
    # 查询条件
    start = (page - 1) * limit
    # 查询条件
    query = db.query(InfluencerModel).filter(InfluencerModel.deleted_at == None).order_by(
        InfluencerModel.updated_at.desc())
    if account:
        query = query.filter(InfluencerModel.influencer_account.like('%{0}%'.format(account)))
    if site_id:
        query = query.filter(InfluencerModel.site_id == site_id)
    # 使用 SQLAlchemy 的分页功能
    total = query.count()
    lists = query.offset(start).limit(limit).all()

    return {"lists": lists, "total": total}


# 添加达人
@router.post("/", response_model=schemas.InfluencerResponse)
async def add_influencer(
        influencer: schemas.Influencer = Body(), db: Session = Depends(get_db)
):
    db_influencer = InfluencerModel(**influencer.model_dump())
    db.add(db_influencer)
    db.commit()
    db.refresh(db_influencer)
    return db_influencer


# 更新达人信息
@router.patch("/{influencer_id}", response_model=schemas.InfluencerResponse)
async def update_influencer(
        influencer_id: int,
        influencer: schemas.Influencer = Body(),
        db: Session = Depends(get_db),
):
    db_influencer = (
        db.query(InfluencerModel).filter(InfluencerModel.id == influencer_id).first()
    )
    if db_influencer:
        if influencer.site_id:
            db_influencer.site_id = influencer.site_id
        if influencer.influencer_account:
            db_influencer.influencer_account = influencer.influencer_account
        if influencer.param:
            db_influencer.param = influencer.param
        db_influencer.updated_at = datetime.now()
        db.commit()
        db.refresh(db_influencer)
        return db_influencer
    else:
        raise HTTPException(status_code=404, detail="Influencer not found")


# 添加达人标签
@router.post("/tags", response_model=schemas.InfluencerTagResponse)
async def add_influencer_tags(
        influencer_tag: schemas.InfluencerTag = Body(), db: Session = Depends(get_db)
):
    try:
        db_influencer_tag = InfluencerManualTagModel(**influencer_tag.model_dump())
        db.add(db_influencer_tag)
        db.commit()
        db.refresh(db_influencer_tag)
        return db_influencer_tag
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 更新达人标签
@router.patch(
    "/tags/{influencer_id}", response_model=schemas.InfluencerTagResponse
)
async def update_influencer_tags(
        influencer_id: int,
        influencer_tag: schemas.InfluencerTag = Body(),
        db: Session = Depends(get_db),
):
    db_influencer_tag = (
        db.query(InfluencerManualTagModel)
        .filter(InfluencerManualTagModel.influencer_id == influencer_id)
        .first()
    )
    if db_influencer_tag:
        db_influencer_tag.tags = influencer_tag.tags
        db_influencer_tag.updated_at = datetime.now()
        db.commit()
        db.refresh(db_influencer_tag)
        return db_influencer_tag
    else:
        raise HTTPException(status_code=404, detail="InfluencerTag not found")


# .xlsx 达人 导入
@router.post("/import", summary="文件导入达人")
@unify_response
async def import_influencer(file: UploadFile, db: Session = Depends(get_db)):
    """单文件上传"""
    # file/20240507/c47cc46be01e42c3ad76ccef307227d1.xlsx
    user_id = 1
    result = await StorageDriver.upload(file)
    # 保存upload 记录
    db.add(UploadModel(
        channel=2,
        folder_id=0,
        uid=1,
        file_type=result["file_type"],
        storage=result["storage"],
        name=result["name"],
        url=result["url"],
        ext=result["ext"],
        size=result["size"]
    ))

    # 使用os.path.sep获取当前系统的路径分隔符
    system_specific_path = os.path.join(*result["url"].split("/"))
    # 确保使用正确的分隔符
    if os.name == "nt":  # Windows系统
        path_separator = "\\"
    else:
        path_separator = "/"

    full_path = settings.UPLOAD_DIR + path_separator + system_specific_path
    print(full_path)
    # 读取上传的Excel文件
    df = get_excel(full_path)
    # 将DataFrame转换为JSON格式
    dict_df = df.to_dict(orient="records")

    # 插入更新数据
    save_list = []
    for i in dict_df:
        # 尝试查询并更新 TODO 文档加入 site_id
        dict_item = {
            "site_id": "tiktok",
            "influencer_account": i["influencer_account"],
            "param": i
        }

        instance = db.query(InfluencerModel).filter(and_(InfluencerModel.site_id == dict_item["site_id"], InfluencerModel.influencer_account == dict_item["influencer_account"])).first()
        if instance and instance.id:
            # 构建更新语句并使用 returning() 获取更新后的行
            stmt = (
                update(InfluencerModel).
                where(InfluencerModel.id == instance.id).
                values(**dict_item).
                returning(InfluencerModel)
            )
            # 执行更新语句并获取更新后的行
            updated_instance = db.execute(stmt).fetchone()
            if updated_instance[0].id:
                save_list.append(InfluencerDBOut(**updated_instance[0].__dict__).dict())
        else:
            # 如果没有查询到数据，则插入新数据。构建插入语句并使用 returning() 获取新插入的行
            stmt = (
                insert(InfluencerModel).
                values(**dict_item).
                returning(InfluencerModel)
            )
            # 执行插入语句并获取新插入的行
            new_instance = db.execute(stmt).fetchone()
            if new_instance[0].id:
                save_list.append(InfluencerDBOut(**new_instance[0].__dict__).dict())

    # 提交事务
    db.commit()
    # print(save_list)
    # 返回JSON格式的响应
    return save_list


# 读取Excel数据
def get_excel(filename):
    # 表头和子段映射关系
    column_name_mapping = {
        '达人名称': 'name',
        '达人ID': 'influencer_account',
        '达人头像': 'avatar',
        '达人分类': 'tags',
        '国家/地区': 'nation',
        'TikTok官网达人主页': 'home_page',
        'FastMoss达人详情': 'fast_moss',
    }

    #  '达人头像', 'TikTok官网达人主页', 'FastMoss达人详情'
    read_column_mapping = ['达人名称', '达人ID', '达人分类', '国家/地区']

    # 读取文件，跳过前两行 skiprows=1
    df = pd.read_excel(filename, usecols=read_column_mapping)
    print(df)
    # 字段间的映射转换，Excel中的表头和数据库表中字段的映射
    df.rename(columns=column_name_mapping, inplace=True)
    return df
