from re import template
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
def get_list_label(skip: int  = 0, limit: int = 100 , db : Session = Depends(get_db)):
    data = cruds.label.getById(db,skip,limit)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)

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