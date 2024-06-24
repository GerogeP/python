from fastapi import APIRouter, Depends, Security

from app.core.verify import verify_user_token
from app.routes import iat, passport, sql


router = APIRouter(prefix="/api")

# 接口
router.include_router(passport.router, tags=["注册登陆"])
router.include_router(iat.router, tags=["AI测试"], dependencies=[Security(verify_user_token)])
router.include_router(sql.router, tags=["databases"], dependencies=[Security(verify_user_token)])