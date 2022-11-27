from pydantic import BaseModel
from typing import Optional


class LabelBase(BaseModel):
    id : Optional[int]
    name : Optional[str]
    categoryId : Optional[int]


class LabelInBase(LabelBase):
    class Config:
        orm_model = True

class LabelCreate(LabelBase):
    name : str
    categoryId : int


class LabelUpdate(LabelBase):
    name : str
    categoryId : int


    