from pydantic import BaseModel
from typing import Optional
from models.village import Village

class LabelBase(BaseModel):

    id : Optional[int]
    label : Optional[str]
    link : Optional[str]
    categoryId : Optional[str]

class LabelInBase(LabelBase):
    class Config:
        orm_model = True

class LabelCreate(LabelBase):
    id : int
    label : str
    link : str
    categoryId : str

class LabelUpdate(LabelBase):
    id : int
    label : str
    link : str
    categoryId : str

    