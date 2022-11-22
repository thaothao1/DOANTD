from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.category import CategoryCreate , CategoryUpdate
from models.category import Category

class CRUDProvince(CRUDBase[ Category, CategoryCreate , CategoryUpdate ]):

    def create(self, db: Session , obj_in : CategoryCreate) -> Category:
        db_obj = Category( 
                category = obj_in.category,
                link = obj_in.link,
                shopId = obj_in.shopId
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Category).offset(skip).limit(limit).all()

    # def update(self, db: Session , districtId : int , obj_in : DistrictUpdate ):
    #     data = db.query(District).filter(District.id == districtId).one_or_none()
     
    def remove(self, db: Session , labelId : int ):
        data = db.query(Category).filter(Category.id == labelId).one_or_none()
        data.delete()
        db.commit()