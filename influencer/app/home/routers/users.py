from fastapi import APIRouter, Depends, Request, Path
from sqlalchemy.orm import Session

from app.exceptions.base import AppException
from app.home.schemas.user import UserListIn, UserDetailIn, UserEditIn, UserCreateIn
from app.home.service.users import UsersService, UserDBOut
from app.dependencies.databases import get_db
from app.core.response import unify_response

router = APIRouter(prefix='/users')


@router.get('/list')
@unify_response
async def user_list(list_in: UserListIn = Depends(), db: Session = Depends(get_db)):
    """
    用户列表
    :return:
    """
    model_service = UsersService(db)
    lists, total = await model_service.list(list_in)
    return {"lists": lists, "total": total}


@router.post('/create')
@unify_response
async def user_create(detail_in: UserCreateIn, db: Session = Depends(get_db)) -> UserDBOut:
    """
    用户详情
    :return:
    """
    model_service = UsersService(db)
    item = model_service.find_by_username(detail_in.username)
    if item:
        raise AppException(msg="用户已存在")
    return await model_service.create(obj_in=detail_in)


@router.get('/detail')
@unify_response
async def user_detail(detail_in: UserDetailIn = Depends(), db: Session = Depends(get_db)) -> UserDBOut:
    """
    用户详情
    :return:
    """
    model_service = UsersService(db)
    return await model_service.detail(detail_in=detail_in)


@router.post('/edit')
@unify_response
async def user_edit(edit_in: UserEditIn, db: Session = Depends(get_db)) -> UserDBOut:
    """
    用户修改
    :return:
    """
    model_service = UsersService(db)
    return await model_service.edit(edit_in=edit_in)



@router.delete("/{item_id}", summary="删除用户")
@unify_response
async def delete(request: Request, db: Session = Depends(get_db), item_id: int = Path(..., description="用户ID")):
    assert item_id != request.state.user_id, '不能删除自己!'
    model_service = UsersService(db)
    await model_service.delete(item_id)
    return {}


