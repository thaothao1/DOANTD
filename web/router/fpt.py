from msilib.schema import Class
from multiprocessing.dummy import Array
from traceback import print_tb
from turtle import title
from re import template
from fastapi import APIRouter , Request , Depends ,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.utils import custom_reponse
from sqlalchemy.orm import Session
import cruds 
from db.get_db import get_db
from chemas.product import ProductCreate , ProductUpdate
from models.product import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import time


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")
# thao
@app.get("/fpt")
def getList(db: Session = Depends(get_db) ):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    caps['acceptSslCerts'] = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()) , options=options , desired_capabilities=caps)
    driver.get("https://fptshop.com.vn/dien-thoai")
    actions =  ActionChains(driver)
    time.sleep(3)
    while True:
        try:
            conatiner = driver.find_element(By.CSS_SELECTOR , '.cdt-product--loadmore a')
            actions.click(on_element=conatiner).perform()
            time.sleep(1.3)
        except:
            break;
        
    links = driver.find_elements(By.XPATH , '//div[contains(@class , "cdt-product-wrapper")]/div[contains(@class , "cdt-product  ")]/div[@class="cdt-product__info"]/h3/a')

    listDict = []

    for link in links:
      
        check = None
        
        content = link.get_attribute("textContent").strip()
        
        xPathCheck = '//div[@class="cdt-product__info"]/h3/a[text()="{}"]/parent::h3/parent::div/div[ (@class="cdt-product__price" or @class="cdt-product__show-promo") and normalize-space(.//text())]'.format(content)
        
        try:
          check = driver.find_element(By.XPATH , xPathCheck)
        except:
          pass;
        
        
        if check == None:
          print("No Money: " ,link.get_attribute("href"))
          print("xPath" , xPathCheck)
          continue
        
        
        time.sleep(2)
        href = 'window.open("' + link.get_attribute("href") + '","_blank");'
        driver.execute_script(href)
        time.sleep(1)
        
        while True:
          time.sleep(1)
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
            prices = driver.find_element(By.XPATH ,'//div[@class="st-price-main"]').get_attribute("textContent")
            price_old = None
            price_installment = None
            price_percent = None
            
            try:
              price_percent = driver.find_element(By.XPATH , '//div[@class="st-pd-btn"]/div[@id="btn-installment"]/div/strong').get_attribute("textContent")
            except:
              pass
            try:
              price_old = driver.find_element(By.XPATH , xPrice + '/div[@class="st-price__left"]/div[@class="st-price-sub"]').get_attribute("textContent")
            except:
              pass
            try:
              price_installment = driver.find_element(By.XPATH , xPrice + '/div[@class="st-price__right"]').get_attribute("textContent")
            except:
              pass
            
            imgs = []
            try:
              clickImage = driver.find_element(By.XPATH , '//div[@class="st-slider__feature"]/a')
              actions.click(on_element=clickImage).perform()
              time.sleep(2)
              imgs = [ img.get_attribute('src') for img in driver.find_elements(By.XPATH , '//div[@class="lg-thumb-item"]/img') ]
              clickButton = driver.find_element(By.XPATH , '//div[@class="lg-toolbar lg-group"]/button')
              actions.click(on_element=clickButton).perform()
            except:
              pass
            
            if len(imgs) == 0:
              try:
                imgs = [ img.get_attribute('src') for img in driver.find_elements(By.XPATH , '//div[@class="swiper-wrapper js--slide--full"]/div/img') ]
              except:
                pass
            
            colors = []
            try:
              colors = [color.text.strip() for color in driver.find_elements(By.XPATH , '//div[@class="st-select-color"]/div/p')]
            except:
              pass
            
            gb = "Chưa có thông tin GB"
            
            try:
              gb = driver.find_element(By.XPATH , '//div[@class="st-select"]/a[contains(@class , "active")]/div').get_attribute("textContent")
            except:
              pass
              
            next_gb = None
            
            try:
              next_gb = driver.find_element(By.XPATH ,'//div[@class="st-select"]/a[contains(@class , "active")]/following-sibling::a')
            except:
              pass
            
            # print("item " , " " ,  name , " " , len(ratting) , " " , ratting_total , " " , price , " " , price_old , " " , price_percent , " " , price_installment , " " , gb)
            # print("imgs " , imgs)
            # print("colors " , colors)
            # print("next" , next_gb)
            # 'gb' : gb.strip(),
            product = name.strip()
            url =  str(driver.current_url).strip()
            # 'star' : {
            #   'value' :  len(ratting) ,
            #   'count' : ratting_total
            # },
            image = imgs
            color = colors
            price =  price_old
            priceSale = price_percent
            base = Product(
                  product = str(product),
                  link = url,
                  image = str(image[0]) ,
                  price = str(price),
                  priceSale = str(priceSale),
                  color = str(color),
                  size = "S",
                  description = "NO",
                  quantity = 7,
          )
            data = cruds.product.create(db , base)

            if next_gb != None:
              actions.click(on_element=next_gb).perform()
              time.sleep(1)
              
            else:
              driver.close()
              driver.switch_to.window(driver.window_handles[0])
              actions = ActionChains(driver)
              break
              
          except Exception as e:
            print(e)
            print('error link: {}'.format(driver.current_url))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            actions = ActionChains(driver)
            break
    return custom_reponse(http_status=200 , data= data)

