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


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")
# thao
@app.get("/thegioididong")
def getList(db: Session = Depends(get_db) ):
    codeHTML = CodeHTML("https://www.thegioididong.com/dtdd")
    htmlTest = codeHTML.beautifulSoup()
    name = htmlTest.findAll("li" , class_="item ajaxed __cate_42")
    test = []
    data_id = []
    for i in name:
        data = i.find("a")
        image = i.find("img")
        product= data["data-name"] 
        link= data["href"]  
        if "-src" in str(image):
            image = image["data-src"]
        else:
            image = image["src"]
        price = data["data-price"] 
        priceSale = "100000"
        color ="3746"
        size = "S"
        description = "Mo ta"
        quantity =  67
        base = Product(
                product = product,
                link = link,
                image = image ,
                price = price,
                priceSale = priceSale,
                color = color,
                size = size,
                description = description,
                quantity =quantity,
        )
        data = cruds.product.create(db , base)
    return custom_reponse(http_status=200 , data= data)



