import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

from base.items import CrawlerItem
 
        
class TgddSpider(scrapy.Spider):
    name = "tgdd"
    
    def start_requests(seft):
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://www.thegioididong.com/dtdd#c=42&o=9&pi=1")
        actions =  ActionChains(driver)
        time.sleep(5)
        while True:
            try:
                conatiner = driver.find_element(By.CSS_SELECTOR , '.view-more a')
                actions.click(on_element=conatiner).perform()
                time.sleep(1.3)
            except:
                break;
            
        links = driver.find_elements(By.XPATH , '//ul[@class="listproduct"]/li/a[@class="main-contain"]')
        
        for link in links:
            href = link.get_attribute('href')
            yield scrapy.Request(href , callback=seft.parse)
            print("thao ơi2" )
        driver.quit()
    
            
    def parse(self, response):
        print("thao ơi1")
        xPathActive = '//a[starts-with(@href , "/dtdd") and contains(@class , "box03__item item act") and not(@data-color)]'
        xPathActiveNext = xPathActive + '/following-sibling::a'
        
        current = Selector(response).xpath(xPathActive)
        current_next = Selector(response).xpath(xPathActiveNext)
        print("thao ơi" , len(current_next))
        
        if len(current_next) > 0 :
            yield self.passItem(current  , response)
            href = 'https://www.thegioididong.com' + current_next[0].xpath('@href').get()
            yield scrapy.Request(href , callback=self.parse)
        else:   
            yield self.passItem(current  , response)
            

    def passItem(self , config , response):
        item = CrawlerItem()
        gb = config.xpath('text()').get()     
        name = response.xpath('//h1/text()').get()
        try:       
            href = 'https://www.thegioididong.com' + config.xpath('@href').get()
        except:
            href = response.url
        print("item = " , name , " " , href)
        itemStar = Selector(response).xpath('count(//div[@class="box02"]/div/div/p[not(@class)]/i[@class="icondetail-star"])').get()
        itemTotal = Selector(response).xpath('//div[@class="box02"]/div/div/p[@class="detail-rate-total"]/text()').get()
        if itemTotal != None:
            itemTotal += ' đánh giá'
        imgs = Selector(response).xpath('//div[@class="item-border"]/img').xpath('@data-src').getall()
        colors = Selector(response).xpath('//a[starts-with(@href , "/dtdd") and contains(@class , "box03__item item") and count(@data-color) > 0]/text()').getall()
        
        # price
        xPathprice = '//div[@class="price-one"]/div[@class="box-price"]'
        prices_container = Selector(response).xpath(xPathprice)
        
        if len(prices_container) == 0:
            xPathprice = '//div[@class="price-two"]/div'
            prices_container = Selector(response).xpath(xPathprice)
        
        xPathpricePresent = './p[@class="box-price-present"]/text()'
        xPathpriceOld = './p[@class="box-price-old"]/text()'
            
        price = prices_container[0].xpath(xPathpricePresent).get()
        price_old = prices_container[0].xpath(xPathpriceOld).get()
        priceO = None    
        price_O_old = None

        
        if  xPathprice == '//div[@class="price-two"]/div':
            
            priceO = prices_container[1].xpath(xPathpricePresent).get()
            price_O_old = prices_container[1].xpath(xPathpriceOld).get()
            
            print("online " , priceO , " " , price_O_old)

        if gb == None:
            gb = "Chưa có thông tin GB"
        
        item['gb'] = gb.strip()
        item['name'] = name.strip()
        item['href'] = href.strip()
        item['star'] = {
            'value' :  itemStar,
            'count' : itemTotal
        }
        item['imgs'] = [ img.strip() for img in imgs ]
        item['colors'] = [ color.strip() for color in colors ]
        item['store'] = {
            'offline': {
                'price' : price,
                'price_old': price_old,
            },
            'online': {
                'price' : priceO,
                'price_old': price_O_old,
            }
        }
        print(item)
        return item
        
# convert Json 
# with open('../../tgdd.json', 'w' , encoding='utf-8') as f:
#     json.dump(carr, f, indent=2 , ensure_ascii= False)
#     print("New json file is created from data.json file")
