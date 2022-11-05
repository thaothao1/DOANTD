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
from chemas.district import DistrictCreate, DistrictUpdate


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.post("/project")
def getList(db: Session = Depends(get_db) ):
    codeHTML = CodeHTML("https://www.thegioididong.com/dtdd")
    htmlTest = codeHTML.beautifulSoup()
    name = htmlTest.findAll("li" , class_="item ajaxed __cate_42")
    test = []
    data_id = []
    for i in name:
        item={}
        data = i.find("a")
        image = i.find("img")
        item["product"] = data["data-name"] 
        item["price"]   = data["data-price"] 
        item["link"] =  data["href"] 
        if "-src" in str(image):
            item["image"] = image["data-src"]
        else:
            item["image"] = image["src"]
        print("item" ,item)
        # data = cruds.product.create(db , item)
    return test
