import scrapy
from scrapy.selector import Selector


class listSpider(scrapy.Spider):

    name = "list"
    start_urls = 'https://www.thegioididong.com/'

    def start_requests(self):
        urls = [
            self.start_urls
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
  
    def parse(self, response):
        lis = Selector(response).xpath('//li[@class="has-list"]')
        
        print("len" , len(lis))
        
        for i in lis :
            href = i.xpath('//a/@href').get()
            name = i.xpath('//a/span/text()').get()
            
            print("item=" , href, " " , name)