from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.product import ProductCreate, ProductUpdate


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/products")
def get_list_product(skip: int  = 0, limit: int = 100 , db : Session = Depends(get_db)):
    data = cruds.product.getById(db,skip,limit)
    if data == None:
        return HTTPException(status_code=400 , detail="false")
    return custom_reponse(http_status=200 , data= data)

@app.post("/products")
def createProduct( body : ProductCreate , db: Session = Depends(get_db)):
    data = cruds.product.create(db , body) 
    return custom_reponse(http_status=200 , data= data)

@app.put("/products/{id}")
def deleteProduct( id : int, db: Session = Depends(get_db)):
    data = cruds.province.remove( db , id)
    return data


@app.get("/randomProducts")
def createProductRandom(db : Session= Depends(get_db)):
    data = cruds.product.getData(db)
    base =[]
    base.extend(data[0:2])
    base.extend(data[3:4])
    base.extend(data[5:9])
    return custom_reponse(http_status=200 , data= base)
