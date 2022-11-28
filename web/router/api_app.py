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


@app.get("/allProduct")
def getAllProduct(db: Session = Depends(get_db)  , page : Optional[int] = None , size : Optional[int] = None, label : Optional[int] = None , shop : Optional[int] = None , category : Optional[int] = None):
    shopId = cruds.shop.getById(db , shop)
    if (shopId is not None):
        if ( category is not None):
            categoryId = cruds.category.getById(db , category)
            if (label is not None):
                Label = cruds.label.getById(db , label)
                product = cruds.product.getProductByShopAndLabelAndCategory(db ,shopId.id , Label.id , categoryId.id )
            else:
                label = None
                product = cruds.product.getProductByShopAndCategory(db , shopId.id , categoryId.id)
        else:
            if (label is not None):
                Label = cruds.label.getById(db , label)
                product = cruds.product.getProductByShopAndLabel(db ,shopId.id , Label.id)
            else:
                label = None
                product = cruds.product.getManyDataByShopId(db , shopId.id)

    else:
        if ( category is not None):
            categoryId = cruds.category.getById(db , category)
            if (label is not None):
                Label = cruds.label.getById(db , label)
                product = cruds.product.getProductByCategoryAndLabel(db,Label.id , categoryId.id )
            else:
                label = None
                product = cruds.product.getProductByCategory(db , categoryId.id)
        else:
            if (label is not None):
                Label = cruds.label.getById(db , label)
                product = cruds.product.getProductByLabel(db , Label.id)
            else:
                label = None
                product = cruds.product.getData(db)

    return custom_reponse(http_status=200 , data= { "shop" : shopId , "product" : paginate(product,page,size)})


@app.get("/allShowProduct")
def getAllProduct(db: Session = Depends(get_db)  , page : Optional[int] = None , size : Optional[int] = None, label : Optional[int] = None , category : Optional[int] = None):
    if ( category is not None):
        categoryId = cruds.category.getById(db , category)
        if (label is not None):
            Label = cruds.label.getById(db , label)
            product = cruds.showProduct.getProductByShopAndLabelAndCategory(db , Label.id , categoryId.id )
        else:
            label = None
            product = cruds.showProduct.getProductByShopAndCategory(db , categoryId.id)
    else:
        if (label is not None):
            Label = cruds.label.getById(db , label)
            product = cruds.showProduct.getProductByShopAndLabel(db , Label.id)
        else:
            label = None
            product = cruds.showProduct.getData()
    return custom_reponse(http_status=200 , data= { "data" : paginate(product,page, size )})