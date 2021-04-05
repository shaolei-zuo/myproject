import data.Stock as st
import strategy.ma_stratey as ma
import matplotlib.pyplot as plt
from scipy import stats

def ttest(df):
    '''
    对策略收益进行t检验,p越大，和H0差别越小（越小月可能赚钱），t值越大样本与总体的均值差异越大
    '''
    # 调用假设检验ttest函数：scipy
    t, p = stats.ttest_1samp(df, 0, nan_policy='omit')
    # 判断是否与理论均值有显著性差异
    p_value = p/2.
    ifrefuse = p_value < 0.05

    # 打印
    print('t_value: ', t)
    print('p_value: ', p_value)
    print('是否拒绝H0: 收益均值 = 0：', ifrefuse)
    return t, p



if __name__ == '__main__':

    # 股票列表
    stocks= ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    for code in stocks:
        print(code)
        # 循环获取数据
        df = st.get_single_price(code, 'daily', '2016-12-01', '2021-01-01')
        df = ma.ma_strategy(df)

        # 策略的单次收益率
        returns = df['profit_pct']
        # print(returns)

        # # 绘制分布图用于观察
        # returns.hist(returns, bins=30)
        # plt.show()

        # 对多个股票进行计算、测试
        ttest(returns)
