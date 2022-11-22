from sys import prefix
from fastapi import APIRouter
from router import thegioididong
from router import shoppe
from router import lazada
from router import showproduct
from router import fptshop
from router import api_app
from router import label

api = APIRouter()
api.include_router(lazada.app , tags=["lazada"] , prefix = "/api")
api.include_router(thegioididong.app , tags=["thegioididong"] , prefix = "/api")
api.include_router(shoppe.app , tags=["shoppe"] , prefix = "/api")
api.include_router(lazada.app , tags=["lazada"] , prefix = "/api")
api.include_router(showproduct.app , tags=["goc"] , prefix = "/api")
api.include_router(fptshop.app , tags=["fpt"] , prefix = "/api")
api.include_router(api_app.app , tags = ["api_web"] , prefix = "/api")
api.include_router(label.app , tags=["label"] , prefix = "/api")

