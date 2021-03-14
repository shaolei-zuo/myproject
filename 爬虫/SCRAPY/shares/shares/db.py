import pymongo
from shares.settings import MONGODB_HOST,MONGODB_PORT


class MongoClient(object):
    def __init__(self, host=MONGODB_HOST, port=MONGODB_PORT, ):
        self.client = pymongo.MongoClient('mongodb://{0}:{1}'.format(host,port))

    def insert_data_many(self, data, dbname, sheetname):
        self.db = self.client[dbname]
        self.collection = self.db[sheetname]
        self.collection.insert_many(data)

    def insert_data_one(self, data, dbname, sheetname):
        self.db = self.client[dbname]
        self.collection = self.db[sheetname]
        self.client.insert_one(data)


if __name__ == '__main__':
    data = [{'1':1,'2':2}]
    sl = MongoClient()
    sl.insert_data_many(data, 'testDB1', 'testSH1')


