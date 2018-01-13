'''
Created on Jan 10, 2018

@author: halil
'''
from binance.client import Client
from  bas.BasContext import _bas
from bas.BasBinanceEnumerations import KLINE_INTERVAL_1MINUTE,\
    CANDLE_FETCH_LIMIT
import json 
from enum import Enum 


    
    
     

class BasBinanceManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        config = _bas.executer.configManager.config
        api_key = config.bas.api.key
        api_secret = config.bas.api.secret
        print ("key,secret:",api_key,api_secret)
        self.client = Client( api_key, api_secret)

    
    def getRecentTrades(self, symbol):
        pass

        #print("BasBinanceManager.getRecentTrades.config:",_bas.executer.configManager.config)
        trades = self.client.get_recent_trades(symbol=symbol)
        #print(trades)
        
    def getCandles(self, symbol="XLMETH", interval=Client.KLINE_INTERVAL_1MINUTE, limit=CANDLE_FETCH_LIMIT, startTime=None):
        pass
        if startTime==None:
            candles = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        else:
            candles = self.client.get_klines(symbol=symbol, interval=interval, startTime=startTime)
        return candles
    
    
    def getServerTime(self):
        #return json.loads(self.client.get_server_time())["serverTime"]
         return self.client.get_server_time()["serverTime"]
