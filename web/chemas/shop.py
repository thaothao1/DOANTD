from pydantic import BaseModel
from typing import Optional

from webss.web.models.village import Village

class ShopBase(BaseModel):

    id : Optional[int]
    shop : Optional[str]
    link : Optional[str]

class ShopInBase(ShopBase):
    class Config:
        orm_model = True

class ShopCreate(ShopBase):
    id : int
    shop : str
    link : str

class ShopUpdate(ShopBase):
    id : int
    shop : str
    link = str


    