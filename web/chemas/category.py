from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    id : Optional[int]
    name : Optional[str]


class CategoryInBase(CategoryBase):
    class Config:
        orm_model = True

class CategoryCreate(CategoryBase):
    name : str


class CategoryUpdate(CategoryBase):
    name : str


    