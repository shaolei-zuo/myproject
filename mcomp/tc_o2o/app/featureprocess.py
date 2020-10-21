import fileio
import pandas as pd
import numpy as np
from datetime import date
from sklearn.impute import SimpleImputer


##############################################
#处理满减
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

##############################################
#处理距离
def process_distance(df):    
    #2将距离 str 转为 int convert Discount_rate and Distance
    df['Distance'] = df['Distance'].fillna(2).astype(int)
    
    return df


##############################################
#处理周末
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
    
    return dfoff




##############################################
#处理nf1
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


#处理nf2
def merge_nf2(df):
    """
    输入dftest或者dfoff,用于合并新特征1.
    新特征是使用dfoff的用户id计算的，所以对于其余df可能无法完全兼容，比如dftest会多两个id没有历史数据
    这里会用most填充
    """
    
    df.loc[:,'UM_id'] = df.User_id.astype('str')+'_'+df.Merchant_id.astype('str')
    dfnf2 = fileio.read_nf2()
    dfobj = pd.merge(df,dfnf2,'left',left_on='UM_id',right_on='用户id')
    
    imp_most = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    dfobj.iloc[:,-6::] = imp_most.fit_transform(dfobj.iloc[:,-6::])
    
    return dfobj

def process_features_main(dfoff):
    dfoff = process_manjian(dfoff)
    dfoff = process_distance(dfoff)
    dfoff = process_Weekday(dfoff)
    #dfoff = merge_nf1(dfoff)
    dfoff = merge_nf2(dfoff)
    return dfoff

