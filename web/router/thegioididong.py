import json
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.category import Category
from models.shop import Shop
from router.utils import custom_reponse
from sqlalchemy.orm import Session
from db.get_db import get_db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from models.product import Product
import re
from models.label import Label
import cruds


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--no-proxy-server")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = None

@app.get("/thegioididong")
def getListProductShoppe(db: Session = Depends(get_db) ):
    global driver
    try:
        # options = webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors-spki-list')
        # options.add_argument('--ignore-ssl-errors')
        # caps = webdriver.DesiredCapabilities.CHROME.copy()
        # caps['acceptInsecureCerts'] = True
        # caps['acceptSslCerts'] = True
        driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
        https = [
        {
            "type": "dienthoai_thegioididong_crawl",
            "url": "https://www.thegioididong.com/dtdd",
        },
        {
            "type": "laptop_thegioididong_crawl",
            "url": "https://www.thegioididong.com/laptop",
        },
        ]
        print(len(https))
        shop = Shop(
            name = "Thế giới di động",
            link = "https://www.thegioididong.com",
        )
        idShop = cruds.shop.getByName(db , "Thế giới di động")
        if idShop is None:
            idShop = cruds.shop.create(db , shop)
        listDict = []
        for i in https:
            print(i)
            if ( i["type"] == "dienthoai_thegioididong_crawl"):
                idCategory = cruds.category.getByName(db , "Điện thoại")
                if idCategory is None:
                    data = Category(
                        name = "Điện thoại"
                    )
                    idCategory = cruds.category.create(db , data)      
            if ( i["type"] == "laptop_thegioididong_crawl"):
                idCategory = cruds.category.getByName(db , "Laptop")
                if idCategory is None:
                    data = Category(
                        name = "Laptop"
                    )
                    idCategory = cruds.category.create(db , data)    
            time.sleep(2)
            driver.get(i.get('url'))
            actions =  ActionChains(driver)
            time.sleep(3)
            while True:
                try:
                    conatiner = driver.find_element(By.CSS_SELECTOR , '.view-more a')
                    actions.click(on_element=conatiner).perform()
                    time.sleep(2)
                except:
                    break

            links = driver.find_elements(By.XPATH , '//ul[@class="listproduct"]/li/a[@class="main-contain"]')

            for link in links:

                href = 'window.open("' + link.get_attribute("href") + '","_blank");'
                driver.execute_script(href)
                time.sleep(2)

                try:
                    label = link.get_attribute("data-brand")
                except:
                    label = ""

                try:
                    driver.switch_to.window(driver.window_handles[-1])
                    actions =  ActionChains(driver)
                    time.sleep(2)

                    name = driver.find_element(By.XPATH , '//section[@class = "detail "]/h1').get_attribute("textContent")
                    # print("name : ", name)

                    ratting = "0.0"
                    ratting_total = None
                    
                    try:
                        ratting = driver.find_elements(By.XPATH , '//div[@class="box02"]/div/div/p[not(@class)]/i[@class="icondetail-star"]') 
                        # print("hello : ", len(ratting))
                    except Exception:
                        ratting = 0
                    
                    try:
                        ratting_total = driver.find_element(By.XPATH , '//div[@class="box02"]/div/div/p[@class="detail-rate-total"]').get_attribute("textContent")
                        # print("xinchao : ", ratting_total)
                    except Exception:
                        ratting_total = 0

                    try:
                        img = driver.find_element(By.XPATH, '//div[@class="owl-item active"]/a/img').get_attribute("src")
                        # print("hinhanh : ", img)
                    except:
                        pass

                    price_present = driver.find_element(By.XPATH, '//p[contains(@class ,"box-price-present")]').get_attribute("textContent")
                    priceSale = price_present.split('*')[0]
                    try:
                        price = driver.find_element(By.XPATH, '//p[@class="box-price-old"]').get_attribute("textContent")
                    except Exception:
                        price = priceSale

                    name = name.strip()
                    link = str(driver.current_url).strip()
                    rating = len(ratting)
                    nameLabel = label.strip()
                    lbId = cruds.label.getByName(db , nameLabel.lower())
                    if (lbId == None):
                        lb = Label(
                            name = nameLabel.lower(),
                            categoryId = idCategory.id,
                            )
                        lbId = cruds.label.create( db, lb )
                    product = Product(
                        name = str(name),
                        link = str(link),
                        image = str(img),
                        priceSale = str(priceSale),
                        price = str(price),
                        rating = str(rating),
                        labelId = lbId.id,
                        shopId = idShop.id,
                        categoryId = idCategory.id
                )
                    data_name = cruds.product.getByName(db , name)
                    if ( data_name != None):
                        cruds.product.update(db , data_name.id , product )
                    else:
                        cruds.product.create(db , product)
                    listDict.append(product)
                except Exception as e:
                    print(e)
                    print('error link: {}'.format(driver.current_url))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                actions = ActionChains(driver)
        return custom_reponse(http_status=200 , data= listDict)
    except Exception as e:
        return HTTPException(status_code=400 , detail="Crawl data TGDD error")
    finally:
        if driver != None:
            driver.quit()
            driver = None