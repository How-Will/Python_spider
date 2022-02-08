from scrapy import cmdline



cmd = 'scrapy crawl Global_Ship_Info_spider -o vessel_info.csv'

cmdline.execute(cmd.split())