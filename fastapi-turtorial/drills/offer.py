from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID

from fastapi import Cookie, Body, Header, FastAPI, Query, Path
from pydantic import BaseModel, Field, HttpUrl,  Required

from items import Item 


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: list[Item]


