'''
Created on Jan 23, 2018

@author: halil
'''
import json

class JsonLoadTest(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def test(self):
        j =json.loads(u'{"a":1,"b":2}')
        print(j["a"])
        print(json.dumps(j))
        
JsonLoadTest().test()