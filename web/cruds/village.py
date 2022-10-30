from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from utils.auth_utils import Auth
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from web.chemas.village import VillageCreate , VillageUpdate
from models.village import Village
class CRUDProvince(CRUDBase[ Village , VillageCreate , VillageUpdate ]):

    def create(self, db: Session , obj_in : VillageCreate) -> Village:
        auth_handler = Auth()
        db_obj = Village( 
                Village = obj_in.village,
                provinceId = obj_in.provinceId,
                district = obj_in.districtId
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Village).offset(skip).limit(limit).all()

    # def update(self, db: Session , districtId : int , obj_in : DistrictUpdate ):
    #     data = db.query(District).filter(District.id == districtId).one_or_none()
     
    def remove(self, db: Session , villageId : int ):
        data = db.query(Village).filter(Village.id == villageId).one_or_none()
        data.delete()
        db.commit()