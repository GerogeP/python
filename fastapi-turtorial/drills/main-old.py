from datetime import datetime, time, timedelta
from typing import Any, Union
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


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(title="The ID of the item toi get", default=1, gt=0, le=1000),
):
    return {"item_id": item_id, "q": q}


# async def read_items(q: str = Query(min_length=3)):
# async def read_items(q: str = Query(default=..., min_length=3)):    
# async def read_items(q: str=Query(default=Required, min_length=3)):    

"""
async def read_items(*,
                     user_agent: Union[str, None] = Header(default=None),
                     ads_id: Union[str, None] = Cookie(default=None),
        q: Union[str, None] = Query(default=None, \
            title="Query string", 
        description="Query string for the items to search in the database " \
    + "that have a good match", \
         min_length=3,  
         max_length=50,
         regex="^fixedquery"),
         size: float = Query(gt=0, lt=10.5)            
        ) -> Any:

    result =  [{"item_id": 0}, {"item_id": 1}]
"""
@app.get("/items/")
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Pli=umbus", "price": 32.0
        }]


@app.post("/items/", response_model=Item)
async def create_item(item: Item) :
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


@app.put("/items/{item_id}")
async def update_item(
    *, 
    item_id: UUID, 
    start_datetime: Union[datetime, None] = Body(default=None),
    end_datetime: Union[datetime, None] = Body(default=None),
    repeat_at: Union[time, None] = Body(default=None),
    process_after: Union[timedelta, None] = Body(default=None),
    item: Item = Body(
        embed=True, 
        examples={
            "normal": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can converte price 'strings' to actual"
                + "numbers automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with error",
                "value": {
                    "name": "Bar",
                    "price": "thirty five point four",
                },
            },
        }), 
    user: User,
    importance: int = Body(gt=0),
    q: Union[str, None] = None
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process

    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
        print(result)
        
    return result

    # return {"item_name": item.name, "item_id": item_id, "item_price":
    #    item.price, **item.dict()} 

