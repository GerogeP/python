"""
如果您创建一个继承自BaseSettings的模型，模型初始化程序将尝试通过从环境中读取，来确定未作为关键字参数传递的任何字段的值。（如果未设置匹配的环境变量，则仍将使用默认值。）
这使得很容易：

创建明确定义、类型提示的应用程序配置类
自动从环境变量中读取对配置的修改
在需要的地方手动覆盖初始化程序中的特定设置（例如在单元测试中）

作者：青火_
链接：https://juejin.cn/post/7079027549896081421
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

from typing import Set

from pydantic import (
    BaseModel,
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    Field,
)


class SubModel(BaseModel):
    foo = 'bar'
    apple = 1


class Settings(BaseSettings):
    auth_key: str
    api_key: str = Field(..., env='my_api_key')

    redis_dsn: RedisDsn = 'redis://panglili:panglili@localhost:6379/1'
    pg_dsn: PostgresDsn = 'postgres://panglili:panglili@localhost:5432/fooba'

    special_function: PyObject = 'math.cos'

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: Set[str] = set()

    # to override more_settings:
    # export my_prefix_more-_settings='{"foo": "x", "apple": 1}'
    more_settings: SubModel = SubModel()

    class Config:
        env_prefix = 'my_prefix_' # defaults to no prefix, i.e. ""
        fields = {
            'auth_key': {
                'env': 'my_auth_key',
            },
            'redis_dsn': {
                'env': ['service_redis_dsn', 'redis_url']
            }
        }


print(Settings().dict())
"""
{
    'auth_key': 'xxx',
    'api_key': 'xxx',
    'redis_dsn': RedisDsn('redis://panglilir:panglili@localhost"6379/1',
                          scheme='redis', user='panglili', password='panglili',
                          host='localhost', host_type='int_domain',
                          port='6379', path='/1'),
    'pg_dsn': PostgresDsn('postgres://panglili:panglili@localhost:5432/foobar',
                          scheme='postgres', user='panglilir',
                          password='panglili', host='localhost',
                          host_type='int_domain', port='5432', path='/foobar'),
    'special_function': <built-in function cos>,
    'domains': set(),
    'more_settings': ('foo': 'bar', 'apple': 1),
}
"""

