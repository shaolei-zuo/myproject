#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   comp_sharpe_ratio.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/4/1 13:55   shaolei.zuo      1.0         None
'''
import data.Stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt


sharpes = []
# 获取3只股票的数据：比亚迪、宁德时代、隆基
codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']
for code in codes:
    data = st.get_single_price(code, 'daily', '2018-10-01', '2021-01-01')
    sharpe = stb.calculate_sharp(data)
    sharpes.append([code,sharpe[1]])
# 可视化3只股票
sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code')
sharpes.plot.bar()
plt.xticks(rotation=30)
plt.show()
