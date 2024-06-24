from fastapi import Request, HTTPException, Depends, status

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext

from app.core.models import User as UserModel
from app.core.database import get_db_session

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    """
    生成token
    :param data: 需要加密到token中的信息
    例如 user_id,解密后可以查询对应用户,并判断用户是否可用状态
    :param expires_in: 过期时间
    :return: token
    """
    to_encode = data.copy()
    if expires_in:
        expire = datetime.utcnow() + expires_in
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    print('jwt', to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_user_token(request: Request, token=Depends(OAuth2)):
    """
    校验Token
    :param request: token
    """
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
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效凭证",
                    headers={"WWW-Authenticate": f"Bearer{token}"},
                )
                raise credentials_exception
        else:
            # Token 不合法
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )
            raise credentials_exception

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ---------------------------------------验证权限-------------------------------------------------------------------
    # 查询用户是否真实有效、或者已经被禁用
    with get_db_session() as session:
        items = session.query(UserModel).filter(UserModel.user_id == user_id).first()

        if items is None or not items.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已经被管理员禁用!",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )
        # 单次请求信息保存
        request.state.user_id = user_id
        request.state.username = items.name
