import socket
import threading

class Client():
    PORT = 4477
    
    def __init__(self, ip):
        try:
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.connect((ip, Client.PORT))
        except:
            print("CLIENT: error occurred trying to connect to server.")
        threading.Thread(target=self.listener, args=()).start()

            
    def listener(self):
        while True:
            line = ""
            try:
                line = self._s.recv(1024).decode()
            except Exception as error:
                print("CLIENT: error in receiver")
                print(error)

            if ":" in line:
                self.parseCommands(line)

    def parseCommands(self, line):
        commands = line.split(";")
        for command in commands:
            self.processCommand(command)
    
    def send(self, commandString):
        try:
            self._s.send(commandString.encode())
        except:
            print("CLIENT: failed to send command.")
        
    def sendCommand(self, command, value):
        self.send(self.makeCommandString(command, value))
    
    def makeCommandString(command, value):
        return command + ":" + value + ";"
    
    def processCommand(self, commandString): #dispatch table??
        print(commandString)
        
        cmdArr = commandString.split(":")
        command = cmdArr[0]
        value = cmdArr[1]
        
        if command == "update-location":
            return
        elif command == "dead":
            return
        elif command == "set-number":
            self._playerNumber = int(value)
    
    # Commands
    def startGame(self):
        return
            
    def sendLocation(self, xPos, yPos): #update user bike
        return

    def updateLocation(self, value): #update server bike
        return

    def notifyDeath(self):
        return
    
    
    
    
    