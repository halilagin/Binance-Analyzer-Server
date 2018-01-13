'''
Created on Jan 10, 2018

@author: halil
'''

from bas.BasExecuter import BasExecuter
from bas.BasContext import _bas

'''

see: https://github.com/faif/python-patterns

binance api:

https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md

pyqt vitorials and installer demo:
https://www.youtube.com/user/Deusdies2/videos
https://www.youtube.com/watch?v=KRMs9z6KoEU

'''
#import BasContext._bas as _bas


class BasExecuterMain(object):
    pass
    def __init__(self):
        pass
    
    def run(self):
        pass
        params={
            "config.file":"/Users/halil/bas.config.yaml"
            }
        _bas.executer = BasExecuter(params)
        _bas.executer.start()




if __name__ == '__main__':
    pass
    BasExecuterMain().run()
    