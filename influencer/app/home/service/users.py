import re
import time
from datetime import datetime
from typing import Union, Dict

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from app.dependencies.verify import get_password_hash
from app.home.schemas.user import UserListIn, UserDBOut, UserEditIn, UserDetailIn, UserCreateIn
from app.common.enums import get_login_client, get_sex, SexEnum
from app.exceptions.base import AppException
from app.core.response import HttpResp
from app.models.users import Users
from app.utils.urls import UrlUtil


class UsersService:
    def __init__(self, db: Session):
        self.db = db

    async def find_by_username(self, username: str) -> Union[UserDBOut, None]:
        """根据账号查找管理员"""
        item = self.db.query(Users).filter(Users.username == username).first()
        return item

    async def list(self, list_in: UserListIn):
        """
        用户列表
        :return:
        """
        start = (list_in.page - 1) * list_in.limit
        # 构建查询语句
        query = self.db.query(Users).filter(Users.is_delete == 0)
        if list_in.keyword is not None:
            query = query.filter(or_(
                Users.username.like('%{0}%'.format(list_in.keyword)),
                Users.nickname.like('%{0}%'.format(list_in.keyword)),
                Users.mobile.like('%{0}%'.format(list_in.keyword))
            ))
        if len(list_in.status) and int(list_in.status) in [0, 1]:
            query = query.filter(Users.status == int(list_in.status))
        # if list_in.start_time is not None:
        #     query = query.filter(Users.create_time >= int(time.mktime(list_in.start_time.timetuple())))
        # if list_in.end_time is not None:
        #     query = query.filter(Users.create_time <= int(time.mktime(list_in.end_time.timetuple())))
        # 使用 SQLAlchemy 的分页功能
        total = query.count()
        items = query.offset(start).limit(list_in.limit).all()

        # 将每个 ORM 模型实例转换为 Pydantic 模型的字典
        lists = [UserDBOut(**u.__dict__).dict() for u in items]
        #
        return lists, total

    async def create(self, obj_in: UserCreateIn):
        if isinstance(obj_in, Dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump()
        hash_pwd = get_password_hash(obj_in.password)
        obj_dict.update({"password": hash_pwd})
        # 创建模型实例并设置属性
        new_user = Users(**obj_dict)

        # 将模型实例添加到会话
        result = self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        print(result)
        return result

    async def edit(self, edit_in: UserEditIn):
        assert self.db.query(Users).filter(and_(Users.username == edit_in.username, Users.id != edit_in.id)).limit(
            1), '当前账号已存在！'
        # 查询要更新的记录
        user_to_update = self.db.query(Users).filter(Users.id == edit_in.id).first()

        if user_to_update:
            # 修改记录
            user_to_update.username = edit_in.username
            user_to_update.nickname = edit_in.nickname
            user_to_update.status = edit_in.status
            if edit_in.password:
                user_to_update.password = get_password_hash(edit_in.password)
            if edit_in.status is not None:
                user_to_update.status = edit_in.status
            # 提交会话
            self.db.commit()
            return user_to_update
        else:
            assert '数据不存在！'

    async def detail(self, detail_in: UserDetailIn) -> UserDBOut:
        # 构建查询
        user = self.db.query(Users).filter(and_(Users.id == detail_in.id, Users.is_delete == 0)).first()

        assert user, '数据不存在！'
        result = UserDBOut(**user.__dict__).dict()
        # result = pydantic.parse_obj_as(UserDBOut, user)
        # result = parse_obj_as(UserDBOut, user)
        result['avatar'] = await UrlUtil.to_absolute_url(result.get('avatar'))
        result['sex'] = get_sex(result.get('sex'))
        result['channel'] = get_login_client(result.get('channel'))
        return result

    async def delete(self, item_id: int):
        """管理员删除"""
        # 查询要更新的记录
        user_to_update = self.db.query(Users).filter(Users.id == item_id).first()

        if user_to_update:
            # 修改记录
            user_to_update.is_delete = 1
            # 提交会话
            self.db.commit()
            return user_to_update
        else:
            assert '数据不存在！'
