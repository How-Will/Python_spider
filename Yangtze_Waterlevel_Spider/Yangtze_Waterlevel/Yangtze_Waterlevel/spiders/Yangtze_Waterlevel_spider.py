import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import YangtzeWaterlevelItem
import re


class YangtzeWaterlevelSpiderSpider(scrapy.Spider):
    name = 'Yangtze_Waterlevel_spider'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://cj.msa.gov.cn/xxgk/xxgkml/aqxx/swgg/index_1.shtml']
    page_num = 2   # 下一起始页码

    # 解析水位公告列表页
    def parse(self, response):
        # 提取每天的水位详情页url
        le = LinkExtractor(restrict_xpaths='//div[@class="lie"]')
        for link in le.extract_links(response):
            if "8点" in link.text or "11点" in link.text:
                # print(link.url)
                yield scrapy.Request(link.url, callback=self.parse_detail)

        # 向下一页url发起请求
        while self.page_num < 352:
            next_url = response.urljoin("index_%s.shtml" % self.page_num)
            self.page_num += 1
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)



    # 解析水位详情页
    def parse_detail(self, response):
        info_item = YangtzeWaterlevelItem()

        tr_list = response.xpath(
            '/html/body/div[2]/div[1]/div/div[2]/div[2]/table//tr[4]/td/div[2]//table[1]//tr | '
            '/html/body/div[2]/div[1]/div/div[2]/div[2]/table//tr[4]/td/table[1]//tr | '
            '/html/body/div[2]/div[1]/div/div[2]/div[2]/table//tr[4]/td/table//tr')

        for tr in tr_list:
            # 提取位置
            un_location = tr.xpath('./td[1]/p/span/text() | ./td[1]/p//text() | ./td[1]/div//text() | '
                                   './text()').extract()
            location = ''.join(''.join(un_location).split())   # 去除空格

            # 提取水位
            water_level = tr.xpath('./td[2]/p/span/text() | ./td[2]/p//text() | ./td[2]/div//text()').extract()
            if water_level:
                water_level = ''.join(''.join(water_level).split())

            # 提取时间
            time = response.xpath('//*[@id="artibodyTitle"]/text()').extract_first()

            info_item['location'] = location
            info_item['water_level'] = water_level
            info_item['time'] = time

            yield info_item

        # # 13年8月13日之后的水位和位置信息重叠，不能分别提取
        # div_list = response.xpath('/html/body/div[2]/div[1]/div/div[2]/div[2]/table//tr[4]/td/div')[1:]
        #
        # for div in div_list:
        #     # 提取信息
        #     content = div.xpath('.//text()').extract()
        #     content = ''.join(content)
        #     content = content.replace('米', '')[:-1]
        #     content = content[:-1]      # 去掉最后涨落情况
        #
        #     # 提取水位
        #     water_level = re.findall(r'(\-?\d+\.?\d*)', content)
        #     remove_word = water_level[0]
        #     if water_level:
        #         info_item['water_level'] = water_level[0]
        #
        #
        #     # 提取位置
        #     location = content.replace(remove_word, '')
        #     location = ''.join(''.join(location).split())  # 去除空格
        #     info_item['location'] = location
        #
        #     # 提取时间
        #     time = response.xpath('//*[@id="artibodyTitle"]/text()').extract_first()
        #     info_item['time'] = time
        #
        #     yield info_item

