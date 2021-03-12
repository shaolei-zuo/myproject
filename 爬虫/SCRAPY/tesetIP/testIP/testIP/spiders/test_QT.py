#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_QT.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/3/12 16:23   shaolei.zuo      1.0         None
'''
from urllib import request

# 要访问的目标页面
targetUrl = 'https://api.ipify.org/?format=json%27'

# 代理服务器
proxyHost = "dyn.horocn.com"
proxyPort = "50000"

# 代理隧道验证信息
proxyUser = "PREL1694013611035523"
proxyPass = "21Siq91kY1Gj1YfY"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxy_handler = request.ProxyHandler({
    "http": proxyMeta,
    "https": proxyMeta,
})

opener = request.build_opener(proxy_handler)

request.install_opener(opener)
resp = request.urlopen(targetUrl).read()

print(resp)