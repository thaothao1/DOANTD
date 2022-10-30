from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.category import CategoryCreate, CategoryUpdate
 


app = APIRouter()
templates = Jinja2Templates(directory = "templates")

@app.get("/category")
def get_list_category(skip: int  = 0, limit: int = 100 , db : Session = Depends(get_db)):
    data = cruds.categorys.getById(db,skip,limit)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)

@app.post("/districts")
def createDistricts( body : CategoryCreate , db: Session = Depends(get_db)):
    data = cruds.districts.create( db , body)
    return custom_reponse(http_status=200 , data= data)

@app.put("/districts/{id}")
def updateDistrict( id : int, db: Session = Depends(get_db)):
    data = cruds.districts.remove( db , id)
    return data