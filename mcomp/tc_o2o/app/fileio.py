#!/usr/bin/env python
# coding: utf-8

import pandas as pd


def read_all(datapath='../data/'):
    """dfoff ,dftest,dfon = fileio.read_all()"""
    
    dfoff = pd.read_csv(datapath+'ccf_offline_stage1_train.csv')
    dftest = pd.read_csv(datapath+'ccf_offline_stage1_test_revised.csv')
    dfon = pd.read_csv(datapath+'ccf_online_stage1_train.csv')
    return dfoff,dftest,dfon

if __name__ == "__main__":
    read_all()