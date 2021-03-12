# -*- coding: utf-8 -*-
import scrapy


class IptestSpiderSpider(scrapy.Spider):
    name = 'iptest_spider'
    allowed_domains = []

    def start_requests(self):
        url = 'https://api.ipify.org/?format=json%27'
        for i in range(9):
            print('{0}start{1}'.format('*'*3,'*'*3))
            # dont_filter:不过滤相同网址
            yield scrapy.Request(url,callback = self.parse,dont_filter=True)


    def parse(self, response):
        print('{0}{1}{2}'.format('*' * 10,response.text, '*' * 10))
