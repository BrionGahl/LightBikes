from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from driver.bike import Bike
from driver.directions import Direction
from driver.colors import Color

class Grid(QFrame):

    SPEED = 80
    BLOCKWIDTH = 60
    BLOCKHEIGHT = 40

    def __init__(self, parent):
        super(Grid, self).__init__(parent)
        self._timer = QBasicTimer()

        self.setStyleSheet("Border : 2px solid black")

        self._bike = [[5, 10], [5, 11]]

        self._players = [Bike(5, 10, Direction.RIGHT, Color.BLUE.value), Bike(55, 30, Direction.LEFT, Color.BLUE.value)]

        self.setFocusPolicy(Qt.StrongFocus)

    def squareWidth(self):
        return self.contentsRect().width() / Grid.BLOCKWIDTH

    def squareHeight(self):
        return self.contentsRect().height() / Grid.BLOCKHEIGHT

    def start(self):
        self._timer.start(Grid.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)

        rect = self.contentsRect()
        gridTop = rect.bottom() - Grid.BLOCKHEIGHT * self.squareHeight()

        for pos in self._players[0].getTrail():
            self.drawSquare(painter, rect.left() + pos[0] * self.squareWidth(), gridTop + pos[1] * self.squareHeight())

    def drawSquare(self, painter, x, y):
        color = QColor(0x228B22)
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 1, self.squareHeight() - 1, color) #integer on square dimensions tells how big painted image should be relative.

    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_Left:
            if self._direction != Direction.RIGHT:
                self._direction = Direction.LEFT
        elif key == Qt.Key_Right:
            if self._direction != Direction.LEFT:
                self._direction = Direction.RIGHT
        elif key == Qt.Key_Down:
            if self._direction != Direction.UP:
                self._direction = Direction.DOWN
        elif key == Qt.Key_Up:
            if self._direction != Direction.DOWN:
                self._direction = Direction.UP
    
    def moveBike(self):
        if self._direction == Direction.LEFT:
            self._currentX, self._currentY = self._currentX - 1, self._currentY
        
        if self._direction == Direction.RIGHT:
            self._currentX, self._currentY = self._currentX + 1, self._currentY
        
        if self._direction == Direction.DOWN:
            self._currentX, self._currentY = self._currentX, self._currentY + 1

        if self._direction == Direction.UP:
            self._currentX, self._currentY = self._currentX, self._currentY - 1
           
        self._bike.insert(0, [self._currentX, self._currentY])

    def timerEvent(self, event):
        if event.timerId() == self._timer.timerId():
            self.moveBike()
            self.collision()
            self.update()

    def collision(self):
        #collision with body
        for i in range(1, len(self._bike)):
            if self._bike[0] == self._bike[i]:
                self.endgame()

        #collision with left wall
        if self._bike[0][0] < 0:
            self.endgame()

        #collision with right wall
        if self._bike[0][0] == Grid.BLOCKWIDTH:
            self.endgame()

        #collision with floor
        if self._bike[0][1] == Grid.BLOCKHEIGHT:
            self.endgame()

        #collision with ceiling
        if self._bike[0][1] < 0:
            self.endgame()


    def endgame(self):
        self.setStyleSheet("background-color : black;")
        self._timer.stop()
        self.update()