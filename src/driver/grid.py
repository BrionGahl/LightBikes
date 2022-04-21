from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from driver.bike import Bike
from driver.constants import *
from connection.client import Client

import time

class Worker(QObject):
    finished = pyqtSignal()
    
    def __init__(self, parent):
        super(Worker, self).__init__()
        self.parent = parent
    
    def run(self):
        while not self.parent._conn.isReady():
            pass
        self.parent._playerNumber = self.parent._conn.getPlayerNumber()
        
        self.parent._controlled = self.parent._players[self.parent._playerNumber]
        self.parent._server = self.parent._players[1 - self.parent._playerNumber]
        
        self.parent._controlledAlive = True
        self.parent._serverAlive = True
        
        for i in range(1,6):
            self.parent._parent.console.append(str(i) + "...")
            time.sleep(1)
        self.parent._parent.console.append("Go!")
        self.parent._parent.stackedWidget.setCurrentIndex(3)
        self.finished.emit()


class Grid(QFrame):
    def checkReady(self, parent):
        self.thread = QThread()
        self.worker = Worker(parent)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.readyEvent)
        
        self.thread.start()
        
    def readyEvent(self):
        self.start()
               
    def __init__(self, parent, ip):
        super(Grid, self).__init__(parent)
        self._parent = parent
        
        parent.stackedWidget.addWidget(self)
        parent.show()
        self._timer = QBasicTimer()
        self.setStyleSheet("Border : 2px solid black")
        self.setFocusPolicy(Qt.StrongFocus)

        self._players = [Bike(5, 10, Direction.RIGHT, Color.BLUE.value), Bike(55, 30, Direction.LEFT, Color.ORANGE.value)]
        self._conn = Client(ip, self._players, parent.console)
        
        self.checkReady(self)        
            
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

        for pos in self._server.getTrail():
            self.drawSquare(painter, rect.left() + pos[0] * self.squareWidth(), gridTop + pos[1] * self.squareHeight(), self._server.getColor())
        for pos in self._controlled.getTrail():
            self.drawSquare(painter, rect.left() + pos[0] * self.squareWidth(), gridTop + pos[1] * self.squareHeight(), self._controlled.getColor())
        

    def drawSquare(self, painter, x, y, color):
        paintColor = QColor(color)
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 1, self.squareHeight() - 1, paintColor) #integer on square dimensions tells how big painted image should be relative.

    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_Left:
            if self._controlled.getDirection() != Direction.RIGHT:
                self._controlled.setDirection(Direction.LEFT) 
        elif key == Qt.Key_Right:
            if self._controlled.getDirection() != Direction.LEFT:
                self._controlled.setDirection(Direction.RIGHT)
        elif key == Qt.Key_Down:
            if self._controlled.getDirection() != Direction.UP:
                self._controlled.setDirection(Direction.DOWN)
        elif key == Qt.Key_Up:
            if self._controlled.getDirection() != Direction.DOWN:
                self._controlled.setDirection(Direction.UP)
    
    def timerEvent(self, event):
        if event.timerId() == self._timer.timerId():
            if not self._conn.isAlive():
                self.endgame("You Win!")
                return
            if self._conn.isDraw():
                self.endgame("Draw")
                return
            
            self._conn.sendLocation(self._controlled.moveBike()) 
            self.collision()
            self.update()

    def collision(self):
        #collision with body
        self._bike = self._controlled.getTrail()
        self._other = self._server.getTrail()
        
        lose = False
        
        if self._bike[0] == self._other[0]: # Draw event
            self.endgame("Draw")
            self._conn.notifyDraw()
            return        
        
        if self._bike[0] in self._other[1:]: #if head of bike 1 is in every other part of another bike. If bike == other head then they collided head on
            lose = True
            
        for i in range(1, len(self._bike)):
            if self._bike[0] == self._bike[i]:
                lose = True

        #collision with left wall
        if self._bike[0][0] < 0:
            lose = True

        #collision with right wall
        if self._bike[0][0] == Controller.BLOCKWIDTH:
            lose = True

        #collision with floor
        if self._bike[0][1] == Controller.BLOCKHEIGHT:
            lose = True

        #collision with ceiling
        if self._bike[0][1] < 0:
            lose = True
            
            
        if lose:
            self.endgame("You Lose!")
            self._conn.notifyDeath()

    def closeConnection(self):
        self._conn.close()

    def endgame(self, result):
        self.setStyleSheet("background-color : black;")
        self._timer.stop()
        self.update()
        self._parent.console.append(result)
        self._parent.stackedWidget.setCurrentIndex(1)
        print(result + "\n")