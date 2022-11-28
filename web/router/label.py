from re import template
from typing import Optional
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.label import LabelCreate, LabelUpdate
 


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/label")
def get_list_label(db : Session = Depends(get_db)):
    data = cruds.label.getData(db)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)

@app.get("/LabelByCategory")
def get_label_by_category(db: Session = Depends(get_db) , id : Optional[int] = None):
    cate = cruds.category.getById(db , id)
    if cate == None:
        return HTTPException(status_code=400 , detail="false")
    else:
        cate.label = cruds.label.getByCate(db ,id)
        return custom_reponse(http_status=200 , data= cate)    

@app.post("/label")
def createLabel( body : LabelCreate , db: Session = Depends(get_db)):
    data = cruds.label.create(db , body) 
    return custom_reponse(http_status=200 , data= data)

@app.delete("/label/{id}")
def deleteLabel( id : int, db: Session = Depends(get_db)):
    data = cruds.label.remove( db , id)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)

@app.put("/label/{id}")
def updateLabel(body : LabelUpdate , id : int , db : Session = Depends(get_db)):
    print(body)
    data = cruds.label.update(db ,id,body)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)