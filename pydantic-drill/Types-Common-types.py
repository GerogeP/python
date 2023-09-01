"""
None，type(None)或Literal[None]只允许None值


bool 布尔类型


int 整数类型


float 浮点数类型


str 字符串类型


bytes 字节类型


list 允许list,tuple,set,frozenset,deque, 或生成器并转换为列表


tuple 允许list,tuple,set,frozenset,deque, 或生成器并转换为元组


dict 字典类型


set 允许list,tuple,set,frozenset,deque, 或生成器和转换为集合；


frozenset 允许list,tuple,set,frozenset,deque, 或生成器和强制转换为冻结集


deque 允许list,tuple,set,frozenset,deque, 或生成器和强制转换为双端队列


datetime 的date,datetime,time,timedelta 等日期类型


typing 中的 Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union，Callable，Pattern等类型


FilePath，文件路径


DirectoryPath 目录路径


EmailStr 电子邮件地址


NameEmail 有效的电子邮件地址或格式


PyObject 需要一个字符串并加载可在该虚线路径中导入的 python 对象；


Color 颜色类型


AnyUrl 任意网址


SecretStr、SecretBytes 敏感信息，将被格式化为'**********'或''


Json 类型


PaymentCardNumber 支付卡类型


约束类型，可以使用con*类型函数限制许多常见类型的值

conlist




item_type: Type[T]: 列表项的类型
min_items: int = None: 列表中的最小项目数
max_items: int = None: 列表中的最大项目数


conset


item_type: Type[T]: 设置项目的类型
min_items: int = None: 集合中的最小项目数
max_items: int = None: 集合中的最大项目数


conint


strict: bool = False: 控制类型强制
gt: int = None: 强制整数大于设定值
ge: int = None: 强制整数大于或等于设定值
lt: int = None: 强制整数小于设定值
le: int = None: 强制整数小于或等于设定值
multiple_of: int = None: 强制整数为设定值的倍数


confloat


strict: bool = False: 控制类型强制
gt: float = None: 强制浮点数大于设定值
ge: float = None: 强制 float 大于或等于设定值
lt: float = None: 强制浮点数小于设定值
le: float = None: 强制 float 小于或等于设定值
multiple_of: float = None: 强制 float 为设定值的倍数


condecimal


gt: Decimal = None: 强制十进制大于设定值
ge: Decimal = None: 强制十进制大于或等于设定值
lt: Decimal = None: 强制十进制小于设定值
le: Decimal = None: 强制十进制小于或等于设定值
max_digits: int = None: 小数点内的最大位数。它不包括小数点前的零或尾随的十进制零
decimal_places: int = None: 允许的最大小数位数。它不包括尾随十进制零
multiple_of: Decimal = None: 强制十进制为设定值的倍数


constr


strip_whitespace: bool = False: 删除前尾空格
to_lower: bool = False: 将所有字符转为小写
strict: bool = False: 控制类型强制
min_length: int = None: 字符串的最小长度
max_length: int = None: 字符串的最大长度
curtail_length: int = None: 当字符串长度超过设定值时，将字符串长度缩小到设定值
regex: str = None: 正则表达式来验证字符串


conbytes


strip_whitespace: bool = False: 删除前尾空格
to_lower: bool = False: 将所有字符转为小写
min_length: int = None: 字节串的最小长度
max_length: int = None: 字节串的最大长度



严格类型，您可以使用StrictStr，StrictBytes，StrictInt，StrictFloat，和StrictBool类型，以防止强制兼容类型

作者：青火_
链接：https://juejin.cn/post/7079027549896081421
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""

