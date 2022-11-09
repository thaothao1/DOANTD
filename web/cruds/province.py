from distutils.sysconfig import get_python_lib
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.province import  ProvinceCreate ,ProvinceUpdate
from models.province import Province
from utils.auth_utils import Auth

class CRUDProvince(CRUDBase[ Province ,  ProvinceCreate , ProvinceUpdate  ]):

    def getById(self, db : Session , provinceId : str ) -> Optional[Province] : 
        return db.query(Province).filter(Province.id == provinceId).one_or_none()
    
    def create(self, db: Session , obj_in : ProvinceCreate) ->Province:
        auth_handler = Auth()
        db_obj = Province( 
                province = obj_in.province
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Province).offset(skip).limit(limit).all()

    # def update(self, db: Session , districtId : int , obj_in : DistrictUpdate ):
    #     data = db.query(District).filter(District.id == districtId).one_or_none()
     
    def remove(self, db: Session , provinceId : int ):
        data = db.query(Province).filter(Province.id == provinceId).one_or_none()
        data.delete()
        db.commit()
        return data

province =CRUDProvince(Province)











