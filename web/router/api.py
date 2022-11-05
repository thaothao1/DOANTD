from sys import prefix
from fastapi import APIRouter
from router import district
from router import province
from router import thegioididong

api = APIRouter()
api.include_router(district.app , tags=["district"] , prefix = "/api")
api.include_router(province.app , tags=["province"] , prefix = "/api")
api.include_router(thegioididong.app , tags=["thegioididong"] , prefix = "/api")