from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from driver.constants import Direction

class Bike():
    def __init__(self, initialX, initialY, direction, color):
        self._trail = [[initialX, initialY]]
        self._currentX = initialX
        self._currentY = initialY

        self._direction = direction
        self._color = color

    def moveBike(self):
        if self._direction == Direction.LEFT:
            self._currentX, self._currentY = self._currentX - 1, self._currentY
        
        if self._direction == Direction.RIGHT:
            self._currentX, self._currentY = self._currentX + 1, self._currentY
        
        if self._direction == Direction.DOWN:
            self._currentX, self._currentY = self._currentX, self._currentY + 1

        if self._direction == Direction.UP:
            self._currentX, self._currentY = self._currentX, self._currentY - 1
        
        self._trail.insert(0, [self._currentX, self._currentY])
        return(str(self._currentX) + "," + str(self._currentY))
        
    def getTrail(self):
        return self._trail

    def getColor(self):
        return self._color

    def getDirection(self):
        return self._direction

    def setDirection(self, direction):
        self._direction = direction
