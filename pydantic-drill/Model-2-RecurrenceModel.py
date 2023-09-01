'''
可以使用模型本身作为注释中的类型来定义更复杂的数据结构。
'''

from typing import List
from pydantic import BaseModel

class Foo(BaseModel):
    count: int
    size: float = None

class Bar(BaseModel):
    apple = 'x'
    banana = 'y'

class Spam(BaseModel):
    foo: Foo
    Bars: List[Bar]


if __name__ == '__main__':
    print(Spam)
   # print(dir(Spam))
    print(Spam.__config__)
    print(Spam.__class__)
    print(Spam.__class_vars__)

