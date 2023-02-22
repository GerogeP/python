from sqlalchemy import create_engine
from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy.orm import sessionmaker

import env 

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:example@127.0.0.1:5432/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":  False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

