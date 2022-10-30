from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):

    id : Optional[int]
    product : Optional[str]
    link : Optional[str]
    image : Optional[str]
    price : Optional[str]
    priceSale : Optional[str]
    color : Optional[str]
    size : Optional[str]
    description : Optional[str]
    quantity : Optional[int]
    id_district : Optional[int]
    labelId : Optional[int]

class ProductInDBBase(ProductBase):
    class Config:
        orm_model = True

class ProductCreate(ProductBase):
    id : int
    product : str
    link : str
    image : str
    price : str
    priceSale : str
    color : str
    size : str
    description : str
    quantity :  int
    id_district : int
    labelId : int

class ProductUpdate(ProductBase):
    id : int
    product : str
    link : str
    image : str
    price : str
    priceSale : str
    color : str
    size : str
    description : str
    quantity :  int
    id_district : int
    labelId : int
