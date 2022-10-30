from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):

    id : Optional[int]
    category : Optional[str]
    link : Optional[str]
    shopId : Optional[int]

class CategoryInDBBase(CategoryBase):
    class Config:
        orm_model = True

class CategoryCreate(CategoryBase):
    id : int
    category : str
    link : str
    shopId : int

class CategoryUpdate(CategoryBase):
    id : int
    category : str
    link : str
    shopId : int

    