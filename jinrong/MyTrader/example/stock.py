#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   stock.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/3/31 13:20   shaolei.zuo      1.0         None
'''
import data.Stock as st

# 本地读数据
data = st.get_csv_price('000002.XSHE', '2020-01-01', '2020-02-01')
print(data)
# # 获取平安银行的行情数据（日K）
# data = st.get_single_price('000001.XSHE', 'daily', '2020-01-01', '2020-01-28')
#
# # 计算涨跌幅，验证准确性
# data= st.calculate_change_pct(data)
#
# # 获取周K
# data = st.transfer_price_freq(data, 'w')
#
# # 计算涨跌幅，验证准确性
# data= st.calculate_change_pct(data)
# print(data)