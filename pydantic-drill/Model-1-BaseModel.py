# import pydantic
from pydantic import *

# print('compiles: ', pydantic.compiled)
print('compiles: ', compiled)

'''
模型具有以下属性：

dict() 模型字段和值的字典
json() JSON 字符串表示dict()
copy() 模型的副本（默认为浅表副本）
parse_obj() 使用dict解析数据
parse_raw 将str或bytes并将其解析为json，然后将结果传递给parse_obj
parse_file 文件路径，读取文件并将内容传递给parse_raw。如果content_type省略，则从文件的扩展名推断
from_orm() 从ORM 对象创建模型
schema() 返回模式的字典
schema_json() 返回该字典的 JSON 字符串表示
construct() 允许在没有验证的情况下创建模型
__fields_set__ 初始化模型实例时设置的字段名称集
__fields__ 模型字段的字典
__config__ 模型的配置类
'''

class User(BaseModel):
    id: int
    name = 'Jane Do'


if __name__ == '__main__':
    print("run myself")

    '''
    print(User.dict())
    print(User.json())
    print(User.copy())
    print(User.pase_obj())
    print(User.schema())
    print(User.construct())
    print(User.__field_set__)
    print(User.__fields__(
    print(User.__config__)
    '''

    user = User(id='123')
    print(user)

else:
    PRINT("calling test.py")

