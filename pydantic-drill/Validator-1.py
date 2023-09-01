"""
使用validator装饰器可以实现自定义验证和对象之间的复杂关系。
"""

from pydantic import BaseModel, ValidationError, validator


class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str
    
        
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


user = UserModel(
    name='samule colvim',
    username='scolvin',
    password1='zxcvbn',
    password2='zxcvbn',
)
print(user)
"""
 name='Samul colvin' username='scolvin' password1='zxcvbn'
password2='zxcvbn'
"""

try:
    UserModel(
        name='samuel',
        username='scolvin',
        password1='zxcvbn',
        password2='zxcvbn2',
    )
except ValidationError as e:
    print('++++++++++++++++')
    print(e)
    """
    2 validation errors for UserModel
    name
        must contain a space (type=value_error)
    password2
        passwords do not match (type=value_error)
    """

