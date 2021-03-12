#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   db.py    
@Contact :   458326291@qq.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time        @Author      @Version    @Desciption
------------      -----------    --------    -----------
2021/3/12 15:05   shaolei.zuo      1.0         None
'''
import redis
from  .settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY# 代理分数
from  .settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice



class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)


    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE) #获取redis数据库中的最高分代理（100分）
        if len(result):  #如果存在
            return choice(result)  #返回该代理
        else:      #不存在最高分代理
            result = self.db.zrevrange(REDIS_KEY, 0, 100) #对redis数据库中的代理 按分数排名获取 取最高排名的代理
            if len(result):
                return choice(result)
            else:
                print('error')



if __name__ == '__main__':
    sl = RedisClient()
    print(sl.random())
