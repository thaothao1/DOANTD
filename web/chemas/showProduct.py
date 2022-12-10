from pydantic import BaseModel
from typing import Optional

class ShowProductBase(BaseModel):

    id : Optional[int]
    name : Optional[str]
    price : Optional[str]
    image : Optional[str]
    thegioididongId : Optional[int]
    lazadaId : Optional[int]
    fptId : Optional[int]
    shopeeId : Optional[int]
    labelId : Optional[int]
    categoryId : Optional[int]
    view: Optional[int]

class ShowProductInBase(ShowProductBase):
    class Config:
        orm_model = True

class ShowProductCreate(ShowProductBase):
    name : str
    price : str
    image : str
    thegioididongId: int
    lazadaId: int
    fptId: int
    shopeeId: int
    labelId: int
    categoryId: int
    view : int


class ShowProductUpdate(ShowProductBase):
    name : str
    price : str
    image : str
    thegioididongId: int
    lazadaId: int
    fptId: int
    shopeeId: int
    labelId: int
    categoryId: int
    view: int
