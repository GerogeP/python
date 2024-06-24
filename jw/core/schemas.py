from pydantic import BaseModel, UUID4, Field


class Role(BaseModel):
    role_id: UUID4
    name: str
    description: str | None = None
    is_active: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    user_id: UUID4
    role_id: str
    name: str
    is_email_verified: bool
    is_active: bool

    class Config:
        orm_mode = True


class Message(BaseModel):
    message_id: UUID4
    owner_id: str
    title: str
    description: str | None = None
    date_time: str
    place: str
    person: str
    event: str


# 用户登陆
class UserLogin(BaseModel):
    username: str = Field(..., description="用户名", example="admin")
    password: str = Field(..., description="密码", example="123456")


class UserRegister(BaseModel):
    name: str = Field(..., description="用户名", example="admin")
    email: str = Field(..., description="邮箱", example="admin@admin.com")
    password: str = Field(..., description="密码", example="123456")
    confirm_password: str = Field(..., description="确认密码", example="123456")


class UserDBOut(BaseModel):
    """
    用户信息DB输出
    """
    user_id: UUID4  # 主键
    role_id: UUID4 | None = None
    name: str
    email: str
    is_email_verified: bool
