#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stock.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/3/31 10:09   shaolei.zuo      1.0         None
'''
import  data.Stock as st
import pandas as pd


#code = '000001.XSHE'
# # 调用一只股票行情数据
# data = st.get_single_price(code=code,
#                            time_freq='daily',
#                            start_date='2021-01-01',
#                            end_date='2021-02-01')
#
# # 存入csv
# st.export_data(data=data,filename=code, type='price')
#
# # 从csv 获取数据
# data = st.get_csv_data(code=code, type='price')
# print(data)

# 实时更新
# 存储
st.init_db()

# 每日更新
#st.update_daily_price(code, 'price')