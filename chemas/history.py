from pydantic import BaseModel
from typing import Optional

class HistoryBase(BaseModel):
    id : Optional[int]
    productId : Optional[int]
    view : Optional[int]

class HistoryInBase(HistoryBase):
    class Config: 
        orm_model : True

class HistoryCreate(HistoryBase):
    productId : int
    view : int

class HistoryUpdate(HistoryBase):
    productId : int
    view : int


    