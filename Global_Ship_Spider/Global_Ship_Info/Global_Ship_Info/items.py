# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VesselInfoItem(scrapy.Item):
    Ship_ID = scrapy.Field()  # 船舶id
    IMO = scrapy.Field()  # IMO
    Ship_Name = scrapy.Field()  # 船舶名
    Vessel_Type_Generic = scrapy.Field()  # 船舶类型-通用描述
    Vessel_Type_Detailed = scrapy.Field()  # 船舶类型-具体描述
    Status = scrapy.Field()  # 船舶状态，服役或退役
    MMSI = scrapy.Field()  # MMSI
    Call_Sign = scrapy.Field()  # 呼号
    Flag = scrapy.Field()  # 所属国家
    Gross_Tonnage = scrapy.Field()  # 总吨位
    Summer_DWT = scrapy.Field()  # 夏季载重吨
    LengthAndBreadth = scrapy.Field()  # 船体长度 x 宽度
    Year_Built = scrapy.Field()  # 建造年份
    Home_Port = scrapy.Field()  # 母港
