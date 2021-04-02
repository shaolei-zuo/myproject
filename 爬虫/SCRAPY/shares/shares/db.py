import pymongo
from shares.settings import MONGODB_HOST,MONGODB_PORT
import random

class MongoClient(object):
    def __init__(self, host=MONGODB_HOST, port=MONGODB_PORT, ):
        self.client = pymongo.MongoClient("mongodb://{0}:{1}".format(host, port))

    def insert_data_many(self, data, dbname, sheetname):
        self.db = self.client[dbname]
        self.collection = self.db[sheetname]
        self.collection.insert_many(data)

    def insert_data_one(self, data, dbname, sheetname):
        self.db = self.client[dbname]
        self.collection = self.db[sheetname]
        self.collection.insert_one(data)

    def clids(self, dbname, sheetname):
        self.db = self.client[dbname]
        self.collection = self.db[sheetname]

    def show_sheets(self, dbname):
        self.db = self.client[dbname]
        collist = self.db.list_collection_names()
        return collist

    def get_scrapyed_url(self, dbname, sheetname):
        '''
        从数据库获取已经爬取过的url
        '''
        ll = []
        self.clids(dbname, sheetname)
        data = self.collection.find({}, {'url': 1})
        for url in data:
            ll.append(url['url'])

        return ll


if __name__ == '__main__':
    sl = MongoClient()
    # data = sl.get_scrapyed_url('tempdb', 'had_scrapy_urls')
    # if 'http://market.finance.sina.com.cn/transHis.php?symbol=sz000001&date=2008-01-04&page=38' in data:
    #     print('yes!')
    print(sl.show_sheets('tempdb'))



