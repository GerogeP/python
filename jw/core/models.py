import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    role_id = Column(Uuid, ForeignKey("roles.role_id"))
    name = Column(String(32))
    email = Column(String(200), unique=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)

    role = relationship("Role", back_populates="users")
    messages = relationship("Message", back_populates="owner")


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Uuid, ForeignKey("users.user_id"))
    date_time = Column(String)
    place = Column(String)
    person = Column(String)
    event = Column(String)

    owner = relationship("User", back_populates="messages")
