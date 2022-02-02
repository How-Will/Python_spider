# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PriceConverterPipeline(object):
    # 英镑兑换人民币汇率
    exchange_rate = 8.5309

    def process_item(self, item, spider):
        # 提取item的price字段
        price = float(item['price'][1:]) * self.exchange_rate

        # 保留2位小数，赋值回item的price字段
        item['price'] = '￥%.2f' % price
        return item



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


