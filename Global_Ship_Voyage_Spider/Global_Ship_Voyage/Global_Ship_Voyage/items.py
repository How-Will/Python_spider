# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlobalShipVoyageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Ship_ID = scrapy.Field()
    # Voyage Information
    Departure = scrapy.Field()  # 出发点
    Destination = scrapy.Field()  # 目的地
    Reported_Destination = scrapy.Field()  # 报告目的地
    ATD = scrapy.Field()  # 实际出发时间
    ATA = scrapy.Field()  # 实际到达时间
    ETA = scrapy.Field()  # 船舶报告预计到达时间，还没到之前估计
    Speed_Recorded_Max = scrapy.Field()  # 航行中最大速度
    Speed_Recorded_Ave = scrapy.Field()  # 航行中平均速度
    Draught_Reported = scrapy.Field()  # 报告吃水深度

    # Latest Position
    Position_Received = scrapy.Field()  # 位置更新时间
    Local_Time = scrapy.Field()  # 当地时间
    Area = scrapy.Field()  # 船舶当前所处区域
    Current_Port = scrapy.Field()  # 目前所在港口
    Latitude = scrapy.Field()  # 纬度
    Longitude = scrapy.Field()  # 经度
    Speed = scrapy.Field()  # 速度
    Course = scrapy.Field()  # 航向
    Wind_Speed = scrapy.Field()  # 风速
    Wind_Direction = scrapy.Field()  # 风向
    Air_Temperature = scrapy.Field()  # 气温
