import scrapy
from ..items import TWShipInfoItem


class TwShipInfoSpiderSpider(scrapy.Spider):
    name = 'TW_Ship_Info_spider'
    # allowed_domains = ['xxx.com']
    # start_urls = ['http://xxx.com/']

    def start_requests(self):
        print('crawl spider——>>>>>>>>>>>')
        # 默认情况下，对同一个URL多次提交下载请求，后面的请求会被去重过滤器过滤。
        # 在多次爬取一个内容随时间而变化的页面时（每次使用相同的URL），可以将该参数
        # 置为True
        yield scrapy.Request('https://mpbais.motcmpb.gov.tw/webservice/geojsonais.ashx',
                             callback=self.parse, dont_filter=True)

    def parse(self, response):
        json_dic = response.json()
        for ship in json_dic['features']:
            ship_item = TWShipInfoItem()
            properties = ship['properties']

            ship_item['IMO_Number'] = properties['IMO_Number']
            ship_item['MMSI'] = properties['MMSI']
            ship_item['ShipName'] = properties['ShipName']
            ship_item['Call_Sign'] = properties['Call_Sign']
            ship_item['Ship_and_Cargo_Type'] = properties['Ship_and_Cargo_Type']
            ship_item['Longitude'] = properties['Longitude']
            ship_item['Latitude'] = properties['Latitude']
            ship_item['COG'] = properties['COG']
            ship_item['SOG'] = properties['SOG']
            ship_item['Record_Time'] = properties['Record_Time']
            ship_item['Navigational_Status'] = properties['Navigational_Status']

            yield ship_item
