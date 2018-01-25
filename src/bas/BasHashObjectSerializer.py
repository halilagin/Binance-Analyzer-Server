'''
Created on Jan 12, 2018

@author: halil
'''

import json


class BasHashObjectSerializer(object):
            #see: https://stackoverflow.com/questions/1305532/convert-python-dict-to-object
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [BasHashObjectSerializer(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, BasHashObjectSerializer(b) if isinstance(b, dict) else b)
    
    
    @staticmethod
    def ofDict(dict_):
        return BasHashObjectSerializer(json.loads())