from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.category import CategoryCreate

 


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

# @app.get("/category")
# def get_list_label(skip: int  = 0, limit: int = 100 , db : Session = Depends(get_db)):
#     data = cruds..getById(db,skip,limit)
#     if data == None:
#         return HTTPException(status_code=400 , detail="false")
#     return custom_reponse(http_status=200 , data= data)

@app.post("/category")
def createCategory( body : CategoryCreate , db: Session = Depends(get_db)):
    data = cruds.category.create(db , body) 
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)


