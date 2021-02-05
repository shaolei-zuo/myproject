#!/usr/bin/env python
# coding: utf-8

#一些处理时间的函数

import time
import datetime
import numpy as np


def day_jiajian(day1,adds):
    """输入'20201101 00:00:00',1，输出'20201102 00:00:00"""
    starTime = datetime.datetime.strptime(day1, '%Y%m%d %H:%M:%S')
    endTime = (starTime+datetime.timedelta(days=adds)).strftime( '%Y%m%d %H:%M:%S')
    #starTime = self.starTime.strftime( '%Y%m%d %H:%M:%S')
    return endTime

def u2b(unixT,timeformat = '%Y%m%d %H:%M:%S'):
    'default %Y%m%d %H:%M:%S,maybe you need %Y-%m-%d %H:%M:%S.%f '
    now = time.strftime(timeformat,time.localtime(unixT/1000))
    return now

def b2u(dt,timeformat = '%Y%m%d %H:%M:%S'):
    'default %Y%m%d %H:%M:%S,maybe you need %Y-%m-%d %H:%M:%S.%f '
    now = int(time.mktime(time.strptime(dt,timeformat))*1000)
    return now

def now_unix():
    return int(time.mktime(datetime.datetime.now().timetuple())*1000)

def earthworm(starTime,endTime,dura = int(86400000*1)):
    u'将输入的时间分为固定间隔的段，最后一段除外.默认段长为int(86400000*1)'
    et = b2u(endTime)
    st = b2u(starTime)
    if et>=now_unix():#如果et大于当前时间
        et =now_unix()
    if et-st<dura:#如果时间跨度小于最大限制时间
        time_list = [st,et]
    else:
        time_list = list(np.arange(st,et,dura))
        time_list.append(et)
    return time_list   