from bas.BasMongoManager import BasMongoManager



class MongoTest(object):
    
    def __init__(self):
        pass
    
    def testGetCandles(self):
        pass
        mm = BasMongoManager(url="mongodb://localhost:27017/")
        candles = mm.getCandles(symbol="XLMETH", timeInterval=60, limit=10)
        print(candles)

MongoTest().testGetCandles()