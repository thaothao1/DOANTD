from pydantic import BaseModel
from typing import Optional


class LabelBase(BaseModel):
    id : Optional[int]
    name : Optional[str]


class LabelInBase(LabelBase):
    class Config:
        orm_model = True

class LabelCreate(LabelBase):
    name : str


class LabelUpdate(LabelBase):
    name : str


    