from sqlalchemy.orm import Session

from . import models, schemas


def create_role(db: Session, role: schemas.Role):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.role_id == role_id).first()

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    print(f'get all roles.'.rjust(80,'-'))

    return db.query(models.Role).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()


def create_user_message(db: Session, message: schemas.Message, user_id: int):
    db_message = models.Message(**message.dict(), owner_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


if __name__ == '__main__':

    pass
