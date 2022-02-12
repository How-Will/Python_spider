# 爬取全球船舶实时航程信息

1. 目标URL：https://www.marinetraffic.com/

2. 目标数据

   ```python
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
   ```

3. 需求实现

   - 不能直接通过目标URL获取数据。目标数据在船舶的详情页当中，所以通过间接爬取船舶详情页来获取数据。船舶详情页的URL为：

     ```html
     https://www.marinetraffic.com/en/ais/details/ships/shipid: 船舶id
     ```

   - 某些船舶的数据是卫星数据，需要会员才能访问，因此该数据是无法获取的，需要过滤掉这类数据。过滤的条件是该类数据的 `ship_id` 是字符串乱码。

     ```python
     if ship_id.isdigit():   # 可以获取到的Ship_id
         # code
     ```

   - 船舶的详情页是动态加载的，因此需要用到 `splash` 动态渲染引擎，实现渲染好页面在进行爬取。在 `settings.py` 文件中配置好 `splash`。并且用 `SplashRequest` 代替 `scrapy.Request`

     ```python
     yield SplashRequest(url=detail_url, endpoint='render.html',
                         args={'images': 0, 'timeout': 30, 'wait': 6, 'resource_timeout': 20},
                         meta={'ship_id': ship_id, 'lat': latitude,'lon': longitude, 'speed': speed,'course': course},
                         callback=self.parse_detail)
     ```
     
   - 提高爬虫效率

     - 如果不是真的需要 cookie ，则在 scrapy 爬取数据时可以禁止cookie从而减少CPU的使用率，提升爬取效率。在配置文件中编写：`COOKIES_ENABLED = False`

     - 在配置文件中设置失败重试的次数，可以提高效率

       ```python
       RETRY_ENABLED = True                     # 默认开启失败重试，一般关闭
       RETRY_TIMES = 2                          # 失败后重试次数，默认两次
       RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]    # 碰到这些验证码，才开启重试
       ```

     - 减少下载超时：如果对一个非常慢的链接进行爬取，减少下载超时可以能让卡住的链接快速被放弃，从而提升效率。在配置文件中进行编写：`DOWNLOAD_TIMEOUT = 10`，超时时间为10s。默认设置下载超时为180s。

     

4. 错误解决

   - 出现如下的错误提示

     ```shell
       hostname, aliases, ipaddrs = gethostbyaddr(name)
     UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbd in position 0: invalid start byte
     ```

     该错误的出现原因是主机名的编码格式无法用utf-8解析。如果是中文主机名，修改成英文即可。

