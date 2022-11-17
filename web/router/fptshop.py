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
from base.getname import getname


app = APIRouter()
# templates = Jinja2Templates(directory = "templates")

@app.get("/fptShop")
def getListProductFPTShop(db: Session = Depends(get_db) ):
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
          # break
      except:
          break
      
  links = driver.find_elements(By.XPATH , '//div[contains(@class , "cdt-product-wrapper")]/div[contains(@class , "cdt-product  ")]/div[@class="cdt-product__info"]/h3/a')

  listDict = []

  shop = Shop(
    name = "FPT shop",
    link = "https://fptshop.com.vn",
  )
  idShop = cruds.shop.getByName(db , "FPT shop")
  if idShop is None:
     idShop = cruds.shop.create(db , shop)

  for link in links:
    
      check = None
      
      content = link.get_attribute("textContent").strip()
      
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
                  price_old = "Không giảm"
          
          try:
            imgs = driver.find_element(By.XPATH , '//div[@class="swiper-wrapper js--slide--full"]/div/img').get_attribute("src")
          except:
            pass
          link = str(driver.current_url).strip(),
          # shop = "https://fptshop.com.vn/dien-thoai/"
          # label = getname.getLabel(shop,link)
          # idLabel = cruds.label.getByName(db ,label)
          # if idLabel == None :
          #   createLabel = Label(
          #     name = label
          #   )
          #   idLabel = cruds.label.create(db, createLabel)
          # print(label)
          # print(idLabel)
          product = Product(
            name = name.strip(),
            link = link,
            image = imgs,
            priceSale = str(price),
            price = str(price_old),
            rating =  str(len(ratting)),
            shopId = idShop.id,
          )
          base = cruds.product.create(db , product)
      except Exception as e:
          print(e)
          print('error link: {}'.format(driver.current_url))
      
      driver.close()
      driver.switch_to.window(driver.window_handles[0])
      actions = ActionChains(driver)
  return base