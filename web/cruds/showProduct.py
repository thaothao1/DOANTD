from distutils.sysconfig import get_python_lib
import json
from typing import Any, Dict, List, Optional, Union
from unicodedata import category
from fastapi.encoders import jsonable_encoder
from models.showProduct import ShowProduct
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from chemas.showProduct import ShowProductCreate, ShowProductUpdate


class CRUDShowProduct(CRUDBase[ ShowProduct , ShowProductCreate , ShowProductUpdate ]):

    def getById(self, db: Session , id : int )->Optional[ShowProduct]:
        return db.query(ShowProduct).filter(ShowProduct.id == id).one_or_none()

    def getByName(self, db: Session , name : str )->Optional[ShowProduct]:
        return db.query(ShowProduct).filter(ShowProduct.name == name).one_or_none()

    def create(self, db: Session , obj_in : ShowProductCreate ) -> ShowProduct:
        db_obj = ShowProduct(
            name = obj_in.name,
            price = obj_in.price,
            thegioididongId = obj_in.thegioididongId,
            lazadaId = obj_in.lazadaId,
            fptId = obj_in.fptId,
            shopeeId = obj_in.shopeeId,
            labelId = obj_in.labelId,
            categoryId = obj_in.categoryId,
            view = obj_in.view
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(ShowProduct).offset(skip).limit(limit).all()

    def update(self, db: Session , id : int , obj_in : ShowProductUpdate ):
        data = self.getById(db,id)
        # data.name = obj_in.name,
        # data.price = obj_in.price,
        # data.thegioididongId = obj_in.thegioididongId,
        # data.lazadaId = obj_in.lazadaId,
        # data.fptId = obj_in.fptId,
        # data.shopeeId = obj_in.shopeeId,
        # data.labelId = obj_in.labelId,
        data.view = obj_in.view
        db.commit()
        db.refresh(data)
        return data
        
    def search(self , db: Session , query : str):
        name = db.query(ShowProduct).filter(ShowProduct.name.contains(query)).all()
        # name = db.query(ShowProduct).filter(ShowProduct.name.like('%query%'))
        # name = db.query(ShowProduct).filter(lambda ShowProduct : query.lower() in ShowProduct["name"].lower() , ShowProduct) 
        return name

    def remove(self, db: Session , id : int ):
        data = db.query(ShowProduct).filter(ShowProduct.id == id ).one_or_none()
        data.delete()
        db.commit()
        return data

showProduct =CRUDShowProduct(ShowProduct)