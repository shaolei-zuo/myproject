# 策略： 银行股票，市值前十，市净率低于0.6买入。首次买40%仓位，每跌10%补仓20%
import data.Stock as st
import pandas as pd
import  numpy as np
import strategy.base as strat
import matplotlib.pyplot as plt

def ba_strategy(data):
    '''

    :param data: df必须包含收盘价
    :param short_window:
    :param long_window:
    :return:
    '''

    # 是否存在市净率、收盘价
    columns = data.columns.values
    print(columns)
    if  'close' not in data.columns:
        print('feature \'close\' should in ')
        return
    if not 'pa_ratio' in columns:
        print('feature \'pa_ratio\' should in ')
        return

    exit()
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
    # 目标股票代码
    stocks = st.get_stock_list_all()
    stock_list = list(stocks[stocks['display_name'].str.contains('银行')].index)

    print(len(stock_list))
    exit()

    # 容器

    # 目标收盘价以及PE指标
    for code in stock_list[:1]:
        print(code)
        dfprice = st.get_single_price(code, 'daily', '2018-01-02', '2018-01-10')
        for date in dfprice.index:
            cc = st.get_single_valuation(code, date, statDate=None)
            dfprice.loc[date, 'pb_ratio'] = cc.pb_ratio[0]
            dfprice.loc[date, 'market_cap'] = cc.market_cap[0]
        #dffina = st.get_single_valuation(code, None, statDate='2016')

    print(dfprice.columns)
    ba_strategy(dfprice)

    # dfprice.loc[:,['pb_ratio']].plot()
    # plt.show()
    #print(dfprice)



