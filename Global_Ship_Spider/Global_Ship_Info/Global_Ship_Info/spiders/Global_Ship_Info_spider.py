import scrapy
from ..items import VesselInfoItem
import pandas as pd


class GlobalShipInfoSpiderSpider(scrapy.Spider):
    name = 'Global_Ship_Info_spider'
    # allowed_domains = ['xxx.com']

    start_urls = ['https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:0/Y:0/station:0',
                  'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:0/Y:1/station:0',
                  'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:1/Y:0/station:0',
                  'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:1/Y:1/station:0']

    ship_id_set = set()  # 对重复的shipid去重
    gotten_ship_set = set(list(pd.read_csv('vessel_info.csv')['Ship_ID']))  # 对已经获取到的船只验证去重

    detail_url_base = 'https://www.marinetraffic.com/en/vesselDetails/vesselInfo/shipid:'

    # 解析获得每艘船的shipid
    def parse(self, response):
        info_dict = response.json()
        area_ships = info_dict['data']['areaShips']  # 获取该地区的船舶数量
        ships_data_list = info_dict['data']['rows']  # 该地区所有船舶的数据列表

        for i in range(area_ships):
            ship_id = ships_data_list[i]['SHIP_ID']
            if ship_id.isdigit() and ship_id not in self.ship_id_set and ship_id not in self.gotten_ship_set:  # 可以获取到Ship_id
                self.ship_id_set.add(ship_id)  # 加入到集合中
                self.gotten_ship_set.add(ship_id)
                detail_url = self.detail_url_base + ship_id

                yield scrapy.Request(detail_url, callback=self.parse_detail,
                                     meta={'ship_id': ship_id})

    # 解析获得详细信息
    def parse_detail(self, response):
        detail_json = response.json()
        vessel_info_item = VesselInfoItem()

        vessel_info_item['Ship_ID'] = response.meta['ship_id']
        vessel_info_item['IMO'] = detail_json['imo']
        vessel_info_item['Ship_Name'] = detail_json['name']
        vessel_info_item['Vessel_Type_Generic'] = detail_json['type']
        vessel_info_item['Vessel_Type_Detailed'] = detail_json['typeSpecific']
        vessel_info_item['Status'] = detail_json['status']
        vessel_info_item['MMSI'] = detail_json['mmsi']
        vessel_info_item['Call_Sign'] = detail_json['callsign']
        vessel_info_item['Flag'] = detail_json['country']
        vessel_info_item['Gross_Tonnage'] = detail_json['grossTonnage']
        vessel_info_item['Summer_DWT'] = detail_json['deadweight']
        # 长度和宽度需要进行下转换
        vessel_info_item['LengthAndBreadth'] = str(detail_json['length']) + ' x ' + str(detail_json['breadth'])
        vessel_info_item['Year_Built'] = detail_json['yearBuilt']
        vessel_info_item['Home_Port'] = detail_json['homePort']

        print('MY_IMO', vessel_info_item['IMO'])

        yield vessel_info_item
