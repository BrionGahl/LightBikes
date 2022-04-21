import socket
import threading
import sys

class Client():
    PORT = 4477
    
    def __init__(self, ip, players, console):        
        self._ready = False
        self._alive = True
        self._draw = False
        
        self._message = ""
        
        self._players = players
        self._console = console
        
        self._playerNumber = -1
        try:
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.connect((ip, Client.PORT))
        except Exception as error:
            print("CLIENT: error occurred trying to connect to server.")
            print(error)
            sys.exit()
        threading.Thread(target=self.listener, args=()).start()
        
    def listener(self):
        while True:
            line = ""
            try:
                data = self._s.recv(1024)
                line = data.decode()
            except Exception as error:
                print("CLIENT: " + str(error))
                sys.exit()
            self.parseCommands(line)

    def parseCommands(self, line):
        commands = line.split(";")
        for command in commands:
            if command == "":
                continue
            self.processCommand(command)
    
    def send(self, commandString):
        try:
            self._s.sendall(commandString.encode())
        except:
            print("CLIENT: failed to send command.")
        
    def sendCommand(self, command, value):
        self.send(self.makeCommandString(command, value))
    
    def makeCommandString(self, command, value):
        return command + ":" + value + ";"
    
    def processCommand(self, commandString): #dispatch table??
        cmdArr = commandString.split(":")
        command = cmdArr[0]
        value = cmdArr[1]
        
        if command == "update-location":
            self.updateLocation(value)
        elif command == "set-dead":
            self._alive = False
        elif command == "set-draw":
            self._draw = True
        elif command == "set-number":
            self._playerNumber = int(value)
        elif command == "start-game":
            self._ready = True
        elif command == "message":
            self._console.append(value)
            
    def getPlayerNumber(self):
        return self._playerNumber
    
    def isAlive(self):
        return self._alive
    
    def isDraw(self):
        return self._draw
    
    def isReady(self):
        return self._ready
              
    # Commands        
    def sendLocation(self, value): #update user bike
        self.sendCommand("set-location", value)

    def updateLocation(self, value): #update server bike
        coords = value.split(",")
        self._players[1 - self._playerNumber].getTrail().insert(0, [int(coords[0]), int(coords[1])])

    def notifyDeath(self):
        self.sendCommand("set-dead", "true")
    
    def notifyDraw(self):
        self.sendCommand("set-draw", "true")
        
    def close(self):
        
        self._s.close()
    
    
    
    
    