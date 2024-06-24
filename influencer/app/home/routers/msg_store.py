from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.home.schemas import schemas
from app.home.schemas.schemas import MsgTaskStates
from app.models.models import (
    MsgStore as MsgStoreModel,
    NewMsg as NewMsgModel,
    Influencer as InfluencerModel,
    MsgTask as MsgTaskModel
)
from app.models.affiliate import Affiliate as AffiliateModel
from app.home.service.messages import MsgTaskService
from app.dependencies.databases import get_db
from app.utils.time_convertor import convert_relative_time_to_datetime
import re
from app.config.settings import settings

msg_store_router = APIRouter(prefix="/msg_stores")


# 保存消息
@msg_store_router.post("/", response_model=schemas.MsgStoreResponse)
async def create_msg_store(
        msg_store: schemas.MsgStore = Body(...), db: Session = Depends(get_db)
):
    db_msg_store = MsgStoreModel(**msg_store.model_dump())
    db.add(db_msg_store)
    db.commit()
    db.refresh(db_msg_store)
    return db_msg_store


# 获取消息详情 response_model=schemas.MsgStoreResponse
@msg_store_router.post("/detail")
async def get_msg_store(data_in: schemas.MsgDetailIn, db: Session = Depends(get_db)):
    # db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.affiliate_id == data_in.affiliate_id).first()
    db_msg_store = db.query(MsgStoreModel).filter(MsgStoreModel.affiliate_id == data_in.affiliate_id).filter(MsgStoreModel.influencer_id == data_in.influencer_id).first()
    if db_msg_store:
        result = schemas.MsgStoreDbOut(**db_msg_store.__dict__).dict()
        if result.get('influencer_id'):
            infuencer_item = db.query(InfluencerModel).filter(InfluencerModel.id == result.get('influencer_id')).first()
            result['infuencer'] = infuencer_item
        return {'code': 200, 'msg': 'success', 'data': result}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MsgStore not found"
        )


# 获取消息存储
@msg_store_router.get("/{msg_store_id}", response_model=schemas.MsgStoreResponse)
async def get_msg_store(msg_store_id: int = Path(...), db: Session = Depends(get_db)):
    db_msg_store = (
        db.query(MsgStoreModel).filter(MsgStoreModel.id == msg_store_id).first()
    )
    if db_msg_store:
        return db_msg_store
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MsgStore not found"
        )


# 更新消息存储
@msg_store_router.put("/{msg_store_id}", response_model=schemas.MsgStoreResponse)
async def update_msg_store(
        msg_store_id: int = Path(...),
        msg_store: schemas.MsgStore = Body(...),
        db: Session = Depends(get_db),
):
    db_msg_store = (
        db.query(MsgStoreModel)
        .with_for_update(nowait=True, of=MsgStoreModel)
        .filter(MsgStoreModel.id == msg_store_id)
        .first()
    )
    if db_msg_store:
        db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.affiliate_account == msg_store.affiliate_account).first()
        db_msg_store.affiliate_id = db_affiliate.id
        db_msg_store.influencer_id = msg_store.influencer_id
        db_msg_store.msg_list = msg_store.msg_list
        db_msg_store.msg_updated_at = msg_store.msg_updated_at
        db_msg_store.updated_at = datetime.now()
        db.commit()
        db.refresh(db_msg_store)
        return db_msg_store
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MsgStore not found"
        )


# 更新消息列表
@msg_store_router.patch("/add_msgs", response_model=schemas.MsgStoreResponse)
async def add_msg(dialog: schemas.Dialog = Body(...), db: Session = Depends(get_db)):
    if dialog.timeZone != settings.timezone:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="TimeZone not True"
        )
    influencer = (
        db.query(InfluencerModel)
        .filter(
            InfluencerModel.site_id == dialog.site_id,
            InfluencerModel.influencer_account == dialog.influencer_account,
        )
        .first()
    )
    if influencer is None:
        # add new influencer
        influencer = InfluencerModel(
            site_id=dialog.site_id,
            influencer_account=dialog.influencer_account,
            param={"name": dialog.influencer_account},
        )
        db.add(influencer)
        db.flush()
        db.refresh(influencer)
    db_affiliate = db.query(AffiliateModel).filter(AffiliateModel.affiliate_account == dialog.affiliate_account).first()
    db_msg_store = (
        db.query(MsgStoreModel)
        .filter(
            MsgStoreModel.influencer_id == influencer.id,
            MsgStoreModel.affiliate_id == db_affiliate.id,
            MsgStoreModel.deleted_at == None,
        )
        .with_for_update(nowait=True, of=MsgStoreModel)
        .first()
    )
    if not db_msg_store:
        db_msg_store = MsgStoreModel(
            affiliate_id=db_affiliate.id,
            influencer_id=influencer.id,
        )
        db.add(db_msg_store)
        db.flush()
        db.refresh(db_msg_store)


    # change the state of related records in msg_task from 'sent' to 'in_store' 
    # MsgTaskService.change_msg_task_state(
    #         dialog.affiliate_account,
    #         influencer.id,
    #         MsgTaskStates.sent,
    #         MsgTaskStates.in_store
    #         )
    db_msg_task = (
        db.query(MsgTaskModel)
        .filter(
            MsgTaskModel.affiliate_id == db_affiliate.id, 
            MsgTaskModel.influencer_id == influencer.id, 
            MsgTaskModel.state == MsgTaskStates.sent)
    )
    for task in db_msg_task.all():
        task.state = MsgTaskStates.in_store

    msgs = []
    chat_time = None
    # RPA新增字段， reversed 为 1 时，传回来的数组是倒序，所以这里需要处理一下
    # print(dialog.reversed)
    if dialog.reversed == 1:
        dialog.dialogs.reverse()
    for msg in dialog.dialogs:
        if msg.chat_time is not None and msg.chat_time.strip() and re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", msg.chat_time) is None:
            chat_time = msg.chat_time
            chat_time = convert_relative_time_to_datetime(chat_time)
        elif msg.chat_time is None or chat_time is None:
            continue
        if not msg.message.strip():
            continue
        msgs.append(
            {
                "direction": "in" if msg.account == dialog.influencer_account else "out",
                "account_type": (
                    schemas.AccountTypes.influencer
                    if msg.account == dialog.influencer_account
                    else schemas.AccountTypes.affiliate
                ),
                "type": msg.type,
                "content": msg.message.strip(),
                "chat_time": chat_time.strftime("%Y-%m-%d %H:%M:%S"),
                "processed": False,
            }
        )
    if db_msg_store.msg_list is None:
        db_msg_store.msg_list = msgs
    else:
        history_msgs = {
            (
                msg["direction"],
                msg["account_type"],
                msg["type"],
                msg["content"],
                msg["chat_time"],
            ): msg
            for msg in (db_msg_store.msg_list[-50:] + msgs)
        }
        db_msg_store.msg_list = db_msg_store.msg_list[:-50] + list(
            history_msgs.values()
        )
        db_msg_store.msg_list = sorted(
            db_msg_store.msg_list, key=lambda msg: msg["chat_time"]
        )
    db_msg_store.msg_updated_at = datetime.now()  # 假设更新时间为请求时间
    db_msg_store.updated_at = datetime.now()
    db_new_msg = NewMsgModel(msg_store_id=db_msg_store.id)
    db.add(db_new_msg)
    db.commit()
    db.refresh(db_msg_store)
    return db_msg_store


@msg_store_router.patch(
    "/process/{msg_store_id}", response_model=schemas.MsgStoreResponse
)
async def process_msg_store(msg_store_id: int, db: Session = Depends(get_db)):
    db_msg_store = (
        db.query(MsgStoreModel)
        .with_for_update(nowait=True, of=MsgStoreModel)
        .filter(MsgStoreModel.id == msg_store_id)
        .first()
    )
    if db_msg_store:
        db.query(NewMsgModel).filter(
            NewMsgModel.msg_store_id == msg_store_id, NewMsgModel.deleted_at == None
        ).update({"deleted_at": datetime.now()})
        for i in range(len(db_msg_store.msg_list) - 1, -1, -1):
            if not db_msg_store.msg_list[i]["processed"]:
                db_msg_store.msg_list[i]["processed"] = True
            else:
                break
        db_msg_store.updated_at = datetime.now()
        db.commit()
        return db_msg_store
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MsgStore not found"
        )
