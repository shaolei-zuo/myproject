#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/2/8 16:31   shaolei.zuo      1.0         None
'''
from scrapy import  cmdline


cmdline.execute('scrapy crawl douban_spider'.split())
