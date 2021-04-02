#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ma_stratey.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/4/2 14:53   shaolei.zuo      1.0         None
'''
import data.Stock as st
import pandas as pd
import  numpy as np
import strategy.base as strat
import matplotlib.pyplot as plt

def ma_strategy(data, short_window=5, long_window=20):
    '''

    :param data: df必须包含收盘价
    :param short_window:
    :param long_window:
    :return:
    '''
    # 计算技术指标
    data = pd.DataFrame(data)
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] =  data['close'].rolling(window=long_window).mean()

    # 生成信号： 金叉买入，死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)

    # 过滤信号
    data = strat.compose_signal(data)

    # 删除多余
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)

    # 计算单次收益
    data= strat.calculate_prof_pct(data)

    # 计算累计收益
    data = strat.calculate_cum_prof(data)

    return data

if __name__ == '__main__':
    # 股票列表
    stocks= ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    # 存放累积收益率
    cum_profits = pd.DataFrame()
    # 循环获取数据
    for code in stocks:
        df = st.get_single_price(code, 'daily', '2016-01-01', '2021-01-01')
        df = ma_strategy(df)
        cum_profits.loc[:,code] = df['cum_profit'].reset_index(drop=True)

        print('开仓次数：', len(df))
        print(cum_profits)
    # print(df[['close','signal', 'profit_pct', 'cum_profit']])
    print(cum_profits)
    cum_profits.plot()
    plt.show()
