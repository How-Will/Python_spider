import scrapy
from scrapy_splash import SplashRequest
from ..items import GlobalShipVoyageItem

lua_script = """

function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(8))
  return splash:html()
end
"""


class GlobalShipVoyageSpiderSpider(scrapy.Spider):
    name = 'Global_Ship_Voyage_spider'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:0/Y:0/station:0',
                  'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:0/Y:1/station:0',
                  'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:1/Y:0/station:0',
                  'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:1/Y:1/station:0']

    base_url = 'https://www.marinetraffic.com/en/ais/details/ships/shipid:'


    def parse(self, response):
        info_dict = response.json()
        area_ships = info_dict['data']['areaShips'] # 获取该地区的船舶总量
        print('Area_ships: ', area_ships)

        ships_data_list = info_dict['data']['rows'] # 该地区所有船舶的数据列表

        for i in range(area_ships):
            ship_id = ships_data_list[i]['SHIP_ID']

            if ship_id.isdigit():   # 可以获取到的Ship_id
                latitude = ships_data_list[i]['LAT']
                longitude = ships_data_list[i]['LON']
                speed = ships_data_list[i]['SPEED']     # 速度，单位knots
                if speed:
                    speed = int(speed)
                    speed *= 0.1
                course = ships_data_list[i]['COURSE']   # 航向

                detail_url = self.base_url + ship_id

                yield SplashRequest(url=detail_url, endpoint='execute',
                                    args={'images': 0, 'timeout': 30, 'lua_source': lua_script},
                                    cache_args=['lua_source'],
                                    meta={'ship_id': ship_id, 'lat': latitude,
                                          'lon': longitude, 'speed': speed,
                                          'course': course},
                                    callback=self.parse_detail)

                # yield SplashRequest(url=detail_url, endpoint='render.html',
                #                     args={'images': 0, 'timeout': 30, 'wait': 10, 'resource_timeout': 20},
                #                     meta={'ship_id': ship_id, 'lat': latitude,
                #                           'lon': longitude, 'speed': speed,
                #                           'course': course},
                #                     callback=self.parse_detail)
            else:
                yield None


    # 解析获得船舶的航行信息和位置信息
    def parse_detail(self, response):
        info_item = GlobalShipVoyageItem()

        info_item['Ship_ID'] = response.meta['ship_id']
        info_item['Latitude'] = response.meta['lat']
        info_item['Longitude'] = response.meta['lon']
        info_item['Speed'] = response.meta['speed']
        info_item['Course'] = response.meta['course']

        # Voyage Info某些船舶可能没有
        Dep_Country = response.xpath(
            '//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]/div[1]/div/div[1]'
            '/a/span/b/text()').extract_first()
        Departure_Port = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]'
                                        '/div[1]/div/div[1]/a/b/text()').extract_first()
        Departure = None
        if Dep_Country and Departure_Port:
            Departure = Dep_Country + ' ' + Departure_Port
        elif Dep_Country:
            Departure = Dep_Country
        elif Departure_Port:
            Departure = Departure_Port

        Des_Country = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]'
                                     '/div[1]/div/div[2]/a/span/b/text()').extract_first()
        Destination_Port = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]'
                                          '/div[1]/div/div[2]/a/b/text()').extract_first()
        Destination = None
        if Des_Country and Destination_Port:
            Destination = Des_Country + ' ' + Destination_Port
        elif Des_Country:
            Destination = Des_Country
        elif Destination_Port:
            Destination = Destination_Port

        Reported_Destination = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div'
                                              '/div[8]/b/text()').extract_first()

        ATD = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]/div[3]/div'
                             '/div[1]/span/span/text()').extract_first()
        if ATD:
            ATD = ATD[1:]
        flag = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]/div[3]/div'
                              '/div[2]/span/b/text()').extract_first()
        time = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div/div[2]/div[3]/div'
                              '/div[2]/span/span/text()').extract_first()
        ATA = None
        if flag == 'ATA':
            ATA = time[1:]
        ETA = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div'
                             '/div/div/div[4]/b/text()').extract_first()

        Speed_Recored = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div/div'
                                       '/div[15]/b/text()').extract()
        Speed_Max, Speed_Ave = None, None
        if Speed_Recored:
            Speed_Max, Speed_Ave = Speed_Recored[0].split('/')

        Draught_Reported = response.xpath('//*[@id="vesselDetails_voyageInfoSection"]/div[2]/div/div'
                                          '/div/div[13]/b/text()').extract_first()
        if Draught_Reported:
            Draught_Reported = Draught_Reported.replace('/', '')

        # Latest Position Info基本都是有的
        Position_Received = response.xpath('//*[@id="vesselDetails_latestPositionSection"]/div[2]/div/div/div'
                                           '/div/div[1]/p[1]/b/text()[1]').extract_first()
        Local_Time = response.xpath('//*[@id="vesselDetails_latestPositionSection"]/div[2]/div'
                                    '/div/div/div/div[1]/p[2]/b/text()').extract_first()
        Area = response.xpath('//*[@id="vesselDetails_latestPositionSection"]/div[2]/div'
                              '/div/div/div/div[1]/p[3]/b/text()').extract_first()
        Current_Port = response.xpath('//*[@id="vesselDetails_latestPositionSection"]/div[2]/'
                                      'div/div/div/div/div[1]/p[4]/b//text()').extract_first()

        Wind_Speed = response.xpath('//*[@id="windInfo"]/div[2]/p[1]/b/text()').extract_first()
        Wind_Direction = response.xpath('//*[@id="windInfo"]/div[2]/p[2]/b/text()').extract_first()
        Air_Temp = response.xpath('//*[@id="windInfo"]/div[2]/p[3]/b/text()').extract_first()

        if Position_Received:
            info_item['Departure'] = Departure
            info_item['Destination'] = Destination
            info_item['Reported_Destination'] = Reported_Destination
            info_item['ATD'] = ATD
            info_item['ATA'] = ATA
            info_item['ETA'] = ETA
            info_item['Speed_Recorded_Max'] = Speed_Max
            info_item['Speed_Recorded_Ave'] = Speed_Ave
            info_item['Draught_Reported'] = Draught_Reported
            info_item['Position_Received'] = Position_Received
            info_item['Local_Time'] = Local_Time
            info_item['Area'] = Area
            info_item['Current_Port'] = Current_Port
            info_item['Wind_Speed'] = Wind_Speed
            info_item['Wind_Direction'] = Wind_Direction
            info_item['Air_Temperature'] = Air_Temp
        else:
            file_name = response.meta['ship_id'] + '.html'
            with open(file_name, 'w', encoding='utf-8') as fp:
                fp.write(response.text)

        print(info_item['Ship_ID'])

        yield info_item




