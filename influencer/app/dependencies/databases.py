# coding:utf-8
import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.exceptions.base import AppException

load_dotenv()

# 从环境变量中获取 DB URL
SQLALCHEMY_DATABASE_URL = os.getenv("PG_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, client_encoding="utf8", echo=True)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        print("connect db")
        yield db
    finally:
        print("disconnect db")
        db.close()


@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# 事务装饰器
def auto_commit(session: Session):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise AppException(code=400, msg=str(e))
            finally:
                session.close()

        return wrapper

    return decorator


class TimestampedMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
