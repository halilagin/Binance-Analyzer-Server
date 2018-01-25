'''
Created on Jan 24, 2018

@author: halil
'''
from bas.BasWebSocket import BasWebSocketCandle_clients
from bson import json_util



class BasWebSocketWriterManager(object):
    pass

    @staticmethod
    def pushMessage(message):
        for c in BasWebSocketCandle_clients:
            c.client.sendMessage(json_util.dumps(message))
    
    
    
    
    @staticmethod
    def pushServerInitializerStarted():
        BasWebSocketWriterManager.pushMessage({"action":"ServerInitializerStarted", "progress":0.0})
    
    @staticmethod
    def pushServerInitializingInProgress(progress):
        BasWebSocketWriterManager.pushMessage({"action":"ServerInitializingInProgress", "progress":progress})
    
    @staticmethod
    def pushServerInitializerFinished():
        BasWebSocketWriterManager.pushMessage({"action":"ServerInitializerFinished", "data":None})
    
    @staticmethod
    def pushCandles(plotClientId, symbol, timeInterval, mostRecentCandle, candles):
        BasWebSocketWriterManager.pushMessage({
            "plotClientId":plotClientId,
            "action":"retrieveCandles", 
            "symbol":symbol, 
            "timeInterval":timeInterval,
            "mostRecentCandle":mostRecentCandle, 
            "candles":candles})
    
        