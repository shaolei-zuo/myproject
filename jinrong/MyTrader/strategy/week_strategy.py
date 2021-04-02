#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   strategy.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/3/31 13:57   shaolei.zuo      1.0         None
用于创建交易策略、生成交易信号
'''
import data.Stock  as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

def compose_signal(data):
    '''
    整合信号
    :param data:
    :return:
    '''
    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1)
                                  & (data['buy_signal'].shift(1) == 1), 0 , data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1)
                                  & (data['sell_signal'].shift(1) == -1), 0 , data['sell_signal'])
    data['signal']  = data['buy_signal'] + data['sell_signal']
    return data

def calculate_prof_pct(data):
    '''
    计算单次收益率： 开仓、平仓（开仓的全部股数)
    '''
    data = data[data['signal'] != 0 ]
    data['profit_pct'] = (data['close'] - data['close'].shift(1))/(data['close'].shift(1))
    data = data[data['signal'] == -1]

    return  data

def calculate_cum_prof(data):
    '''
    计算累计收益率
    :param data:
    :return:
    '''
    data['cum_profit'] = pd.DataFrame(1+data['profit_pct']).cumprod() -1
    return data

def calculate_max_drawdown(data):
    '''
    计算最大回撤比
    :param data:
    :return:
    '''
    # 选取时间周期
    window = 252
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window = window, min_periods=1).max()
    # 计算当天的回撤比L:（谷值-峰值）/峰值
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()

    return data

def calculate_sharp(data):
    '''
    计算夏普比率，返回年化的夏普比率
    :param data:
    :return:
    '''
    # 公式： sharp = （回报率的期望值-无风险利率）/回报率的标准差
    # 因子项
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普指数: 每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharp_year = sharpe * np.sqrt(252)

    return sharpe, sharp_year

def week_period_strategy(code, time_freq, start_date, end_date):
    """
    一种最简单的选股策略：周一卖，周四买
    要考虑休市等出现连续买入或者连续卖出信号的问题，做了信号整合
    """
    data = st.get_single_price(code, time_freq, start_date, end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3),1,0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0),-1,0)

    # 整合信号
    data = compose_signal(data)
    #  计算收益率
    data = calculate_prof_pct(data)
    # 计算累计收益
    data =calculate_cum_prof(data)

    return data

if __name__ == '__main__':
    # data = week_period_strategy('000001.XSHE', 'daily', None, datetime.datetime.today() )
    # print(data)
    # data['cum_profit'].plot()
    # plt.show()

    # # 最大回撤
    # df = st.get_single_price('000001.XSHE', 'daily', '2006-01-01', datetime.datetime.today())
    # df = calculate_max_drawdown(df)
    # print(df)
    # df[['daily_dd', 'max_dd']].plot()
    # plt.show()

    # 夏普比率
    df = st.get_single_price('000001.XSHE', 'daily', '2006-01-01', '2021-01-01')
    sharp = calculate_sharp(df)
    print(sharp)




