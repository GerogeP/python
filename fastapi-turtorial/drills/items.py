from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID

from fastapi import Cookie, Body, Header, FastAPI, Query, Path
from pydantic import BaseModel, Field, HttpUrl,  Required

from app import app, Image, Item, Offer, User 


@app.get("/items/{item_id}")
async def read_item(item_id: int, ):
    return {"item_id": item_id, "q": q}


@app.get("/items/")
# async def read_items(q: str = Query(min_length=3)):
# async def read_items(q: str = Query(default=..., min_length=3)):    
# async def read_items(q: str=Query(default=Required, min_length=3)):    
async def read_items(*,
                     user_agent: Union[str, None] = Header(default=None),
                     ads_id: Union[str, None] = Cookie(default=None),
    item_id: int = Path(title="The ID of the item toi get", gt=0, le=1000),
        q: Union[str, None] = Query(default=None, \
            title="Query string", 
        description="Query string for the items to search in the database " \
    + "that have a good match", \
         min_length=3,  
         max_length=50,
         regex="^fixedquery"),
         size: float = Query(gt=0, lt=10.5)            
        ):

    result = {"items": [{"item_id": "Foo"}, {"item_id":"Bar"}]}
    if q:
        result.update({"q": q})
    return result

                    # return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item) -> dict:
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

