# coding:utf-8
from fastapi import APIRouter, Request, Security, Depends
from sqlalchemy.orm import Session

from app.dependencies.databases import get_db
from app.exceptions.base import AppException
from app.home.schemas.user import UserDBOut
from app.models.users import Users as UsersModel
from app.home.service.users import UsersService
from app.home.schemas.passport import AccountLogin
from app.common.enums import StatusEnum
from app.config.settings import settings
from app.core.response import unify_response, HttpResp
from app.dependencies.verify import verify_user_token, verify_password, create_access_token

router = APIRouter(prefix="/passport")


@router.post("/login", summary="登录")
async def login(data_in: AccountLogin, db: Session = Depends(get_db)):
    """
    用户登陆
    :param db: db Session
    :param data_in: username，password
    :return: jwt token
    """
    if data_in.username and data_in.password:
        # 账号密码登陆
        user_info = db.query(UsersModel).filter(UsersModel.username == data_in.username).first()
        if user_info is None:
            # TODO await record_login_log(0, user_info.username, HttpResp.LOGIN_ACCOUNT_ERROR.msg)
            raise AppException(HttpResp.LOGIN_ACCOUNT_ERROR)
        if not user_info.password:
            raise AppException(HttpResp.LOGIN_ACCOUNT_ERROR)
        if not verify_password(data_in.password, user_info.password):
            raise AppException(HttpResp.LOGIN_ACCOUNT_ERROR)
        if user_info.status != StatusEnum.normal:
            raise AppException(HttpResp.LOGIN_DISABLE_ERROR)

        jwt_data = {
            "user_id": user_info.id,
            "username": user_info.username,
        }

        jwt_token = create_access_token(data=jwt_data)
        data = {"token": jwt_token, "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES}
        # await write_access_log(req, get_user.pk, "通过用户名登陆了系统!")
        return {"msg": "登陆成功😄", "data": data, "code": 200}


@router.get("/get_user_info", summary="用户信息", dependencies=[Security(verify_user_token)])
@unify_response
async def get_user_info(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    print(user_id)
    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    user_info = UserDBOut(**user.__dict__).dict()
    return user_info

# @router.post("/register", summary="注册用户")
# async def register(admin: AdminRegister):
#     """
#     创建用户
#     :param admin: AdminRegister
#     :return:
#     """
#     users_service = UsersService()
#     # 过滤用户
#     if admin.password != admin.confirm_password:
#         return response_fail(msg="确认密码不一致")
#
#     get_user = await users_service.find({"username": admin.username})
#     if get_user:
#         return response_fail(msg=f"用户名{admin.username}已经存在!")
#
#     # 创建用户
#     create_user = await users_service.register(admin)
#     if not create_user:
#         return response_fail(msg=f"用户{admin.username}创建失败!")
#     # if admin.roles:
#     #     # 有分配角色
#     #     roles = await Role.filter(id__in=admin.roles, role_status=True)
#     #     await create_user.role.add(*roles)
#     return response_ok(msg=f"用户{admin.username}注册成功")
