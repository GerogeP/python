"""
关于验证器的一些注意事项：

验证器是“类方法”，因此它们接收的第一个参数值是UserModel类，而不是UserModel
第二个参数始终是要验证的字段值，可以随意命名
单个验证器可以通过传递多个字段名称来应用于多个字段，也可以通过传递特殊值在所有字段上调用单个验证器'*'
关键字参数pre将导致在其他验证之前调用验证器
通过each_item=True将导致验证器被施加到单独的值（例如List，Dict，Set等），而不是整个对象

作者：青火_
链接：https://juejin.cn/post/7079027549896081421
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

from typing import List
from pydantic import BaseModel, ValidationError, validator


class ParentModel(BaseModel):
    names: List[str]


class ChildModel(ParentModel):
    @validator('names', each_item=True)
    def check_names_not_empty(cls, v):
        assert v !=  '', 'Empty strings are not allowed.'
        return v


# This will NOT raise a ValidationError because the validator was not called
try:
    child = ChildModel(names=['alice', 'Bob', 'Eve', ''])
except ValidationError as e:
    print(e)
else:
    print('No ValidationError caught.')
    #> No ValidationError caught.


class ChildModel2(ParentModel):
    @validator('names')
    def check_names_not_empty(cls, v):
        for name in v:
            print(name)
            assert name != '', 'Empty strings are not allowed.'
        return v


try:
    child = ChildModel2(names=['Alic', 'Bob', 'Eve', '']) 
    print(child)
except ValidationError as e:
    print(e)
    """
    1 validatotion error for ChildModel2 
    names
        Empty string are not allowed. (type=assertion_error)
    """


