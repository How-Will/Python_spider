# 爬取长江海事局的水位数据

1. 目标URL：https://cj.msa.gov.cn/xxgk/xxgkml/aqxx/swgg/

2. 目标数据
   - 地点
   - 水位
   - 时间
   
3. 需求实现
   - 下一页URL是动态生成的，不能直接获取。但是通过观察发现，URL之间大部分是相同的，仅页码有所变化，因此可以通过改变页码进行跳转。
   
     ```python
     # 向下一页url发起请求
     while self.page_num < 2:
         next_url = response.urljoin("index_%s.shtml" % self.page_num)
         self.page_num += 1
         # print(next_url)
         yield scrapy.Request(next_url, callback=self.parse)
     ```
   
   - CSV导出乱码问题解决
   
     在 `settings.py` 中添加如下字段
   
     ```python
     FEED_EXPORT_ENCODING = 'gb18030'
     ```
   
   - 需要将时间的格式进行调整
   
     利用管道实现该需求
   
     ```python
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
     ```
   
     