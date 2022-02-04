# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YangtzeWaterlevelItem(scrapy.Item):
    location = scrapy.Field()   # 地点
    water_level = scrapy.Field()     # 水位
    time = scrapy.Field()   # 时间
