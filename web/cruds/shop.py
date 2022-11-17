from distutils.sysconfig import get_python_lib
from typing import Any, Dict, List, Optional, Union
from unicodedata import category
from fastapi.encoders import jsonable_encoder
from cruds.base import CRUDBase
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union , List
from web.chemas.shop import ShopCreate , ShopUpdate
from models.shop import Shop
from sqlalchemy.orm import Session
from utils.auth_utils import Auth

from chemas.shop import ShopCreate, ShopUpdate


class CRUDShop(CRUDBase[ Shop , ShopCreate , ShopUpdate ]):

    def getById(self, db : Session , id : str ) -> Optional[Shop] : 
        return db.query(Shop).filter(Shop.id == id).one_or_none()

    def getByName(self, db : Session , name : str ) -> Optional[Shop] : 
        return db.query(Shop).filter(Shop.name == name).one_or_none()

    def create(self, db: Session , obj_in : ShopCreate) -> Shop:
        db_obj = Shop( 
                name = obj_in.name,
                link = obj_in.link,

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getData(self, db : Session , skip : int = 0 , limit : int = 100):
        return db.query(Shop).offset(skip).limit(limit).all()

    def update(self, db: Session , id : int , db_obj :Shop , obj_in : Union[ ShopUpdate , Dict[str , Any]] ) -> Shop:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else: 
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in obj_data:
                setattr(db_obj , field , update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
     
    def remove(self, db: Session , shopId : int ):
        data = db.query(Shop).filter(Shop.id == shopId).one_or_none()
        data.delete()
        db.commit()
        return data

shop =CRUDShop(Shop)