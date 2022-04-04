from re import X
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from driver.grid import Grid
from connection.client import *

class Window(QMainWindow):
    def __init__(self, ip):
        super(Window, self).__init__()
        self._grid = Grid(self, ip)
        self.setCentralWidget(self._grid)
        self.setWindowTitle('Light Bikes')
        self.setGeometry(100, 100, 600, 400)
        self.show()

