'''
Created on Jan 12, 2018

@author: halil
'''
import pymongo
from pymongo import *
from bas.BasContext import _bas
from datetime import datetime
import time
from bas.BasBinanceTimeManager import basTimer, BasBinanceTimeInterval
from bson.json_util import loads
from bson.json_util import dumps
from bson.objectid import ObjectId
from bas.BasBinanceCandleReader import basCandleReader

# see: https://docs.mongodb.com/manual/reference/mongo-shell/
# see: https://docs.mongodb.com/manual/crud/
# see: http://api.mongodb.com/python/current/api/bson/json_util.html


class BasMongoManager(object):
    '''
    classdocs
    '''


    def __init__(self, url=None):
        '''
        Constructor
        '''
        if url==None:
            self.client = MongoClient(_bas.executer.configManager.config.bas.db.mongodb.connection)
        else:
            self.client = MongoClient(url)
        self.dbbas = self.client.dbbas
        self.candles = self.dbbas.candles        
        self.trades = self.dbbas.trades
    
    def saveUpdate(self,collection, doc):

#         if "_id" not in doc:
#             collection.insert_one(doc)
#             return
        fo = collection.find_one({"timeInterval":int(doc["timeInterval"]), "openTime":int(doc["openTime"])})
        if fo==None:
            collection.insert_one(doc)
        else:
            collection.replace_one({"timeInterval":int(doc["timeInterval"]), "openTime":int(doc["openTime"])}, doc, True)
    def testConnection(self):
        pass
        candle_ = {"symbol":"XLMETH", 
                "coin":"XLM", 
                "bcoin":"ETH", 
                "timestamp": basTimer.nowInMicrosecond(),
                "timeInterval":BasBinanceTimeInterval.OneMinute.value, # in seconds
                "sequence":0, # in timeinterval metric
                "candle":{}
                }
        self.candles.insert_one(candle_)
        list = dumps(self.candles.find({"coin":"XLM"}))
        print (list)
    
    def getCandles(self, symbol="XLMETH", timeInterval=60, openTime=None, limit=500):
        pass
        candleDocs=[]
        if openTime==None:
            candleDocs = list(self.candles.find({"timeInterval":timeInterval},limit=limit).sort([("openTime", pymongo.ASCENDING)]))
        else:
            candleDocs = list(self.candles.find({"timeInterval":timeInterval, "openTime":openTime},limit=limit).sort([("openTime", pymongo.ASCENDING)]))
            
        return candleDocs
        
        