from pydantic import BaseModel
from typing import Optional

class ProvinceBase(BaseModel):

    id : Optional[int]
    province : Optional[str]

class ProvinceInBase(ProvinceBase):
    class Config:
        orm_model = True

class ProvinceCreate(ProvinceBase):
    province: str

class ProvinceUpdate(ProvinceBase):
    province: str

    