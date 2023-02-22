from pydantic import BaseModel, Field, HttpUrl,  Required


class Image(BaseModel):
    url: HttpUrl 
    name: str


