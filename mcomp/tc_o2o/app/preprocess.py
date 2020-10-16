import fileio
import pandas as pd
import numpy as np
from datetime import date
from sklearn.impute import SimpleImputer


#处理标签
def get_label(dfoff,off=True):
    """线下数据off=True,线上数据dfoff=False,因为线上有fix字段"""
    
    def get_off_label(row):
        """无券-1；有券且15天内消费1；其他0（包括有券不消费、有券15天后消费）"""
        if pd.isnull(row['Date_received']):
            return -1
        if pd.notnull(row['Date']):
            td = pd.to_datetime(row['Date'], format='%Y%m%d') -  pd.to_datetime(row['Date_received'], format='%Y%m%d')
            if td <= pd.Timedelta(15, 'D'):
                return 1
        return 0
    
    def get_on_label(row):
        print('还没写，等搞清楚fixed和label的关系再说')
        pass
    

    if off:
        dfoff['label'] = dfoff.apply(get_off_label, axis = 1)
    else:
        dfoff['label'] = dfoff.apply(get_on_label, axis = 1)
    return dfoff



##############################################
#分割测试和训练集

def split_receivetime(dfall,spline = 20160516):
    """
    输入dfoff（或类似的），根据自带的Date_received特征，将数据集分割为两部分
    分割默认为20160516
    """
    train = dfall[(dfall['Date_received'] < 20160516)].copy()
    valid = dfall[(dfall['Date_received'] >= 20160516) & (dfall['Date_received'] <= 20160615)].copy()
    
    return train,valid


def preprocess(dfoff):
    dfoff = get_label(dfoff)
    dfall = dfoff[dfoff['label'] != -1].copy()    
    train,valid = split_receivetime(dfall)    
    
    return dfoff,dfall,train,valid

def split_xy(train,valid,columns=None):
    """
    train,valid划分特征和标签。另外输出的默认是全部特征，也可以自己输入特征
    """
    if not columns:
        columns = train.columns.drop('label')
    else:
        columns = columns
        
    x_train,y_train = train[columns],train.label
    x_test,y_test = valid[columns],valid.label
    
    return x_train,y_train,x_test,y_test

if __name__ == '__main__':
    dfoff ,dftest,dfon = fileio.read_all()
    dfoff,dfall,train,valid = preprocess(dfoff)
