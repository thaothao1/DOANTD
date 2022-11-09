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


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")
# thao
@app.get("/thudieu")
def getList():
    data = TgddSpider()
    test = data.start_requests()
    return custom_reponse(http_status=200 , data= test)