from fastapi import APIRouter
from router import thegioididong
from router import shoppe
from router import lazada
from router import showproduct
from router import fptshop
from router import api_app
from router import label

api = APIRouter()
api.include_router(lazada.app ,         prefix = "/api",    tags=["lazada"])
api.include_router(thegioididong.app ,  prefix = "/api",    tags=["thegioididong"])
api.include_router(shoppe.app ,         prefix = "/api",    tags=["shoppe"])
api.include_router(lazada.app ,         prefix = "/api",    tags=["lazada"])
api.include_router(showproduct.app ,    prefix = "/api",    tags=["goc"])
api.include_router(fptshop.app ,        prefix = "/api",    tags=["fpt"])
api.include_router(api_app.app ,        prefix = "/api",    tags=["api_web"])
api.include_router(label.app ,          prefix = "/api",    tags=["label"])

