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
        data= db.query(ShowProduct).filter(ShowProduct.id == id).first()
        return data

    def getByName(self, db: Session , name : str )->Optional[ShowProduct]:
        return db.query(ShowProduct).filter(ShowProduct.name == name).one_or_none()

    
    def getProduct(self, db: Session , id : int )->Optional[ShowProduct]:
        return db.query(ShowProduct).filter(ShowProduct.id == id).one_or_none()

    def getProductByLabel(self, db: Session , label : int ) -> Optional[ShowProduct]:
        return db.query(ShowProduct).filter(ShowProduct.labelId == label).all()

    def getProductByCategory(self, db: Session , category : int)-> Optional[ShowProduct]:
        return db.query(ShowProduct).filter(ShowProduct.categoryId == category).all()

    def getProductByShopAndLabel(self, db : Session , labelId : int ):
        return db.query(ShowProduct).filter( ShowProduct.labelId == labelId).all()

    def getProductByShopAndCategory(self, db : Session , category : int):
        return db.query(ShowProduct).filter(ShowProduct.categoryId == category).all()

    def getProductByShopAndLabelAndCategory(self , db :Session , label : int , category : int):
        return  db.query(ShowProduct).filter(ShowProduct.labelId == label , ShowProduct.categoryId == category).all()

    def getProductByCategoryAndLabel(self, db: Session , category : int , label: int):
        return db.query(ShowProduct).filter(ShowProduct.categoryId == category , ShowProduct.labelId == label).all()

    def create(self, db: Session , obj_in : ShowProductCreate ) -> ShowProduct:
        db_obj = ShowProduct(
            name = obj_in.name,
            price = obj_in.price,
            image = obj_in.image,
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

    def getData(self, db : Session):
        return db.query(ShowProduct).all()

    def update(self, db: Session , id : int , obj_in : ShowProductUpdate ):
        data = self.getById(db,id)
        data.name = obj_in.name,
        data.price = obj_in.price,
        data.image = obj_in.image,
        data.thegioididongId = obj_in.thegioididongId,
        data.lazadaId = obj_in.lazadaId,
        data.fptId = obj_in.fptId,
        data.shopeeId = obj_in.shopeeId,
        data.labelId = obj_in.labelId,
        data.view = obj_in.view
        db.commit()
        db.refresh(data)
        return data
        
    def search(self , db: Session , query : str):
        name = db.query(ShowProduct).filter(ShowProduct.name.contains(query)).all()
        # name = db.query(ShowProduct).filter(ShowProduct.name.like('%{query}%')).all()
        # # name = db.query(ShowProduct).filter(lambda ShowPro.lower() , ShowProduct) 
        return name
    
    def searchCategory(self , db: Session , query : str, categoryID: int):
        name = db.query(ShowProduct).filter(ShowProduct.name.contains(query), ShowProduct.categoryId == categoryID).all()
        return name

    def remove(self, db: Session , id : int ):
        data = db.query(ShowProduct).filter(ShowProduct.id == id ).one_or_none()
        data.delete()
        db.commit()
        return data

showProduct =CRUDShowProduct(ShowProduct)
