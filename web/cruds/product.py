from cProfile import label
from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from utils.auth_utils import Auth
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.product import ProductCreate , ProductUpdate
from models.product import Product

class CRUDProduct(CRUDBase[ Product , ProductCreate , ProductUpdate ]):

    def getById(self, db: Session , productId : str )->Optional[Product]:
        return db.query(Product).filter(Product.id == productId).one_or_none()

    def getByName(self, db: Session , name : str )->Optional[Product]:
        return db.query(Product).filter(Product.product == name).one_or_none()

    def create(self, db: Session , obj_in : ProductCreate ) -> Product:
        auth_handler = Auth()
        db_obj = Product(
                product = obj_in.product,
                link = obj_in.link,
                image = obj_in.image ,
                price = obj_in.price,
                priceSale = obj_in.priceSale,
                color = obj_in.color,
                size = obj_in.size,
                description = obj_in.description,
                 = obj_in.quantity,
                # id_district = obj_in.id_district,
                # labelId = obj_in.labelId,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Product).offset(skip).limit(limit).all()

    # def update(self, db: Session , districtId : int , obj_in : DistrictUpdate ):
    #     data = db.query(District).filter(District.id == districtId).one_or_none()
     
    def remove(self, db: Session , productId : int ):
        data = db.query(Product).filter(Product.id == productId ).one_or_none()
        data.delete()
        db.commit()
        return data


product =CRUDProduct(Product)
