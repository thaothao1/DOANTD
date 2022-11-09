# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    gb = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    star = scrapy.Field()
    imgs = scrapy.Field()
    colors = scrapy.Field()
    store = scrapy.Field()
