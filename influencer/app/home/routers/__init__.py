from fastapi import APIRouter, Depends, Security

from .msg_store import msg_store_router
from .msg_task import msg_task_router
from .workflow import workflow_router
from app.home.routers import product_cards, chat, promotion, passport, users, affiliate, influencer
from app.dependencies.verify import verify_user_token

home_router = APIRouter(prefix="/api")

# 接口
home_router.include_router(passport.router, tags=["passport"])
home_router.include_router(workflow_router, tags=["workflow"])
home_router.include_router(msg_task_router, tags=["msg_task"])
home_router.include_router(msg_store_router, tags=["msg_store"])
home_router.include_router(promotion.router, tags=["推广任务"], dependencies=[Security(verify_user_token)])
home_router.include_router(influencer.router, tags=["达人管理"], dependencies=[Security(verify_user_token)])
home_router.include_router(affiliate.router, tags=["机构管理"], dependencies=[Security(verify_user_token)])
home_router.include_router(product_cards.router, tags=["商品卡片"], dependencies=[Security(verify_user_token)])
home_router.include_router(users.router, tags=["用户管理"], dependencies=[Security(verify_user_token)])
home_router.include_router(chat.router, tags=["chat"], dependencies=[Security(verify_user_token)])
