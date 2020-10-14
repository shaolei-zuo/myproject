#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import sys

star_file = os.path.split(os.path.realpath(__file__))[0] +'/../'


def ifmakdir(path):
    "文件夹不存在则创建"
    if not os.path.exists(path):
        os.makedirs(path)

def read_all():
    """dfoff ,dftest,dfon = fileio.read_all()"""
    
    dfoff = pd.read_csv(star_file+'data/ccf_offline_stage1_train.csv')
    dftest = pd.read_csv(star_file+'data/ccf_offline_stage1_test_revised.csv')
    dfon = pd.read_csv(star_file+'data/ccf_online_stage1_train.csv')
    return dfoff,dftest,dfon

def read_nf1(offed = True):
    """现在可以读取另一个文件，默认是读取分割后的那份"""
    if offed:
        df = pd.read_csv(star_file+'storage/newfeatures/dfoff_add_f1/new_fea_1_offdeceived.csv')
    else:
        df = pd.read_csv(star_file+'storage/newfeatures/dfoff_add_f1/new_fea_1.csv')
    return df

if __name__ == "__main__":
    read_all()