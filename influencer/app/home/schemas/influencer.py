# coding:utf-8
import json
from typing import Any, Dict, Optional

from pydantic import BaseModel


class InfluencerIn(BaseModel):
    site_id: Optional[str] = ""
    influencer_account: Optional[str] = ""
    param: Optional[str] = ""


class InfluencerUpdate(BaseModel):
    influencer_account: Optional[str] = ""
    param: Optional[str] = ""


class InfluencerDBOut(BaseModel):
    id: int
    site_id: str
    influencer_account: str
    param: dict
