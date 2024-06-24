# coding:utf-8
from typing import Optional, Union

from pydantic import BaseModel


class AffiliateBase(BaseModel):
    site_id: str
    affiliate_account: str
    nickname: Union[str, None] = ""
    home_page: Union[str, None] = ""


class AffiliateUpdate(AffiliateBase):
    id: int
