"""
Pydantic 附带了一个 mypy 插件，向 mypy 添加了许多重要的特定于 pydantic 的功能，以提高其对代码进行类型检查的能力。
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, NoneStr


class Model(BaseModel):
    age: int
    first_name = 'John'
    last_name: NoneStr = None
    signup_ts: Optional[datetime] = None
    List_of_ints: List[int]


m = Model(age=42, List_of_ints=[1, '2', b'3'])
print(m.middle_name) # not a model field!
Model() # will raise a validation error for age and List_of_ints

"""
    在没有任何特殊配置的情况下，mypy 会捕获其中一个错误：
13: error: "Model" has no attribute "middle_name"
复制代码
启用插件后，它会同时捕获：
13: error: "Model" has no attribute "middle_name"
16: error: Missing named argument "age" for "Model"
16: error: Missing named argument "list_of_ints" for "Model"
复制代码
要启用该插件，只需添加pydantic.mypy到mypy 配置文件中的插件列表：
[mypy]
plugins = pydantic.mypy
复制代码
要更改插件设置的值，请​​在 mypy 配置文件中创建一个名为 的部分[pydantic-mypy]，并为要覆盖的设置添加键值对：
[mypy]
plugins = pydantic.mypy

follow_imports = silent
warn_redundant_casts = True
warn_unused_ignores = True
disallow_any_generics = True
check_untyped_defs = True
no_implicit_reexport = True

# for strict mypy: (this is the tricky one :-))
disallow_untyped_defs = True

[pydantic-mypy]
init_forbid_extra = True
init_typed = True
warn_required_dynamic_aliases = True
warn_untyped_fields = True


作者：青火_
链接：https://juejin.cn/post/7079027549896081421
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

