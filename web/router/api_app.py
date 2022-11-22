from typing import List, Optional , Union
import cruds 
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from models.product import Product
from models.shop import Shop
from router.utils import custom_reponse
from sqlalchemy.orm import Session
from db.get_db import get_db
from pydantic import BaseModel



app = APIRouter()

def paginate(data , page , size):
    data_size = len(data)
    start = (page -1 ) * size
    end = start + size
    response = {
        "data":data[start:end],
        "total": data_size,
        "count" : size,
    }
    return response

@app.get("/allProductShow")
def getListShowProduct(request: Request,db: Session = Depends(get_db) , page_num : Optional[int] = None , size : Optional[int] = None ):
    show = cruds.showProduct.getData(db)
    base = []
    for s in show:
        datas = {}
        shop1 = None
        shop2 = None
        shop3 = None
        shop4 = None
        data1 = cruds.product.getProduct(db , s.fptId)
        if (data1 != None):
            shop1 = cruds.shop.getByIdShop(db , data1.shopId)
        data2 = cruds.product.getProduct(db , s.lazadaId)
        if (data2 != None):
            shop2 = cruds.shop.getByIdShop(db , data2.shopId)
        data3 = cruds.product.getProduct(db , s.thegioididongId)
        if (data3 != None):
            shop3 = cruds.shop.getByIdShop(db , data3.shopId)
        data4 = cruds.product.getProduct(db , s.shopeeId)
        if (data4 != None):
            shop4 = cruds.shop.getByIdShop(db , data4.shopId)

        datas = {
            "show_product" : s,
            "product1" : data1,
            "shop1" : shop1,
            "product2" : data2,
            "shop2" : shop2,
            "product3" : data3,
            "shop3" : shop3,
            "product4" : data4,
            "shop4" : shop4,
        }
        base.append(datas)
    data_size = len(base)
    start = (page_num -1 ) * size
    end = start + size
    response = {
        "data":base[start:end],
        "total": data_size,
        "count" : size,
    }
    return custom_reponse(http_status=200 , data= response)


@app.get("/allProductFPT")
def getAllProduct(db: Session = Depends(get_db)  , page : Optional[int] = None , size : Optional[int] = None):
    shop = cruds.shop.getByName(db , "fpt")
    print(shop)
    product = cruds.product.getManyDataByShopId(db , shop.id)
    return custom_reponse(http_status=200 , data= { "shop" : shop , "product" : paginate(product,page,size)})

@app.get("/allProductLazada")
def getAllProduct(db: Session = Depends(get_db)  , page : Optional[int] = None , size : Optional[int] = None):
    shop = cruds.shop.getByName(db , "lazada")
    product = cruds.product.getManyDataByShopId(db , shop.id)
    return custom_reponse(http_status=200 , data= { "shop" : shop , "product" : paginate(product,page,size)})


@app.get("/allProductShopee")
def getAllProduct(db: Session = Depends(get_db)  , page : Optional[int] = None , size : Optional[int] = None):
    shop = cruds.shop.getByName(db , "Shopee")
    product = cruds.product.getManyDataByShopId(db , shop.id)
    return custom_reponse(http_status=200 , data= { "shop" : shop , "product" : paginate(product,page,size)})

@app.get("/allProductThegioididong")
def getAllProduct(db: Session = Depends(get_db)  , page : Optional[int] = None , size : Optional[int] = None, label : Optional[str] = None):
    shop = cruds.shop.getByName(db , "Thế giới di động")
    if (label is not None):
        Label = cruds.label.getByName(db , label)
        print(Label.id)
        # product = cruds.product.getProductByShopAndLabel(db ,shop.id , labelId.id)
        product = db.query(Product).filter(Product.shopId == shop.id and Product.labelId == Label.id).all()
        print(product)
    else:
        product = cruds.product.getManyDataByShopId(db , shop.id)
    return custom_reponse(http_status=200 , data= { "shop" : shop , "product" : paginate(product,page,size)})

