# -*- coding: utf-8 -*-
import scrapy
import re
from shares.db import MongoClient
from shares.geturls  import getStartUrls
from shares.geturls import getfullurls
from shares.logg import  logging
import time
import random

class SharePriceSpider(scrapy.Spider):
    """先获取股票代码-日期解析确定有数据，以及得到总页数后，得到整个完整的网址"""
    start_urls = []
    name = 'share_price'
    #allowed_domains = ['market.finance.sina.com']

    """测试代理ip,要使用，将后面的全部注释即可。
    # start_urls = ['https://api.ipify.org/?format=json%27']
    # def parse(self, response):
    #     print('*'*20, response.text)
    #     for i in range(4):
    #         yield scrapy.Request('https://api.ipify.org/?format=json%27', callback=self.parse2)
    # 
    # def parse2(self, response):
    #     print('*'*20, response.text)
    """


#   构造全部的网址,股票代码-日期-第一页，list
    sharecodes = {'sz000001': '平安银行',
                  'sz002142': '宁波银行',
                  'sz002807': '江阴银行',
                  'sz002936': '郑州银行',
                  'sz002948': '青岛银行',
                  'sz002966': '苏州银行',
                  'sh600000': '浦发银行',
                  'sh600015': '华夏银行',
                  'sh600016': '民生银行',
                  'sh600036': '招商银行',
                  'sh600908': '无锡银行',
                  'sh600919': '江苏银行',
                  'sh600926': '杭州银行',
                  'sh600928': '西安银行',
                  'sh601009': '南京银行',
                  'sh601128': '常熟银行',
                  'sh601166': '兴业银行',
                  'sh601169': '北京银行',
                  'sh601187': '厦门银行',
                  'sh601229': '上海银行',
                  'sh601288': '农业银行',
                  'sh601328': '交通银行',
                  'sh601398': '工商银行',
                  'sh601577': '长沙银行',
                  'sh601658': '邮储银行',
                  'sh601818': '光大银行',
                  'sh601838': '成都银行',
                  'sh601860': '紫金银行',
                  'sh601916': '浙商银行',
                  'sh601939': '建设银行',
                  'sh601963': '重庆银行',
                  'sh601988': '中国银行',
                  'sh601997': '贵阳银行',
                  'sh601998': '中信银行',
                  'sh603323': '苏农银行'}

    for key in sharecodes:
        sl = getStartUrls(key, st='20080101 00:00:00', et='20210312 00:00:00')
        sl.geturls_page1()
        start_urls = start_urls+sl.url_list
    # start_urls = ['http://market.finance.sina.com.cn/transHis.php?symbol=sh600000&date=2016-02-01']

#   先解析总页数，并生成最后一层url
    def parse(self, response):
        time.sleep(random.randint(15, 25))
        old_urls_list = []
        sl = MongoClient()
        old_urls_list = sl.get_scrapyed_url('tempdb', 'had_scrapy_urls')

        if '输入的代码有误或没有交易数据' in response.text:
            thislog = response.url+'输入的代码有误或没有交易数据'+'\n'
            ifgoon = False
        else:
            page_list = re.findall('\[(\d+),\'.+?\',\'.+?\'\]', response.text)
            thislog = response.url+'——ok'+'\n'
            ifgoon = True

        logging(thislog)

        if not ifgoon:
            print('*'*50, '当天无数据退出')
            return

        # 获取了
        full_urllist = getfullurls(response.url, page_list)
        for url in full_urllist:
            '''这里加重复判断'''
            if url not in old_urls_list:
                yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        time.sleep(random.randint(15, 25))
        thislog = 'start run--{0}\n'.format(response.url)
        print('*'*50, thislog)
        logging(thislog)

        if '输入的代码有误或没有交易数据' in response.text:
            thislog = '--{0}输入的代码有误或没有交易数据,但是首页存在数据\n'.format(response.url)
            logging(thislog)
            return

        dbname = 'sharePrice'
        date = re.findall('date=(.+?)&', response.url)
        sheetname = re.findall('symbol=(.+?)&', response.url)[0]

        data = re.findall('<tr ><th>(.+?)</th><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><th><h[56]>(.+?)</h[56]></th></tr>', response.text)
        data = [{'date': date, 'time': i[0], '成交价': i[1], '价格变动': i[2], '成交量（手）':i[3], '成交额（元）':i[4], '性质':i[5]} for i in data]
        conn = MongoClient()
        # 把目标数据存进数据库
        conn.insert_data_many(data, dbname, sheetname)
        # 把爬过的url存进数据库
        conn.insert_data_one({'url': response.url}, 'tempdb', 'had_scrapy_urls')
        thislog = '--{0}数据储存完成\n'.format(response.url)
        logging(thislog)
        return
