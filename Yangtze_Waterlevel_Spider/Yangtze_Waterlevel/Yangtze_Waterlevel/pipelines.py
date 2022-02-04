# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class TimeFormatPipeline(object):
    # 对时间的格式进行调整
    def time_format(self, time):
        time = time.replace('年', '/')
        time = time.replace('月', '/')
        time = time.replace('日', '/')
        time = time.replace('点', '')

        time_list = time.split('/')
        if len(time_list[1]) == 1:
            time_list[1] = '0' + time_list[1]
        if len(time_list[2]) == 1:
            time_list[2] = '0' + time_list[2]
        if len(time_list[3]) == 1:
            time_list[3] = '0' + time_list[3]

        time = '/'.join(time_list)
        return time

    def process_item(self, item, spider):
        time = item['time']
        time = time.replace('水位公告', '')
        time = self.time_format(time)

        # 将格式化后的时间赋值给item['time']
        item['time'] = time

        return item


