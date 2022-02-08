# 爬取全球船舶信息

1. 目标URL：https://www.marinetraffic.com/

2. 目标数据

   爬取船舶基本信息，如船舶名，呼号，所属国家等属性。

   在 `items.py` 文件中写入需要爬取的属性

   ```python
       # Vessel information
       Ship_ID = scrapy.Field()  # 船舶id
       IMO = scrapy.Field()    # IMO
       Ship_Name = scrapy.Field()  # 船舶名
       Vessel_Type_Generic = scrapy.Field()    # 船舶类型-通用描述
       Vessel_Type_Detailed = scrapy.Field()   # 船舶类型-具体描述
       Status = scrapy.Field()  # 船舶状态，服役或退役
       MMSI = scrapy.Field()   # MMSI
       Call_Sign =scrapy.Field()   # 呼号
       Flag = scrapy.Field()   # 所属国家
       Gross_Tonnage = scrapy.Field()  # 总吨位
       Summer_DWT = scrapy.Field()     # 夏季载重吨
       LengthAndBreadth = scrapy.Field() # 船体长度 x 宽度
       Year_Built = scrapy.Field() # 建造年份
       Home_Port = scrapy.Field()  # 母港
   ```

3. 需求实现

   - 使用UA伪装池。利用下载中间件实现，添加如下代码。之后再 `settings.py` 文件中开启该中间件。

     ```python
     class UA_PoolsMiddleware(UserAgentMiddleware):
         # 初始化
         settings = get_project_settings()
         def __init__(self, user_agent=''):
             self.user_agent = user_agent
     
         def process_request(self, request, spider):
             thisua = random.choice(self.settings.get('UA_POOL'))
             # print('当前使用的User-Agent是: ' + thisua)
             request.headers.setdefault('User-Agent', thisua)
     ```

   - 增加加载页面失败后的重试次数，默认是3次。在 `settings.py` 文件中添加如下字段

     ```python
     # 增加失败重试次数
     RETRY_TIMES = 5
     ```

   - 利用开发者工具进行页面分析后，发现目标数据无法通过目标URL获得。但是可以通过以下URL获取到船舶的 `ship_id`。 之后拼接 `https://www.marinetraffic.com/en/vesselDetails/vesselInfo/shipid:`与 `ship_id` 获得目标URL。

     ```python
     start_urls = ['https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:0/Y:0/station:0',
                   'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:0/Y:1/station:0',
                   'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:1/Y:0/station:0',
                   'https://www.marinetraffic.com/getData/get_data_json_4/z:2/X:1/Y:1/station:0']
     ```

   - 由于要爬取实时数据，故该代码需要多次运行。为了避免爬取到重复的数据，需要做去重操作。

     ```python
     ship_id_set = set()  # 对重复的shipid去重
     gotten_ship_set = set(list(pd.read_csv('vessel_info.csv')['Ship_ID']))  # 对已经获取到的船只验证
     
     if ship_id.isdigit() and ship_id not in self.ship_id_set and ship_id not in self.gotten_ship_set:  # 可以获取到Ship_id
         self.ship_id_set.add(ship_id)  # 加入到集合中
         self.gotten_ship_set.add(ship_id)
         detail_url = self.detail_url_base + ship_id
     ```