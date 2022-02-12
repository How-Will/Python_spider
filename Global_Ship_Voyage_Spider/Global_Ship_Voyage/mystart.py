from scrapy import cmdline
import datetime


cmd = 'scrapy crawl Global_Ship_Voyage_spider -o info_%s.csv' % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

cmdline.execute(cmd.split())