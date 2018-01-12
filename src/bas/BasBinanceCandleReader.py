'''
Created on Jan 11, 2018

@author: halil
'''

class BasBinanceCandleReader(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    '''
    [
        [
            1499040000000,      # Open time
            "0.01634790",       # Open
            "0.80000000",       # High
            "0.01575800",       # Low
            "0.01577100",       # Close
            "148976.11427815",  # Volume
            1499644799999,      # Close time
            "2434.19055334",    # Quote asset volume
            308,                # Number of trades
            "1756.87402397",    # Taker buy base asset volume
            "28.46694368",      # Taker buy quote asset volume
            "17928899.62484339" # Can be ignored
        ]
    ]
    '''
    def openTime0(self, candle):
        return float(candle[0])
    def open1(self, candle):
        return float(candle[1])
    def high2(self, candle):
        return float(candle[2])
    def low3(self, candle):
        return float(candle[3])
    def close4(self, candle):
        return float(candle[4])
    def volume5(self, candle):
        return float(candle[5])
    def closeTime6(self, candle):
        return float(candle[6])
    def assetVolume7(self, candle):
        return float(candle[7])
    def tradeCount8(self, candle):
        return float(candle[8])
    def takerBaseVolume9(self, candle):
        return float(candle[9])
    def takerQuoteVolume10(self, candle):
        return float(candle[10])
    def dummy11(self, candle):
        return float(candle[11])
    
    def _0openTime(self, candle):
        return float(candle[0])
    def _1open(self, candle):
        return float(candle[1])
    def _2high(self, candle):
        return float(candle[2])
    def _3low(self, candle):
        return float(candle[3])
    def _4close(self, candle):
        return float(candle[4])
    def _5volume(self, candle):
        return float(candle[5])
    def _6closeTime(self, candle):
        return float(candle[6])
    def _7assetVolume(self, candle):
        return float(candle[7])
    def _8tradeCount(self, candle):
        return float(candle[8])
    def _9takerBaseVolume(self, candle):
        return float(candle[9])
    def _10takerQuoteVolume(self, candle):
        return float(candle[10])
    def _11dummy(self, candle):
        return float(candle[11])
    
    
    
    
    '''
    [
        [
            1499040000000,      # Open time
            "0.01634790",       # Open
            "0.80000000",       # High
            "0.01575800",       # Low
            "0.01577100",       # Close
            "148976.11427815",  # Volume
            1499644799999,      # Close time
            "2434.19055334",    # Quote asset volume
            308,                # Number of trades
            "1756.87402397",    # Taker buy base asset volume
            "28.46694368",      # Taker buy quote asset volume
            "17928899.62484339" # Can be ignored
        ]
    ]
    '''
    def map(self, candles, timeInterval):
        #time interval can be 1 minute, 5, minute, 15, 1 hour, 1 day. see: BasBinanceTimeInterval
        map_ = [
         {
          "timeInterval":timeInterval,
          "openTime": float(c[0]),
          "open":float(c[1]),
          "high":float(c[2]),
          "low":float(c[3]),
          "close":float(c[4]),
          "volume":float(c[5]),
          "closeTime":float(c[6]),
          "assetVolume":float(c[7]),
          "tradeCount":float(c[8]),
          "takerBaseVolume":float(c[9]),
          "takerQuoteVolume":float(c[10]),
          "dummy":float(c[11]),
          "middle": (float(c[1])+float(c[4]))/2.0
          } for c in candles
        ]
        return map_
    
    def mapMongoDoc(self, candles, timeInterval):
        #time interval can be 1 minute, 5, minute, 15, 1 hour, 1 day. see: BasBinanceTimeInterval
        map_ = [
         {
          "timeInterval":timeInterval,
          "openTime": float(c[0]),
          "open":float(c[1]),
          "high":float(c[2]),
          "low":float(c[3]),
          "close":float(c[4]),
          "volume":float(c[5]),
          "closeTime":float(c[6]),
          "assetVolume":float(c[7]),
          "tradeCount":float(c[8]),
          "takerBaseVolume":float(c[9]),
          "takerQuoteVolume":float(c[10]),
          "dummy":float(c[11]),
          "middle": (float(c[1])+float(c[4]))/2.0
          } for c in candles
        ]
        return map_
    

basCandleReader = BasBinanceCandleReader()