from sys import prefix
from fastapi import APIRouter
from router import district
from router import province
from router import tgdd_spider
from router import product
from router import tgdd_spider
from router import shop
from router import fpt
from router import lazada

api = APIRouter()
api.include_router(district.app , tags=["district"] , prefix = "/api")
api.include_router(province.app , tags=["province"] , prefix = "/api")
api.include_router(tgdd_spider.app , tags=["thegioididong"] , prefix = "/api")
api.include_router(product.app , tags=["product"] , prefix = "/api")
api.include_router(tgdd_spider.app , tags=["tgdd_spider"] , prefix = "/api")
api.include_router(shop.app , tags=["shop"] , prefix = "/api")
api.include_router(fpt.app , tags=["fpt"] , prefix = "/api")
api.include_router(lazada.app , tags=["lazada"] , prefix = "/api")