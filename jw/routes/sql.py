
import uuid
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.core import crud, schemas


router = APIRouter( prefix="/databases")


@router.post("/roles/", response_model=schemas.Role)
def create_user(role: schemas.Role, db: Session = Depends(get_db)):
    db_role = crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role name already registered")

    role.role_id = str(uuid.uuid4())
    return crud.create_role(db=db, role=role)


@router.get("/roles/", response_model=list[schemas.Role])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles


@router.get("/roles/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role



@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=schemas.Message)
def create_message_for_user(
    user_id: int, item: schemas.Message, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/message/", response_model=list[schemas.Message])
def read_message(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_items(db, skip=skip, limit=limit)
    return messages


