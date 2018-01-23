'''
Created on Jan 23, 2018

@author: halil
'''

class StaticMethodTest(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.var1="var1"
        print("staticmethodtest.class initialized")
    @staticmethod
    def test1(data):
        print(data)
        


StaticMethodTest.test1("halil")