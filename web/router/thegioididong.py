import json
import requests
import cruds 
from msilib.schema import Class
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from base.getname import getname
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
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


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/thegioididong")
def getListProductShoppe(db: Session = Depends(get_db) ):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    caps['acceptSslCerts'] = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.thegioididong.com/dtdd")
    actions =  ActionChains(driver)
    time.sleep(5)
    while True:
        try:
            conatiner = driver.find_element(By.CSS_SELECTOR , '.view-more a')
            actions.click(on_element=conatiner).perform()
            time.sleep(2)
        except:
            break

    links = driver.find_elements(By.XPATH , '//ul[@class="listproduct"]/li/a[@class="main-contain"]')
    shop = Shop(
        name = "Thế giới di động",
        link = "https://www.thegioididong.com",
    )
    idShop = cruds.shop.getByName(db , "Thế giới di động")
    if idShop is None:
        idShop = cruds.shop.create(db , shop)
    for link in links:

        href = 'window.open("' + link.get_attribute("href") + '","_blank");'
        driver.execute_script(href)
        time.sleep(2)

        try:
            driver.switch_to.window(driver.window_handles[-1])
            actions =  ActionChains(driver)
            time.sleep(2)

            name = driver.find_element(By.XPATH , '//section[@class = "detail "]/h1').get_attribute("textContent")
            # print("DIEU123 : ", name)

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

            img = driver.find_element(By.XPATH, '//div[@class="owl-item active"]/a/img').get_attribute("src")
            print("hinhanh : ", img)

            price_present = driver.find_element(By.XPATH, '//p[@class="box-price-present"]').get_attribute("textContent")
            priceSale = price_present.split('*')[0]
            try:
                price = driver.find_element(By.XPATH, '//p[@class="box-price-old"]').get_attribute("textContent")
            except Exception:
                price = "Không giảm"
            # print("price1 : ", priceSale)
            # print("DieuPrice : ", price)
            size = len(ratting)
            product = Product(
                name = name.strip(),
                link = str(driver.current_url).strip(),
                image = img,
                priceSale = str(priceSale),
                price = str(price),
                rating = str(size),
                shopId = idShop.id,
            )
            base = cruds.product.create(db , product)
            print(base)
        except Exception as e:
            print(e)
            print('error link: {}'.format(driver.current_url))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        actions = ActionChains(driver)

    return True
