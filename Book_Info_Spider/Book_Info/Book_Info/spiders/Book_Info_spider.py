import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import BookInfoItem


class BookInfoSpiderSpider(scrapy.Spider):
    name = 'Book_Info_spider'
    # allowed_domains = ['xxx.com']

    # 爬虫爬取的起始点，起始点可以是多个，这里只有一个
    start_urls = ['https://books.toscrape.com/']

    # 书籍列表页面解析函数
    def parse(self, response):
        # 提取每本书的链接
        le = LinkExtractor(restrict_xpaths='//article[@class="product_pod"]/h3')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book)

        # 提取下一页的url
        next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    # 书籍页面的解析函数
    def parse_book(self, response):
        # 提取数据
        book = BookInfoItem()

        sel = response.css('div.product_main')
        book['name'] = sel.xpath('./h1/text()').extract_first()
        book['price'] = sel.css('p.price_color::text').extract_first()
        book['review_rating'] = sel.css('p.star-rating::attr(class)').re_first('star-rating ([A-Za-z]+)')

        sel = response.css('table.table.table-striped')
        book['upc'] = sel.xpath('(.//tr)[1]/td/text()').extract_first()
        book['stock'] = sel.xpath('(.//tr)[last()-1]/td/text()').re_first('\((\d+) available\)')
        book['review_num'] = sel.xpath('(.//tr)[last()]/td/text()').extract_first()

        yield book

