from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from utils.auth_utils import Auth
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.label import LabelUpdate ,LabelCreate
from models.label import Label

class CRUDLabel(CRUDBase[ Label , LabelCreate , LabelUpdate ]):

    def getById(self, db: Session , id : str )->Optional[Label]:
        return db.query(Label).filter(Label.id == id).one_or_none()

    def getByName(self, db: Session , name : str )->Optional[Label]:
        return db.query(Label).filter(Label.name == name).one_or_none()

    def create(self, db: Session , obj_in : LabelCreate) -> Label:
        auth_handler = Auth()
        db_obj = Label( 
                name = obj_in.name,
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
        return data

label =CRUDLabel(Label)   
