from pydantic import BaseModel
from typing import Optional

class ShowProductBase(BaseModel):

    id : Optional[int]
    name : Optional[str]
    price : Optional[str]
    thegioididongId : Optional[int]
    lazadaId : Optional[int]
    fptId : Optional[int]
    shopeeId : Optional[int]

class ShowProductInBase(ShowProductBase):
    class Config:
        orm_model = True

class ShowProductCreate(ShowProductBase):
    name : str
    price : str
    thegioididongId: int
    lazadaId: int
    fptId: int
    shopeeId: int


class ShowProductUpdate(ShowProductBase):
    name : str
    price : str
    thegioididongId: int
    lazadaId: int
    fptId: int
    shopeeId: int
