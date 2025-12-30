import scrapy


class XiaoSpider(scrapy.Spider):
    name = "xiao" #爬虫名称
    allowed_domains = ["4399.com"] #允许爬取的域名
    start_urls = ["https://www.4399.com/flash/"] #起始爬取的url列表

    def parse(self, response):#解析的作用
        list_list = response.xpath('//ul[@class="n-game cf"]/li')
        for i in list_list:
            name = i.xpath('./a/b/text()').extract_first()
            classify = i.xpath('./em/a/text()').extract_first() 
            date = i.xpath('./em/text()').extract_first()
            print(name, classify, date)
            break
