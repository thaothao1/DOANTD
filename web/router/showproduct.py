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
        if ( item.priceSale != "Không giảm"):
            price = item.priceSale
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
            product = item.name
            label = item.labelId
            category = item.categoryId
            image = item.image
        if id == 2:
            product = item.name
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

def getName(nameOne , nameTwo):
    shopOne = nameOne.split(' ')
    shopTwo = nameTwo.split(' ')
    count = 0
    for i in range(len(shopTwo)):
        if shopTwo[i] in shopOne:
            count+=1
    if (count >= shopOne.length-2):
        return True
    else:
        return False


@app.get("/showProduct")
def getList(db: Session = Depends(get_db) ):
    idFpt = cruds.shop.getByName(db , "fpt")
    fpt = cruds.product.getManyDataByShopId(db , idFpt.id)
    dataFpt = getListData(fpt , 1 )
    idlazada = cruds.shop.getByName(db , "lazada")
    lazada = cruds.product.getManyDataByShopId(db , idlazada.id)
    dataLazada = getListData(lazada ,0)
    idShopee = cruds.shop.getByName(db , "shopee")
    shopee = cruds.product.getManyDataByShopId(db , idShopee.id)
    dataShopee = getListData(shopee , 0) 
    idTgdt = cruds.shop.getByName(db , "Thế giới di động")
    thegioididong = cruds.product.getManyDataByShopId(db , idTgdt.id)
    dataTgdd = getListData(thegioididong , 2)
    base = []
    base.extend(dataFpt)
    base.extend(dataLazada)
    base.extend(dataShopee)
    base.extend(dataTgdd)
    with open('../../data.json', 'w' , encoding='utf-8') as f:
        json.dump(base, f, indent=2 , ensure_ascii= False)  
    rs = []
    for i in dataFpt:
        min = i["price"]
        for j in dataLazada:
            lzd = None
            if ( i["labelId"] == j["labelId"]):
                checkName = getName(i["name"] , j["name"])
                if checkName == True:
                    lzd = j["id"]
                    if min > j["price"] :
                        min = j["price"]
                    break
        for k in dataShopee:
            sp= None
            if ( i["labelId"] == k["labelId"]):
                checkName = getName(i["name"] , k["name"])
                if checkName == True:
                    sp = k["id"]
                    if min > k["price"] :
                        min = k["price"]
                    break
        for m in dataTgdd: 
            tgdd = None
            if ( i["labelId"] == m["labelId"]):
                checkName = getName(i["name"] , m["name"])
                if checkName == True:
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
                    view = 0
            )
            name = cruds.showProduct.getByName(db , i["name"])
            if name is None :
                base = cruds.showProduct.create(db ,show)
                rs.append(base)
        
    for l in dataTgdd:
        min = l["price"]
        for j in dataLazada:
            lzd = None
            if ( l["labelId"] == j["labelId"]):
                checkName = getName(l["name"] , j["name"])
                if checkName == True:
                    lzd = j["id"]
                    if min > j["price"] :
                        min = j["price"]
                    break
        for k in dataShopee:
            sp= None
            if ( l["labelId"] == k["labelId"]):
                checkName = getName(l["name"] , k["name"])
                if checkName == True:
                    sp = k["id"]
                    if min > k["price"] :
                        min = k["price"]
                    break
        for m in dataFpt: 
            fs = None
            if ( l["labelId"] == m["labelId"]):
                checkName = getName(l["name"] , m["name"])
                if checkName == True:
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
def searchCategory(request: Request, db: Session = Depends(get_db), query: Optional[str] = None, categoryId: Optional[int] = 0):
    if categoryId == 0:
        search = cruds.showProduct.search(db, query)
        return custom_reponse(http_status=200 , data= search)
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


