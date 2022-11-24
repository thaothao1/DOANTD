from distutils.sysconfig import get_python_lib
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.category import CategoryCreate , CategoryUpdate
from models.category import Category
from fastapi.encoders import jsonable_encoder


class CRUDCategory(CRUDBase[ Category , CategoryCreate , CategoryUpdate]):

    def getById(self, db: Session , id : str)->Optional[Category]:
        return db.query(Category).filter(Category.id == id).one_or_none()

    def getByName(self, db: Session , name : str )-> Optional[Category]:
        return db.query(Category).filter(Category.name == name).one_or_none()

    def create(self, db: Session , obj_in : CategoryCreate)-> Category:
        db_obj = Category(
            name = obj_in.name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session , id: int , obj_in : CategoryUpdate ) -> Category:
        data = self.getById(db , id)
        data.name = obj_in.name
        db.commit()
        db.refresh(data)
        return data

    def remove(self, db: Session , id : int ):
        data = db.query(Category).filter(Category.id == id).one_or_none()
        data.delete()
        db.commit()
        return data

category = CRUDCategory(Category)
