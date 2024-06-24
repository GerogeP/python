# coding:utf-8
from fastapi import APIRouter, Request, Security, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.schemas import UserLogin, UserRegister, UserDBOut
from app.core.models import User as UserModel
from app.core.verify import verify_user_token, verify_password, create_access_token, get_password_hash

router = APIRouter(prefix="/passport")


@router.post("/login", summary="登录")
async def login(data_in: UserLogin, db: Session = Depends(get_db)):
    """
    用户登陆
    :param db: db Session
    :param data_in: username，password
    :return: jwt token
    """
    if data_in.username and data_in.password:
        # 账号密码登陆
        user_info = db.query(UserModel).filter(UserModel.name == data_in.username).first()
        print(user_info.__dict__)
        if user_info is None:
            return {"msg": "登录账号或密码错误", "data": {}, "code": 200}
        if not user_info.hashed_password:
            return {"msg": "登录账号或密码错误", "data": {}, "code": 200}
        if not verify_password(data_in.password, user_info.hashed_password):
            return {"msg": "登录账号或密码错误", "data": {}, "code": 200}
        if not user_info.is_active:
            return {"msg": "登录账号已被禁用了", "data": {}, "code": 200}
        # 这里放 jwt 加密的数据,校验的时候可以解密
        jwt_data = {
            "user_id": str(user_info.user_id),
            "username": user_info.name,
        }
        # 调用方法直接得到token
        jwt_token = create_access_token(data=jwt_data)
        print('jwt_token', jwt_token)
        data = {"token": jwt_token, "userinfo": user_info}
        return {"msg": "登陆成功😄", "data": data, "code": 200}



@router.post("/register", summary="注册用户")
async def register(data_in: UserRegister, db: Session = Depends(get_db)):
    """
    创建用户
    :param data_in: UserRegister
    :return:
    """
    # 过滤用户
    if data_in.password != data_in.confirm_password:
        return {"msg": "确认密码不一致", "data": {}, "code": 200}

    get_user = db.query(UserModel).filter(UserModel.email == data_in.email).first()
    print(get_user)
    if get_user is not None:
        return {"msg": f"邮箱{data_in.email}不可用!", "data": {}, "code": 200}

    # 获取加密码
    hash_pwd = get_password_hash(data_in.password)
    print('hash_pwd', hash_pwd)
    # 创建用户
    insert_user = UserModel(
        name=data_in.name,
        email=data_in.email,
        hashed_password=hash_pwd
    )
    db.add(insert_user)
    db.commit()
    db.refresh(insert_user)
    return {"msg": f"用户{insert_user.name}注册成功", "data": {}, "code": 200}


@router.get("/get_user_info", summary="用户信息", dependencies=[Security(verify_user_token)])
async def get_user_info(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    print(user_id)
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    user_info = UserDBOut(**user.__dict__).dict()
    return {"msg": "success", "data": user_info, "code": 200}