# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TWShipInfoItem(scrapy.Item):
    IMO_Number = scrapy.Field()
    MMSI = scrapy.Field()
    ShipName = scrapy.Field()   # 船名
    Call_Sign = scrapy.Field()  # 呼号
    Ship_and_Cargo_Type = scrapy.Field()    # 船舶类型
    Longitude = scrapy.Field()  # 经度
    Latitude = scrapy.Field()   # 纬度
    COG = scrapy.Field()    # 航行
    SOG = scrapy.Field()    # 航速
    Record_Time = scrapy.Field()    # 记录时间
    Navigational_Status = scrapy.Field()    # 航行状态
