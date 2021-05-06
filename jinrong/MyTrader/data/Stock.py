    #!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Stock.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/3/30 9:25   shaolei.zuo      1.0         None
'''
import time
from jqdatasdk import *
auth('18608169587', 'JQszuo123')
import  pandas as pd
import datetime
from setting import sourth_path
import os
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)



#上证 .XSHG  '600519.XSHG' 贵州茅台
#深交 .XSHE  '000001.XSHE' 平安银行
def init_db():
    '''初始化股票数据库'''
    # 获取股票代码
    stocks = get_stock_list()
    # 获取数据
    for code in stocks:
        df = get_single_price(code, 'daily')
        export_data(df, code, 'price')

class jijin(object):
    '''基金相关的内容'''
    def jijin_normalize_code(self, code):
        return normalize_code(code)


    def jijin_get_price(self, security, start_date=None, end_date=None, frequency='daily',
                        fields=None, skip_paused=False, fq='pre', count=None):
        '''df = get_price('510300.XSHG', start_date='2018-08-01 10:00:00', end_date='2018-08-01 10:05:00', frequency='1m')'''
        return get_price(security, start_date, end_date, frequency,
                         fields, skip_paused, fq, count)


def get_stock_list():
    '''获取所有A股股票列表'''
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list

def get_stock_list_all():
    '''获取所有A股股票列表'''
    stock_list = get_all_securities(['stock'])
    return stock_list

def get_single_price(code, time_freq, start_date=None, end_date=None):
    '''
    获取单个股票行情数据
    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    '''
    # 如果start_date = None, 默认从上市开始
    if  start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()
    # 获取行情数据
    data = get_price(code, start_date=start_date, end_date=end_date,
                     frequency=time_freq, panel=False)
    return data

def export_data(data, filename, type, mode=None):
    '''
    导出股票相关数据
    :param data:
    :param filename:
    :param type: 可以是：price\finance
    :param data:
    :return:
    '''
    # file_root = rice/' + filename + '.csv'
    file_root = sourth_path+'data/{0}/{1}.csv'.format(type, filename)
    data.index.name = 'date'
    if mode == 'a':
        data.to_csv(file_root, mode=mode, header= False)
        # 删除重复值
        data= pd.read_csv(file_root)
        data = data.drop_duplicates(subset=['date'])
        data.to_csv(file_root)
    else:
        data.to_csv(file_root)
    print('成功储存：', file_root)

def get_csv_data(code, type):
    file_root = sourth_path+'data/{0}/{1}.csv'.format(type, code)
    return pd.read_csv(file_root)

def get_csv_price(code, start_date, end_date ):
    '''获取本地数据，顺便完成更新'''
    type = 'price'
    # 使用update直接更新
    data = update_daily_price(code)
    # 读取数据
    file_root = sourth_path+'data/{0}/{1}.csv'.format(type, code)
    data = pd.read_csv(file_root,index_col='date')
    # 根据日期选数据
    data[(data.index >= start_date) & (data.index <= end_date)]

    return data


def transfer_price_freq(df, time_freq):
    '''
    转换股票行情周期,获取周/月等周期的：开盘价、收盘价、最高价、最低价
    :param df:
    :param time_freq:
    :return:
    '''
    df_trans = pd.DataFrame()
    df_trans['open'] = df['open'].resample(time_freq).first()
    df_trans['close'] = df['close'].resample(time_freq).last()
    df_trans['high'] = df['high'].resample(time_freq).max()
    df_trans['low'] = df['low'].resample(time_freq).min()

    return df_trans

def get_single_finance(code, date, statDate):
    '''
    获取单个股票财务指标
    :param code:
    :param date:
    :param statDate:
    :return:
    '''
    df = get_fundamentals(query(indicator).filter(indicator.code == code) ,date=date,  statDate=statDate)
    return df

def get_single_valuation(code, date, statDate):
    '''
    获取单个股票估值指标
    :param code:
    :param date:
    :param statDate:
    :return:
    '''
    df = get_fundamentals(query(valuation).filter(valuation.code == code) ,date=date,  statDate=statDate)
    return df

def calculate_change_pct(data):
    '''
    涨跌幅 = （当前收盘价-前期收盘价）/前期收盘价
    :param data: DF，有收盘价
    :return: df, 有涨跌幅
    '''
    data['close_pct'] = data['close']-data['close'].shift(1)/data['close'].shift(1)

    return data

def update_daily_price(stock_code, type='price'):
    file_root = sourth_path+'data/{0}/{1}.csv'.format(type, stock_code)
    if os.path.exists(file_root):
        # 获取增量数据
        startdate = pd.read_csv(file_root, usecols=['date'])['date'].iloc[-1]
        df = get_single_price(stock_code, 'daily', startdate,
                               datetime.datetime.today())
        # 追加已有文件
        export_data(df, stock_code, 'price', 'a')
    else:
        df = get_single_price(stock_code, 'daily')
        export_data(df, stock_code, 'price')

    print("股票数据更新成功：", stock_code)


