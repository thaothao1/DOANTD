from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    
    id : Optional[int]
    name : Optional[str]
    link : Optional[str]
    image : Optional[str]
    price : Optional[str]
    priceSale : Optional[str]
    rating : Optional[str]
    shopId : Optional[int]



class ProductInDBBase(ProductBase):
    class Config:
        orm_model = True

class ProductCreate(ProductBase):
    name : str
    link : str
    image : str
    price : str
    priceSale : str
    rating : str
    shopId: int




class ProductUpdate(ProductBase):
    name : str
    link : str
    image : str
    price : str
    priceSale : str
    rating : str
    shopId : int

