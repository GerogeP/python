from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID

from fastapi import Cookie, Body, Header, FastAPI, Query, Path
from pydantic import BaseModel, Field, HttpUrl,  Required

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl 
    name: str


class Item(BaseModel):
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(
        default=None, 
        title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0,
        description="The price must be greater than zero",
        example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2) 
#    price_with_tax: int
    is_offer: Union[bool, None] = None
    tags: set[str] = set()
    image: Union[list[Image], None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


