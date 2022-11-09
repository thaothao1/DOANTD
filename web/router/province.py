from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.district import DistrictCreate, DistrictUpdate
from chemas.province import ProvinceCreate
 


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/province")
def get_list_province(skip: int  = 0, limit: int = 100 , db : Session = Depends(get_db)):
    data = cruds.province.getById(db,skip,limit)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)

@app.post("/province")
def createProvince( body : ProvinceCreate , db: Session = Depends(get_db)):
    data = cruds.province.create(db , body) 
    return custom_reponse(http_status=200 , data= data)

@app.put("/province/{id}")
def updateProvince( id : int, db: Session = Depends(get_db)):
    data = cruds.province.remove( db , id)
    return data