'''
Created on Jan 12, 2018

@author: halil
'''
from bas.BasContext import _bas
import pymongo

class BasInitializer(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    def initMongoDB(self):
        pass
        _bas.executer.mongoManager.candles.create_index(
            [
             ("timeInterval", pymongo.ASCENDING),
             ("openTime", pymongo.ASCENDING)
            ], unique=True)
    
    def start(self):
        pass
        self.initMongoDB()
        