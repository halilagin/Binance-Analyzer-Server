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

# see: https://docs.mongodb.com/manual/reference/mongo-shell/
# see: https://docs.mongodb.com/manual/crud/
# see: http://api.mongodb.com/python/current/api/bson/json_util.html


class BasMongoManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.client = MongoClient(_bas.executer.configManager.config.bas.db.mongodb.connection)
        self.dbbas = self.client.dbbas
        self.candles = self.dbbas.candles        
        self.trades = self.dbbas.trades
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
        
        
        