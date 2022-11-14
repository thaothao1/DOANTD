from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import json
import time

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

listDict = []

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

        listDict.append({
          'name' : name.strip(),
          'link' : str(driver.current_url).strip(),
          'image' : img,
          'priceSale' : priceSale,
          'price' : price,
          'rating' : len(ratting)
        })
        print(len(listDict))
    except Exception as e:
        print(e)
        print('error link: {}'.format(driver.current_url))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    actions = ActionChains(driver)
    

        
