from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from driver.bike import Bike
from driver.constants import *
from connection.client import Client

class Grid(QFrame):
    
    def __init__(self, parent, ip):
        super(Grid, self).__init__(parent)
        self._timer = QBasicTimer()
        self.setStyleSheet("Border : 2px solid black")

        self._players = [Bike(5, 10, Direction.RIGHT, Color.GREEN.value), Bike(55, 30, Direction.LEFT, Color.PINK.value)]

        #conn will be closed inthis class
        conn = Client(ip)
        
        self.setFocusPolicy(Qt.StrongFocus)

    def squareWidth(self):
        return self.contentsRect().width() / Controller.BLOCKWIDTH

    def squareHeight(self):
        return self.contentsRect().height() / Controller.BLOCKHEIGHT

    def start(self):
        self._timer.start(Controller.SPEED, self)

    def paintEvent(self, event):
        painter = QPainter(self)

        rect = self.contentsRect()
        gridTop = rect.bottom() - Controller.BLOCKHEIGHT * self.squareHeight()

        for pos in self._players[0].getTrail():
            self.drawSquare(painter, rect.left() + pos[0] * self.squareWidth(), gridTop + pos[1] * self.squareHeight(), self._players[0].getColor())
        for pos in self._players[1].getTrail():
            self.drawSquare(painter, rect.left() + pos[0] * self.squareWidth(), gridTop + pos[1] * self.squareHeight(), self._players[1].getColor())

    def drawSquare(self, painter, x, y, color):
        paintColor = QColor(color)
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 1, self.squareHeight() - 1, paintColor) #integer on square dimensions tells how big painted image should be relative.

    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_Left:
            if self._players[0].getDirection() != Direction.RIGHT:
                self._players[0].setDirection(Direction.LEFT) 
        elif key == Qt.Key_Right:
            if self._players[0].getDirection() != Direction.LEFT:
                self._players[0].setDirection(Direction.RIGHT)
        elif key == Qt.Key_Down:
            if self._players[0].getDirection() != Direction.UP:
                self._players[0].setDirection(Direction.DOWN)
        elif key == Qt.Key_Up:
            if self._players[0].getDirection() != Direction.DOWN:
                self._players[0].setDirection(Direction.UP)
    
    def timerEvent(self, event):
        if event.timerId() == self._timer.timerId():
            self._players[0].moveBike()
            self._players[1].moveBike()
            self.collision()
            self.update()

    def collision(self):
        #collision with body
        self._bike = self._players[0].getTrail()
        self._other = self._players[1].getTrail()

        if self._bike[0] in self._other[1:]: #if head of bike 1 is in every other part of another bike. If bike == other head then they collided head on
            self.endgame()
            
        if self._bike[0] == self._other[0]:
            print("Draw")
            self.endgame()

        for i in range(1, len(self._bike)):
            if self._bike[0] == self._bike[i]:
                self.endgame()

        #collision with left wall
        if self._bike[0][0] < 0:
            self.endgame()

        #collision with right wall
        if self._bike[0][0] == Controller.BLOCKWIDTH:
            self.endgame()

        #collision with floor
        if self._bike[0][1] == Controller.BLOCKHEIGHT:
            self.endgame()

        #collision with ceiling
        if self._bike[0][1] < 0:
            self.endgame()

        #collision with other bike

    def endgame(self):
        self.setStyleSheet("background-color : black;")
        self._timer.stop()
        self.update()