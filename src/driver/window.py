import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from driver.constants import *
from driver.grid import Grid
from driver.bike import Bike
from connection.client import *
from connection.server import *

from os import path

PATH = path.dirname(path.abspath(__file__))

class Window(QMainWindow):
    def __init__(self, ip):
        super(Window, self).__init__()
        
        uic.loadUi(path.join(PATH, '../../assets/view.ui'), self)
        self.stackedWidget.setCurrentIndex(1)
        self.setWindowTitle('Light Bikes')
        self.setGeometry(100, 100, 600, 400)
        self._grid = Grid(self, ip)
        #self.show()
     
    def closeEvent(self, event):
        try:
            self._grid.closeConnection()
        except:
            pass

