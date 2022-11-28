from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.label import LabelUpdate ,LabelCreate
from models.label import Label
from fastapi.encoders import jsonable_encoder

class CRUDLabel(CRUDBase[ Label , LabelCreate , LabelUpdate ]):

    def getById(self, db: Session , id : int )->Optional[Label]:
        return db.query(Label).filter(Label.id == id).one_or_none()

    def getByName(self, db: Session , name : str )->Optional[Label]:
        return db.query(Label).filter(Label.name == name).one_or_none()

    def getByCate(self, db: Session , id : int )->Optional[Label]:
        return db.query(Label).filter(Label.categoryId == id).all()

    def create(self, db: Session , obj_in : LabelCreate) -> Label:
        db_obj = Label( 
            name = obj_in.name,
            categoryId = obj_in.categoryId
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session ):
        return db.query(Label).all()

    def update(self, db: Session , id : int , obj_in : LabelUpdate) -> Label:
        data = self.getById(db , id)
        data.name = obj_in.name
        db.commit()
        db.refresh(data)
        return data
     
    def remove(self, db: Session , labelId : int ):
        data = db.query(Label).filter(Label.id == labelId).one_or_none()
        data.delete()
        db.commit()
        return data

label =CRUDLabel(Label)   
