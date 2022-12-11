import cruds 
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models.label import Label
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
import time
from models.product import Product
import re
from models.category import Category

app = APIRouter()

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--no-proxy-server")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = None

@app.get("/fptShop")
def getListProductFPTShop(db: Session = Depends(get_db) ):
    global driver
    try:
        # options = webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors-spki-list')
        # options.add_argument('--ignore-ssl-errors')
        # options.add_argument("--headless")
        # caps = webdriver.DesiredCapabilities.CHROME.copy()
        # caps['acceptInsecureCerts'] = True
        # caps['acceptSslCerts'] = True

        driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
        # driver = webdriver.Chrome(options=options, executable_path='../chromedriver')

        https = [
        {
            "type": "dienthoai",
            "url": "https://fptshop.com.vn/dien-thoai",
        },
        {
            "type": "laptop",
            "url": "https://fptshop.com.vn/may-tinh-xach-tay",
        },
        ]

        shop = Shop(
            name = "fpt",
            link = "https://fptshop.com.vn",
        )
        idShop = cruds.shop.getByName(db , "fpt")
        if idShop is None:
            idShop = cruds.shop.create(db , shop)
        base = []
        for http in https:
            
            if ( http["type"] == "dienthoai"):
                idCategory = cruds.category.getByName(db , "Điện thoại")
                if idCategory is None:
                    data = Category(
                        name = "Điện thoại"
                    )
                    idCategory = cruds.category.create(db , data)      
            if ( http["type"] == "laptop"):
                idCategory = cruds.category.getByName(db , "Laptop")
                if idCategory is None:
                    data = Category(
                        name = "Laptop"
                    )
                    idCategory = cruds.category.create(db , data)        
            driver.get(http.get('url'))
            actions =  ActionChains(driver)
            time.sleep(3)
            while True:
                try:
                    conatiner = driver.find_element(By.CSS_SELECTOR , '.cdt-product--loadmore a')
                    actions.click(on_element=conatiner).perform()
                    time.sleep(1.3)
                    # break
                except:
                    break
                
            links = driver.find_elements(By.XPATH , '//div[contains(@class , "cdt-product-wrapper")]/div[contains(@class , "cdt-product")]/div[@class="cdt-product__info"]/h3/a')
            for link in links:
                check = None
                content = link.get_attribute("textContent")
                
                xPathCheck = '//div[@class="cdt-product__info"]/h3/a[text()="{}"]/parent::h3/parent::div/div[ (@class="cdt-product__price" or @class="cdt-product__show-promo") and normalize-space(.//text())]'.format(content)
                
                try:
                    check = driver.find_element(By.XPATH , xPathCheck)
                except:
                    pass
                
                
                if check == None:
                    print("No Money: " , link.get_attribute("href"))
                    print("xPath" , xPathCheck)
                    continue
                
                
                time.sleep(2)
                href = 'window.open("' + link.get_attribute("href") + '","_blank");'
                driver.execute_script(href)
                time.sleep(2)

                driver.switch_to.window(driver.window_handles[-1])
                actions =  ActionChains(driver)
                time.sleep(2)

                try:
                    
                    name = driver.find_element(By.XPATH , '//h1[@class="st-name"]').get_attribute("textContent")
                    
                    spName = name.split()
                    spName.pop()
                    name = ' '.join(spName)
                    
                    ratting = "0.0"
                    ratting_total = None
                    
                    try:        
                        ratting = driver.find_elements(By.XPATH , '//ul[@class="st-rating__star"]/li/span[contains(@class , "icon-star fill")]')  
                    except:
                        pass
                    
                    try:
                        ratting_total = driver.find_element(By.XPATH , '//div[@class="st-rating__link"]/a').get_attribute("textContent")
                    except:
                        pass
                    
                    xPrice = '//div[@class="st-price"]'
                    try:
                        price = driver.find_element(By.XPATH ,'//div[@class="st-price-main"]').get_attribute("textContent")
                    except:
                        xPrice = '//div[@class="shock-deal"]/div/div/div[@class="text"]/p/'
                        price = driver.find_element(By.XPATH , xPrice + 'b').get_attribute("textContent")

                    price_old = None
                    
                    try:
                        price_old = driver.find_element(By.XPATH , xPrice + '/div[@class="st-price__left"]/div[@class="st-price-sub"]').get_attribute("textContent")
                    except:
                        try:
                            price_old = driver.find_element(By.XPATH , xPrice + 'strike').get_attribute("textContent")
                        except:
                            price_old = price
                    
                    try:
                        imgs = driver.find_element(By.XPATH , '//div[@class="swiper-wrapper js--slide--full"]/div/img').get_attribute("src")
                        print("DIEU12345678", imgs)
                    except:
                        pass

                    try:        
                        label = driver.find_element(By.XPATH , '//div[@class="row"]//li[@class="breadcrumb-item  active"]/a').get_attribute("title")
                    except:
                        label = ""
                    nameLabel = label.strip()
                    lbId = cruds.label.getByName(db , nameLabel.lower())
                    if (lbId == None):
                        lb = Label(
                            name = nameLabel.lower(),
                            categoryId = idCategory.id,
                        )
                        lbId = cruds.label.create( db, lb )
                    listDict = Product(
                        name = name.strip(),
                        link = str(driver.current_url).strip(),
                        image = imgs,
                        priceSale = str(price),
                        price = str(price_old),
                        rating = str(len(ratting)),
                        labelId = lbId.id,
                        shopId = idShop.id,
                        categoryId = idCategory.id
                    )
                    # data_name = cruds.product.getByName(db , name.strip())
                    # if ( data_name != None):
                    #     cruds.product.update(db , data_name.id , listDict)
                    # else:
                    cruds.product.create(db , listDict)
                    base.append(listDict)
                except Exception as e:
                    print(e)
                    print('error link: {}'.format(driver.current_url))
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                actions = ActionChains(driver)  
        return custom_reponse(http_status=200 , data= base)
    except Exception as e:
        return HTTPException(status_code=400 , detail="Crawl data FPT error")
    finally :
        if driver != None:
            driver.quit()
            driver = None
