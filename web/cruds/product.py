from cProfile import label
from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from utils.auth_utils import Auth
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.product import ProductCreate , ProductUpdate
from models.product import Product
import cruds

class CRUDProduct(CRUDBase[ Product , ProductCreate , ProductUpdate ]):

    def getById(self, db: Session , id : str )->Optional[Product]:
        return db.query(Product).filter(Product.id == id).one_or_none()

    def getByName(self, db: Session , name : str )->Optional[Product]:
        return db.query(Product).filter(Product.name == name).one_or_none()

    def getProduct(self, db: Session , id : int )->Optional[Product]:
        return db.query(Product).filter(Product.id == id).one_or_none()

    def getManyDataByShopId(self, db: Session , shop : int )->Optional[Product]:
        return db.query(Product).filter(Product.shopId == shop).all()

    def getProductByShopAndLabel(self, db : Session , shop : int , labelId : int):
        return db.query(Product).filter(Product.shopId == shop and Product.labelId == labelId).all()

    def create(self, db: Session , obj_in : ProductCreate ) -> Product:
        auth_handler = Auth()
        db_obj = Product(
                name = obj_in.name ,
                link = obj_in.link,
                image = obj_in.image ,
                price = obj_in.price,
                priceSale = obj_in.priceSale,
                rating = obj_in.rating,
                shopId = obj_in.shopId,
                labelId = obj_in.labelId
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
