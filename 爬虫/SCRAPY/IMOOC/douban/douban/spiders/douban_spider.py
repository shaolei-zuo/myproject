# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名字，不能与项目名称一致，运行的时候也需要用这个名字
    name = 'douban_spider'
    # 允许的域名，就是request必须在这个域名内
    allowed_domains = ['movie.douban.com']
    # 入口url,会进入调度器
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            # 这里实际上就是导入的items自定义的数据结构，所以名称什么的都是一样的
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            print(douban_item['movie_name'])