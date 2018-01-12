'''
Created on Jan 11, 2018

@author: halil
'''

from PyQt5 import QtWidgets
import sys
from bas.BasExecuter import BasExecuter
from bas.BasContext import _bas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

import random
from binance.client import Client
import matplotlib.dates as mdate
import time
from PyQt5.Qt import QThread, pyqtProperty, Qt
import PyQt5
from pyqtgraph.Qt import PYQT5, PYQT4
from PyQt5.QtCore import pyqtSignal
from bas.BasThreadCandleTracker import BasThreadCandleTracker


class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=12, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
 
    def plot(self):
        #data = [random.random() for i in range(25)]
        data = _bas.executer.currencyManager.fetchCandle(symbol="XLMETH", interval=Client.KLINE_INTERVAL_1MINUTE)
        print (data["candleMiddle"])
        ax = self.figure.add_subplot(111)
        ax.tick_params(axis='both', which='major', labelsize=7)
        ax.tick_params(axis='both', which='minor', labelsize=5)
        time_ =data["time"]
        middle_ = data["candleMiddle"]
        ax.set_title('XLM/ETH')
        secs = mdate.epoch2num(time_)
        date_fmt = '%H:%M'
        date_formatter = mdate.DateFormatter(date_fmt)
        ax.xaxis.set_major_formatter(date_formatter)
        ax.yaxis.tick_right()

        ax.plot_date(secs,middle_, 'r-')

        self.draw()
 
 


#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
class BasMainWindow(QMainWindow):
    '''
    classdocs
    '''
    
    pyqts_ = pyqtSignal([dict], name="newCandle")



    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'Binance XLM/ETH timeline'
        self.width = 900
        self.height = 500
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.canvas = PlotCanvas(self, width=16, height=8)
        self.canvas.move(0,0)
 
        button = QPushButton('Refresh', self)
        button.setToolTip('This s an example button')
        button.move(800,0)
        button.resize(100,100)
        button.clicked.connect(self.refresh)
        
        self.candleTrackerThread = BasThreadCandleTracker(self.pyqts_)
        #self.connect(self.candleTrackerThread, SIGNAL("newCandle(String)") )
        self.pyqts_.connect(self.readSignal,type=Qt.AutoConnection)
        #self.candleTrackerThread.connect(self.readSignal,type=Qt.AutoConnection)
        self.show()
 
 
    def readSignal(self, data):
        print ("signal received:", data)
        
    def refresh(self):
        print("refresed!")
        self.candleTrackerThread.start()

 
    def initBatchBasExecuter(self):
        params={
            "config.file":"/Users/halil/bas.config.yaml"
            }
        _bas.executer = BasExecuter(params)
        _bas.executer.start()
    
        
    def run(self):
        pass
        
        self.initBatchBasExecuter()
        self.initUI()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BasMainWindow({})
    ex.run()
    sys.exit(app.exec_())
    
