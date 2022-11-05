from pydantic import BaseModel
from typing import Optional
from models.village import Village


class VillageBase(BaseModel):

    id : Optional[int]
    village : Optional[str]
    provinceId : Optional[int]
    districtId : Optional[int]

class VillageInBase(VillageBase):
    class Config:
        orm_model = True

class VillageCreate(VillageBase):
    id : int
    village : str
    provinceId : int
    districtId : int

class VillageUpdate(VillageBase):
    id : int
    village : str
    provinceId : int
    districtId : int

    