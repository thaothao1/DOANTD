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

@app.post("/project")
def getList(db: Session = Depends(get_db) ):
    codeHTML = CodeHTML("https://www.thegioididong.com/dtdd")
    htmlTest = codeHTML.beautifulSoup()
    name = htmlTest.findAll("li" , class_="item ajaxed __cate_42")
    test = []
    data_id = []
    for i in name:
        item={}
        data = i.find("a")
        image = i.find("img")
        item["product"] = data["data-name"] 
        item["price"]   = data["data-price"] 
        item["link"] =  data["href"] 
        if "-src" in str(image):
            item["image"] = image["data-src"]
        else:
            item["image"] = image["src"]
        test.append(item)
        # data = cruds.product.create(db , item)
    return test
