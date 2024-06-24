# coding:utf-8
from typing import Optional, Union

from fastapi import Query
from pydantic import BaseModel


class ProductCardsBase(BaseModel):
    site_id: str
    product_card_id: Union[str, int]
    product_name: str
    commission_rate: Optional[int] = 0
    params: Union[str, None] = None


class ProductCardsUpdate(ProductCardsBase):
    id: int
