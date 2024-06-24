# coding:utf-8
from typing import Optional

from pydantic import BaseModel


class ChatIn(BaseModel):
    influencer_name: Optional[str] = "",
    influencer_tags: Optional[str] = "",
    materials: Optional[str] = "",
    dialog: Optional[str] = "",
