# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
import re
import base64


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名字，不能与项目名称一致，运行的时候也需要用这个名字
    name = 'douban_spider'
    # 允许的域名，就是request必须在这个域名内
    #allowed_domains = ['movie.douban.com']
    # 入口url,会进入调度器
    #start_urls = ['http://movie.douban.com/top250']
    start_urls = ['https://ifconfig.me/ip']
    start_urls = ['https://myip.is/']

    # 默认的解析方法

    def parse(self, response):
        print('*'*10)
        print(re.findall(':doCopy\(.+?\)', response.text)[0])
        print('*'*50)
        n = 0
        yield scrapy.Request('https://myip.is/', meta={'n_n': n}, dont_filter=True, callback=self.parse1)

    def parse1(self, response):
        n = response.meta['n_n']
        n = n+1
        print(n, re.findall(':doCopy\(.+?\)', response.text)[0], response.request.headers['User-Agent'])
        if n < 5:
            yield scrapy.Request('https://myip.is/', meta={'n_n': n}, dont_filter=True, callback=self.parse1)


    def parse2(self, response):
        # 循环电影条目

        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            # item 文件导进来
            # 这里实际上就是导入的items自定义的数据结构，所以名称什么的都是一样的
            douban_item = DoubanItem()
            # 写详细的解析
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            #print(douban_item)
            # 需要将数据yield到pipelines里去
            yield douban_item
        print('*'*20, response.request.headers['User-Agent'])
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        # 解析下一页规则，取后页的Xpath
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('http://movie.douban.com/top250'+next_link, callback=self.parse)
