import json
from msilib.schema import Class
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from typing import Optional
from base.CodeHTML import CodeHTML
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.showProduct import ShowProduct
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.product import ProductCreate , ProductUpdate
from models.product import Product
from base.getname import getname


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")
# thao

def getListData(data , id):
    rs = []
    for item in data:
        if ( item.price != "Không giảm"):
            price = item.price
            if "₫" in price:
                price =  price.replace('₫', '')
            if "." in price:
                price =  price.replace('.', '')
        else:
            price = item.priceSale
            if "₫" in price:
                price =  price.replace('₫', '')
            if "." in price:
                price =  price.replace('.', '')
    
        if id == 1:
            product =  getNameFpt(item.name)
        if id == 2:
            product = getNameTgdt(item.name)
        if id == 0 :
            product = item.name
        base = {
            "id" : item.id,
            "name" : product,
            "price" : int(price),
        }
        rs.append(base)
    return rs

def getNameFpt(name):
    names = name.split(' ')
    product = ""
    for i in range(len(names)-1):
        product += names[i] + " "  
    return product

def getNameTgdt(name):
    names = name.split(' ')
    product = ""
    for i in range(2,len(names)-1):
        product += names[i] + " "  
    return product

@app.get("/getname")
def getList(db: Session = Depends(get_db) ):
    fpt = cruds.product.getManyDataByShopId(db , 1)
    data1 = getListData(fpt , 1 )
    lazada = cruds.product.getManyDataByShopId(db , 2)
    data2 = getListData(lazada ,0)
    shopee = cruds.product.getManyDataByShopId(db , 3)
    data3 = getListData(shopee , 0) 
    thegioididong = cruds.product.getManyDataByShopId(db , 4)
    data4 = getListData(thegioididong , 2)
    rs = []
    for i in data1:
        min = i["price"]
        for j in data2:
            lzd = None
            if i["name"] in j["name"]:
                lzd = j["id"]
                if min > j["price"] :
                    min = j["price"]
                break
        for k in data3:
            sp= None
            if i["name"] in k["name"]:
                sp = k["id"]
                if min > k["price"] :
                    min = k["price"]
                break
        for m in data4: 
            tgdd = None
            if i["name"] in m["name"]:
                tgdd = m["id"]
                if min > m["price"] :
                    min = m["price"]
                break
        if ( tgdd == None and lzd == None and  sp == None):
            base =  {     
                "name" : i["name"],
                "price" : str(min),
                "fptId" : i["id"],
                "thegioididongId" : tgdd,
                "lazadaId" : lzd,
                "shopeeId" : sp
            }
            print(base)
        else:
            show = ShowProduct(
                    name = i["name"],
                    price = str(min),
                    thegioididongId =tgdd,
                    fptId = i["id"],
                    lazadaId = lzd,
                    shopeeId = sp
            )
            name = cruds.showProduct.getByName(db , i["name"])
            if name is None :
                base = cruds.showProduct.create(db ,show)
                rs.append(base)
        
    for i in data4:
        min = i["price"]
        for j in data2:
            lzd = None
            if i["name"] in j["name"]:
                lzd = j["id"]
                if min > j["price"] :
                    min = j["price"]
                break
        for k in data3:
            sp= None
            if i["name"] in k["name"]:
                sp = k["id"]
                if min > k["price"] :
                    min = k["price"]
                break
        for m in data1: 
            fs = None
            if i["name"] in m["name"]:
                fs = m["id"]
                if min > m["price"] :
                    min = m["price"]
                break
        if ( fs == None and lzd == None and  sp == None):
            base =  {     
                "name" : i["name"],
                "price" : str(min),
                "thegioididongId" : i["id"],
                "fptId" : fs,
                "lazadaId" : lzd,
                "shopeeId" : sp
            }
            print(base)
        else:
            show = ShowProduct(
                    name = i["name"],
                    price = str(min),
                    thegioididongId = i["id"],
                    fptId = fs,
                    lazadaId = lzd,
                    shopeeId = sp
            )
            name = cruds.showProduct.getByName(db , i["name"])
            if name is None :
                base = cruds.showProduct.create(db ,show)
                rs.append(base)

    return custom_reponse(http_status=200 , data= True)


@app.get("/search")
def search(request: Request, db: Session = Depends(get_db), query: Optional[str] = None):
    search = cruds.showProduct.search(db , query)
    return custom_reponse(http_status=200 , data= search)


