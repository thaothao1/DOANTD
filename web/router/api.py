from sys import prefix
from fastapi import APIRouter
from router import district
from router import province

api = APIRouter()
api.include_router(district.app , tags=["district"] , prefix = "/api")
api.include_router(province.app , tags=["province"] , prefix = "/api")