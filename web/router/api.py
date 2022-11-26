from fastapi import APIRouter
from router import lazada
from router import label
from router import fptshop
from router import category
from router import thegioididong
from router import shoppe


api = APIRouter()

api.include_router(lazada.app ,prefix = "/api",tags=["lazada"])
api.include_router(label.app , prefix="/api" , tags=["label"])
api.include_router(fptshop.app , prefix="/api", tags=["fptshop"])
api.include_router(category.app , prefix="/api", tags=["category"])
api.include_router(thegioididong.app , prefix="/api", tags=["thegioididong"])
api.include_router(shoppe.app , prefix="/api", tags=["shoppe"])