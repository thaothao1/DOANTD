from re import template
from typing import Optional
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db

 


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/shop")
def get_shop(db : Session = Depends(get_db)):
    data = cruds.shop.getData(db)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)