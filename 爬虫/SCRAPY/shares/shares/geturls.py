# 为sharePrice的获取构造starturl列表
import sys
import os
print(os.getcwd())
sys.path.append('../../../')
from  app import  time_relevent as tr

class getStartUrls(object):
    """
    构造startlist列表
    """

    def __init__(self, symbol, st=None, et=None):
        self.symbol = symbol
        self.st = '20180101 00:00:00' if not st else st
        self.et = '20180201 00:00:00' if not et else et

    def geturls_page1(self):
        """
        构造url的list,这里是第一页的，还要根据页面进行页码分析。
        返回'输入的代码有误或没有交易数据'可能是拒绝，也可能放假没有数据

        """
        def tranhisurl(symbol, date):
            """
            构造开盘价的获取url
            网址示例为：http://market.finance.sina.com.cn/transHis.php?symbol=sz000001&date=2008-04-24&page=1
            """
            url = 'http://market.finance.sina.com.cn/transHis.php?symbol={0}&date={1}&page=1'.format(symbol, date)
            return url

        st = self.st
        et = self.et
        date_list = [tr.u2b(i, timeformat='%Y-%m-%d') for i in tr.earthworm(st, et)]
        url_list = [tranhisurl(self.symbol, date) for date in date_list]

        self.url_list = url_list

def getfullurls(nowurl,pagelist):
    strurl = nowurl.split('page=')[0]+'page='
    return [strurl + i for i in pagelist]

if __name__ == '__main__':
    sl = getStartUrls('sz000001')
    sl.geturls_page1()
    print(sl.url_list)

