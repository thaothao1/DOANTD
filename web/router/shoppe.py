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

dat_global = 'AAcyLjQuMS0zAAABhGH3FisAAAuiAlQAAAAAAAAAAAvjwIoWke4CGaJeKojpPMg/k/BnGH0dFr4BNqSRFEryKlpQoLPyGTqmXqL5F/8SvcTp8K6TCnpSZk1H9ceC295JHXrjVKy54uYqF/6KFSsRJsilt8Bl4VIIFFyt8ulG8UJIxlZGjuvBxpCGq/7Ekqct2WHRhYqwgcI+TgqizPqXvcUXZVbatanxNH0gKodDr23p0E7FOEJgWHqhRCLDJkB0UgDz+xhpe28iS3zrEtxrnqOCipnpmbrVxCJ6Cg53vZNG5GgQ+HsLteH6eVU3KBRO6TUWVKy54uYqF/6KFSsRJsilty2PWF1vp9y2imn+N+uBHgJlZE4aTD1D9NGmgVGpNOedNmTzAjP0z5Y7go/IS4xzxfxG68JIz1kdG26cjkgr0D/EglVWpAH3+ml9dBD0jOKcOP6C4Ahz5YvdrXhxvkF6PYTxL1Bi/QaV/bDhRzMirZgFMCqxEWTAuop9aZVNrRIzkWOzjLDykZY2dhCO2aemlvehiJf6OllW/EgYrZ8LIcB86KbMmVCtE8FeOCCu7uHzmmlMQ+JYTMHF6kF68iRD85aWYi9ro3Wl9b3oSySuEOpGWi6bh4+hmc4vyZj9m+PseobDmMRSuHW9TbiqXtBy0VUbmoSJfPFuNtApXssr4XpNH7fWRaE+gIIn10yHpYNCruOapZZuvoxvu1S2cxD/MlDLSBK1N1b3pekmIH1xIUbeQ2UuGVKCVt7Br0arRDenkWOzjLDykZY2dhCO2aemlr74btV9We2J/wW0zAc9hKKoXKVRqTvHq9RpN69TGYZLZEstVv2FuMYqHMCSS4LSPg=='
cookie_global = 'REC_T_ID=4b55f218-509b-11eb-965c-48df37dd9770; SPC_IA=-1; SPC_F=Su2xj6KcWdbtzIsAPiNk6UXLbuGoMv5b; REC_T_ID=4b5b69c6-509b-11eb-8e1f-b49691844b7c; G_ENABLED_IDPS=google; SPC_CLIENTID=U3UyeGo2S2NXZGJ0ujafepwfxvfkbyoj; SPC_U=-; SPC_EC=-; SPC_T_IV="4o8JMhoYAlW5aSw1HiKsPg=="; SPC_T_ID="Yw9LwfWRg4LqO1bh+J+5rmoe8ZBgNBMb+NpzXPArU+4THtAt11t9bZOMuCQtQyvFNq5p2ppcsbJViUxRxkEwf2uKMrPyAGETRuKHZRjwaOM="; SPC_T_ID=Yw9LwfWRg4LqO1bh+J+5rmoe8ZBgNBMb+NpzXPArU+4THtAt11t9bZOMuCQtQyvFNq5p2ppcsbJViUxRxkEwf2uKMrPyAGETRuKHZRjwaOM=; SPC_T_IV=4o8JMhoYAlW5aSw1HiKsPg==; _gcl_au=1.1.905702711.1661437059; SPC_R_T_ID=Yw9LwfWRg4LqO1bh+J+5rmoe8ZBgNBMb+NpzXPArU+4THtAt11t9bZOMuCQtQyvFNq5p2ppcsbJViUxRxkEwf2uKMrPyAGETRuKHZRjwaOM=; SPC_R_T_IV=4o8JMhoYAlW5aSw1HiKsPg==; _gcl_aw=GCL.1667314202.CjwKCAjwh4ObBhAzEiwAHzZYU_mx4LeM5f8_cKeCDcKGmI0hlsWNNqs734r5IWLfnpet5Xxc4m3XLxoC5gEQAvD_BwE; _med=refer; SPC_SI=ijtfYwAAAAA3R0ZCZ3QwSVENUQAAAAAAck1EWU1ySEc=; __LOCALE__null=VN; csrftoken=Lv1tyg94efZpqCRB3pJsfNBrVsnL0Eve; _QPWSDCXHZQA=a8df8611-0481-471f-86db-6a5017ab4d0d; shopee_webUnique_ccd=bcr%2Bs%2Bcs%2Bts35egIKazAsg%3D%3D%7CmECYNL7j3im2WEQjrNMOcLjnU7oqOrdptDUcM%2F8VAwy%2FWRd55374g3J%2FmWbf5U%2BBs2pcyUREq2PHfcMrqJ7pbmiYkLU8k1phCjJj%7Cr2U%2BXJAqdtLdGBNO%7C06%7C3; ds=a18e4aab8e5a738f4279acb11b2d342c'
csrftoken_global = 'Lv1tyg94efZpqCRB3pJsfNBrVsnL0Eve'
token_global = "bcr+s+cs+ts35egIKazAsg==|mECYNL7j3im2WEQjrNMOcLjnU7oqOrdptDUcM/8VAwy/WRd55374g3J/mWbf5U+Bs2pcyUREq2PHfcMrqJ7pbmiYkLU8k1phCjJj|r2U+XJAqdtLdGBNO|06|3"
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
