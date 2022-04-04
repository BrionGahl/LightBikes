import socket

class Client():
    PORT = 4477
    
    def __init__(self, ip):
        try:
            self._s = socket.socket()
            self._s.connect((ip, Client.PORT))
        except:
            print("error occurred trying to connect to server.")
            
    def listener(self):
        return
    
    def send(self, commandString):
        try:
            self._s.send(commandString.encode())
        except:
            print("failed to send command.")
        
    def sendCommand(self, command, value):
        self.send(self.makeCommandString(command, value))
    
    def makeCommandString(command, value):
        return command + ":" + value + ";"
    
    def processCommand(self, commandString): #dispatch table??
        return
    
    # Commands
    def startGame(self):
        return
            
    def sendLocation(self, xPos, yPos): #update user bike
        return

    def updateLocation(self, value): #update server bike
        return

    def notifyDeath(self):
        return
    
    
    
    
    