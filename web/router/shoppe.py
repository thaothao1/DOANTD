import json
import os
import requests
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.category import Category
from models.product import Product
from models.shop import Shop
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
import json
import time
from seleniumwire import webdriver

# ----------------------------------------------------- Xử lý chặn ------------------------------------
# af-ac-enc-dat
# sz-token
# x-csrftoken
# cookie

app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

dat_global = 'AAcyLjUuMC0yAAABhQAhKFIAAAzVAnAAAAAAAAAAAuvlR3weVVU60ykHUkkzSmQs+0sol/82EyfDx/bVRcPaaRvYm+PHtYZVLa9mEth0/Y6J5T2dwRhbFrjS00z52l8KbfavDGItKTK1eC80VyIMhKDXTll/KU1IWYq3J5cA0fg3DRr5ucxzA6P+HlxI8a0e0EITl/82EyfDx/bVRcPaaRvYm5eD3UHik0uRdNnuj4TimMs/8S1z1zP9AjeXZLkGYgPtUEkJLoWNR3Y5qPiVz5AkhX+He32Lxkvyc3NMF4HNnbxhAkujzghUnCa4Ta8/Zbci0Ab14qbCPm6nRU3AmUISmQ/5r0PT2xQnVi0F5o4pzQ4H/QSea5pczzIHNVQ0HNs+lySktY1KEY1FNUfm2LmMAS63v/aYivfSpAgFmNnbMYpUYmXmiyQlSVNEnxuXUS8lnUwcw8qmPqeTefoJ2YFmSPap+xOCy0qf6FceYCNc1JRGrbfJWuRYlFp+J0tcUk6v6ek4yxPbB0sT8oSqMAcIpEcN2aoQquR/Fv/7bIqlDWlCAWpI74qOTHTYmWbxwU1eTxcIwQ5gQLv4U+cgQTKitRgLefJo2nTgkqnSRiTJY3JUYmXmiyQlSVNEnxuXUS8lChiMFapSpb7hT3RbbjSWoIvRiKwQcI+tZF/gbCRv7zjE5v0pM36kj1Rj5HE4yTJxhSAhU4gKl/Ayxh0Fmb3M2PfI2f/dNbaWMImE4xhf9sQi1WQ1xtbLsuTyPytM95ipAkJkdlfknt7NF44LQBkvEgltCKSMs3BbcdDy1I14/JTOkeK/RVSQQoUnZnyKrNBJTksvy2OisBRQx/hbSF0/6WoyGBhfDCD6n91ozk1ZQE4='
cookie_global = '_gcl_au=1.1.477035483.1668435919; _med=refer; SPC_F=9VWV6QyoIxdxaRADBYrKL8VJgWxedtRM; REC_T_ID=2a3323e5-6428-11ed-af4f-9440c93e1538; SPC_R_T_ID=aznHzn4wYdBE+ZnfwkDj1LsRU5MMEGYPa2uY3Y4Ul7bFF2AT0bHBQFazyAW3HGjLbYOMSL+3ck+1j0r1Wcm6RvnlaJOU2gIHXG/ms6EaL17u93qxGdFM5nfEPGGXD6GnLhYiVQMaGHZxGEk9dwIitc8/qTJyXl5uduEjfbcMiyU=; SPC_R_T_IV=b2w2ajNxZ3JwS1A2UzBVWg==; SPC_T_ID=aznHzn4wYdBE+ZnfwkDj1LsRU5MMEGYPa2uY3Y4Ul7bFF2AT0bHBQFazyAW3HGjLbYOMSL+3ck+1j0r1Wcm6RvnlaJOU2gIHXG/ms6EaL17u93qxGdFM5nfEPGGXD6GnLhYiVQMaGHZxGEk9dwIitc8/qTJyXl5uduEjfbcMiyU=; SPC_T_IV=b2w2ajNxZ3JwS1A2UzBVWg==; _fbp=fb.1.1668435919003.1861778103; _hjSessionUser_868286=eyJpZCI6IjAyNGNjYjk3LTI2ZjAtNWU4Ni1hYzRlLTk5MjljZjk1ZmQ2MCIsImNyZWF0ZWQiOjE2Njg0MzU5MjEzNjYsImV4aXN0aW5nIjp0cnVlfQ==; __LOCALE__null=VN; SPC_SI=Hrh0YwAAAABFVmFsR2JBZvcD9wIAAAAATnpmRjFjSFE=; csrftoken=5MOPzN4zABWiGVX6MTaxC30EKffEVcYy; _QPWSDCXHZQA=29548cca-6006-4670-9d9c-916216e1e676; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.564796872.1670744385; cto_bundle=8ybP-F9tJTJCcGhsdWRUbzBTUXdOWFRGZjRlYWpaR04ydHhkaXh1UFZ4aFolMkJiNTY1Q2lPdFh4WG9YaVJFbGRxSUxTZ3FzSiUyRnFvWnpWQktacCUyRjh5czB3MyUyRnBJUGRTdWJERFowOVhUaFhwU1YwTTZpMFFCb1Y5QThKRnd0JTJGTzRFdTYlMkZLQk1pViUyQnpDYktraFk3a3Y4RU54aVMlMkJHV3clM0QlM0Q; _hjIncludedInSessionSample=0; _hjSession_868286=eyJpZCI6IjljYzczMDFiLWM3OGItNGVmOC05MmZmLTY2YmEyMjcxZmM2ZCIsImNyZWF0ZWQiOjE2NzA3NDQ0Mzk4MzksImluU2FtcGxlIjpmYWxzZX0=; _ga_M32T05RVZT=GS1.1.1670744384.6.1.1670744451.53.0.0; _ga=GA1.1.440289248.1668435920; _dc_gtm_UA-61914164-6=1; shopee_webUnique_ccd=Iba7WFSbUKqMG5BpIC83lw%3D%3D%7CAaw%2F6sIu2%2BoY76NUY6MW%2BXzAmwnKUK9glmeGWtU9h1aLd80CQw1xP2ZVnTpMCysPN%2BKmpJyjGx%2BW47nZCLHHy3mWmvnj19tzZls%3D%7CGpzzjZgaBwrBnWhY%7C06%7C3; ds=f9c50b3acf1a17ff30fc6a2272f402a4'
csrftoken_global = '5MOPzN4zABWiGVX6MTaxC30EKffEVcYy'
token_global = "Iba7WFSbUKqMG5BpIC83lw==|Aaw/6sIu2+oY76NUY6MW+XzAmwnKUK9glmeGWtU9h1aLd80CQw1xP2ZVnTpMCysPN+KmpJyjGx+W47nZCLHHy3mWmvnj19tzZls=|GpzzjZgaBwrBnWhY|06|3"
options = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--no-proxy-server")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = None

TIME_MAX_REQ = 20

def interceptor(request):
    request.headers['af-ac-enc-dat'] = dat_global
    request.headers['cookie'] = cookie_global
    request.headers['x-csrftoken'] = csrftoken_global
    request.headers['sz-token'] = token_global     

def getHeader(key):
    global drive
    global dat_global
    global cookie_global
    global csrftoken_global
    global token_global
    time_max = 1

    while time_max <= TIME_MAX_REQ:
                
        url = "https://shopee.vn/search?keyword=" + key
        driver.get(url)
        for request in driver.requests:
            try:
                url = request.url
                index = url.find("https://shopee.vn/api/v4/search/search_items")
                if index != -1:

                    dat_global = request.headers['af-ac-enc-dat']
                    cookie_global = request.headers['cookie']
                    csrftoken_global = request.headers['x-csrftoken']
                    token_global = request.headers['sz-token']

                    # dictionary = {
                    #     "dat_global" : dat_global,
                    #     "cookie_global" : cookie_global,
                    #     "csrftoken_global" : csrftoken_global,
                    #     "token_global" : token_global
                    # }
                    return
            except: continue

        time_max = time_max + 1


def info_items(data ,key , db):
    list_item = []
    items = data['items']
    shop = Shop(
            name = "shopee",
            link = "https://shopee.vn",
            )
    idShop = cruds.shop.getByName(db , "shopee")
    if idShop is None:
        idShop = cruds.shop.create(db , shop)

    idCategory = None
    if ( key == "điện thoại"):
        idCategory = cruds.category.getByName(db , "Điện thoại")
        if idCategory is None:
            data = Category(
                name = "Điện thoại"
            )
            idCategory = cruds.category.create(db , data)      

    if ( key == "laptop"):
        idCategory = cruds.category.getByName(db , "Laptop")
        if idCategory is None:
            data = Category(
                name = "Laptop"
            )
            idCategory = cruds.category.create(db , data) 
    for item in items:
        tmp = item['item_basic']
        name =  tmp['name']
        image = "https://cf.shopee.vn/file/" + tmp['image']
        price_min =  int(tmp['price_min']) / 100000
        price_max = int(tmp['price_max']) / 100000
        rating = tmp['item_rating']['rating_star']
        link ="https://shopee.vn/product/{}/{}".format(tmp['shopid'], tmp['itemid'])
        listDict = Product(
            name = str(name),
            link = str(link),
            image = str(image),
            priceSale = str(price_min),
            price = str(price_max),
            rating = str(rating),
            labelId = None,
            categoryId = idCategory.id,
            shopId= idShop.id
        )
        data_name = None
        try:
            data_name = cruds.product.getByName(db , name)
        except Exception as e:
            return name
        if ( data_name != None):
            cruds.product.update(db , data_name.id , listDict)
        else:
            cruds.product.create(db , listDict)
        list_item.append(listDict)
    return list_item

def getProducts(url , key , db):
    global driver
    driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
    time_max = 1
    while time_max <= TIME_MAX_REQ:
            driver.request_interceptor = interceptor
            driver.get(url)
            try:
                r=(driver.find_element("xpath",("/html/body/pre")).text)
                list_item = info_items(json.loads(r) , key , db)
                driver.quit()
                driver = None
                return list_item
            except:
                getHeader(key)
                time_max = time_max + 1
    driver.quit()
    driver = None
    return []

@app.get("/shopee")
def search( db: Session = Depends(get_db)):
    keys = ["điện thoại" , "laptop"]
    list = []
    for key in keys:
        for i in range(0,5) :   
            url = "https://shopee.vn/api/v4/search/search_items?by=relevancy&keyword={}&newest={}&limit=60".format(key, i*60)
            list += getProducts(url , key , db)
    return list
