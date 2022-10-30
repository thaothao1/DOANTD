from distutils.sysconfig import get_python_lib
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.district import DistrictCreate, DistrictUpdate
from models.district import District
from utils.auth_utils import Auth

class CRUDDistrict(CRUDBase[ District , DistrictCreate , DistrictUpdate ]):

    def getById(self, db : Session , districtId : str ) -> Optional[District] : 
        return db.query(District).filter(District.id == districtId).one_or_none()
    
    def create(self, db: Session , obj_in : DistrictCreate) ->District:
        auth_handler = Auth()
        db_obj = District( 
                district = obj_in.district ,
                provinceId = obj_in.provinceId
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(District).offset(skip).limit(limit).all()

    # def update(self, db: Session , districtId : int , obj_in : DistrictUpdate ):
    #     data = db.query(District).filter(District.id == districtId).one_or_none()
     
    def remove(self, db: Session , districtId : int ):
        data = db.query(District).filter(District.id == districtId).one_or_none()
        data.delete()
        db.commit()
        return data

districts =CRUDDistrict(District)











