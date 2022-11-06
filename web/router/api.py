from sys import prefix
from fastapi import APIRouter
from router import district
from router import province
from router import thegioididong
from router import shoppe
from router import lazada

api = APIRouter()
api.include_router(district.app , tags=["district"] , prefix = "/api")
api.include_router(province.app , tags=["province"] , prefix = "/api")
api.include_router(lazada.app , tags=["lazada"] , prefix = "/api")
api.include_router(thegioididong.app , tags=["thegioididong"] , prefix = "/api")
api.include_router(shoppe.app , tags=["shoppe"] , prefix = "/api")
api.include_router(lazada.app , tags=["lazada"] , prefix = "/api")
