from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Grid(QFrame):

    _speed = 80
    _widthInBlocks = 60
    _heighInBlocks = 40

    def __init__(self, parent):
        super(Grid, self).__init__(parent)

        self.timer = QBasicTimer()
