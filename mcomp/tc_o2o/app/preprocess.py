#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 包括打标签、训练集和测试集的划分
# td = pd.to_datetime(dfoff['Date'], format='%Y%m%d') -  pd.to_datetime(dfoff['Date_received'], format='%Y%m%d'),后续单独成为一个函数


# In[9]:

import fileio
import pandas as pd
import numpy as np
from datetime import date
from sklearn.impute import SimpleImputer


# 特征处理
#1将满xx减yy类型(xx:yy)的券变成折扣率 : 1 - yy/xx，同时建立折扣券相关的特征 discount_rate, discount_man, discount_jian, discount_type
#2将距离 str 转为 int convert Discount_rate and Distance
def process_manjian(df):
    
    def getDiscountType(row):
        if pd.isnull(row):
            return np.nan
        elif ':' in row:
            return 1
        else:
            return 0
    
    def convertRate(row):
        """Convert discount to rate"""
        if pd.isnull(row):
            return 1.0
        elif ':' in str(row):
            rows = row.split(':')
            return 1.0 - float(rows[1])/float(rows[0])
        else:
            return float(row)
    
    def getDiscountMan(row):
        if ':' in str(row):
            rows = row.split(':')
            return int(rows[0])
        else:
            return 0
    
    def getDiscountJian(row):
        if ':' in str(row):
            rows = row.split(':')
            return int(rows[1])
        else:
            return 0    
        
    
    #1将满xx减yy类型(xx:yy)的券变成折扣率 : 1 - yy/xx，同时建立折扣券相关的特征 discount_rate, discount_man, discount_jian, discount_type
    df.loc[:,'discount_rate'] = df.loc[:,'Discount_rate'].apply(convertRate)
    df.loc[:,'discount_man'] =  df.loc[:,'Discount_rate'].apply(getDiscountMan)
    df.loc[:,'discount_jian'] = df.loc[:,'Discount_rate'].apply(getDiscountJian)
    df.loc[:,'discount_type'] = df.loc[:,'Discount_rate'].apply(getDiscountType)
    
    return df 

def process_distance(df):    
    #2将距离 str 转为 int convert Discount_rate and Distance
    df['Distance'] = df['Distance'].fillna(2).astype(int)
    
    return df


# In[27]:


def process_Weekday(dfoff):
    
    def getWeekday(row):
        if row == 'nan':
            return np.nan
        else:
            return date(int(row[0:4]), int(row[4:6]), int(row[6:8])).weekday() + 1
        
    # 领券是周几,没券就nan
    dfoff['weekday'] = dfoff['Date_received'].astype(str).apply(getWeekday)
    # weekday_type :  周六和周日为1，其他为0
    dfoff['weekday_type'] = dfoff['weekday'].apply(lambda x : 1 if x in [6,7] else 0 )
    
    # change weekday to one-hot encoding 
    weekdaycols = ['weekday_' + str(i) for i in range(1,8)]
    tmpdf = pd.get_dummies(dfoff['weekday'].replace('nan', np.nan))
    tmpdf.columns = weekdaycols
    dfoff[weekdaycols] = tmpdf
    
    return dfoff,weekdaycols


# In[28]:


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

def merge_nf1(df):
    """
    输入dftest或者dfoff,用于合并新特征1.
    新特征是使用dfoff的用户id计算的，所以对于其余df可能无法完全兼容，比如dftest会多两个id没有历史数据
    这里会用most填充
    """
    dfnf1 = fileio.read_nf1()
    dfobj = pd.merge(df,dfnf1,'left',left_on='User_id',right_on='用户id')
    
    imp_most = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    dfobj.iloc[:,-6::] = imp_most.fit_transform(dfobj.iloc[:,-6::])
    
    return dfobj
# In[29]:


def preprocess(dfoff):
    dfoff = process_manjian(dfoff)
    dfoff = process_distance(dfoff)
    dfoff,weekdaycols = process_Weekday(dfoff)
    dfoff = merge_nf1(dfoff)
    
    return dfoff,weekdaycols




def get_last_features(weekdaycols):
    """获取最终用于模型的特征"""
    lastfeatures = ['discount_rate','discount_type','discount_man', 'discount_jian','Distance', 'weekday', 'weekday_type'] + weekdaycols
    lastfeatures = lastfeatures +['只领券', '核销数', '直接买', '单商铺最大购买次数', '成交商家数']
    return lastfeatures


def split_t_v(dfoff,weekdaycols):
    """从dfoff分割测试子集和训练子集"""
    # 获取标签,dfall待表所有拿券的线下记录
    dfoff = get_label(dfoff)
    dfall = dfoff[dfoff['label'] != -1].copy()
    #目前就只有Date有nan,后续有需要再填充
    #dfall.Date.fillna(0,inplace=True)
    
    
    ## 过采样，因为用auc所以暂时不需要
    #model_smote = SMOTE()
    #dfall_X, dfall_y = model_smote.fit_sample(dfall.drop(['label','Discount_rate'],axis = 1),dfall.label)  # 输入数据并作过抽样处理
    #dfall = pd.concat([dfall_X,dfall_y],axis=1)
    
    train = dfall[(dfall['Date_received'] < 20160516)].copy()
    valid = dfall[(dfall['Date_received'] >= 20160516) & (dfall['Date_received'] <= 20160615)].copy()
    
    lastfeatures = get_last_features(weekdaycols)
    x_train,y_train = train[lastfeatures],train.label
    x_test,y_test = valid[lastfeatures],valid.label

    
    return x_train,y_train,x_test,y_test,train,valid

if __name__ == "__main__":
    dfoff = pd.read_csv('../data/ccf_offline_stage1_train.csv')
    dftest = pd.read_csv('../data/ccf_offline_stage1_test_revised.csv')
    dfon = pd.read_csv('../data/ccf_online_stage1_train.csv')
    # 预处理，部分特征处理
    dfoff,weekdaycols = preprocess(dfoff)
    dftest,weekdaycols = preprocess(dftest)
    # 分割测试子集和训练子集
    x_train,y_train,x_test,y_test,train,valid = split_t_v(dfoff,weekdaycols)