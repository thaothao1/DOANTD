from cProfile import label
from distutils.sysconfig import get_python_lib
from unicodedata import category
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from chemas.product import ProductCreate , ProductUpdate
from models.product import Product
import cruds

class CRUDProduct(CRUDBase[ Product , ProductCreate , ProductUpdate ]):

    def getById(self, db: Session , id : int )->Optional[Product]:
        data = db.query(Product).filter(Product.id == id).one_or_none()
        return data
        
    def getByName(self, db: Session , name : str )->Optional[Product]:
        return db.query(Product).filter(Product.name == name).one_or_none()

    def getProduct(self, db: Session , id : int )->Optional[Product]:
        return db.query(Product).filter(Product.id == id).one_or_none()

    def getManyDataByShopId(self, db: Session , shop : int )->Optional[Product]:
        return db.query(Product).filter(Product.shopId == shop).all()

    def getProductByLabel(self, db: Session , label : int ) -> Optional[Product]:
        return db.query(Product).filter(Product.labelId == label).all()

    def getProductByCategory(self, db: Session , category : int)-> Optional[Product]:
        return db.query(Product).filter(Product.categoryId == category).all()

    def getProductByShopAndLabel(self, db : Session , shop : int , labelId : int ):
        return db.query(Product).filter(Product.shopId == shop , Product.labelId == labelId).all()

    def getProductByShopAndCategory(self, db : Session , shop : int , category : int):
        return db.query(Product).filter(Product.shopId == shop , Product.categoryId == category).all()

    def getProductByShopAndLabelAndCategory(self , db :Session , shop: int , label : int , category : int):
        return  db.query(Product).filter(Product.shopId == shop , Product.labelId == label , Product.categoryId == category).all()

    def getProductByCategoryAndLabel(self, db: Session , category : int , label: int):
        return db.query(Product).filter(Product.categoryId == category , Product.labelId == label).all()
    
    def create(self, db: Session , obj_in : ProductCreate ) -> Product:
        db_obj = Product( 
                name = obj_in.name,
                link = obj_in.link,
                image = obj_in.image ,
                price = obj_in.price,
                priceSale = obj_in.priceSale,
                rating = obj_in.rating,
                shopId = obj_in.shopId,
                labelId = obj_in.labelId,
                categoryId = obj_in.categoryId,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Product).all()

    def update(self, db: Session , Id : int , obj_in : ProductUpdate ):
        data = self.getById(db , Id)
        data.name = obj_in.name
        data.link = obj_in.link
        data.image = obj_in.image
        data.price = obj_in.price
        data.priceSale = obj_in.priceSale
        data.rating = obj_in.rating
        data.shopId = obj_in.shopId
        data.labelId = obj_in.labelId
        data.categoryId = obj_in.categoryId
        db.commit()
        db.refresh(data)
        return data
        
    def remove(self, db: Session , productId : int ):
        data = db.query(Product).filter(Product.id == productId ).one_or_none()
        data.delete()
        db.commit()
        return data


product =CRUDProduct(Product)
