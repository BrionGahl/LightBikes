import socket
import threading
import sys

class Client():
    PORT = 4477
    
    def __init__(self, ip):
        self._ready = False
        self._playerNumber = -1
        try:
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.connect((ip, Client.PORT))
        except Exception as error:
            print("CLIENT: error occurred trying to connect to server.")
            print(error)
            sys.exit()
        #line = ""
        #line += self._s.recv(1024).decode()
        #line = ""
        #line += self._s.recv(1024).decode()      
        #self.parseCommands(line)
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
        print(line)
        commands = line.split(";")
        print(commands)
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
    
    def makeCommandString(command, value):
        return command + ":" + value + ";"
    
    def processCommand(self, commandString): #dispatch table??
        print("CLIENT: "+ commandString)
        
        cmdArr = commandString.split(":")
        command = cmdArr[0]
        value = cmdArr[1]
        
        if command == "update-location":
            return
        elif command == "dead":
            return
        elif command == "set-number":
            self._playerNumber = int(value)
        elif command == "start-game":
            self.startGame()
    # Commands
    def startGame(self):
        self._ready = True
        return
    
    def isReady(self):
        return self._ready
            
    def sendLocation(self, xPos, yPos): #update user bike
        return

    def updateLocation(self, value): #update server bike
        return

    def notifyDeath(self):
        return
    
    
    
    
    