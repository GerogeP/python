"""

    关键字参数 always 将导致始终验证，出于性能原因，默认情况下，当未提供值时，不会为字段调用验证器。然而，在某些情况下，始终调用验证器可能很有用或需要，例如设置动态默认值。
    allow_reuse 可以在多个字段/模型上使用相同的验证器
"""

from pydantic import BaseModel, validator


def normalizer(name: str) -> str:
    return ' '.join((word.capitalize()) for word in name.split(' '))

    
class Producer(BaseModel):
    name: str

    # validators
    _normalize_name = validator('name', allow_reuse=True)(normalize)


class Consumer(BaseModel):
    name: str

    # validators
    _nomalize_name = validator('name', allow_reuse=True)(normalize)

