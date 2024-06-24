from fastapi import Request, HTTPException, Depends, status

from datetime import datetime, timedelta
from typing import Union
from fastapi.security import SecurityScopes
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.response import HttpResp
from app.exceptions.base import AppException
from app.models.users import Users
from app.dependencies.databases import get_db_session


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

OAuth2 = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    密码校验
    :param plain_password: 用户输入的密码
    :param hashed_password: 数据库密码
    :return: Boolean
    """
    check = pwd_context.verify(plain_password, hashed_password)
    if check:
        return True
    else:
        return False


def get_password_hash(password):
    """
    密码加密
    :param password:
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_in: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_in:
        expire = datetime.utcnow() + expires_in
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 后台管理用户 Token 校验
# async def verify_token(request: Request, security_scopes: SecurityScopes, token=Depends(OAuth2)):
#     """校验Token"""
#     try:
#         # token解密
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload:
#             # 用户ID
#             user_id = payload.get("user_id", None)
#             # 用户类型
#             username = payload.get("username", None)
#             # 无效用户信息
#             if user_id is None or username is None:
#                 credentials_exception = HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="无效凭证",
#                     headers={"WWW-Authenticate": f"Bearer{token}"},
#                 )
#                 raise credentials_exception
#         else:
#             credentials_exception = HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="无效凭证",
#                 headers={"WWW-Authenticate": f"Bearer {token}"},
#             )
#             raise credentials_exception
# 
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
# 
#     # ---------------------------------------验证权限-------------------------------------------------------------------
#     # 查询用户是否真实有效、或者已经被禁用
#     check_user = await Admin.get_or_none(id=user_id)
#     if not check_user or check_user.status != 1:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="用户不存在或已经被管理员禁用!",
#             headers={"WWW-Authenticate": f"Bearer {token}"},
#         )
#     # 用户角色
#     role_ids = []
#     if len(check_user.role_ids) > 1:
#         role_ids = [int(i) for i in check_user.role_ids.split(',')]
#     # 判断是否设置了权限域
#     if security_scopes.scopes:
#         # 非超级管理员且当前域需要验证
#         if not check_user.is_super and security_scopes.scopes:
#             # 未查询用户是否有对应权限
#             # 查询用户所有权限
#             allowed_scopes = await SystemRoleMenu.filter(role_id__in=role_ids).values_list('menu_id', flat=True)
#             # 访问所需要的权限 查询不出权限，说明所有的都不符合
#             need_scopes = await SystemMenu.filter(scopes__in=security_scopes.scopes).values_list('id', flat=True)
#             contains_all = False
#             if len(need_scopes) > 0:
#                 contains_all = all(item in allowed_scopes for item in need_scopes)
#             if not contains_all:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="Not permissions",
#                     headers={"scopes": security_scopes.scope_str},
#                 )
# 
#     # 单次请求信息保存
#     request.state.admin_id = user_id
#     request.state.role_ids = role_ids
#     request.state.is_super = check_user.is_super
#     request.state.username = check_user.username
#     # 校验角色权限是否存在


# 前台用户 Token 校验
async def verify_user_token(request: Request, token=Depends(OAuth2)):
    """校验Token"""
    # Token是否为空
    if not token:
        raise AppException(HttpResp.NO_AUTH)
    try:
        # token解密
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload:
            # 用户ID
            user_id = payload.get("user_id", None)
            # 用户类型
            username = payload.get("username", None)
            # 无效用户信息
            if user_id is None or username is None:
                raise AppException(HttpResp.NO_AUTH)
        else:
            # Token 不合法
            raise AppException(HttpResp.NO_AUTH)

    except JWTError:
        raise AppException(HttpResp.NO_AUTH)

    # ---------------------------------------验证权限-------------------------------------------------------------------
    # 查询用户是否真实有效、或者已经被禁用
    with get_db_session() as session:
        items = session.query(Users).filter(Users.id ==user_id).first()

        if items is None or items.status != 1 or items.is_delete == 1:
            raise AppException(HttpResp.LOGIN_DISABLE_ERROR)
        # 单次请求信息保存
        request.state.user_id = user_id
        request.state.username = items.username
