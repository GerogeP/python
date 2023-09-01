"""
在某些情况下，直到运行时才知道模型的结构。为此 pydantic 提供了create_model允许动态创建模型的方法。
"""
from pydantic import BaseModel, create_model

DynamicFoobarModel = create_model('DynamicFoobarModel', foo=(str, ...), bar=123)

