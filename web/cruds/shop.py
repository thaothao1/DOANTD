from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from utils.auth_utils import Auth
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from web.chemas.shop import ShopCreate , ShopUpdate
from models.shop import Shop
class CRUDProvince(CRUDBase[ Shop , ShopCreate , ShopUpdate ]):

    def create(self, db: Session , obj_in : ShopCreate) -> Shop:
        auth_handler = Auth()
        db_obj = Shop( 
                shop = obj_in.shop,
                link = obj_in.link,

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Shop).offset(skip).limit(limit).all()

    # def update(self, db: Session , districtId : int , obj_in : DistrictUpdate ):
    #     data = db.query(District).filter(District.id == districtId).one_or_none()
     
    def remove(self, db: Session , shopId : int ):
        data = db.query(Shop).filter(Shop.id == shopId).one_or_none()
        data.delete()
        db.commit()