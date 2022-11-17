import json
import requests
# from msilib.schema import Class
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from base.CodeHTML import CodeHTML
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.label import Label
from models.product import Product
from models.shop import Shop
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from base.getname import getname

# ----------------------------------------------------- Xử lý chặn ------------------------------------
# af-ac-enc-dat
# sz-token
# x-csrftoken
# cookie

# headers_dict = {'cookie': 'REC_T_ID=4b55f218-509b-11eb-965c-48df37dd9770; SPC_IA=-1; SPC_F=Su2xj6KcWdbtzIsAPiNk6UXLbuGoMv5b; REC_T_ID=4b5b69c6-509b-11eb-8e1f-b49691844b7c; G_ENABLED_IDPS=google; SPC_CLIENTID=U3UyeGo2S2NXZGJ0ujafepwfxvfkbyoj; SPC_U=-; SPC_EC=-; SPC_T_IV="4o8JMhoYAlW5aSw1HiKsPg=="; SPC_T_ID="Yw9LwfWRg4LqO1bh+J+5rmoe8ZBgNBMb+NpzXPArU+4THtAt11t9bZOMuCQtQyvFNq5p2ppcsbJViUxRxkEwf2uKMrPyAGETRuKHZRjwaOM="; SPC_T_ID=Yw9LwfWRg4LqO1bh+J+5rmoe8ZBgNBMb+NpzXPArU+4THtAt11t9bZOMuCQtQyvFNq5p2ppcsbJViUxRxkEwf2uKMrPyAGETRuKHZRjwaOM=; SPC_T_IV=4o8JMhoYAlW5aSw1HiKsPg==; _gcl_au=1.1.905702711.1661437059; SPC_R_T_ID=Yw9LwfWRg4LqO1bh+J+5rmoe8ZBgNBMb+NpzXPArU+4THtAt11t9bZOMuCQtQyvFNq5p2ppcsbJViUxRxkEwf2uKMrPyAGETRuKHZRjwaOM=; SPC_R_T_IV=4o8JMhoYAlW5aSw1HiKsPg==; _gcl_aw=GCL.1667314202.CjwKCAjwh4ObBhAzEiwAHzZYU_mx4LeM5f8_cKeCDcKGmI0hlsWNNqs734r5IWLfnpet5Xxc4m3XLxoC5gEQAvD_BwE; __LOCALE__null=VN; csrftoken=5w3NR2lR4E4zxH4bxeyJohifMqQAqG0m; SPC_SI=PXpiYwAAAABMcE1jZ09rZIbHgQAAAAAAYW5WME45Umw=; _QPWSDCXHZQA=a8df8611-0481-471f-86db-6a5017ab4d0d; _med=refer; shopee_webUnique_ccd=6k8XpdpRE9K%2Bjpz%2B0Uvrig%3D%3D%7C3dmzx7BkLlSn1ODzQvoyfwVxFtmgKuKNxbGOInemn0FeWvOTHBAvnDwE3oC6qtpLmH73E1t8YL2cyDyoDLVKSobhSqPsMfml074%3D%7CK1pAhlH9UxH%2Fc687%7C06%7C3; ds=b84a853575843efcace82902772f0c6c'}
# headers = {'af-ac-enc-dat': 'AAcyLjQuMS0yAAABhEh4iHcAAAupAk4AAAAAAAAAAOYyhFAbVQMMpIKa2+dGIBkKaWUVkWOzjLDykZY2dhCO2aemlhrEiA3xw6v/mV1A4lbcUPq8HZ2GTC6Gy8upKta1AomlahQQzJTI3QAyabrcR+HjRB1nCnAsDVuG+2obETHDZK7Q5PH3Xqg0882frwuCRe0Ok28tKKHiTV4D5gf79ZYOW84EIeup0Rg7l1XPKsYI+5DAd9HyBzAJpyJuhD7Dc8X9XY0ke35fJGYjRaddXddiaiOBk6nCAEz7dK2GP5YOBmbQ0V3+Mdsk3C2CEmY450fQFIz4ZpelPN3OGEe+P752Y0gNhERmKKzBwxDcOGffk7nIvJy6vpSRrBf0EGeHKXhtmVG2rUT03+NpNuFFxwWbInF7PMo9yho3vYDOQwXRqfUguwM6a3Cf3bwDLdWRNqUHmaHW0BG6F5XX51UBWjFiEWuD1z4GWz020K0uqSKS549+5WUBK9xgWXbPI9r+9MmSr49M1q3M0f4Yfe7U8c8nCtA79/awLrhgvlemw6Je7UJpBIbQbXDxLMVUxj1MCnsUK96iVyp2MGEmZOEtJSKrwKjnZNpryLZEMMkCWnPWEMdSXd5QvkRBOEXfoNAyRPSpnUwMBLiPd5Ppfm00yrO1nid8j3Guwm3qylfUPZAXrrQQt6u6+wJrvxXEv34sECKydJcX+IWnaFTkKpRRRSRnbhM/UvUvafrVdRyH2WjwY7uLbHihsz5v3IpNHBySBy46kWOzjLDykZY2dhCO2aemlpFjs4yw8pGWNnYQjtmnppY92XhVPxBvNd1umDcbUxS7'}
# tokens = {'sz-token': '6k8XpdpRE9K+jpz+0Uvrig==|3dmzx7BkLlSn1ODzQvoyfwVxFtmgKuKNxbGOInemn0FeWvOTHBAvnDwE3oC6qtpLmH73E1t8YL2cyDyoDLVKSobhSqPsMfml074=|K1pAhlH9UxH/c687|06|3'}
# csrftoken = {'x-csrftoken': '5w3NR2lR4E4zxH4bxeyJohifMqQAqG0m'}

app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/shopee")
def getListProductShoppe(db: Session = Depends(get_db) ):
    url='https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11036031&limit=160&offset=0&fbclid=IwAR2K1Zt4mLVtD58ChX2Td0tkp9cE0fzy2ALQ4MJWcKYDPfhVgM86kxOb7IU'
    response = requests.get(url)

    data = json.loads(response.text)
    data = data["data"]["sections"]
    list_data = []
    shop = Shop(
      name = "Shopee",
      link = "https://shopee.vn/",
  )
    idShop = cruds.shop.getByName(db , "Shopee")
    if idShop is None:
      idShop = cruds.shop.create(db , shop)
    for item in data:
        _data = item["data"]["item"]
        for _data_ in _data :
          price = int(_data_['price_min']) / 100000
          priceSale  =  int(_data_['price_max']) / 100000
          rating = _data_['item_rating']['rating_star']
          product = Product(
            name = _data_['name'],
            image = "https://cf.shopee.vn/file/" + _data_['image'],
            price = str(price),
            priceSale  =  str(priceSale),
            rating =  str(rating),
            link = "https://shopee.vn/product/{}/{}".format(_data_['shopid'], _data_['itemid']),
            shopId = idShop.id
            )
          cruds.product.create(db , product)
    return True
