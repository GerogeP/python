from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import settings

print(settings.DATABASE_URL)
print('-'.rjust(80, '-'))

# Create database engine
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

# Create database declarative base
Base = declarative_base()

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()