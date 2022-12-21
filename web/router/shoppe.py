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

dat_global = 'AAcyLjUuMC0yAAABhTX5vv4AAA37ApAAAAAAAAAAAuvlR3weVVU60ykHUkkzSmQs+0sol/82EyfDx/bVRcPaaRvYm+PHtYZVLa9mEth0/Y6J5T2dwRhbFrjS00z52l8KbfavUwekXRhU3Rs19VCSdB0pN1A+AelRhDrFRDC9Mlj8MA/5ucxzA6P+HlxI8a0e0EITl/82EyfDx/bVRcPaaRvYmzvqDNUPsQEZyLCu17ywBvipszZ5PjfJLkGZMCfBD5pmjdQ4ez+iFy1+Dr+jkwoD7ZzLxEYJKJSy2WOfVmOdv8iVxQco17P30pBfNv9FJ9K8073afh54UW3qhlLZw1RsCQ9dqC+UdGbvAnxRPpn3VIni3bqiAN7F+S30/b42yDJpzqvmuhjAqpAhDPMkxfAxm0IBakjvio5MdNiZZvHBTV5105vwOAtHpqMUBmnTN0sV9qn7E4LLSp/oVx5gI1zUlEatt8la5FiUWn4nS1xSTq/yp28hATM6inW7ZMD1VCWz8MS3gD4Lv0cZsWDYYHdpR1c3Np8BzcsRRPm/ZZgFLUk01Y0pb29WyQXcoSq5w1NxpohFHsEFTkPArlIVDn5bBVRiZeaLJCVJU0SfG5dRLyWGh3ZH1PL55m32VjfoJNqAWPh/elbTlxqfcbiW5YZw4Uatt8la5FiUWn4nS1xSTq+SyXmY7YHCbZBEVvhbmbRGt/9oFsMly3ytjpnanSZSPP8aB6e5ohT8GOJs7PQReAUUJHovgFvBhxulEP1rqz6yCW0IpIyzcFtx0PLUjXj8lKHh2XiAdfleyeMSDdZLZvbZdj+oKLtRJcl98A0rBl1C4uCgisFY7om8kJPXrmzIjjyJxtPZIBeSRENgRLufjFvLjtPywHFXW1L8xytap/YzFMzZJmHLp/ONlAyJJqRgtA=='
cookie_global = '_gcl_au=1.1.477035483.1668435919; SPC_F=9VWV6QyoIxdxaRADBYrKL8VJgWxedtRM; REC_T_ID=2a3323e5-6428-11ed-af4f-9440c93e1538; _fbp=fb.1.1668435919003.1861778103; _hjSessionUser_868286=eyJpZCI6IjAyNGNjYjk3LTI2ZjAtNWU4Ni1hYzRlLTk5MjljZjk1ZmQ2MCIsImNyZWF0ZWQiOjE2Njg0MzU5MjEzNjYsImV4aXN0aW5nIjp0cnVlfQ==; cto_bundle=8ybP-F9tJTJCcGhsdWRUbzBTUXdOWFRGZjRlYWpaR04ydHhkaXh1UFZ4aFolMkJiNTY1Q2lPdFh4WG9YaVJFbGRxSUxTZ3FzSiUyRnFvWnpWQktacCUyRjh5czB3MyUyRnBJUGRTdWJERFowOVhUaFhwU1YwTTZpMFFCb1Y5QThKRnd0JTJGTzRFdTYlMkZLQk1pViUyQnpDYktraFk3a3Y4RU54aVMlMkJHV3clM0QlM0Q; __LOCALE__null=VN; SPC_SI=hNeiYwAAAABhYVRSVnVsaHnZCAAAAAAAN0Z2WlZOSmY=; csrftoken=fXQuCvrxWa5Hw2J0VOXyei8NhxfBwapR; _QPWSDCXHZQA=29548cca-6006-4670-9d9c-916216e1e676; _gid=GA1.2.175717588.1671641486; SPC_CLIENTID=OVZXVjZReW9JeGR4xkjoxbdplrmhkzcf; SPC_ST=.T3lSdThzeG0zaW9ZM1VnclrK5IbBuOBDd6w8d5qKDhATYM2uR/VBqqcZ6TYrzTxMCTEb4vGUH21hqXkIXc8JvmsnaN0RPk2pFvYk0utyVIUvFZPtSsP+UpM/q0aU6mRmar3eNh8pd57c+jNo0b7Y3Sy4OpANZfT4Cc+W+KiqPxGoRLGFJ1PoVhUQaCErUI9wfITXTMjdZ5Zg2srVvK18FA==; _ga_CGXK257VSB=GS1.1.1671641540.1.0.1671641540.60.0.0; SPC_U=224499167; SPC_R_T_IV=WkVmRVpBYk82TUh1Y1BaeQ==; SPC_T_ID=nRVNYSrW3KICpT9I5C5nYEwCI686duHPFgtiQBHh4aj1rhrh0bUsbPItBGCzJCrMIjM1PUkGl536vf49irDbet8Y8xYA1gOmH1u5F1zcswztYo44hJUEJ6zmv0ud/oDdogyZvEG4n6FnQHSkjH5qY0Sg7GnYmQJBYbFJBH94hIY=; SPC_T_IV=WkVmRVpBYk82TUh1Y1BaeQ==; SPC_R_T_ID=nRVNYSrW3KICpT9I5C5nYEwCI686duHPFgtiQBHh4aj1rhrh0bUsbPItBGCzJCrMIjM1PUkGl536vf49irDbet8Y8xYA1gOmH1u5F1zcswztYo44hJUEJ6zmv0ud/oDdogyZvEG4n6FnQHSkjH5qY0Sg7GnYmQJBYbFJBH94hIY=; _gcl_aw=GCL.1671647820.Cj0KCQiA-oqdBhDfARIsAO0TrGHzyBXR72GHaT-K-yd98IYtgtt6I6Tsyr8OT46kTaPU2ADQ90zGCBAaAiyREALw_wcB; _hjIncludedInSessionSample=0; _hjSession_868286=eyJpZCI6Ijg3NjQ5N2YzLTcyZTItNDJiOC04YTAzLWRhM2RlOWU5NjEyMyIsImNyZWF0ZWQiOjE2NzE2NDc4MjM3OTIsImluU2FtcGxlIjpmYWxzZX0=; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.440289248.1668435920; _gac_UA-61914164-6=1.1671647824.Cj0KCQiA-oqdBhDfARIsAO0TrGHzyBXR72GHaT-K-yd98IYtgtt6I6Tsyr8OT46kTaPU2ADQ90zGCBAaAiyREALw_wcB; _dc_gtm_UA-61914164-6=1; _gali=shopee-searchbar-listbox; _ga_M32T05RVZT=GS1.1.1671647823.8.1.1671647836.47.0.0; _med=refer; SPC_EC=cTRybGNCeldaYnhkRXNVVt79a4VhRpvu2BnMIfPj1bAQA4GOEtq4RbrBVialQsQFXaHkmbut00BQRqdZG1IHdlknpVBN8EsqcFPRaX16ot54Cb8D+1/x+MAQhPqzXBCnCZ36vagjsGrR5AUWcAB9IPiyGWouVb0ADXxhxw9ABIs=; shopee_webUnique_ccd=WXjgsbAQaqh7qb57j0nAtg%3D%3D%7CcTsVQJlURLpHn7s6keKlWjYwAQFqi2WpU%2FvsCwsDVCoCDsy%2FJ1nr4TAZPEeepOKnHYn7ZrJylkdse0o1TkrbkInf5MJUsmuRL80%3D%7Ccw5IjQEt%2BOF0P97E%7C06%7C3; ds=e62a1471141a0e692bc0e96ef4505a93'
csrftoken_global = 'fXQuCvrxWa5Hw2J0VOXyei8NhxfBwapR'
token_global = "WXjgsbAQaqh7qb57j0nAtg==|cTsVQJlURLpHn7s6keKlWjYwAQFqi2WpU/vsCwsDVCoCDsy/J1nr4TAZPEeepOKnHYn7ZrJylkdse0o1TkrbkInf5MJUsmuRL80=|cw5IjQEt+OF0P97E|06|3"
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
        data_name = None
        labelId = None
        nameLabel = []
        idlabel = []
        getLabel = cruds.label.getData(db)
        if ( getLabel != None):
            for i in range(len(getLabel)):
                nameLabel.append(getLabel[i].name)
                idlabel.append(getLabel[i].id)
        for i in range(len(nameLabel)):
            # print (nameLabel[i])
            if nameLabel[i].lower() in name.lower():
                labelId = idlabel[i]
                listDict = Product(
                    name = str(name.strip()),
                    link = str(link),
                    image = str(image),
                    priceSale = str(price_min),
                    price = str(price_max),
                    rating = str(rating),
                    labelId = labelId,
                    categoryId = idCategory.id,
                    shopId= idShop.id
                )
                try:
                    data_name = cruds.product.getByName(db , listDict.name)
                except Exception as e:
                    return name
                if (data_name != None):
                    cruds.product.update(db , data_name.id , listDict)
                else:
                    cruds.product.create(db , listDict)
                list_item.append(listDict)
            else:
                continue
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
