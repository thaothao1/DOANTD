from pydantic import BaseModel
from typing import Optional

class DistrictBase(BaseModel):

    id : Optional[int]
    district : Optional[str]
    provinceId : Optional[int]

class DistrictInDBBase(DistrictBase):
    class Config:
        orm_model = True

class DistrictCreate(DistrictBase):
    id : int
    district: str
    provinceId: int

class DistrictUpdate(DistrictBase):
    id : int
    district: str
    provinceId: int

    