import json
from msilib.schema import Class
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from base.CodeHTML import CodeHTML
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.product import ProductCreate , ProductUpdate
from models.product import Product
from base.tgdd import TgddSpider
from seleniumwire import webdriver 
from selenium.webdriver.common.by import By
import random, string
import requests


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")
# thao
@app.get("/shoppe")
def getList(db: Session = Depends(get_db)):
    url='https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11036031&limit=160&offset=0&fbclid=IwAR2K1Zt4mLVtD58ChX2Td0tkp9cE0fzy2ALQ4MJWcKYDPfhVgM86kxOb7IU'
    response = requests.get(url)

    data = json.loads(response.text)
    data = data["data"]["sections"]
    list_data = []
    for item in data:
        print(item)
        _data = item["data"]["item"]
        for _data_ in _data :
                # "itemid" : _data_['itemid']
                # "shopid" : _data_['shopid']
                product = _data_['name']
                image = "https://cf.shopee.vn/file/" + _data_['image']
                # "historical_sold" : _data_['historical_sold'],
                price =   int(_data_['price_min']) / 100000
                priceSale =  int(_data_['price_max']) / 100000
                # "shop_location" : _data_['shop_location'],
                # color= _data_['tier_variations'][0]['options'],
                # "gb" : _data_['tier_variations'][1]['options'], 
                # "rating" : _data_['item_rating']['rating_star'],
                # url = "https://shopee.vn/api/v4/item/get?itemid={}&shopid={}".format(_data_['itemid'], _data_['shopid']),
                link = "https://shopee.vn/product/{}/{}".format(_data_['shopid'], _data_['itemid'])
                size = "S"
                quantity = 3
                description = "NO"
                color = "thao"
                base = Product(
                    product = product,
                    link = link,
                    image = image ,
                    price = str(price),
                    priceSale = str(priceSale),
                    color = color,
                    size = size,
                    description = description,
                    quantity =quantity,
                   )
                test = cruds.product.getByName(db , product)
                if(test == None):
                    cruds.product.create(db , base)
                continue
        return custom_reponse(http_status=200)
           
