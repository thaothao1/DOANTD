import json
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from typing import Optional
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from chemas.showProduct import ShowProductCreate , ShowProductUpdate
from models.showProduct import ShowProduct
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.product import ProductCreate , ProductUpdate
from models.product import Product


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

def getListData(data , id):
    rs = []
    for item in data:
        if ( item.price != "Không giảm"):
            price = item.price
            if "₫" in price:
                price =  price.replace('₫', '')
            if "đ" in price:
                price =  price.replace('đ', '')
            if ".0" in price[-3:-1]:
                price = price[0: price.length - 1]
            if "." in price:
                price =  price.replace('.', '')
        else:
            price = item.priceSale
            if "₫" in price:
                price =  price.replace('₫', '')
            if "đ" in price:
                price =  price.replace('đ', '')
            if ".0" in price[-3:-1]:
                price = price[0: price.length - 1]
            if "." in price:
                price =  price.replace('.', '')
        if id == 1:
            product =  getNameFpt(item.name)
            label = item.labelId
            category = item.categoryId
            image = item.image
        if id == 2:
            product = getNameTgdt(item.name)
            label = item.labelId
            category = item.categoryId
            image = item.image
        if id == 0 :
            product = item.name
            label = None
            category = None
            image = item.image
            # price = price[0: price.length()-1]
        base = {
            "id" : item.id,
            "name" : product,
            "price" : int(price),
            "image" : image,
            "labelId" : label,
            "categoryId" : category
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

@app.get("/showProduct")
def getList(db: Session = Depends(get_db) ):
    idFpt = cruds.shop.getByName(db , "fpt")
    fpt = cruds.product.getManyDataByShopId(db , idFpt.id)
    data1 = getListData(fpt , 1 )
    idlazada = cruds.shop.getByName(db , "lazada")
    lazada = cruds.product.getManyDataByShopId(db , idlazada.id)
    data2 = getListData(lazada ,0)
    idShopee = cruds.shop.getByName(db , "shopee")
    shopee = cruds.product.getManyDataByShopId(db , idShopee.id)
    data3 = getListData(shopee , 0) 
    idTgdt = cruds.shop.getByName(db , "Thế giới di động")
    thegioididong = cruds.product.getManyDataByShopId(db , idTgdt.id)
    data4 = getListData(thegioididong , 2)
    print("data1" ,data1)
    print("data2" ,data2)
    print("data3" ,data3)
    print("data4" ,data4)

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
            continue
        else:
            show = ShowProduct(
                    name = i["name"],
                    price = str(min),
                    thegioididongId =tgdd,
                    image = i["image"],
                    fptId = i["id"],
                    lazadaId = lzd,
                    shopeeId = sp,
                    labelId = i["labelId"],
                    categoryId = i["categoryId"],
                    view = 100
            )
            name = cruds.showProduct.getByName(db , i["name"])
            if name is None :
                base = cruds.showProduct.create(db ,show)
                rs.append(base)
        
    for l in data4:
        min = l["price"]
        for j in data2:
            lzd = None
            if l["name"] in j["name"]:
                lzd = j["id"]
                if min > j["price"] :
                    min = j["price"]
                break
        for k in data3:
            sp= None
            if l["name"] in k["name"]:
                sp = k["id"]
                if min > k["price"] :
                    min = k["price"]
                break
        for m in data1: 
            fs = None
            if l["name"] in m["name"]:
                fs = m["id"]
                if min > m["price"] :
                    min = m["price"]
                break
        if ( fs == None and lzd == None and  sp == None):
            continue
        else:
            show = ShowProduct(
                    name = l["name"],
                    price = str(min),
                    image = l["image"],
                    thegioididongId = l["id"],
                    fptId = fs,
                    lazadaId = lzd,
                    shopeeId = sp,
                    labelId = l["labelId"],
                    categoryId = l["categoryId"],
                    view = 100
            )
            name = cruds.showProduct.getByName(db , l["name"])
            if name is None :
                base = cruds.showProduct.create(db ,show)
                rs.append(base)

    return custom_reponse(http_status=200 , data= True)


@app.get("/search")
def search(request: Request, db: Session = Depends(get_db), query: Optional[str] = None):
    search = cruds.showProduct.search(db , query)
    return custom_reponse(http_status=200 , data= search)

@app.get("/searchCategory")
def searchCategory(request: Request, db: Session = Depends(get_db), query: Optional[str] = None, categoryId: Optional[int] = None):
    if categoryId == None:
        return cruds.showProduct.search(db, query)
    else:
        search_category = cruds.showProduct.searchCategory(db, query, categoryId)
        return custom_reponse(http_status=200 , data=search_category)
    
@app.get("/detailProduct/{id}")
def detailProduct(request : Request, db : Session = Depends(get_db), id : int = 1):
    shop1 = None
    shop2 = None
    shop3 = None
    shop4 = None
    data = cruds.showProduct.getById(db, id)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    data.view = data.view + 1
    base = cruds.showProduct.update(db , id , data)
    fpt = cruds.product.getById(db, base.fptId)
    if fpt is not None:
        shop1 = cruds.shop.getById(db, fpt.shopId)
    shopee = cruds.product.getById(db , base.shopeeId)
    if shopee is not None:
        shop2 =  cruds.shop.getById(db, shopee.shopId)
    thegioididong =  cruds.product.getById(db , base.thegioididongId)
    if thegioididong is not None:
        shop3 = cruds.shop.getById(db, thegioididong.shopId)
    lazada = cruds.product.getById(db , base.lazadaId)
    if lazada is not None:
        shop4 = cruds.shop.getById(db, lazada.shopId)
    return custom_reponse(http_status=200 ,data = { "data": data, "product1": fpt, "shop1": shop1, "product2": shopee, "shop2": shop2, "product3": thegioididong , "shop3": shop3 , "product4": lazada, "shop4": shop4})


@app.put("/showProduct/{id}")
def updateLabel(body : ShowProductCreate , id : int , db : Session = Depends(get_db)):
    print(body)
    data = cruds.showProduct.update(db ,id, body)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)


