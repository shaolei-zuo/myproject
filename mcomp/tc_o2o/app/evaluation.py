#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score,auc,confusion_matrix,f1_score, \
    precision_score,recall_score,roc_curve



def get_official_auc(y_prob,y_test,valid):
    """根据官方的描述，大概做了一个计算方法。不过细节对不对不知道.注意y_prob输入的是【:,1】之后的值"""

    def auc_count_1(y_prob,y_test):
        """来自宋，输入的不是概率值而是01,"""     
        fpr, tpr, _ = roc_curve(y_test, y_prob)  # ROC
        auc_s = auc(fpr, tpr)  # AUC    
        #或者直接使用
        #auc_s = roc_auc_score(y_test,y_prob)
        return auc_s
    
    
    aucdict = {}
    dfyprob = pd.Series(index=valid.index,data = y_prob)
    n=0
    for i  in valid.groupby('Coupon_id'):
        if (i[1].label==0).all():
            aucdict[i[0]] = np.nan
        else:
            inx = i[1].index
            y_prob_this = dfyprob[inx]
            y_test_this = y_test[inx]
            aucdict[i[0]] = auc_count_1(y_prob_this,y_test_this)
            
    dfauc = pd.DataFrame.from_dict(aucdict,orient='index')
    s_auc = dfauc.dropna().mean()
    return s_auc[0]

def get_model_scores(model,x_test,y_test,pre_y):
    """有多个评价，另外这里计算auc的方式还没有改，备用"""
    #print(model.score(x_test, valid['label']))
    
    tn, fp, fn, tp = confusion_matrix(y_test, pre_y).ravel()  # 获得混淆矩阵
    confusion_matrix_table = prettytable.PrettyTable(['','prediction-0','prediction-1'])  # 创建表格实例
    confusion_matrix_table.add_row(['actual-0',tp,fn])  # 增加第一行数据
    confusion_matrix_table.add_row(['actual-1',fp,tn])  # 增加第二行数据
    #print('confusion matrix \n',confusion_matrix_table)
    
    # 核心评估指标
    #y_test = valid.label
    #x_test = valid[original_feature]
    y_score = model.predict_proba(x_test)  # 获得决策树的预测概率
    fpr, tpr, _ = roc_curve(y_test, y_score[:, 1])  # ROC
    auc_s = auc(fpr, tpr)  # AUC
    scores = [round(i(y_test, pre_y),3 )for  i in (accuracy_score,precision_score,\
                                         recall_score,f1_score)]
    scores.insert(0,auc_s)
    core_metrics = prettytable.PrettyTable()  # 创建表格实例
    core_metrics.field_names = ['auc', 'accuracy', 'precision', 'recall', 'f1']  # 定义表格列名
    core_metrics.add_row(scores)  # 增加数据
    print('core metrics\n',core_metrics)
    return auc_s