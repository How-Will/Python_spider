# 爬取书籍信息

1. 目标URL：https://books.toscrape.com/

2. 项目搭建

   ```bash
   scrapy startproject Yangtze_Waterlevel   # 创建项目
   scrapy genspider Yangtze_Waterlevel_spider xxx.com  # 创建爬虫文件
   scrapy crawl Yangtze_Waterlevel_spider -o books.csv # 开始爬取
   ```

3. 目标数据

   - 书名
   - 价格
   - 评价等级
   - 产品编码
   - 库存量
   - 评价数量

4. 需求实现

   - 价格以RMB为单位存储

     在 `pipeline.py` 中实现 `PriceConverterPipeline` ，之后再 `settings.py` 中启用该管道

     ```cpp
     class PriceConverterPipeline(object):
         # 英镑兑换人民币汇率
         exchange_rate = 8.5309
         def process_item(self, item, spider):
             # 提取item的price字段
             price = float(item['price'][1:]) * self.exchange_rate
     
             # 保留2位小数，赋值回item的price字段
             item['price'] = '￥%.2f' % price
             return item
     ```

   - 过滤重复数据

     同样利用管道的方式实现

     ```python
     class DuplicatesPipeline(object):
         # 去除重复数据
         def __init__(self):
             self.book_set = set()
     
         def process_item(self, item, spider):
             name = item['name']
             if name in self.book_set:
                 # DropItem异常，则该item会被抛弃，不在递送给后面的Pipeline处理，也不会导出到文件。
                 # 如果检测到无效数据或要过滤数据时，抛出DropItem异常
                 raise DropItem("Duplicate book found: %s" % item)
     
             self.book_set.add(name)
             return item
     ```
     
   - 使评价等级易读

     利用管道实现

     ```python
     class BookPipeline(object):
         review_rating_map = {
             'One': 1,
             'Two': 2,
             'Three': 3,
             'Four': 4,
             'Five': 5,
         }
     
         def process_item(self, item, spider):
             rating = item.get('review_rating')
             if rating:
                 item['review_rating'] = self.review_rating_map[rating]
     
             return item
     ```

     