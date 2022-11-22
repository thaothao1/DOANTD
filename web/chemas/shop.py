from pydantic import BaseModel
from typing import Optional

class ShopBase(BaseModel):

    id : Optional[int]
    name : Optional[str]
    link : Optional[str]

class ShopInBase(ShopBase):
    class Config:
        orm_model = True

class ShopCreate(ShopBase):
    name : str
    link : str

class ShopUpdate(ShopBase):
    name : str
    link = str


    