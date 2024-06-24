# coding:utf-8
from typing import Optional, Union

from pydantic import BaseModel


class PromotionCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    site_id: str
    affiliate_id: Union[str, int]
    product_card: dict
    influencers_list: list


