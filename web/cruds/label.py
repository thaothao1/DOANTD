from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from utils.auth_utils import Auth
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from web.chemas.label import LabelUpdate ,LabelCreate
from models.label import Label
class CRUDProvince(CRUDBase[ Label , LabelCreate , LabelUpdate ]):

    def create(self, db: Session , obj_in : LabelCreate) -> Label:
        auth_handler = Auth()
        db_obj = Label( 
                label = obj_in.label,
                link = obj_in.link,
                categoryId = obj_in.categoryId
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Label).offset(skip).limit(limit).all()

    # def update(self, db: Session , districtId : int , obj_in : DistrictUpdate ):
    #     data = db.query(District).filter(District.id == districtId).one_or_none()
     
    def remove(self, db: Session , labelId : int ):
        data = db.query(Label).filter(Label.id == labelId).one_or_none()
        data.delete()
        db.commit()
